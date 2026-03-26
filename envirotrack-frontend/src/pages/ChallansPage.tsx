import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { challansService } from '@/services/api/resourceServices';
import type { Challan } from '@/types';
import { fmtCurrency, fmtDate } from '@/utils/format';
import { StatusBadge } from '@/components/ui/StatusBadge';

export function ChallansPage() {
  const [items, setItems] = useState<Challan[]>([]);
  useEffect(() => { challansService.list().then(setItems); }, []);

  return (
    <article className="card table-card">
      <div className="card__header"><h3>Challans</h3><p>Issued and disputed enforcement actions</p></div>
      <table className="data-table">
        <thead><tr><th>Challan</th><th>Plate</th><th>Owner</th><th>Date</th><th>Fine</th><th>Status</th><th /></tr></thead>
        <tbody>
          {items.map((item) => (
            <tr key={item.id}>
              <td>{item.challanNumber}</td><td>{item.plateText}</td><td>{item.ownerName}</td><td>{fmtDate(item.issuedAt)}</td><td>{fmtCurrency(item.fineAmount)}</td><td><StatusBadge status={item.status} /></td><td><Link to={`/challans/${item.id}`}>View</Link></td>
            </tr>
          ))}
        </tbody>
      </table>
    </article>
  );
}
