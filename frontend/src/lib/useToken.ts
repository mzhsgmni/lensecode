"use client";

import { useSyncExternalStore } from "react";
import { getToken, subscribeToken } from "./api";

const noopSubscribe = () => () => {};

/** localStorage'daki token degerine abone ol. Sunucu tarafinda hep null. */
export function useToken(): string | null {
  return useSyncExternalStore(subscribeToken, getToken, () => null);
}

/**
 * Hydration tamamlandi mi?
 *
 * Sunucuda false, istemcide true doner. Hydration sirasinda React sunucu
 * ciktisini (false) kullanir, boyama bittikten sonra getSnapshot ile true'ya
 * gecer. Boylece yanlis icerik ilk boyamada gorunmez.
 */
export function useHydrated(): boolean {
  return useSyncExternalStore(
    noopSubscribe,
    () => true,
    () => false
  );
}
