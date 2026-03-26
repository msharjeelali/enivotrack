import { useEffect, useState } from 'react';
import { usersService } from '@/services/api/resourceServices';
import type { User } from '@/types';
import { fmtDate } from '@/utils/format';
import { StatusBadge } from '@/components/ui/StatusBadge';

export function UsersPage() {
  const [items, setItems] = useState<User[]>([]);
  useEffect(() => { usersService.list().then(setItems); }, []);
  return (
    <article className="card table-card">
      <div className="card__header"><h3>User Management</h3><p>Authorized admin and super admin access</p></div>
      <table className="data-table">
        <thead><tr><th>Name</th><th>Email</th><th>Role</th><th>Status</th><th>Joined</th><th>Last Activity</th></tr></thead>
        <tbody>
          {items.map((item) => <tr key={item.id}><td>{item.name}</td><td>{item.email}</td><td><StatusBadge status={item.role} /></td><td><StatusBadge status={item.status} /></td><td>{fmtDate(item.joinedAt)}</td><td>{fmtDate(item.lastActivity)}</td></tr>)}
        </tbody>
      </table>
    </article>
  );
}
