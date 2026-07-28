import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "lensecode - AI Project Architect",
  description: "Projeni yükle, AI mimari analizini al, eksikleri gör, yol haritanı oluştur.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="tr">
      <body className="antialiased">{children}</body>
    </html>
  );
}