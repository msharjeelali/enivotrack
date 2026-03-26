import { dashboardStats, detectionTrend, recentActivities, statusDistribution } from '@/services/mocks/data';

export const dashboardService = {
  async getStats() {
    return dashboardStats;
  },
  async getTrend() {
    return detectionTrend;
  },
  async getStatusDistribution() {
    return statusDistribution;
  },
  async getActivities() {
    return recentActivities;
  },
};
