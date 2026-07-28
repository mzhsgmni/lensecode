"use client";

import { useState, useRef } from "react";
import { uploadZip, uploadGithub, uploadPaste, errorMessage } from "@/lib/api";

interface Props {
  onProjectReady: (projectId: string) => void;
}

export default function FileUploader({ onProjectReady }: Props) {
  const [dragOver, setDragOver] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [mode, setMode] = useState<"zip" | "github" | "paste">("zip");
  const [githubUrl, setGithubUrl] = useState("");
  const [pasteCode, setPasteCode] = useState("");
  const fileRef = useRef<HTMLInputElement>(null);

  const handleUploadResult = (data: { project_id: string }) => {
    onProjectReady(data.project_id);
  };

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file) await uploadFile(file);
  };

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) await uploadFile(file);
  };

  const uploadFile = async (file: File) => {
    setUploading(true);
    try {
      const data = await uploadZip(file);
      handleUploadResult(data);
    } catch (err) {
      alert(errorMessage(err, "Yükleme başarısız"));
    } finally {
      setUploading(false);
    }
  };

  const handleGithub = async () => {
    if (!githubUrl.trim()) return;
    setUploading(true);
    try {
      const data = await uploadGithub(githubUrl.trim());
      handleUploadResult(data);
    } catch (err) {
      alert(errorMessage(err, "GitHub yükleme başarısız"));
    } finally {
      setUploading(false);
    }
  };

  const handlePaste = async () => {
    if (!pasteCode.trim()) return;
    setUploading(true);
    try {
      const data = await uploadPaste(pasteCode);
      handleUploadResult(data);
    } catch (err) {
      alert(errorMessage(err, "Kod gönderme başarısız"));
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="animate-fade-in">
      <div className="flex gap-2 mb-6">
        {(["zip", "github", "paste"] as const).map((m) => (
          <button
            key={m}
            onClick={() => setMode(m)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition cursor-pointer ${
              mode === m
                ? "bg-accent text-white"
                : "bg-bg-card text-text-secondary border border-border hover:border-accent"
            }`}
          >
            {m === "zip" ? "📦 ZIP" : m === "github" ? "🔗 GitHub" : "📝 Kod"}
          </button>
        ))}
      </div>

      {mode === "zip" && (
        <div
          className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all duration-300 ${
            dragOver
              ? "border-accent bg-[rgba(124,58,237,0.1)] scale-[1.01]"
              : "border-border bg-bg-card hover:border-accent hover:bg-bg-card-hover"
          }`}
          onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
          onDragLeave={() => setDragOver(false)}
          onDrop={handleDrop}
          onClick={() => fileRef.current?.click()}
        >
          <input type="file" ref={fileRef} onChange={handleFileSelect} hidden accept=".zip" />
          {uploading ? (
            <div className="flex items-center justify-center gap-3">
              <div className="w-6 h-6 border-2 border-border border-t-accent rounded-full animate-spin-slow" />
              <p className="text-text-secondary">Yükleniyor...</p>
            </div>
          ) : (
            <>
              <div className="text-5xl mb-4">📤</div>
              <p className="text-text-primary text-lg font-medium mb-1">Projeni sürükle-bırak veya tıkla</p>
              <p className="text-text-secondary text-sm">ZIP dosyası (max 100MB)</p>
            </>
          )}
        </div>
      )}

      {mode === "github" && (
        <div className="bg-bg-card border border-border rounded-xl p-8">
          <label className="block text-sm text-text-secondary mb-2">GitHub Repo URL (public)</label>
          <input
            type="text"
            placeholder="https://github.com/kullanici/proje"
            value={githubUrl}
            onChange={(e) => setGithubUrl(e.target.value)}
            className="w-full px-4 py-3 bg-bg-secondary border border-border rounded-lg text-text-primary outline-none focus:border-accent focus:shadow-[0_0_0_3px_var(--color-accent-glow)] mb-4"
          />
          <button
            onClick={handleGithub}
            disabled={uploading || !githubUrl.trim()}
            className="w-full px-6 py-3 bg-accent text-white rounded-lg font-medium hover:bg-accent-hover transition disabled:opacity-50 cursor-pointer"
          >
            {uploading ? "Klonlanıyor..." : "Analiz Et"}
          </button>
        </div>
      )}

      {mode === "paste" && (
        <div className="bg-bg-card border border-border rounded-xl p-8">
          <label className="block text-sm text-text-secondary mb-2">Kodunu yapıştır (max 1MB)</label>
          <textarea
            rows={10}
            placeholder="Kodunu buraya yapıştır..."
            value={pasteCode}
            onChange={(e) => setPasteCode(e.target.value)}
            className="w-full px-4 py-3 bg-bg-secondary border border-border rounded-lg text-text-primary outline-none focus:border-accent focus:shadow-[0_0_0_3px_var(--color-accent-glow)] mb-4 font-mono text-sm resize-none"
          />
          <button
            onClick={handlePaste}
            disabled={uploading || !pasteCode.trim()}
            className="w-full px-6 py-3 bg-accent text-white rounded-lg font-medium hover:bg-accent-hover transition disabled:opacity-50 cursor-pointer"
          >
            {uploading ? "Gönderiliyor..." : "Analiz Et"}
          </button>
        </div>
      )}
    </div>
  );
}