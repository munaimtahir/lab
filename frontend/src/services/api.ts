import { API_BASE_URL, STORAGE_KEYS } from '../utils/constants'

export { API_BASE_URL }

export class ApiError extends Error {
  status?: number
  data?: unknown

  constructor(message: string, status?: number, data?: unknown) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.data = data
  }
}

class ApiClient {
  private baseURL: string
  private accessToken: string | null = null
  private refreshToken: string | null = null

  constructor(baseURL: string) {
    this.baseURL = baseURL
    this.loadTokens()
  }

  private loadTokens() {
    this.accessToken = localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN)
    this.refreshToken = localStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN)
  }

  public setTokens(access: string, refresh: string) {
    this.accessToken = access
    this.refreshToken = refresh
    localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, access)
    localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, refresh)
  }

  public clearTokens() {
    this.accessToken = null
    this.refreshToken = null
    localStorage.removeItem(STORAGE_KEYS.ACCESS_TOKEN)
    localStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN)
    localStorage.removeItem(STORAGE_KEYS.USER)
  }

  public getAccessToken() {
    return this.accessToken
  }

  private async refreshAccessToken(): Promise<string> {
    if (!this.refreshToken) {
      throw new ApiError('No refresh token available', 401)
    }

    const response = await fetch(`${this.baseURL}/api/auth/refresh/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ refresh: this.refreshToken }),
    })

    if (!response.ok) {
      this.clearTokens()
      throw new ApiError('Failed to refresh token', response.status)
    }

    const data = await response.json()
    this.accessToken = data.access
    localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, data.access)
    return data.access
  }

  public async request<T>(path: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseURL}${path}`
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string>),
    }

    if (this.accessToken) {
      headers['Authorization'] = `Bearer ${this.accessToken}`
    }

    let response = await fetch(url, {
      ...options,
      headers,
    })

    // If 401, try to refresh token and retry once
    if (
      response.status === 401 &&
      this.refreshToken &&
      !path.includes('/auth/')
    ) {
      try {
        await this.refreshAccessToken()
        headers['Authorization'] = `Bearer ${this.accessToken}`
        response = await fetch(url, {
          ...options,
          headers,
        })
      } catch {
        this.clearTokens()
        throw new ApiError('Authentication failed', 401)
      }
    }

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new ApiError(
        errorData.message || `Request failed with status ${response.status}`,
        response.status,
        errorData
      )
    }

    // Handle empty responses
    const contentType = response.headers.get('content-type')
    if (contentType && contentType.includes('application/json')) {
      return response.json()
    }

    return {} as T
  }

  public async get<T>(path: string, options?: RequestInit): Promise<T> {
    return this.request<T>(path, { ...options, method: 'GET' })
  }

  public async post<T>(
    path: string,
    data?: unknown,
    options?: RequestInit
  ): Promise<T> {
    return this.request<T>(path, {
      ...options,
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  public async put<T>(
    path: string,
    data?: unknown,
    options?: RequestInit
  ): Promise<T> {
    return this.request<T>(path, {
      ...options,
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  public async patch<T>(
    path: string,
    data?: unknown,
    options?: RequestInit
  ): Promise<T> {
    return this.request<T>(path, {
      ...options,
      method: 'PATCH',
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  public async delete<T>(path: string, options?: RequestInit): Promise<T> {
    return this.request<T>(path, { ...options, method: 'DELETE' })
  }
}

export const apiClient = new ApiClient(API_BASE_URL)
