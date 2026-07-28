"use client";

import { useSyncExternalStore } from "react";
import { getToken, subscribeToken } from "./api";

export function useToken(): string | null {
  return useSyncExternalStore(subscribeToken, getToken, () => null);
}
