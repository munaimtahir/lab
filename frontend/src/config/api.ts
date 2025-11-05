const DEFAULT_API_BASE_URL = 'http://172.235.33.181:8000'

const resolveEnvBaseUrl = () => {
  if (typeof import.meta !== 'undefined' && import.meta.env) {
    const envBase =
      (import.meta.env.VITE_API_BASE_URL ?? import.meta.env.VITE_API_URL ?? '').trim()
    if (envBase) {
      return envBase
    }
  }
  return ''
}

const sanitizeBaseUrl = (value: string): string => {
  const trimmed = value.trim()
  if (!trimmed) {
    return DEFAULT_API_BASE_URL
  }
  const withoutTrailingSlash = trimmed.replace(/\/+$/, '')
  return withoutTrailingSlash || DEFAULT_API_BASE_URL
}

export const API_BASE_URL = sanitizeBaseUrl(resolveEnvBaseUrl() || DEFAULT_API_BASE_URL)

export { DEFAULT_API_BASE_URL }
