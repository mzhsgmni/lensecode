import Link from "next/link";

const FEATURES = [
  {
    icon: "📦",
    title: "Projeyi Yükle",
    desc: "ZIP dosyası, public GitHub reposu veya doğrudan kod yapıştırma. Kurulum yok, terminal yok.",
  },
  {
    icon: "🔍",
    title: "Teknoloji Tespiti",
    desc: "Framework, dil, veritabanı, UI kütüphanesi ve kimlik doğrulama sistemini otomatik tanır.",
  },
  {
    icon: "🛡️",
    title: "Güvenlik Analizi",
    desc: "Gömülü kimlik bilgileri, eval kullanımı, kırılgan karma algoritmaları ve TLS hatalarını raporlar.",
  },
  {
    icon: "📊",
    title: "Kod Kalitesi Puanı",
    desc: "Kullanılmayan paketler, gereksiz bağımlılıklar ve yapısal sorunlar puanı doğrudan düşürür.",
  },
  {
    icon: "❌",
    title: "Eksik Özellik Tespiti",
    desc: "Rate limit, 2FA, sağlık kontrolü, test, Docker, hata yönetimi ve daha fazlası kontrol edilir.",
  },
  {
    icon: "✨",
    title: "AI Prompt Üretici",
    desc: "Bulunan sorunları düzeltmek için AI kod editörüne yapıştırılabilir hazır prompt üretir.",
  },
];

const STEPS = [
  { n: "1", title: "Yükle", desc: "ZIP, GitHub URL'si veya kod yapıştırın." },
  { n: "2", title: "Analiz", desc: "Teknoloji tespiti, güvenlik ve kalite taraması çalışır." },
  { n: "3", title: "Raporu al", desc: "Puanlar, eksikler, yol haritası ve düzeltme prompt'u." },
];

const OUTPUTS = [
  "Genel puan ve kategori puanları (kalite, mimari, performans, güvenlik)",
  "Güvenlik açıkları listesi (severity, dosya, satır)",
  "Kullanılmayan paketler ve gereksiz bağımlılıklar",
  "Eksik özellikler ve önerilen yol haritası",
  "PDF, Markdown ve JSON formatında indirilebilir rapor",
  "AI kod editörüne yapıştırılabilir düzeltme prompt'u",
];

export default function Home() {
  return (
    <div className="min-h-screen bg-bg-primary">
      <nav className="sticky top-0 z-50 bg-bg-secondary/80 backdrop-blur-lg border-b border-border">
        <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
          <span className="flex items-center gap-3">
            <span className="text-2xl">🔍</span>
            <span className="text-xl font-bold gradient-text">lensecode</span>
          </span>
          <Link
            href="/app"
            className="px-5 py-2 bg-accent text-white rounded-lg text-sm font-medium hover:bg-accent-hover transition"
          >
            Analizi Başlat
          </Link>
        </div>
      </nav>

      <main>
        <section
          className="px-6 py-24 text-center"
          style={{ background: "radial-gradient(ellipse at 50% 0%, #1e1b3a 0%, #0a0a0f 70%)" }}
        >
          <div className="max-w-3xl mx-auto">
            <h1 className="text-5xl md:text-6xl font-bold leading-tight mb-6">
              <span className="gradient-text">Projene AI mimari analizi</span>
            </h1>
            <p className="text-lg md:text-xl text-text-secondary max-w-2xl mx-auto mb-10">
              Kodunuzu yükleyin; teknoloji yığınını tespit edin, güvenlik açıklarını ve eksik özellikleri görün,
              düzeltmek için hazır bir yol haritası alın.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                href="/app"
                className="px-8 py-4 bg-accent text-white rounded-xl font-semibold hover:bg-accent-hover transition"
              >
                Ücretsiz Analiz Başlat
              </Link>
              <a
                href="#nasil-calisir"
                className="px-8 py-4 bg-bg-card border border-border text-text-primary rounded-xl font-semibold hover:border-accent transition"
              >
                Nasıl Çalışır?
              </a>
            </div>
            <p className="text-sm text-text-secondary mt-6">
              Kurulum gerekmez · ZIP, GitHub veya kod yapıştırma · PDF/Markdown rapor
            </p>
          </div>
        </section>

        <section className="max-w-5xl mx-auto px-6 py-20">
          <h2 className="text-3xl font-bold text-center mb-4">Neler yapıyor?</h2>
          <p className="text-text-secondary text-center mb-12 max-w-2xl mx-auto">
            lensecode, projeyi okuyup mimari kalitesini puanlar ve geliştirmenin en verimli yolunu çıkarır.
          </p>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-5">
            {FEATURES.map((f) => (
              <div
                key={f.title}
                className="bg-bg-card border border-border rounded-xl p-6 hover:border-accent transition"
              >
                <span className="text-3xl block mb-3">{f.icon}</span>
                <h3 className="text-text-primary font-semibold mb-2">{f.title}</h3>
                <p className="text-text-secondary text-sm leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </section>

        <section id="nasil-calisir" className="bg-bg-secondary/40 border-y border-border">
          <div className="max-w-5xl mx-auto px-6 py-20">
            <h2 className="text-3xl font-bold text-center mb-12">Nasıl çalışır?</h2>
            <div className="grid md:grid-cols-3 gap-8">
              {STEPS.map((s) => (
                <div key={s.n} className="text-center">
                  <div className="w-12 h-12 mx-auto mb-4 rounded-full bg-accent/20 border border-accent flex items-center justify-center text-accent font-bold text-lg">
                    {s.n}
                  </div>
                  <h3 className="text-text-primary font-semibold mb-2">{s.title}</h3>
                  <p className="text-text-secondary text-sm">{s.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="max-w-3xl mx-auto px-6 py-20">
          <h2 className="text-3xl font-bold text-center mb-4">Raporda neler var?</h2>
          <p className="text-text-secondary text-center mb-10">
            Her analiz sonucu tek bir raporda toplanır.
          </p>
          <ul className="space-y-3">
            {OUTPUTS.map((o) => (
              <li key={o} className="flex items-start gap-3 text-text-secondary">
                <span className="text-accent mt-0.5">✓</span>
                <span>{o}</span>
              </li>
            ))}
          </ul>
        </section>

        <section className="max-w-3xl mx-auto px-6 pb-24">
          <div
            className="bg-gradient-to-r from-accent/10 to-purple-500/10 border border-accent/30 rounded-2xl p-10 text-center animate-pulse-glow"
          >
            <h2 className="text-3xl font-bold mb-3">Kodun ne durumda?</h2>
            <p className="text-text-secondary mb-8 max-w-lg mx-auto">
              Projenizi yükleyin, 20-90 saniye içinde puanlanmış bir rapor ve düzeltme planı alın.
            </p>
            <Link
              href="/app"
              className="inline-block px-8 py-4 bg-accent text-white rounded-xl font-semibold hover:bg-accent-hover transition"
            >
              Analizi Başlat
            </Link>
          </div>
        </section>
      </main>

      <footer className="border-t border-border">
        <div className="max-w-5xl mx-auto px-6 py-8 flex flex-col sm:flex-row items-center justify-between gap-3">
          <span className="flex items-center gap-2 text-sm text-text-secondary">
            <span>🔍</span>
            <span className="font-semibold text-text-primary">lensecode</span>
            <span>— AI Project Architect</span>
          </span>
          <span className="text-xs text-text-secondary">
            Kodunuz yalnızca analiz süresince işlenir.
          </span>
        </div>
      </footer>
    </div>
  );
}
