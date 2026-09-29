import type { Metadata, Viewport } from "next";
import "./globals.css";
import { SITE_DESCRIPTION, SITE_NAME, SITE_TAGLINE, SITE_URL } from "@/lib/site";

/**
 * Yalnizca tum rotalarda gecerli olan metadata burada.
 *
 * `canonical`, `openGraph.url` ve `robots` bilerek burada tanimli degil:
 * Next metadata'yi alt segmentlere miras biraktigi icin burada "/" degeri
 * tum rotalara yayilir ve /app ile /dashboard/* de ana sayfayi isaret eder.
 * Rota bazli degerler (landing)/layout.tsx, app/layout.tsx ve
 * dashboard/layout.tsx dosyalarinda.
 */
export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: `${SITE_NAME} — ${SITE_TAGLINE}`,
    template: `%s | ${SITE_NAME}`,
  },
  description: SITE_DESCRIPTION,
  applicationName: SITE_NAME,
  keywords: [
    "yapay zeka kod analizi",
    "AI code review",
    "proje mimari analizi",
    "kod kalitesi puanı",
    "güvenlik açığı taraması",
    "eksik özellik tespiti",
    "yapay zeka proje analizi",
    "lensecode",
  ],
  authors: [{ name: SITE_NAME }],
  creator: SITE_NAME,
  openGraph: {
    type: "website",
    locale: "tr_TR",
    siteName: SITE_NAME,
    title: `${SITE_NAME} — ${SITE_TAGLINE}`,
    description: SITE_DESCRIPTION,
  },
  twitter: {
    card: "summary_large_image",
    title: `${SITE_NAME} — ${SITE_TAGLINE}`,
    description: SITE_DESCRIPTION,
  },
  category: "developer",
};

export const viewport: Viewport = {
  themeColor: "#0a0a0f",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="tr">
      <body className="antialiased">{children}</body>
    </html>
  );
}
