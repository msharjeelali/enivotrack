import { AlertTriangle, Search } from 'lucide-react';
import { useEffect, useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import { EmptyState } from '@/components/ui/EmptyState';
import { Pagination } from '@/components/ui/Pagination';
import { StatusBadge } from '@/components/ui/StatusBadge';
import { ConfidenceBar } from '@/components/ui/ConfidenceBar';
import { violationsService } from '@/services/api/resourceServices';
import type { Violation } from '@/types';
import { fmtDate, fmtTime } from '@/utils/format';

export function ViolationsPage() {
  const [items, setItems] = useState<Violation[]>([]);
  const [search, setSearch] = useState('');
  const [status, setStatus] = useState('all');
  const [page, setPage] = useState(1);
  const perPage = 8;

  useEffect(() => { violationsService.list().then(setItems); }, []);

  const filtered = useMemo(() => items.filter((item) => {
    const hit = !search || `${item.id} ${item.plateText} ${item.location}`.toLowerCase().includes(search.toLowerCase());
    const state = status === 'all' || item.status === status;
    return hit && state;
  }), [items, search, status]);

  const pageItems = filtered.slice((page - 1) * perPage, page * perPage);

  return (
    <div className="page-grid">
      <section className="toolbar card-inline">
        <div className="search-input"><Search size={16} /><input value={search} onChange={(e) => { setSearch(e.target.value); setPage(1); }} placeholder="Search by plate, ID, location" /></div>
        <select value={status} onChange={(e) => { setStatus(e.target.value); setPage(1); }}>
          <option value="all">All statuses</option>
          <option value="pending">Pending review</option>
          <option value="warning_issued">Warning issued</option>
          <option value="challan_issued">Challan issued</option>
          <option value="dismissed">Dismissed</option>
        </select>
      </section>
      <article className="card table-card">
        <table className="data-table">
          <thead><tr><th>ID</th><th>Plate</th><th>Location</th><th>Time</th><th>Smoke</th><th>Status</th><th /></tr></thead>
          <tbody>
            {pageItems.length === 0 ? <tr><td colSpan={7}><EmptyState icon={AlertTriangle} title="No violations found" desc="Try changing your filters." /></td></tr> : pageItems.map((item) => (
              <tr key={item.id}>
                <td>{item.id}</td>
                <td><strong>{item.plateText}</strong></td>
                <td>{item.location}</td>
                <td>{fmtDate(item.timestamp)} <small>{fmtTime(item.timestamp)}</small></td>
                <td><ConfidenceBar value={item.smokeConfidence} /></td>
                <td><StatusBadge status={item.status} /></td>
                <td><Link to={`/violations/${item.id}`}>View</Link></td>
              </tr>
            ))}
          </tbody>
        </table>
        <Pagination page={page} total={filtered.length} perPage={perPage} onPage={setPage} />
      </article>
    </div>
  );
}
