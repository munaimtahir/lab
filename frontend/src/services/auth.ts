import { apiClient } from './api'
import { AUTH_ENDPOINTS, STORAGE_KEYS } from '../utils/constants'
import type { LoginResponse, User } from '../types'

/**
 * A service for handling authentication-related API calls.
 */
export const authService = {
  /**
   * Logs in a user with the given credentials.
   *
   * @param {string} username - The user's username.
   * @param {string} password - The user's password.
   * @returns {Promise<LoginResponse>} The login response, including tokens and user data.
   */
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

  /**
   * Logs out the current user.
   *
   * This method sends a request to the backend to invalidate the refresh token
   * and then clears all user-related data from local storage.
   */
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

  /**
   * Retrieves the current user from local storage.
   *
   * @returns {User | null} The current user object, or null if not found.
   */
  getCurrentUser(): User | null {
    const userStr = localStorage.getItem(STORAGE_KEYS.USER)
    if (!userStr) return null

    try {
      return JSON.parse(userStr)
    } catch {
      return null
    }
  },

  /**
   * Checks if the user is currently authenticated.
   *
   * @returns {boolean} True if the user has an access token, false otherwise.
   */
  isAuthenticated(): boolean {
    return !!apiClient.getAccessToken()
  },
}
