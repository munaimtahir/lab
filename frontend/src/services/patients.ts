import { apiClient } from './api'
import { PATIENT_ENDPOINTS } from '../utils/constants'
import type { Patient } from '../types'

/**
 * A service for handling patient-related API calls.
 */
export const patientService = {
  /**
   * Searches for patients by a query string.
   *
   * @param {string} query - The search query.
   * @returns {Promise<Patient[]>} A list of patients matching the query.
   */
  async search(query: string): Promise<Patient[]> {
    const response = await apiClient.get<{ results: Patient[] }>(
      `${PATIENT_ENDPOINTS.LIST}?query=${encodeURIComponent(query)}`
    )
    return response.results || []
  },

  /**
   * Retrieves all patients.
   *
   * @returns {Promise<Patient[]>} A list of all patients.
   */
  async getAll(): Promise<Patient[]> {
    const response = await apiClient.get<{ results: Patient[] }>(
      PATIENT_ENDPOINTS.LIST
    )
    return response.results || []
  },

  /**
   * Retrieves a patient by their ID.
   *
   * @param {number} id - The ID of the patient to retrieve.
   * @returns {Promise<Patient>} The patient data.
   */
  async getById(id: number): Promise<Patient> {
    return apiClient.get<Patient>(PATIENT_ENDPOINTS.DETAIL(id))
  },

  /**
   * Creates a new patient.
   *
   * @param {Partial<Patient>} data - The data for the new patient.
   * @returns {Promise<Patient>} The created patient data.
   */
  async create(data: Partial<Patient>): Promise<Patient> {
    return apiClient.post<Patient>(PATIENT_ENDPOINTS.LIST, data)
  },
}
