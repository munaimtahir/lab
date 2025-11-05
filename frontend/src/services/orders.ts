import { apiClient } from './api'
import { ORDER_ENDPOINTS } from '../utils/constants'
import type { Order } from '../types'

interface CreateOrderData {
  patient_id: number
  test_ids: number[]
  bill_amount: number
  discount?: number
  amount_paid?: number
  report_date?: string
  report_time?: string
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
}
