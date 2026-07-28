interface Props {
  scores: { label: string; score: number }[];
}

export default function AnalysisChart({ scores }: Props) {
  const size = 220;
  const cx = size / 2;
  const cy = size / 2;
  const radius = 80;
  const levels = 5;

  const points = scores.map((s, i) => {
    const angle = (Math.PI * 2 * i) / scores.length - Math.PI / 2;
    const r = (s.score / 100) * radius;
    return { x: cx + r * Math.cos(angle), y: cy + r * Math.sin(angle), label: s.label, score: s.score };
  });

  const polygon = points.map((p) => `${p.x},${p.y}`).join(" ");

  return (
    <div className="bg-bg-card border border-border rounded-xl p-6 flex flex-col items-center animate-fade-in">
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        {Array.from({ length: levels }).map((_, li) => {
          const lr = ((li + 1) / levels) * radius;
          const lp = scores.map((_, si) => {
            const angle = (Math.PI * 2 * si) / scores.length - Math.PI / 2;
            return `${cx + lr * Math.cos(angle)},${cy + lr * Math.sin(angle)}`;
          }).join(" ");
          return <polygon key={li} points={lp} fill="none" stroke="#2a2a3e" strokeWidth={1} />;
        })}
        {scores.map((_, si) => {
          const angle = (Math.PI * 2 * si) / scores.length - Math.PI / 2;
          const x2 = cx + radius * Math.cos(angle);
          const y2 = cy + radius * Math.sin(angle);
          return <line key={si} x1={cx} y1={cy} x2={x2} y2={y2} stroke="#2a2a3e" strokeWidth={1} />;
        })}
        <polygon points={polygon} fill="rgba(124,58,237,0.2)" stroke="#7c3aed" strokeWidth={2} />
        {points.map((p, i) => (
          <circle key={i} cx={p.x} cy={p.y} r={4} fill="#7c3aed" />
        ))}
      </svg>
      <div className="grid grid-cols-2 gap-x-6 gap-y-1 mt-4">
        {scores.map((s, i) => (
          <div key={i} className="flex items-center gap-2 text-sm">
            <span className="w-2 h-2 rounded-full bg-accent" />
            <span className="text-text-secondary">{s.label}</span>
            <span className="text-text-primary font-medium">{s.score}</span>
          </div>
        ))}
      </div>
    </div>
  );
}