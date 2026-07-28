"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import FileUploader from "@/components/FileUploader";
import { login, clearToken, errorMessage } from "@/lib/api";
import { useToken } from "@/lib/useToken";

export default function AppPage() {
  const token = useToken();
  const [password, setPassword] = useState("");
  const [loginError, setLoginError] = useState("");
  const [loginLoading, setLoginLoading] = useState(false);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("");
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoginError("");
    setLoginLoading(true);
    try {
      await login(password);
    } catch (err) {
      setLoginError(errorMessage(err, "Şifre yanlış"));
    } finally {
      setLoginLoading(false);
    }
  };

  const handleLogout = () => {
    clearToken();
  };

  const handleProjectReady = async (projectId: string) => {
    setLoading(true);
    setStatus("🔍 Proje yüklendi, analiz başlıyor...");
    try {
      const { analyzeProject } = await import("@/lib/api");
      await analyzeProject(projectId);
      router.push(`/dashboard/${projectId}`);
    } catch (err) {
      setStatus(`❌ ${errorMessage(err, "Hata oluştu")}`);
      setTimeout(() => setStatus(""), 5000);
    } finally {
      setLoading(false);
    }
  };

  if (!token) {
    return (
      <div
        className="min-h-screen bg-bg-primary flex items-center justify-center px-6"
        style={{ background: "radial-gradient(ellipse at center, #12121a 0%, #0a0a0f 100%)" }}
      >
        <div className="bg-bg-card border border-border rounded-2xl p-10 w-full max-w-sm text-center shadow-lg animate-fade-in">
          <div className="text-5xl mb-4">🔍</div>
          <h1 className="text-3xl font-bold gradient-text mb-2">lensecode</h1>
          <p className="text-text-secondary text-sm mb-8">AI Project Architect</p>
          <form onSubmit={handleLogin}>
            <input
              type="password"
              placeholder="Şifre..."
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-3 bg-bg-secondary border border-border rounded-lg text-text-primary outline-none focus:border-accent focus:shadow-[0_0_0_3px_var(--color-accent-glow)] mb-4 text-center"
              autoFocus
            />
            {loginError && <p className="text-red-400 text-sm mb-3">{loginError}</p>}
            <button
              type="submit"
              disabled={loginLoading || !password}
              className="w-full py-3 bg-accent text-white rounded-lg font-medium hover:bg-accent-hover transition disabled:opacity-50 cursor-pointer"
            >
              {loginLoading ? "Kontrol ediliyor..." : "Giriş"}
            </button>
          </form>
          <Link
            href="/"
            className="block mt-6 text-xs text-text-secondary hover:text-text-primary transition"
          >
            ← Ana sayfaya dön
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-bg-primary">
      <nav className="sticky top-0 z-50 bg-bg-secondary/80 backdrop-blur-lg border-b border-border">
        <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-3">
            <span className="text-2xl">🔍</span>
            <span className="text-xl font-bold gradient-text">lensecode</span>
          </Link>
          <button
            onClick={handleLogout}
            className="text-xs text-text-secondary bg-bg-card px-3 py-1.5 rounded-full border border-border hover:border-red-500 hover:text-red-400 transition cursor-pointer"
          >
            Çıkış
          </button>
        </div>
      </nav>

      <main className="max-w-3xl mx-auto px-6 py-16">
        <div className="text-center mb-12 animate-fade-in">
          <h1 className="text-5xl font-bold mb-4">
            <span className="gradient-text">Projene yükle</span>
          </h1>
          <p className="text-text-secondary text-lg max-w-xl mx-auto">
            Projeni yükle, AI mimari analizini al. Eksikleri gör, güvenlik açıklarını bul, yol haritanı oluştur.
          </p>
        </div>

        <FileUploader onProjectReady={handleProjectReady} />

        {loading && (
          <div className="mt-8 bg-bg-card border border-border rounded-xl p-6 animate-fade-in">
            <div className="flex items-center gap-4">
              <div className="w-10 h-10 border-2 border-border border-t-accent rounded-full animate-spin-slow" />
              <div>
                <p className="text-text-primary font-medium">{status}</p>
                <p className="text-text-secondary text-sm mt-1">Bu işlem 20-90 saniye sürebilir</p>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
