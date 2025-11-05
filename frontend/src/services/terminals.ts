import { apiClient } from './api'
import { TERMINAL_ENDPOINTS } from '../utils/constants'
import type { LabTerminal, LabTerminalFormData } from '../types'

interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export const terminalService = {
  async getAll(): Promise<LabTerminal[]> {
    const response = await apiClient.get<PaginatedResponse<LabTerminal>>(
      TERMINAL_ENDPOINTS.LIST
    )
    return response.results || []
  },

  async getById(id: number): Promise<LabTerminal> {
    return apiClient.get<LabTerminal>(TERMINAL_ENDPOINTS.DETAIL(id))
  },

  async create(data: LabTerminalFormData): Promise<LabTerminal> {
    return apiClient.post<LabTerminal>(TERMINAL_ENDPOINTS.LIST, data)
  },

  async update(
    id: number,
    data: Partial<LabTerminalFormData>
  ): Promise<LabTerminal> {
    return apiClient.patch<LabTerminal>(TERMINAL_ENDPOINTS.DETAIL(id), data)
  },

  async delete(id: number): Promise<void> {
    await apiClient.delete(TERMINAL_ENDPOINTS.DETAIL(id))
  },
}
