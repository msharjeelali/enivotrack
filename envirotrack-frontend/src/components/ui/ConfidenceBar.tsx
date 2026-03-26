export function ConfidenceBar({ value }: { value: number }) {
  const pct = Math.round(value * 100);
  const color = pct >= 85 ? '#16a34a' : pct >= 70 ? '#f59e0b' : '#ef4444';

  return (
    <div className="confidence-wrap">
      <div className="confidence-track">
        <div className="confidence-fill" style={{ width: `${pct}%`, background: color }} />
      </div>
      <span style={{ color }}>{pct}%</span>
    </div>
  );
}
