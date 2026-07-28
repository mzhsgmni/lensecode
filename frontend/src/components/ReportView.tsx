"use client";

import ScoreCard from "./ScoreCard";
import AnalysisChart from "./AnalysisChart";
import FeatureChecklist from "./FeatureChecklist";
import PromptGenerator from "./PromptGenerator";

interface Props {
  report: any;
}

export default function ReportView({ report }: Props) {
  const categories = report.categories || {};
  const scores = Object.entries(categories).map(([key, val]: any) => ({
    label: key.replace(/_/g, " ").toUpperCase(),
    score: val.score,
  }));

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold gradient-text mb-2">Analiz Raporu</h1>
        <div className="flex items-center justify-center gap-2 text-text-secondary">
          <span>📊 Genel Puan:</span>
          <span className="text-5xl font-bold gradient-text">{report.overall_score}</span>
          <span className="text-text-secondary">/100</span>
        </div>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {Object.entries(categories).map(([key, val]: any) => (
          <ScoreCard
            key={key}
            label={key.replace(/_/g, " ").toUpperCase()}
            score={val.score}
            icon={val.icon}
          />
        ))}
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        <AnalysisChart scores={scores} />

        <div className="bg-bg-card border border-border rounded-xl p-6 animate-fade-in">
          <h3 className="text-text-primary font-semibold mb-3 flex items-center gap-2">
            <span>📊</span> İstatistikler
          </h3>
          <div className="space-y-3">
            <div className="flex justify-between py-2 border-b border-border">
              <span className="text-text-secondary">Toplam Dosya</span>
              <span className="text-text-primary font-medium">{report.stats?.total_files || 0}</span>
            </div>
            <div className="flex justify-between py-2 border-b border-border">
              <span className="text-text-secondary">Toplam Satır</span>
              <span className="text-text-primary font-medium">{report.stats?.total_lines?.toLocaleString() || 0}</span>
            </div>
            <div className="flex justify-between py-2 border-b border-border">
              <span className="text-text-secondary">Framework</span>
              <span className="text-text-primary font-medium">{report.tech_stack?.framework || "—"}</span>
            </div>
            <div className="flex justify-between py-2 border-b border-border">
              <span className="text-text-secondary">Dil</span>
              <span className="text-text-primary font-medium">{report.tech_stack?.language || "—"}</span>
            </div>
            <div className="flex justify-between py-2">
              <span className="text-text-secondary">Veritabanı</span>
              <span className="text-text-primary font-medium">{report.tech_stack?.database || "—"}</span>
            </div>
          </div>
        </div>
      </div>

      {report.summary && (
        <div className="bg-bg-card border border-border rounded-xl p-6 animate-fade-in">
          <h3 className="text-text-primary font-semibold mb-2">📋 Özet</h3>
          <p className="text-text-secondary leading-relaxed">{report.summary}</p>
        </div>
      )}

      <div className="grid lg:grid-cols-3 gap-4">
        <FeatureChecklist title="Eksik Özellikler" items={report.missing_features || []} icon="📋" type="missing" />
        <FeatureChecklist title="Gereksiz Yapılanmalar" items={report.redundant_features || []} icon="⚠️" type="redundant" />
        <FeatureChecklist
          title="Güvenlik Sorunları"
          items={(report.security_issues || []).map((i: any) => `[${i.severity}] ${i.description}`)}
          icon="🛡️"
          type="security"
        />
      </div>

      {report.ai_mistakes && report.ai_mistakes.length > 0 && (
        <div className="bg-bg-card border border-red-500/20 rounded-xl p-6 animate-fade-in">
          <h3 className="text-text-primary font-semibold mb-4 flex items-center gap-2">
            <span>🤖</span> AI Hataları
          </h3>
          <div className="space-y-2">
            {report.ai_mistakes.map((m: string, i: number) => (
              <div key={i} className="flex items-start gap-2 text-sm text-red-400 bg-red-500/5 px-3 py-2 rounded-lg">
                <span>⚠️</span>
                <span>{m}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {report.recommendations && report.recommendations.length > 0 && (
        <div className="bg-bg-card border border-border rounded-xl p-6 animate-fade-in">
          <h3 className="text-text-primary font-semibold mb-4 flex items-center gap-2">
            <span>💡</span> Öneriler
          </h3>
          <div className="space-y-2">
            {report.recommendations.map((r: string, i: number) => (
              <div key={i} className="flex items-start gap-2 text-sm text-text-primary bg-bg-secondary px-3 py-2 rounded-lg">
                <span className="text-accent">{i + 1}.</span>
                <span>{r}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {report.roadmap && report.roadmap.length > 0 && (
        <div className="bg-bg-card border border-border rounded-xl p-6 animate-fade-in">
          <h3 className="text-text-primary font-semibold mb-4 flex items-center gap-2">
            <span>🗺️</span> Yol Haritası
          </h3>
          <div className="space-y-3">
            {report.roadmap.map((step: string, i: number) => (
              <div key={i} className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-accent/20 flex items-center justify-center text-accent font-bold text-sm">
                  {i + 1}
                </div>
                <div className="flex-1 py-1.5">
                  <p className="text-text-primary text-sm">{step}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <PromptGenerator prompt={report.prompt_generator} />

      <div className="flex flex-wrap gap-3 justify-center pt-4">
        <button
          onClick={() => window.print()}
          className="px-6 py-2.5 bg-bg-card border border-border text-text-primary rounded-lg text-sm font-medium hover:border-accent transition cursor-pointer"
        >
          🖨️ Yazdır
        </button>
      </div>
    </div>
  );
}