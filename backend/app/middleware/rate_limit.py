"""Basit, bellek ici IP bazli hiz sinirlayici.

Tek paylasilan bir sifre koruyor. Sifre yanlsa bile koruma saglamak icin
basarisiz giris denemeleri sayilir ve esik asilirsa IP gecici olarak kilitlenir.

Not: bu sayaclar surec belleginde tutulur. Birden fazla backend ornegi
calistiriyorsan her ornek kendi sayacini tutar; Railway'de replika sayisini
1'de birak veya Redis gibi paylasilan bir sayac kullan.
"""

import threading
import time
from collections import OrderedDict

from fastapi import HTTPException, Request

from app.config import LOGIN_MAX_ATTEMPTS, LOGIN_WINDOW_SECONDS, MAX_TRACKED_CLIENTS


class SlidingWindowLimiter:
    """Basarisiz denemeleri sayan, basarili girdide sifirlayan pencere."""

    def __init__(self, max_attempts: int, window_seconds: int) -> None:
        self._max_attempts = max_attempts
        self._window = window_seconds
        self._failures: OrderedDict[str, list[float]] = OrderedDict()
        self._lock = threading.Lock()

    def _prune(self, now: float) -> None:
        cutoff = now - self._window
        stale = [k for k, v in self._failures.items() if not v or v[-1] <= cutoff]
        for k in stale:
            del self._failures[k]

        while len(self._failures) > MAX_TRACKED_CLIENTS:
            self._failures.popitem(last=False)

    def retry_after(self, key: str) -> int:
        """Kilitliyse kalan saniye, aciksa 0 dondurur."""
        now = time.monotonic()
        with self._lock:
            self._prune(now)
            attempts = self._failures.get(key)
            if not attempts or len(attempts) < self._max_attempts:
                return 0
            return max(1, int(attempts[0] + self._window - now))

    def record_failure(self, key: str) -> None:
        now = time.monotonic()
        with self._lock:
            self._prune(now)
            self._failures.setdefault(key, []).append(now)
            self._failures.move_to_end(key)

    def reset(self, key: str) -> None:
        with self._lock:
            self._failures.pop(key, None)


login_limiter = SlidingWindowLimiter(LOGIN_MAX_ATTEMPTS, LOGIN_WINDOW_SECONDS)


def client_key(request: Request) -> str:
    """Istemci IP'si. Proxy arkasinda X-Forwarded-For tercih edilir."""
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip.strip()
    return request.client.host if request.client else "unknown"


def enforce_login_limit(request: Request) -> None:
    wait = login_limiter.retry_after(client_key(request))
    if wait:
        raise HTTPException(
            status_code=429,
            detail=f"Cok fazla basarisiz deneme. {wait} saniye sonra tekrar dene.",
            headers={"Retry-After": str(wait)},
        )
