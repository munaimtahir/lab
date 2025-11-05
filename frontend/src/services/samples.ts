import { apiClient } from './api'
import { SAMPLE_ENDPOINTS } from '../utils/constants'
import type { Sample } from '../types'

export const sampleService = {
  async getAll(filters?: Record<string, string>): Promise<Sample[]> {
    const queryParams = filters
      ? '?' + new URLSearchParams(filters).toString()
      : ''
    const response = await apiClient.get<{ results: Sample[] }>(
      SAMPLE_ENDPOINTS.LIST + queryParams
    )
    return response.results || []
  },

  async getById(id: number): Promise<Sample> {
    return apiClient.get<Sample>(SAMPLE_ENDPOINTS.DETAIL(id))
  },

  async collect(id: number): Promise<Sample> {
    return apiClient.post<Sample>(SAMPLE_ENDPOINTS.COLLECT(id))
  },

  async receive(id: number): Promise<Sample> {
    return apiClient.post<Sample>(SAMPLE_ENDPOINTS.RECEIVE(id))
  },

  async reject(id: number, reason: string): Promise<Sample> {
    return apiClient.post<Sample>(SAMPLE_ENDPOINTS.REJECT(id), {
      rejection_reason: reason,
    })
  },
}
