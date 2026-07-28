"use client";

interface Props {
  prompt: string;
}

export default function PromptGenerator({ prompt }: Props) {
  if (!prompt) return null;

  const copyPrompt = () => {
    navigator.clipboard.writeText(prompt);
  };

  return (
    <div className="bg-gradient-to-r from-accent/10 to-purple-500/10 border border-accent/30 rounded-xl p-6 animate-fade-in">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-text-primary font-semibold flex items-center gap-2">
          <span>✨</span> AI Prompt Generator
        </h3>
        <span className="text-xs text-text-secondary bg-bg-secondary px-3 py-1 rounded-full">
          OpenCode · Claude · Cursor
        </span>
      </div>
      <p className="text-text-secondary text-sm mb-3">
        Bu prompt'u AI kod editörüne yapıştır, eksikleri otomatik düzeltsin:
      </p>
      <pre className="bg-bg-primary border border-border rounded-lg p-4 text-sm text-text-primary font-mono whitespace-pre-wrap max-h-48 overflow-y-auto mb-4">
        {prompt}
      </pre>
      <button
        onClick={copyPrompt}
        className="px-6 py-2.5 bg-accent text-white rounded-lg text-sm font-medium hover:bg-accent-hover transition cursor-pointer"
      >
        📋 Prompt'u Kopyala
      </button>
    </div>
  );
}