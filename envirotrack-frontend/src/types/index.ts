export type UserRole = 'super_admin' | 'admin';
export type UserStatus = 'active' | 'inactive';
export type CameraStatus = 'active' | 'offline' | 'maintenance';
export type ViolationStatus = 'pending' | 'warning_issued' | 'challan_issued' | 'dismissed';
export type ChallanStatus = 'issued' | 'paid' | 'cancelled' | 'disputed';
export type WarningStatus = 'sent' | 'delivered' | 'failed';
export type VehicleStatus = 'repeat_offender' | 'warned' | 'active';

export interface User {
  id: string;
  username: string;
  name: string;
  email: string;
  role: UserRole;
  status: UserStatus;
  joinedAt: string;
  lastActivity: string;
}

export interface AuthUser {
  id: string;
  username: string;
  name: string;
  email: string;
  role: UserRole;
}

export interface DashboardStats {
  activeCameras: number;
  detectionsToday: number;
  challansIssued: number;
  warningsIssued: number;
  pendingReview: number;
  repeatOffenders: number;
  totalViolations: number;
  resolvedToday: number;
}

export interface TrendPoint {
  day: string;
  detections: number;
  challans: number;
  warnings: number;
}

export interface DistributionItem {
  name: string;
  value: number;
  color: string;
}

export interface ActivityItem {
  id: string;
  description: string;
  time: string;
  targetId: string;
  type: string;
}

export interface Camera {
  id: string;
  location: string;
  ipAddress: string;
  streamUrl: string;
  status: CameraStatus;
  installationDate: string;
  detectionCount: number;
}

export interface Violation {
  id: string;
  vehicleId: string;
  plateText: string;
  cameraId: string;
  location: string;
  timestamp: string;
  smokeConfidence: number;
  plateConfidence: number;
  status: ViolationStatus;
  hasProof: boolean;
  warningCount: number;
}

export interface Challan {
  id: string;
  challanNumber: string;
  vehicleId: string;
  plateText: string;
  ownerName: string;
  violationId: string;
  location: string;
  issuedAt: string;
  fineAmount: number;
  status: ChallanStatus;
  proofLink: string;
  smokeConfidence: number;
}

export interface Warning {
  id: string;
  vehicleId: string;
  plateText: string;
  ownerName: string;
  violationId: string;
  location: string;
  issuedAt: string;
  status: WarningStatus;
  warningNumber: number;
}

export interface Vehicle {
  plateText: string;
  ownerId: string;
  ownerName: string;
  ownerEmail: string;
  totalViolations: number;
  totalWarnings: number;
  totalChallans: number;
  lastSeen: string;
  status: VehicleStatus;
}

export interface Settings {
  challanThreshold: number;
  confidenceThreshold: number;
  emailNotifications: boolean;
  autoIssueChallans: boolean;
  reviewWindow: number;
}

export interface ApiListResult<T> {
  items: T[];
  total: number;
}
