import { useState, useEffect } from 'react'
import { settingsService, UserPermissions } from '../services/settings'

export function useUserPermissions() {
  const [permissions, setPermissions] = useState<UserPermissions | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchPermissions()
  }, [])

  const fetchPermissions = async () => {
    try {
      setLoading(true)
      const data = await settingsService.getUserPermissions()
      setPermissions(data)
      setError(null)
    } catch (err) {
      setError(
        err instanceof Error ? err.message : 'Failed to fetch permissions'
      )
    } finally {
      setLoading(false)
    }
  }

  const refresh = () => {
    fetchPermissions()
  }

  // Helper functions
  const canRegister = permissions?.permissions.can_register ?? false
  const canCollect = permissions?.permissions.can_collect ?? false
  const canEnterResult = permissions?.permissions.can_enter_result ?? false
  const canVerify = permissions?.permissions.can_verify ?? false
  const canPublish = permissions?.permissions.can_publish ?? false
  const canEditCatalog = permissions?.permissions.can_edit_catalog ?? false
  const canEditSettings = permissions?.permissions.can_edit_settings ?? false

  return {
    permissions,
    loading,
    error,
    refresh,
    // Permission flags
    canRegister,
    canCollect,
    canEnterResult,
    canVerify,
    canPublish,
    canEditCatalog,
    canEditSettings,
  }
}
