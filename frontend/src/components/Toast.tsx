import { useEffect } from 'react'

interface ToastProps {
  message: string
  type: 'success' | 'error' | 'info'
  onClose: () => void
  duration?: number
}

export function Toast({ message, type, onClose, duration = 5000 }: ToastProps) {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose()
    }, duration)

    return () => clearTimeout(timer)
  }, [duration, onClose])

  const bgColor =
    type === 'success'
      ? 'bg-green-50 border-green-200'
      : type === 'error'
        ? 'bg-red-50 border-red-200'
        : 'bg-blue-50 border-blue-200'

  const textColor =
    type === 'success'
      ? 'text-green-800'
      : type === 'error'
        ? 'text-red-800'
        : 'text-blue-800'

  const icon =
    type === 'success' ? '✓' : type === 'error' ? '✕' : 'ℹ'

  return (
    <div
      className={`fixed top-4 right-4 z-50 ${bgColor} border rounded-lg shadow-lg p-4 max-w-sm flex items-start gap-3 animate-slide-in`}
      role="alert"
    >
      <span className={`text-xl ${textColor}`}>{icon}</span>
      <p className={`text-sm flex-1 ${textColor}`}>{message}</p>
      <button
        onClick={onClose}
        className={`${textColor} hover:opacity-70 text-lg leading-none`}
        aria-label="Close"
      >
        ×
      </button>
    </div>
  )
}
