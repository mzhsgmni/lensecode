interface Props {
  title: string;
  items: string[];
  icon: string;
  type?: "missing" | "redundant" | "security";
}

export default function FeatureChecklist({ title, items, icon, type = "missing" }: Props) {
  if (!items || items.length === 0) return null;

  const colors = {
    missing: { icon: "❌", bg: "bg-red-500/10", text: "text-red-400", border: "border-red-500/20" },
    redundant: { icon: "⚠️", bg: "bg-yellow-500/10", text: "text-yellow-400", border: "border-yellow-500/20" },
    security: { icon: "🛡️", bg: "bg-orange-500/10", text: "text-orange-400", border: "border-orange-500/20" },
  };

  const c = colors[type];

  return (
    <div className="bg-bg-card border border-border rounded-xl p-6 animate-fade-in">
      <h3 className="text-text-primary font-semibold mb-4 flex items-center gap-2">
        <span>{icon}</span> {title} <span className="text-text-secondary text-sm">({items.length})</span>
      </h3>
      <div className="space-y-2">
        {items.slice(0, 15).map((item, i) => (
          <div key={i} className={`flex items-center gap-2 px-3 py-2 rounded-lg ${c.bg} ${c.border} border`}>
            <span>{c.icon}</span>
            <span className={`text-sm ${c.text}`}>{item}</span>
          </div>
        ))}
        {items.length > 15 && (
          <p className="text-text-secondary text-xs text-center pt-1">+{items.length - 15} daha...</p>
        )}
      </div>
    </div>
  );
}