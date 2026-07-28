const raw = process.env.NEXT_PUBLIC_SITE_URL || "http://localhost:3000";

export const SITE_URL = raw.replace(/\/+$/, "");
export const SITE_NAME = "lensecode";
export const SITE_TAGLINE = "AI Project Architect";
export const SITE_DESCRIPTION =
  "Projelerinizi yükleyin; teknoloji yığını tespiti, güvenlik açığı analizi, kod kalitesi puanı, eksik özellik listesi ve düzeltme yol haritası alın. PDF ve Markdown rapor desteği.";

export const isPlaceholderUrl = SITE_URL.startsWith("http://localhost");
