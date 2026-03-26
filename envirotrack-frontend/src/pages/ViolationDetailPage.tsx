import { ChevronLeft, FileText, AlertTriangle } from 'lucide-react';
import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { Modal } from '@/components/ui/Modal';
import { StatusBadge } from '@/components/ui/StatusBadge';
import { ConfidenceBar } from '@/components/ui/ConfidenceBar';
import { vehiclesService, violationsService } from '@/services/api/resourceServices';
import type { Vehicle, Violation } from '@/types';
import { fmtDateTime } from '@/utils/format';

export function ViolationDetailPage() {
  const { id = '' } = useParams();
  const [item, setItem] = useState<Violation | null>(null);
  const [vehicle, setVehicle] = useState<Vehicle | null>(null);
  const [modal, setModal] = useState<string | null>(null);

  useEffect(() => {
    violationsService.getById(id).then((found) => {
      setItem(found);
      if (found) vehiclesService.getByPlate(found.plateText).then(setVehicle);
    });
  }, [id]);

  if (!item) return <div className="screen-center">Violation not found.</div>;

  return (
    <div className="page-grid detail-layout">
      <div className="detail-main">
        <Link to="/violations" className="back-link"><ChevronLeft size={16} /> Back to violations</Link>
        <article className="card">
          <div className="detail-evidence">
            <div className="smoke-box">SMOKE {Math.round(item.smokeConfidence * 100)}%</div>
            <div className="plate-box">{item.plateText}</div>
          </div>
          <div className="detail-grid two-cols">
            <div><span>Smoke Confidence</span><ConfidenceBar value={item.smokeConfidence} /></div>
            <div><span>Plate Confidence</span><ConfidenceBar value={item.plateConfidence} /></div>
            <div><span>Camera</span><strong>{item.cameraId}</strong></div>
            <div><span>Timestamp</span><strong>{fmtDateTime(item.timestamp)}</strong></div>
          </div>
        </article>
      </div>
      <aside className="detail-side">
        <article className="card stack-sm">
          <h3>Violation Info</h3>
          <div className="kv"><span>ID</span><strong>{item.id}</strong></div>
          <div className="kv"><span>Plate</span><strong>{item.plateText}</strong></div>
          <div className="kv"><span>Location</span><strong>{item.location}</strong></div>
          <div className="kv"><span>Status</span><StatusBadge status={item.status} /></div>
        </article>
        {vehicle ? (
          <article className="card stack-sm">
            <h3>Vehicle / Owner</h3>
            <div className="kv"><span>Owner</span><strong>{vehicle.ownerName}</strong></div>
            <div className="kv"><span>Email</span><strong>{vehicle.ownerEmail}</strong></div>
            <div className="kv"><span>Total Violations</span><strong>{vehicle.totalViolations}</strong></div>
            <Link to={`/vehicles/${vehicle.plateText}`}>View full history</Link>
          </article>
        ) : null}
        <article className="card stack-sm">
          <h3>Actions</h3>
          <button className="btn btn-secondary" onClick={() => setModal('warning')}><AlertTriangle size={16} /> Issue Warning</button>
          <button className="btn btn-primary" onClick={() => setModal('challan')}><FileText size={16} /> Issue Challan</button>
        </article>
      </aside>
      <Modal open={!!modal} onClose={() => setModal(null)} title={modal === 'warning' ? 'Issue Warning' : 'Issue Challan'}>
        <p>This is wired as a reusable modal and can later be connected to the real backend.</p>
        <button className="btn btn-primary" onClick={() => setModal(null)}>Confirm</button>
      </Modal>
    </div>
  );
}
