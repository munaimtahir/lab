// API Configuration
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Auth endpoints
export const AUTH_ENDPOINTS = {
  LOGIN: '/api/auth/login/',
  REFRESH: '/api/auth/refresh/',
  LOGOUT: '/api/auth/logout/',
} as const

// Patient endpoints
export const PATIENT_ENDPOINTS = {
  LIST: '/api/patients/',
  DETAIL: (id: number) => `/api/patients/${id}/`,
} as const

// Catalog endpoints
export const CATALOG_ENDPOINTS = {
  LIST: '/api/catalog/',
  DETAIL: (id: number) => `/api/catalog/${id}/`,
} as const

// Order endpoints
export const ORDER_ENDPOINTS = {
  LIST: '/api/orders/',
  DETAIL: (id: number) => `/api/orders/${id}/`,
} as const

// Sample endpoints
export const SAMPLE_ENDPOINTS = {
  LIST: '/api/samples/',
  DETAIL: (id: number) => `/api/samples/${id}/`,
  COLLECT: (id: number) => `/api/samples/${id}/collect/`,
  RECEIVE: (id: number) => `/api/samples/${id}/receive/`,
} as const

// Result endpoints
export const RESULT_ENDPOINTS = {
  LIST: '/api/results/',
  DETAIL: (id: number) => `/api/results/${id}/`,
  ENTER: (id: number) => `/api/results/${id}/enter/`,
  VERIFY: (id: number) => `/api/results/${id}/verify/`,
  PUBLISH: (id: number) => `/api/results/${id}/publish/`,
} as const

// Report endpoints
export const REPORT_ENDPOINTS = {
  LIST: '/api/reports/',
  DETAIL: (id: number) => `/api/reports/${id}/`,
  GENERATE: (orderId: number) => `/api/reports/generate/${orderId}/`,
  DOWNLOAD: (id: number) => `/api/reports/${id}/download/`,
} as const

// Health endpoint
export const HEALTH_ENDPOINT = '/api/health/'

// Route paths
export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  LAB: '/lab',
  LAB_NEW: '/lab/new',
  LAB_WORKLIST: '/lab/worklist',
  LAB_ORDER: '/lab/orders/:id',
  LAB_ORDER_DETAIL: (id: number | string) => `/lab/orders/${id}`,
  SETTINGS: '/settings',
} as const

// Role-based permissions
export const ROLE_PERMISSIONS = {
  ADMIN: ['all'],
  RECEPTION: ['patients', 'orders', 'reports.view'],
  PHLEBOTOMY: ['samples.collect', 'worklist.view'],
  TECHNOLOGIST: ['samples.receive', 'results.enter', 'worklist.view'],
  PATHOLOGIST: ['results.verify', 'results.publish', 'reports.generate', 'worklist.view'],
} as const

// Color scheme matching existing xMed EMR
export const COLORS = {
  header: {
    bg: 'bg-red-900',
    text: 'text-white',
  },
  section: {
    bg: 'bg-blue-700',
    text: 'text-white',
  },
  card: {
    bg: 'bg-teal-50',
    border: 'border-teal-200',
    hover: 'hover:bg-teal-100',
  },
  status: {
    NEW: 'bg-blue-100 text-blue-800',
    COLLECTED: 'bg-yellow-100 text-yellow-800',
    IN_PROCESS: 'bg-purple-100 text-purple-800',
    VERIFIED: 'bg-green-100 text-green-800',
    PUBLISHED: 'bg-green-200 text-green-900',
    PENDING: 'bg-gray-100 text-gray-800',
    RECEIVED: 'bg-teal-100 text-teal-800',
    DRAFT: 'bg-gray-100 text-gray-800',
    ENTERED: 'bg-blue-100 text-blue-800',
  },
} as const

// Local storage keys
export const STORAGE_KEYS = {
  ACCESS_TOKEN: 'access_token',
  REFRESH_TOKEN: 'refresh_token',
  USER: 'user',
} as const
