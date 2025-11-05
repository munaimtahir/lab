import { apiClient } from './api'
import { AUTH_ENDPOINTS, STORAGE_KEYS } from '../utils/constants'
import type { LoginResponse, User } from '../types'

export const authService = {
  async login(username: string, password: string): Promise<LoginResponse> {
    const response = await apiClient.post<LoginResponse>(AUTH_ENDPOINTS.LOGIN, {
      username,
      password,
    })

    // Store tokens and user data
    apiClient.setTokens(response.access, response.refresh)
    localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(response.user))

    return response
  },

  async logout(): Promise<void> {
    const refreshToken = localStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN)

    try {
      if (refreshToken) {
        await apiClient.post(AUTH_ENDPOINTS.LOGOUT, { refresh: refreshToken })
      }
    } catch (error) {
      // Ignore logout errors, clear local state anyway
      console.error('Logout error:', error)
    } finally {
      apiClient.clearTokens()
    }
  },

  getCurrentUser(): User | null {
    const userStr = localStorage.getItem(STORAGE_KEYS.USER)
    if (!userStr) return null

    try {
      return JSON.parse(userStr)
    } catch {
      return null
    }
  },

  isAuthenticated(): boolean {
    return !!apiClient.getAccessToken()
  },
}
