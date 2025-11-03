import { apiClient } from './api'
import { CATALOG_ENDPOINTS } from '../utils/constants'
import type { Test } from '../types'

export const catalogService = {
  async search(query: string): Promise<Test[]> {
    const response = await apiClient.get<{ results: Test[] }>(
      `${CATALOG_ENDPOINTS.LIST}?search=${encodeURIComponent(query)}`
    )
    return response.results || []
  },

  async getAll(): Promise<Test[]> {
    const response = await apiClient.get<{ results: Test[] }>(
      CATALOG_ENDPOINTS.LIST
    )
    return response.results || []
  },

  async getById(id: number): Promise<Test> {
    return apiClient.get<Test>(CATALOG_ENDPOINTS.DETAIL(id))
  },
}
