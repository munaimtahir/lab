import { apiClient } from './api'
import { DASHBOARD_ENDPOINTS } from '../utils/constants'
import type { DashboardAnalytics } from '../types'

export const dashboardService = {
  async getAnalytics(params?: {
    start_date?: string
    end_date?: string
  }): Promise<DashboardAnalytics> {
    const queryParams = new URLSearchParams()
    if (params?.start_date) {
      queryParams.append('start_date', params.start_date)
    }
    if (params?.end_date) {
      queryParams.append('end_date', params.end_date)
    }

    const url =
      queryParams.toString() !== ''
        ? `${DASHBOARD_ENDPOINTS.ANALYTICS}?${queryParams.toString()}`
        : DASHBOARD_ENDPOINTS.ANALYTICS

    return apiClient.get<DashboardAnalytics>(url)
  },
}
