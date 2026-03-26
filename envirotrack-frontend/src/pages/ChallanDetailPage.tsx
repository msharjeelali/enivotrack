import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { challansService } from '@/services/api/resourceServices';
import type { Challan } from '@/types';
import { fmtCurrency, fmtDateTime } from '@/utils/format';
import { StatusBadge } from '@/components/ui/StatusBadge';

export function ChallanDetailPage() {
  const { id = '' } = useParams();
  const [item, setItem] = useState<Challan | null>(null);
  useEffect(() => { challansService.getById(id).then(setItem); }, [id]);
  if (!item) return <div className="screen-center">Challan not found.</div>;

  return (
    <div className="page-grid detail-layout">
      <article className="card detail-main stack-sm">
        <Link to="/challans" className="back-link">← Back to challans</Link>
        <h2>{item.challanNumber}</h2>
        <div className="detail-grid two-cols">
          <div><span>Plate</span><strong>{item.plateText}</strong></div>
          <div><span>Owner</span><strong>{item.ownerName}</strong></div>
          <div><span>Issued At</span><strong>{fmtDateTime(item.issuedAt)}</strong></div>
          <div><span>Fine Amount</span><strong>{fmtCurrency(item.fineAmount)}</strong></div>
          <div><span>Location</span><strong>{item.location}</strong></div>
          <div><span>Status</span><StatusBadge status={item.status} /></div>
        </div>
      </article>
      <aside className="detail-side"><article className="card"><h3>Evidence</h3><p>Proof link: {item.proofLink}</p></article></aside>
    </div>
  );
}
