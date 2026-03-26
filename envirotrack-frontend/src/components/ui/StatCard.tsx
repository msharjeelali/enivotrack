import type { LucideIcon } from 'lucide-react';

export function StatCard({ label, value, icon: Icon, iconClass, trend, onClick }: { label: string; value: number; icon: LucideIcon; iconClass: string; trend?: string; onClick?: () => void }) {
  return (
    <button className="stat-card" onClick={onClick}>
      <div className="stat-card__top">
        <span className={`stat-card__icon ${iconClass}`}><Icon size={20} /></span>
        {trend ? <small>{trend}</small> : null}
      </div>
      <strong>{value.toLocaleString()}</strong>
      <span>{label}</span>
    </button>
  );
}
