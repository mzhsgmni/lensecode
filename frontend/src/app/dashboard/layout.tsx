import type { Metadata } from "next";

/** Rapor sayfalari hicbir zaman indekslenmemeli. */
export const metadata: Metadata = {
  title: "Analiz raporu",
  robots: {
    index: false,
    follow: false,
    googleBot: {
      index: false,
      follow: false,
    },
  },
};

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
