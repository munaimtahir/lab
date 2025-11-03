// CNIC validation (Pakistani format: #####-#######-#)
export function validateCNIC(cnic: string): boolean {
  const cnicRegex = /^\d{5}-\d{7}-\d$/
  return cnicRegex.test(cnic)
}

export function formatCNIC(value: string): string {
  // Remove all non-digit characters
  const digits = value.replace(/\D/g, '')
  
  // Format as #####-#######-#
  if (digits.length <= 5) {
    return digits
  } else if (digits.length <= 12) {
    return `${digits.slice(0, 5)}-${digits.slice(5)}`
  } else {
    return `${digits.slice(0, 5)}-${digits.slice(5, 12)}-${digits.slice(12, 13)}`
  }
}

// Phone validation (Pakistani format)
export function validatePhone(phone: string): boolean {
  const phoneRegex = /^(\+92|0)?3\d{9}$/
  return phoneRegex.test(phone.replace(/\s|-/g, ''))
}

export function formatPhone(value: string): string {
  // Remove all non-digit and non-plus characters
  const cleaned = value.replace(/[^\d+]/g, '')
  
  // Basic formatting
  if (cleaned.startsWith('+92')) {
    return cleaned.slice(0, 13)
  } else if (cleaned.startsWith('0')) {
    return cleaned.slice(0, 11)
  }
  return cleaned.slice(0, 11)
}

// Date of Birth validation
export function validateDOB(dob: string): boolean {
  const date = new Date(dob)
  const today = new Date()
  return date <= today && !isNaN(date.getTime())
}

// Age calculation
export function calculateAge(dob: string): { age: number; unit: 'years' | 'months' | 'days' } {
  const birthDate = new Date(dob)
  const today = new Date()
  
  const years = today.getFullYear() - birthDate.getFullYear()
  const months = today.getMonth() - birthDate.getMonth()
  const days = today.getDate() - birthDate.getDate()
  
  if (years > 0) {
    return { age: years, unit: 'years' }
  } else if (months > 0) {
    return { age: months, unit: 'months' }
  } else {
    return { age: Math.max(days, 0), unit: 'days' }
  }
}

// Format currency
export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('en-PK', {
    style: 'currency',
    currency: 'PKR',
  }).format(amount)
}

// Date/Time formatting
export function formatDate(date: string | Date): string {
  return new Date(date).toLocaleDateString('en-PK', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  })
}

export function formatTime(date: string | Date): string {
  return new Date(date).toLocaleTimeString('en-PK', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
  })
}

export function formatDateTime(date: string | Date): string {
  return `${formatDate(date)} ${formatTime(date)}`
}
