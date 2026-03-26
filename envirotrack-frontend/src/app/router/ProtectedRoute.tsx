import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';

export function ProtectedRoute({ requireSuperAdmin = false }: { requireSuperAdmin?: boolean }) {
  const { user, loading } = useAuth();
  if (loading) return <div className="screen-center">Loading…</div>;
  if (!user) return <Navigate to="/login" replace />;
  if (requireSuperAdmin && user.role !== 'super_admin') return <Navigate to="/dashboard" replace />;
  return <Outlet />;
}
