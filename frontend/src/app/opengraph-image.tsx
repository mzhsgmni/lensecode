import { ImageResponse } from "next/og";
import { SITE_NAME, SITE_TAGLINE } from "@/lib/site";

export const alt = `${SITE_NAME} — ${SITE_TAGLINE}`;
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

// Not: next/og yalnizca Geist Regular (400) icerir. fontWeight istekleri
// sessizce yok sayilir; hiyerarsi puntoda ve renkte kurulur.
const FEATURES = [
  "Teknoloji tespiti",
  "Güvenlik açığı analizi",
  "Kod kalitesi puanı",
  "Eksik özellik raporu",
  "PDF & Markdown rapor",
];

export default function Image() {
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          backgroundColor: "#0a0a0f",
          backgroundImage:
            "radial-gradient(circle at 50% 0%, #2a1a5e 0%, #0a0a0f 65%)",
          padding: "80px",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 20, marginBottom: 48 }}>
          <div
            style={{
              width: 64,
              height: 64,
              borderRadius: 16,
              backgroundColor: "#7c3aed",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "#ffffff",
              fontSize: 40,
            }}
          >
            L
          </div>
          <div style={{ display: "flex", flexDirection: "column" }}>
            <div style={{ fontSize: 52, color: "#e8e8f0", letterSpacing: -1 }}>{SITE_NAME}</div>
            <div style={{ fontSize: 22, color: "#8888a0" }}>{SITE_TAGLINE}</div>
          </div>
        </div>

        <div
          style={{
            fontSize: 72,
            color: "#ffffff",
            lineHeight: 1.15,
            marginBottom: 28,
            letterSpacing: -2,
          }}
        >
          Projeni yükle, AI mimari analizini al.
        </div>

        <div style={{ fontSize: 30, color: "#8888a0", marginBottom: 56, lineHeight: 1.4 }}>
          Eksikleri gör, güvenlik açıklarını bul, yol haritası oluştur.
        </div>

        <div style={{ display: "flex", flexWrap: "wrap", gap: 14 }}>
          {FEATURES.map((f) => (
            <div
              key={f}
              style={{
                fontSize: 24,
                color: "#c9b8f5",
                border: "1px solid #3b2a6b",
                borderRadius: 999,
                padding: "12px 26px",
                display: "flex",
              }}
            >
              {f}
            </div>
          ))}
        </div>
      </div>
    ),
    { ...size }
  );
}
