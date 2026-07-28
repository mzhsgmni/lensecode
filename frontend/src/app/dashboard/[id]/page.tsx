"use client";

import { useEffect, useState, use } from "react";
import Link from "next/link";
import ReportView from "@/components/ReportView";
import { getReport, clearToken } from "@/lib/api";

export default function DashboardPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const [report, setReport] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;

    const fetchReport = async () => {
      try {
        const data = await getReport(id);
        if (!cancelled) {
          setReport(data);
          setLoading(false);
        }
      } catch (err: any) {
        if (!cancelled) {
          if (err.message?.includes("401") || err.message?.includes("Yetkisiz")) {
            clearToken();
            window.location.href = "/";
            return;
          }
          setError("Rapor alınamadı. Analiz henüz tamamlanmamış olabilir.");
          setLoading(false);
        }
      }
    };

    fetchReport();

    return () => { cancelled = true; };
  }, [id]);

  if (loading) {
    return (
      <div className="min-h-screen bg-bg-primary flex items-center justify-center">
        <div className="text-center animate-fade-in">
          <div className="w-12 h-12 border-2 border-border border-t-accent rounded-full animate-spin-slow mx-auto mb-4" />
          <p className="text-text-primary font-medium">Rapor hazırlanıyor...</p>
          <p className="text-text-secondary text-sm mt-1">AI değerlendirmesi tamamlanıyor</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-bg-primary flex items-center justify-center">
        <div className="text-center animate-fade-in">
          <p className="text-4xl mb-4">🔍</p>
          <p className="text-text-primary font-medium mb-2">{error}</p>
          <Link href="/" className="text-accent hover:underline text-sm">
            ← Ana sayfaya dön
          </Link>
        </div>
      </div>
    );
  }

  if (!report) return null;

  return (
    <div className="min-h-screen bg-bg-primary">
      <nav className="sticky top-0 z-50 bg-bg-secondary/80 backdrop-blur-lg border-b border-border">
        <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-3">
            <span className="text-2xl">🔍</span>
            <span className="text-xl font-bold gradient-text">lensecode</span>
          </Link>
          <Link
            href="/"
            className="text-sm text-text-secondary hover:text-text-primary border border-border px-4 py-2 rounded-lg hover:border-accent transition"
          >
            ← Yeni Analiz
          </Link>
        </div>
      </nav>

      <main className="max-w-5xl mx-auto px-6 py-10">
        <ReportView report={report} />
      </main>
    </div>
  );
}