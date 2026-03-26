const STATUS_CONFIG: Record<string, { label: string; color: string; bg: string }> = {
  pending: { label: 'Pending Review', color: '#6366f1', bg: '#eef2ff' },
  warning_issued: { label: 'Warning Issued', color: '#d97706', bg: '#fffbeb' },
  challan_issued: { label: 'Challan Issued', color: '#dc2626', bg: '#fef2f2' },
  dismissed: { label: 'Dismissed', color: '#64748b', bg: '#f1f5f9' },
  issued: { label: 'Issued', color: '#16a34a', bg: '#f0fdf4' },
  paid: { label: 'Paid', color: '#0891b2', bg: '#ecfeff' },
  cancelled: { label: 'Cancelled', color: '#64748b', bg: '#f1f5f9' },
  disputed: { label: 'Disputed', color: '#d97706', bg: '#fffbeb' },
  sent: { label: 'Sent', color: '#16a34a', bg: '#f0fdf4' },
  delivered: { label: 'Delivered', color: '#0891b2', bg: '#ecfeff' },
  failed: { label: 'Failed', color: '#dc2626', bg: '#fef2f2' },
  active: { label: 'Active', color: '#16a34a', bg: '#f0fdf4' },
  offline: { label: 'Offline', color: '#dc2626', bg: '#fef2f2' },
  maintenance: { label: 'Maintenance', color: '#d97706', bg: '#fffbeb' },
  repeat_offender: { label: 'Repeat Offender', color: '#dc2626', bg: '#fef2f2' },
  warned: { label: 'Warned', color: '#d97706', bg: '#fffbeb' },
  inactive: { label: 'Inactive', color: '#64748b', bg: '#f1f5f9' },
  super_admin: { label: 'Super Admin', color: '#7c3aed', bg: '#f5f3ff' },
  admin: { label: 'Admin', color: '#1d4ed8', bg: '#eff6ff' },
};

export function StatusBadge({ status }: { status: string }) {
  const cfg = STATUS_CONFIG[status] ?? { label: status, color: '#64748b', bg: '#f1f5f9' };
  return (
    <span className="badge" style={{ color: cfg.color, background: cfg.bg, borderColor: `${cfg.color}30` }}>
      {cfg.label}
    </span>
  );
}
