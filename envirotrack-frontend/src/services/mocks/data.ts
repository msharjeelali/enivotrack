import type { ActivityItem, AuthUser, Camera, Challan, DashboardStats, DistributionItem, Settings, TrendPoint, User, Vehicle, Violation, Warning } from '@/types';

export const mockAuthUser: AuthUser = {
  id: 'u1',
  username: 'admin',
  name: 'Sarah Khan',
  email: 'sarah@psca.gov.pk',
  role: 'super_admin',
};

export const dashboardStats: DashboardStats = {
  activeCameras: 34,
  detectionsToday: 47,
  challansIssued: 128,
  warningsIssued: 312,
  pendingReview: 11,
  repeatOffenders: 23,
  totalViolations: 1047,
  resolvedToday: 36,
};

export const detectionTrend: TrendPoint[] = [
  { day: 'Mar 11', detections: 32, challans: 8, warnings: 24 },
  { day: 'Mar 12', detections: 41, challans: 11, warnings: 30 },
  { day: 'Mar 13', detections: 28, challans: 6, warnings: 22 },
  { day: 'Mar 14', detections: 55, challans: 14, warnings: 41 },
  { day: 'Mar 15', detections: 38, challans: 9, warnings: 29 },
  { day: 'Mar 16', detections: 63, challans: 17, warnings: 46 },
  { day: 'Mar 17', detections: 47, challans: 12, warnings: 35 },
  { day: 'Mar 18', detections: 52, challans: 15, warnings: 37 },
  { day: 'Mar 19', detections: 39, challans: 9, warnings: 30 },
  { day: 'Mar 20', detections: 71, challans: 19, warnings: 52 },
  { day: 'Mar 21', detections: 44, challans: 11, warnings: 33 },
  { day: 'Mar 22', detections: 58, challans: 16, warnings: 42 },
  { day: 'Mar 23', detections: 65, challans: 18, warnings: 47 },
  { day: 'Mar 24', detections: 47, challans: 12, warnings: 35 },
];

export const statusDistribution: DistributionItem[] = [
  { name: 'Warnings', value: 312, color: '#f59e0b' },
  { name: 'Challans Issued', value: 128, color: '#ef4444' },
  { name: 'Dismissed', value: 41, color: '#94a3b8' },
  { name: 'Pending', value: 11, color: '#6366f1' },
];

export const recentActivities: ActivityItem[] = [
  { id: 'ACT-8927', description: 'Smoke emission detected', time: '10:30 AM', targetId: 'CAM-001', type: 'detection' },
  { id: 'ACT-8926', description: 'Challan issued for vehicle', time: '11:15 AM', targetId: 'LEA-4432', type: 'challan' },
  { id: 'ACT-8925', description: 'Warning issued', time: '09:00 AM', targetId: 'LHR-5512', type: 'warning' },
  { id: 'ACT-8924', description: 'Admin logged in', time: '08:47 AM', targetId: 'Admin-Sarah', type: 'auth' },
  { id: 'ACT-8923', description: 'Challan cancelled by admin', time: '08:20 AM', targetId: 'CH-0041', type: 'action' },
];

export const cameras: Camera[] = [
  { id: 'CAM-001', location: 'Mall Road Intersection', ipAddress: '192.168.1.101', streamUrl: 'rtsp://cam001', status: 'active', installationDate: '2024-01-15', detectionCount: 234 },
  { id: 'CAM-002', location: 'Gulberg Main Blvd', ipAddress: '192.168.1.102', streamUrl: 'rtsp://cam002', status: 'active', installationDate: '2024-01-15', detectionCount: 189 },
  { id: 'CAM-003', location: 'Liberty Roundabout', ipAddress: '192.168.1.103', streamUrl: 'rtsp://cam003', status: 'offline', installationDate: '2024-02-01', detectionCount: 67 },
  { id: 'CAM-004', location: 'Canal Road - DHA', ipAddress: '192.168.1.104', streamUrl: 'rtsp://cam004', status: 'active', installationDate: '2024-02-10', detectionCount: 156 },
  { id: 'CAM-005', location: 'Ferozepur Road Toll', ipAddress: '192.168.1.105', streamUrl: 'rtsp://cam005', status: 'active', installationDate: '2024-03-01', detectionCount: 312 },
  { id: 'CAM-006', location: 'Raiwind Road Junction', ipAddress: '192.168.1.106', streamUrl: 'rtsp://cam006', status: 'maintenance', installationDate: '2024-03-05', detectionCount: 78 },
];

export const violations: Violation[] = Array.from({ length: 22 }, (_, i) => ({
  id: `VIO-${1000 + i}`,
  vehicleId: `VEH-${200 + i}`,
  plateText: ['LEA-4432', 'LHR-5512', 'ABC-1234', 'PXZ-7788', 'KHI-3310', 'RWP-0021', 'ISB-8844', 'FSD-6601'][i % 8],
  cameraId: `CAM-00${(i % 6) + 1}`,
  location: ['Mall Road Intersection', 'Gulberg Main Blvd', 'Liberty Roundabout', 'Canal Road - DHA', 'Ferozepur Road Toll'][i % 5],
  timestamp: new Date(Date.now() - i * 3600000 * 2.5).toISOString(),
  smokeConfidence: Number((0.72 + (i % 20) * 0.012).toFixed(2)),
  plateConfidence: Number((0.85 + (i % 12) * 0.01).toFixed(2)),
  status: ['pending', 'warning_issued', 'challan_issued', 'dismissed'][i % 4] as Violation['status'],
  hasProof: true,
  warningCount: Math.floor(i / 4),
}));

export const challans: Challan[] = Array.from({ length: 15 }, (_, i) => ({
  id: `CH-${1000 + i}`,
  challanNumber: `ENT-2024-${5000 + i}`,
  vehicleId: `VEH-${200 + i}`,
  plateText: ['LEA-4432', 'LHR-5512', 'ABC-1234', 'PXZ-7788', 'KHI-3310'][i % 5],
  ownerName: ['Raza Ahmed', 'Tariq Mehmood', 'Amna Bibi', 'Faisal Khan', 'Sana Iqbal'][i % 5],
  violationId: `VIO-${1000 + i}`,
  location: ['Mall Road', 'Gulberg', 'Liberty Market', 'Canal Road', 'Ferozepur Road'][i % 5],
  issuedAt: new Date(Date.now() - i * 86400000).toISOString(),
  fineAmount: [2000, 3000, 2500, 4000][i % 4],
  status: ['issued', 'paid', 'cancelled', 'disputed'][i % 4] as Challan['status'],
  proofLink: 'evidence.jpg',
  smokeConfidence: Number((0.88 + (i % 10) * 0.008).toFixed(2)),
}));

export const warnings: Warning[] = Array.from({ length: 18 }, (_, i) => ({
  id: `WRN-${2000 + i}`,
  vehicleId: `VEH-${200 + i}`,
  plateText: ['LEA-4432', 'LHR-5512', 'ABC-1234', 'PXZ-7788', 'KHI-3310', 'RWP-0021'][i % 6],
  ownerName: ['Raza Ahmed', 'Tariq Mehmood', 'Amna Bibi', 'Faisal Khan', 'Sana Iqbal', 'Kamran Malik'][i % 6],
  violationId: `VIO-${1000 + i}`,
  location: ['Mall Road', 'Gulberg', 'Liberty Market', 'Canal Road', 'Ferozepur Road', 'MM Alam'][i % 6],
  issuedAt: new Date(Date.now() - i * 72000000).toISOString(),
  status: ['sent', 'delivered', 'failed'][i % 3] as Warning['status'],
  warningNumber: i + 1,
}));

export const vehicles: Vehicle[] = [
  { plateText: 'LEA-4432', ownerId: 'OWN-001', ownerName: 'Raza Ahmed', ownerEmail: 'raza@gmail.com', totalViolations: 7, totalWarnings: 4, totalChallans: 2, lastSeen: '2024-03-24T10:30:00Z', status: 'repeat_offender' },
  { plateText: 'LHR-5512', ownerId: 'OWN-002', ownerName: 'Tariq Mehmood', ownerEmail: 'tariq@gmail.com', totalViolations: 3, totalWarnings: 2, totalChallans: 1, lastSeen: '2024-03-23T14:15:00Z', status: 'warned' },
  { plateText: 'ABC-1234', ownerId: 'OWN-003', ownerName: 'Amna Bibi', ownerEmail: 'amna@gmail.com', totalViolations: 1, totalWarnings: 1, totalChallans: 0, lastSeen: '2024-03-22T09:00:00Z', status: 'warned' },
  { plateText: 'PXZ-7788', ownerId: 'OWN-004', ownerName: 'Faisal Khan', ownerEmail: 'faisal@gmail.com', totalViolations: 5, totalWarnings: 3, totalChallans: 1, lastSeen: '2024-03-21T16:30:00Z', status: 'repeat_offender' },
  { plateText: 'KHI-3310', ownerId: 'OWN-005', ownerName: 'Sana Iqbal', ownerEmail: 'sana@gmail.com', totalViolations: 2, totalWarnings: 1, totalChallans: 0, lastSeen: '2024-03-20T11:00:00Z', status: 'active' },
];

export const users: User[] = [
  { id: 'u1', username: 'sarah.khan', name: 'Sarah Khan', email: 'sarah@psca.gov.pk', role: 'super_admin', status: 'active', joinedAt: '2024-01-01T00:00:00Z', lastActivity: '2024-03-24T08:47:00Z' },
  { id: 'u2', username: 'ali.raza', name: 'Ali Raza', email: 'ali.raza@psca.gov.pk', role: 'admin', status: 'active', joinedAt: '2024-01-15T00:00:00Z', lastActivity: '2024-03-24T09:30:00Z' },
  { id: 'u3', username: 'fatima.malik', name: 'Fatima Malik', email: 'fatima@epa.gov.pk', role: 'admin', status: 'active', joinedAt: '2024-02-01T00:00:00Z', lastActivity: '2024-03-23T14:00:00Z' },
  { id: 'u4', username: 'omar.sheikh', name: 'Omar Sheikh', email: 'omar@ltp.gov.pk', role: 'admin', status: 'inactive', joinedAt: '2024-02-15T00:00:00Z', lastActivity: '2024-03-10T10:00:00Z' },
];

export const settings: Settings = {
  challanThreshold: 3,
  confidenceThreshold: 0.75,
  emailNotifications: true,
  autoIssueChallans: true,
  reviewWindow: 48,
};
