import { ChevronLeft, ChevronRight } from 'lucide-react';

export function Pagination({ page, total, perPage, onPage }: { page: number; total: number; perPage: number; onPage: (page: number) => void }) {
  const totalPages = Math.ceil(total / perPage);
  if (totalPages <= 1) return null;
  return (
    <div className="pagination">
      <span>Showing {(page - 1) * perPage + 1}-{Math.min(page * perPage, total)} of {total}</span>
      <div className="pagination-controls">
        <button onClick={() => onPage(page - 1)} disabled={page === 1}><ChevronLeft size={16} /></button>
        {Array.from({ length: totalPages }, (_, i) => i + 1).slice(0, 5).map((p) => (
          <button key={p} className={p === page ? 'active' : ''} onClick={() => onPage(p)}>{p}</button>
        ))}
        <button onClick={() => onPage(page + 1)} disabled={page === totalPages}><ChevronRight size={16} /></button>
      </div>
    </div>
  );
}
