import type { NextConfig } from "next";

/**
 * Backend proxy'si `src/app/api/[...path]/route.ts` icinde yapiliyor.
 *
 * Once burada `rewrites()` vardi ama Next.js next.config dosyasini BUILD
 * aninda degerlendirip ciktiyi `.next/routes-manifest.json` icine
 * donduruyor. Docker/Railway'de calisma aninda verilen BACKEND_URL bu
 * yuzden okunmuyor ve tum API cagrilari localhost:8000'e gidiyordu.
 */
const nextConfig: NextConfig = {};

export default nextConfig;
