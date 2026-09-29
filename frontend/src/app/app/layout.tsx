import type { Metadata } from "next";

/**
 * Sifre korumali arac sayfasi. Arayuz bir Client Component oldugu icin metadata
 * export edemez; bu yuzden noindex sinyali ayri bir server layout'ta veriliyor.
 * robots.txt de /app'i disallow ediyor, ikisi birlikte tutarli.
 */
export const metadata: Metadata = {
  title: "Analiz aracı",
  alternates: {
    canonical: "/app",
  },
  openGraph: {
    type: "website",
    url: "/app",
    title: "Analiz aracı | lensecode",
  },
  robots: {
    index: false,
    follow: false,
    googleBot: {
      index: false,
      follow: false,
    },
  },
};

export default function ToolLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
