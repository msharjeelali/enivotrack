import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { ProtectedRoute } from './ProtectedRoute';
import { AppShell } from '@/components/layout/AppShell';
import { LoginPage } from '@/pages/LoginPage';
import { DashboardPage } from '@/pages/DashboardPage';
import { ViolationsPage } from '@/pages/ViolationsPage';
import { ViolationDetailPage } from '@/pages/ViolationDetailPage';
import { ChallansPage } from '@/pages/ChallansPage';
import { ChallanDetailPage } from '@/pages/ChallanDetailPage';
import { WarningsPage } from '@/pages/WarningsPage';
import { CamerasPage } from '@/pages/CamerasPage';
import { VehiclesPage } from '@/pages/VehiclesPage';
import { VehicleDetailPage } from '@/pages/VehicleDetailPage';
import { UsersPage } from '@/pages/UsersPage';
import { SettingsPage } from '@/pages/SettingsPage';
import { NotFoundPage } from '@/pages/NotFoundPage';

export function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route element={<ProtectedRoute />}>
          <Route element={<AppShell />}>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/violations" element={<ViolationsPage />} />
            <Route path="/violations/:id" element={<ViolationDetailPage />} />
            <Route path="/challans" element={<ChallansPage />} />
            <Route path="/challans/:id" element={<ChallanDetailPage />} />
            <Route path="/warnings" element={<WarningsPage />} />
            <Route path="/cameras" element={<CamerasPage />} />
            <Route path="/vehicles" element={<VehiclesPage />} />
            <Route path="/vehicles/:plate" element={<VehicleDetailPage />} />
            <Route path="/settings" element={<SettingsPage />} />
            <Route element={<ProtectedRoute requireSuperAdmin />}>
              <Route path="/users" element={<UsersPage />} />
            </Route>
          </Route>
        </Route>
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </BrowserRouter>
  );
}
