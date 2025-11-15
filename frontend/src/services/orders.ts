import { apiClient } from './api'
import { ORDER_ENDPOINTS } from '../utils/constants'
import type { Order } from '../types'

interface CreateOrderData {
  patient: number
  test_ids: number[]
  priority?: 'ROUTINE' | 'URGENT' | 'STAT'
  notes?: string
}

interface EditOrderTestsData {
  tests_to_add?: number[]
  tests_to_remove?: number[]
}

export const orderService = {
  async getAll(filters?: Record<string, string>): Promise<Order[]> {
    const queryParams = filters
      ? '?' + new URLSearchParams(filters).toString()
      : ''
    const response = await apiClient.get<{ results: Order[] }>(
      ORDER_ENDPOINTS.LIST + queryParams
    )
    return response.results || []
  },

  async getById(id: number): Promise<Order> {
    return apiClient.get<Order>(ORDER_ENDPOINTS.DETAIL(id))
  },

  async create(data: CreateOrderData): Promise<Order> {
    return apiClient.post<Order>(ORDER_ENDPOINTS.LIST, data)
  },

  async cancel(id: number): Promise<Order> {
    return apiClient.post<Order>(ORDER_ENDPOINTS.CANCEL(id))
  },

  async editTests(id: number, data: EditOrderTestsData): Promise<Order> {
    return apiClient.patch<Order>(ORDER_ENDPOINTS.EDIT_TESTS(id), data)
  },
}
