import { apiClient, API_BASE_URL } from './api'
import { REPORT_ENDPOINTS } from '../utils/constants'
import type { Report } from '../types'

export const reportService = {
  async getAll(): Promise<Report[]> {
    const response = await apiClient.get<{ results: Report[] }>(
      REPORT_ENDPOINTS.LIST
    )
    return response.results || []
  },

  async getById(id: number): Promise<Report> {
    return apiClient.get<Report>(REPORT_ENDPOINTS.DETAIL(id))
  },

  async generate(orderId: number): Promise<Report> {
    return apiClient.post<Report>(REPORT_ENDPOINTS.GENERATE(orderId))
  },

  getDownloadUrl(id: number): string {
    return `${API_BASE_URL}${REPORT_ENDPOINTS.DOWNLOAD(id)}`
  },
}
