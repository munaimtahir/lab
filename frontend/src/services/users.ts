import { apiClient } from './api'
import { USER_ENDPOINTS } from '../utils/constants'
import type { User, UserFormData } from '../types'

interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export const userService = {
  async getAll(): Promise<User[]> {
    const response = await apiClient.get<PaginatedResponse<User>>(
      USER_ENDPOINTS.LIST
    )
    return response.results || []
  },

  async getById(id: number): Promise<User> {
    return apiClient.get<User>(USER_ENDPOINTS.DETAIL(id))
  },

  async create(data: UserFormData): Promise<User> {
    return apiClient.post<User>(USER_ENDPOINTS.LIST, data)
  },

  async update(id: number, data: Partial<UserFormData>): Promise<User> {
    return apiClient.patch<User>(USER_ENDPOINTS.DETAIL(id), data)
  },

  async delete(id: number): Promise<void> {
    await apiClient.delete(USER_ENDPOINTS.DETAIL(id))
  },
}
