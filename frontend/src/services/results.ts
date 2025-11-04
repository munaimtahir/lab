import { apiClient } from './api'
import { RESULT_ENDPOINTS } from '../utils/constants'
import type { Result } from '../types'

interface EnterResultData {
  value: string
  unit?: string
  reference_range?: string
  flag?: 'normal' | 'high' | 'low' | 'abnormal'
  notes?: string
}

export const resultService = {
  async getAll(filters?: Record<string, string>): Promise<Result[]> {
    const queryParams = filters
      ? '?' + new URLSearchParams(filters).toString()
      : ''
    const response = await apiClient.get<{ results: Result[] }>(
      RESULT_ENDPOINTS.LIST + queryParams
    )
    return response.results || []
  },

  async getById(id: number): Promise<Result> {
    return apiClient.get<Result>(RESULT_ENDPOINTS.DETAIL(id))
  },

  async enter(id: number, data: EnterResultData): Promise<Result> {
    // First update the result with the data
    await apiClient.patch<Result>(RESULT_ENDPOINTS.DETAIL(id), {
      value: data.value,
      unit: data.unit,
      reference_range: data.reference_range,
      flags: data.flag,
      notes: data.notes,
    })
    // Then mark it as entered
    return apiClient.post<Result>(RESULT_ENDPOINTS.ENTER(id))
  },

  async verify(id: number): Promise<Result> {
    return apiClient.post<Result>(RESULT_ENDPOINTS.VERIFY(id))
  },

  async publish(id: number): Promise<Result> {
    return apiClient.post<Result>(RESULT_ENDPOINTS.PUBLISH(id))
  },
}
