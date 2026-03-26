import { useEffect, useState } from 'react';
import { camerasService } from '@/services/api/resourceServices';
import type { Camera } from '@/types';
import { StatusBadge } from '@/components/ui/StatusBadge';
import { fmtDate } from '@/utils/format';

export function CamerasPage() {
  const [items, setItems] = useState<Camera[]>([]);
  useEffect(() => { camerasService.list().then(setItems); }, []);
  return (
    <article className="card table-card">
      <div className="card__header"><h3>Cameras</h3><p>Monitoring and stream health overview</p></div>
      <table className="data-table">
        <thead><tr><th>Camera</th><th>Location</th><th>IP</th><th>Installed</th><th>Detections</th><th>Status</th></tr></thead>
        <tbody>
          {items.map((item) => <tr key={item.id}><td>{item.id}</td><td>{item.location}</td><td>{item.ipAddress}</td><td>{fmtDate(item.installationDate)}</td><td>{item.detectionCount}</td><td><StatusBadge status={item.status} /></td></tr>)}
        </tbody>
      </table>
    </article>
  );
}
