import type { MetadataRoute } from "next";
import { SITE_URL } from "@/lib/site";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: "*",
        allow: "/",
        // Analiz araci giris arkasinda, indekslenmesine gerek yok.
        // "/dashboard" trailing slash'siz yazildi: REP prefix eslesmesiyle
        // hem /dashboard hem /dashboard/<id> alt yollarini kapsar.
        disallow: ["/app", "/dashboard"],
      },
    ],
    sitemap: `${SITE_URL}/sitemap.xml`,
    host: SITE_URL,
  };
}
