import type { LucideIcon } from 'lucide-react';

export function EmptyState({ icon: Icon, title, desc }: { icon: LucideIcon; title: string; desc: string }) {
  return (
    <div className="empty-state">
      <div className="empty-icon"><Icon size={24} /></div>
      <h3>{title}</h3>
      <p>{desc}</p>
    </div>
  );
}
