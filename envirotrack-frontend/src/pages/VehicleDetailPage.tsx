import { useEffect, useMemo, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { vehiclesService, violationsService, challansService, warningsService } from '@/services/api/resourceServices';
import type { Challan, Vehicle, Violation, Warning } from '@/types';
import { fmtDateTime } from '@/utils/format';

export function VehicleDetailPage() {
  const { plate = '' } = useParams();
  const [vehicle, setVehicle] = useState<Vehicle | null>(null);
  const [violations, setViolations] = useState<Violation[]>([]);
  const [challans, setChallans] = useState<Challan[]>([]);
  const [warnings, setWarnings] = useState<Warning[]>([]);

  useEffect(() => {
    vehiclesService.getByPlate(plate).then(setVehicle);
    violationsService.list().then(setViolations);
    challansService.list().then(setChallans);
    warningsService.list().then(setWarnings);
  }, [plate]);

  const vehicleViolations = useMemo(() => violations.filter((item) => item.plateText === plate), [violations, plate]);
  const vehicleChallans = useMemo(() => challans.filter((item) => item.plateText === plate), [challans, plate]);
  const vehicleWarnings = useMemo(() => warnings.filter((item) => item.plateText === plate), [warnings, plate]);

  if (!vehicle) return <div className="screen-center">Vehicle not found.</div>;

  return (
    <div className="page-grid">
      <article className="card stack-sm">
        <Link to="/vehicles" className="back-link">← Back to vehicles</Link>
        <h2>{vehicle.plateText}</h2>
        <div className="detail-grid two-cols">
          <div><span>Owner</span><strong>{vehicle.ownerName}</strong></div>
          <div><span>Email</span><strong>{vehicle.ownerEmail}</strong></div>
          <div><span>Total Violations</span><strong>{vehicle.totalViolations}</strong></div>
          <div><span>Total Challans</span><strong>{vehicle.totalChallans}</strong></div>
        </div>
      </article>
      <article className="card"><div className="card__header"><h3>Violation History</h3><p>{vehicleViolations.length} records</p></div><div className="simple-list">{vehicleViolations.map((item) => <div key={item.id}><strong>{item.id}</strong><span>{item.location} • {fmtDateTime(item.timestamp)}</span></div>)}</div></article>
      <article className="card"><div className="card__header"><h3>Warnings</h3><p>{vehicleWarnings.length} records</p></div><div className="simple-list">{vehicleWarnings.map((item) => <div key={item.id}><strong>{item.id}</strong><span>{item.location}</span></div>)}</div></article>
      <article className="card"><div className="card__header"><h3>Challans</h3><p>{vehicleChallans.length} records</p></div><div className="simple-list">{vehicleChallans.map((item) => <div key={item.id}><strong>{item.challanNumber}</strong><span>{item.location}</span></div>)}</div></article>
    </div>
  );
}
