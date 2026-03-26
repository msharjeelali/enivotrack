import { Bell, Menu, Activity, LayoutDashboard, AlertTriangle, FileText, Camera, Car, Users, Settings, LogOut } from 'lucide-react';
import { NavLink, Outlet } from 'react-router-dom';
import { useState } from 'react';
import { useAuth } from '@/context/AuthContext';

const navItems = [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/violations', label: 'Violations', icon: AlertTriangle },
  { to: '/challans', label: 'Challans', icon: FileText },
  { to: '/warnings', label: 'Warnings', icon: Bell },
  { to: '/cameras', label: 'Cameras', icon: Camera },
  { to: '/vehicles', label: 'Vehicles', icon: Car },
  { to: '/users', label: 'User Management', icon: Users, superAdminOnly: true },
  { to: '/settings', label: 'Settings', icon: Settings },
];

export function AppShell() {
  const [collapsed, setCollapsed] = useState(false);
  const { user, logout } = useAuth();

  return (
    <div className="app-shell">
      <aside className={`sidebar ${collapsed ? 'collapsed' : ''}`}>
        <div className="sidebar__brand">
          <span className="brand-icon"><Activity size={20} /></span>
          {!collapsed && <div><strong>EnviroTrack</strong><span>Admin Portal</span></div>}
          <button onClick={() => setCollapsed((v) => !v)}><Menu size={16} /></button>
        </div>
        <nav className="sidebar__nav">
          {navItems.map(({ to, label, icon: Icon, superAdminOnly }) => {
            if (superAdminOnly && user?.role !== 'super_admin') return null;
            return (
              <NavLink key={to} to={to} className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}>
                <Icon size={18} />
                {!collapsed && <span>{label}</span>}
              </NavLink>
            );
          })}
        </nav>
        <div className="sidebar__footer">
          {!collapsed && (
            <div className="profile-block">
              <div className="avatar">{user?.name?.charAt(0)}</div>
              <div>
                <strong>{user?.name}</strong>
                <span>{user?.role === 'super_admin' ? 'Super Admin' : 'Admin'}</span>
              </div>
            </div>
          )}
          <button className="logout-btn" onClick={logout}><LogOut size={16} /></button>
        </div>
      </aside>
      <section className="content-area">
        <header className="topbar">
          <div>
            <p>Punjab Safe Cities Authority</p>
            <h1>Environmental Monitoring Dashboard</h1>
          </div>
          <div className="topbar-actions">
            <button><Bell size={16} /></button>
            <span className="avatar">{user?.name?.charAt(0)}</span>
          </div>
        </header>
        <main className="page-content"><Outlet /></main>
      </section>
    </div>
  );
}
