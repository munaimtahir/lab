import { useState, useEffect } from 'react'
import { settingsService, WorkflowSettings } from '../services/settings'

export function useWorkflowSettings() {
  const [settings, setSettings] = useState<WorkflowSettings | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchSettings()
  }, [])

  const fetchSettings = async () => {
    try {
      setLoading(true)
      const data = await settingsService.getWorkflowSettings()
      setSettings(data)
      setError(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch settings')
    } finally {
      setLoading(false)
    }
  }

  const refresh = () => {
    fetchSettings()
  }

  return {
    settings,
    loading,
    error,
    refresh,
    // Helper flags
    enableSampleCollection: settings?.enable_sample_collection ?? true,
    enableSampleReceive: settings?.enable_sample_receive ?? true,
    enableVerification: settings?.enable_verification ?? true,
  }
}
