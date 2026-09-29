import type { NextRequest } from "next/server";

/**
 * Backend proxy'si.
 *
 * Neden rewrite degil? Next.js `next.config.ts` dosyasini BUILD aninda
 * degerlendirip `rewrites()` ciktisini `.next/routes-manifest.json` icine
 * donduruyor. Bu yuzden Docker/Railway'de calisma aninda verilen
 * `BACKEND_URL` degeri hic okunmuyor ve proxy `localhost:8000`'ye gitiyordu.
 *
 * Burada adres her istekte okunur; backend domaini deploy sonrasi degisse
 * yeniden build gerekmez. (Railway'de backend adresi ilk deploy'dan sonra
 * kesf edilir, bu yuzel build-time'a baglamak Pratik olarak ise yaramaz.)
 */

const BACKEND_URL = () => (process.env.BACKEND_URL || "http://localhost:8000").replace(/\/+$/, "");

// Her zaman backend'e git; bu deger Next'in onbellegini degil, proxy'yi ilgilendirir.
export const dynamic = "force-dynamic";

const HOP_BY_HOP = new Set([
  "connection",
  "keep-alive",
  "proxy-authenticate",
  "proxy-authorization",
  "te",
  "trailer",
  "transfer-encoding",
  "upgrade",
  "host",
  "content-length",
]);

function forwardHeaders(req: NextRequest): Headers {
  const headers = new Headers();
  for (const [key, value] of req.headers) {
    if (!HOP_BY_HOP.has(key.toLowerCase())) headers.set(key, value);
  }
  return headers;
}

async function proxy(req: NextRequest, ctx: { params: Promise<{ path: string[] }> }) {
  const { path } = await ctx.params;
  const target = `${BACKEND_URL()}/api/${path.join("/")}${req.nextUrl.search}`;

  const hasBody = !["GET", "HEAD"].includes(req.method);
  const upstream = await fetch(target, {
    method: req.method,
    headers: forwardHeaders(req),
    body: hasBody ? await req.arrayBuffer() : undefined,
    cache: "no-store",
    redirect: "manual",
  });

  // Yanitin body'sini okunabilir sekilde dondur; Set-Cookie gibi basliklar
  // korunur ama Next'in otomatik ekledigi icerik kodlamasi karismasin.
  const headers = new Headers();
  upstream.headers.forEach((value, key) => {
    if (!HOP_BY_HOP.has(key.toLowerCase())) headers.set(key, value);
  });

  return new Response(upstream.body, {
    status: upstream.status,
    statusText: upstream.statusText,
    headers,
  });
}

export const GET = proxy;
export const POST = proxy;
export const PUT = proxy;
export const PATCH = proxy;
export const DELETE = proxy;
export const HEAD = proxy;
