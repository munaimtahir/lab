import { apiClient } from './api'
import { CATALOG_ENDPOINTS } from '../utils/constants'
import type { Test, TestCatalog, TestCatalogFormData } from '../types'

interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export const catalogService = {
  async search(query: string): Promise<Test[]> {
    const response = await apiClient.get<{ results: Test[] }>(
      `${CATALOG_ENDPOINTS.LIST}?search=${encodeURIComponent(query)}`
    )
    return response.results || []
  },

  async getAll(): Promise<TestCatalog[]> {
    const response = await apiClient.get<PaginatedResponse<TestCatalog>>(
      CATALOG_ENDPOINTS.LIST
    )
    return response.results || []
  },

  async getById(id: number): Promise<TestCatalog> {
    return apiClient.get<TestCatalog>(CATALOG_ENDPOINTS.DETAIL(id))
  },

  async create(data: TestCatalogFormData): Promise<TestCatalog> {
    return apiClient.post<TestCatalog>(CATALOG_ENDPOINTS.LIST, data)
  },

  async update(
    id: number,
    data: Partial<TestCatalogFormData>
  ): Promise<TestCatalog> {
    return apiClient.patch<TestCatalog>(CATALOG_ENDPOINTS.DETAIL(id), data)
  },

  async delete(id: number): Promise<void> {
    await apiClient.delete(CATALOG_ENDPOINTS.DETAIL(id))
  },
}
