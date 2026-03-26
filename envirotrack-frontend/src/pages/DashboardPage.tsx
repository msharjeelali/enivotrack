import { AlertOctagon, AlertTriangle, Camera, FileText, Zap } from 'lucide-react';
import { Area, AreaChart, CartesianGrid, Cell, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { dashboardService } from '@/services/api/dashboardService';
import { useEffect, useState } from 'react';
import type { ActivityItem, DashboardStats, DistributionItem, TrendPoint } from '@/types';
import { StatCard } from '@/components/ui/StatCard';
import { useNavigate } from 'react-router-dom';

export function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [trend, setTrend] = useState<TrendPoint[]>([]);
  const [distribution, setDistribution] = useState<DistributionItem[]>([]);
  const [activities, setActivities] = useState<ActivityItem[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    dashboardService.getStats().then(setStats);
    dashboardService.getTrend().then(setTrend);
    dashboardService.getStatusDistribution().then(setDistribution);
    dashboardService.getActivities().then(setActivities);
  }, []);

  if (!stats) return <div className="screen-center">Loading dashboard…</div>;

  return (
    <div className="page-grid">
      <section className="stats-grid">
        <StatCard label="Active Cameras" value={stats.activeCameras} icon={Camera} iconClass="cyan" trend="+5%" onClick={() => navigate('/cameras')} />
        <StatCard label="Detections Today" value={stats.detectionsToday} icon={Zap} iconClass="purple" trend="+12%" onClick={() => navigate('/violations')} />
        <StatCard label="Warnings Issued" value={stats.warningsIssued} icon={AlertTriangle} iconClass="amber" trend="+8%" onClick={() => navigate('/warnings')} />
        <StatCard label="Challans Issued" value={stats.challansIssued} icon={FileText} iconClass="red" trend="+3%" onClick={() => navigate('/challans')} />
        <StatCard label="Repeat Offenders" value={stats.repeatOffenders} icon={AlertOctagon} iconClass="red" trend="-2%" onClick={() => navigate('/vehicles')} />
      </section>
      <section className="charts-grid">
        <article className="card">
          <div className="card__header"><h3>Detection Trends</h3><p>Last 14 days</p></div>
          <ResponsiveContainer width="100%" height={260}>
            <AreaChart data={trend}>
              <defs>
                <linearGradient id="d1" x1="0" y1="0" x2="0" y2="1"><stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} /><stop offset="95%" stopColor="#6366f1" stopOpacity={0} /></linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="day" tick={{ fontSize: 12 }} />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip />
              <Area type="monotone" dataKey="detections" stroke="#6366f1" fill="url(#d1)" />
              <Area type="monotone" dataKey="warnings" stroke="#f59e0b" fill="transparent" />
            </AreaChart>
          </ResponsiveContainer>
        </article>
        <article className="card">
          <div className="card__header"><h3>Status Distribution</h3><p>Overall enforcement state</p></div>
          <ResponsiveContainer width="100%" height={240}>
            <PieChart>
              <Pie data={distribution} dataKey="value" innerRadius={52} outerRadius={78}>
                {distribution.map((item) => <Cell key={item.name} fill={item.color} />)}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
          <div className="legend-list">
            {distribution.map((item) => (
              <div key={item.name}><span><i style={{ background: item.color }} />{item.name}</span><strong>{item.value}</strong></div>
            ))}
          </div>
        </article>
      </section>
      <article className="card">
        <div className="card__header"><h3>Recent Activity</h3><p>System actions and enforcement workflow</p></div>
        <div className="simple-list">
          {activities.map((item) => <div key={item.id}><strong>{item.description}</strong><span>{item.time} • {item.targetId}</span></div>)}
        </div>
      </article>
    </div>
  );
}
