import { useEffect, useState } from 'react';
import { warningsService } from '@/services/api/resourceServices';
import type { Warning } from '@/types';
import { fmtDate } from '@/utils/format';
import { StatusBadge } from '@/components/ui/StatusBadge';

export function WarningsPage() {
  const [items, setItems] = useState<Warning[]>([]);
  useEffect(() => { warningsService.list().then(setItems); }, []);

  return (
    <article className="card table-card">
      <div className="card__header"><h3>Warnings</h3><p>Pre-challan warning communication log</p></div>
      <table className="data-table">
        <thead><tr><th>ID</th><th>Plate</th><th>Owner</th><th>Location</th><th>Date</th><th>Status</th></tr></thead>
        <tbody>
          {items.map((item) => <tr key={item.id}><td>{item.id}</td><td>{item.plateText}</td><td>{item.ownerName}</td><td>{item.location}</td><td>{fmtDate(item.issuedAt)}</td><td><StatusBadge status={item.status} /></td></tr>)}
        </tbody>
      </table>
    </article>
  );
}
