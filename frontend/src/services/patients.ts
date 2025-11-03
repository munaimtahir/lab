import { apiClient } from './api'
import { PATIENT_ENDPOINTS } from '../utils/constants'
import type { Patient } from '../types'

export const patientService = {
  async search(query: string): Promise<Patient[]> {
    const response = await apiClient.get<{ results: Patient[] }>(
      `${PATIENT_ENDPOINTS.LIST}?query=${encodeURIComponent(query)}`
    )
    return response.results || []
  },

  async getAll(): Promise<Patient[]> {
    const response = await apiClient.get<{ results: Patient[] }>(
      PATIENT_ENDPOINTS.LIST
    )
    return response.results || []
  },

  async getById(id: number): Promise<Patient> {
    return apiClient.get<Patient>(PATIENT_ENDPOINTS.DETAIL(id))
  },

  async create(data: Partial<Patient>): Promise<Patient> {
    return apiClient.post<Patient>(PATIENT_ENDPOINTS.LIST, data)
  },
}
