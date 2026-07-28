FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Semgrep opsiyoneldir ve imaji buyutur; gerekiyorsa build arg ile aç:
#   docker build --build-arg INSTALL_SEMGREP=1 .
ARG INSTALL_SEMGREP=0
RUN if [ "$INSTALL_SEMGREP" = "1" ]; then \
      pip install --no-cache-dir -r requirements-semgrep.txt; \
    fi

RUN groupadd -r lensecode && useradd -r -g lensecode -u 10001 lensecode && \
    mkdir -p /app/app/uploads /data && \
    chown -R lensecode:lensecode /app/app/uploads /data

USER lensecode

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
