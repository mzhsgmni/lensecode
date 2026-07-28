interface Props {
  label: string;
  score: number;
  icon: string;
  color?: string;
}

export default function ScoreCard({ label, score, icon, color = "accent" }: Props) {
  const barColor =
    color === "accent" ? "bg-accent" :
    color === "green" ? "bg-green-500" :
    color === "yellow" ? "bg-yellow-500" :
    color === "red" ? "bg-red-500" : "bg-accent";

  return (
    <div className="bg-bg-card border border-border rounded-xl p-5 hover:border-accent transition-all duration-300 animate-fade-in">
      <div className="flex items-center justify-between mb-3">
        <span className="text-2xl">{icon}</span>
        <span className="text-3xl font-bold gradient-text">{score}</span>
      </div>
      <p className="text-text-secondary text-sm mb-2">{label}</p>
      <div className="w-full h-2 bg-bg-secondary rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-1000 ${barColor}`}
          style={{ width: `${score}%` }}
        />
      </div>
    </div>
  );
}