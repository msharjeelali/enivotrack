import { useEffect, useState } from 'react';
import { settingsService } from '@/services/api/resourceServices';
import type { Settings } from '@/types';

export function SettingsPage() {
  const [settings, setSettings] = useState<Settings | null>(null);
  useEffect(() => { settingsService.get().then(setSettings); }, []);
  if (!settings) return <div className="screen-center">Loading settings…</div>;
  return (
    <div className="page-grid">
      <article className="card stack-sm">
        <div className="card__header"><h3>Enforcement Thresholds</h3><p>Mock-configured for now, ready for API wiring</p></div>
        <div className="setting-row"><span>Challan Threshold</span><strong>{settings.challanThreshold} warnings</strong></div>
        <div className="setting-row"><span>Smoke Confidence Threshold</span><strong>{Math.round(settings.confidenceThreshold * 100)}%</strong></div>
        <div className="setting-row"><span>Review Window</span><strong>{settings.reviewWindow} hours</strong></div>
        <div className="setting-row"><span>Email Notifications</span><strong>{settings.emailNotifications ? 'Enabled' : 'Disabled'}</strong></div>
        <div className="setting-row"><span>Auto Issue Challans</span><strong>{settings.autoIssueChallans ? 'Enabled' : 'Disabled'}</strong></div>
      </article>
    </div>
  );
}
