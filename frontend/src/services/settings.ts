import { apiClient } from './api'

export interface WorkflowSettings {
  enable_sample_collection: boolean
  enable_sample_receive: boolean
  enable_verification: boolean
  updated_at?: string
}

export interface RolePermission {
  id?: number
  role: string
  can_register: boolean
  can_collect: boolean
  can_enter_result: boolean
  can_verify: boolean
  can_publish: boolean
  can_edit_catalog: boolean
  can_edit_settings: boolean
  updated_at?: string
}

export const settingsService = {
  async getWorkflowSettings(): Promise<WorkflowSettings> {
    return apiClient.get<WorkflowSettings>('/settings/workflow/')
  },

  async updateWorkflowSettings(
    settings: Partial<WorkflowSettings>
  ): Promise<WorkflowSettings> {
    return apiClient.put<WorkflowSettings>('/settings/workflow/', settings)
  },

  async getRolePermissions(): Promise<RolePermission[]> {
    return apiClient.get<RolePermission[]>('/settings/permissions/')
  },

  async updateRolePermissions(
    permissions: RolePermission[]
  ): Promise<RolePermission[]> {
    return apiClient.put<RolePermission[]>(
      '/settings/permissions/update/',
      permissions
    )
  },
}
