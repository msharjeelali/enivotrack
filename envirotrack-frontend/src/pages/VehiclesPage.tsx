import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { vehiclesService } from '@/services/api/resourceServices';
import type { Vehicle } from '@/types';
import { fmtDate } from '@/utils/format';
import { StatusBadge } from '@/components/ui/StatusBadge';

export function VehiclesPage() {
  const [items, setItems] = useState<Vehicle[]>([]);
  useEffect(() => { vehiclesService.list().then(setItems); }, []);
  return (
    <article className="card table-card">
      <div className="card__header"><h3>Vehicles</h3><p>Vehicle history and repeat offender tracking</p></div>
      <table className="data-table">
        <thead><tr><th>Plate</th><th>Owner</th><th>Violations</th><th>Warnings</th><th>Challans</th><th>Last Seen</th><th>Status</th><th /></tr></thead>
        <tbody>
          {items.map((item) => <tr key={item.plateText}><td>{item.plateText}</td><td>{item.ownerName}</td><td>{item.totalViolations}</td><td>{item.totalWarnings}</td><td>{item.totalChallans}</td><td>{fmtDate(item.lastSeen)}</td><td><StatusBadge status={item.status} /></td><td><Link to={`/vehicles/${item.plateText}`}>View</Link></td></tr>)}
        </tbody>
      </table>
    </article>
  );
}
