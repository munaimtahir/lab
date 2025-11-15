// User and Auth types
export interface User {
  id: number
  username: string
  email: string
  role: UserRole
  first_name: string
  last_name: string
  is_active?: boolean
  phone?: string
}

export interface UserFormData {
  username: string
  email: string
  password?: string
  role: UserRole
  first_name: string
  last_name: string
  is_active: boolean
  phone?: string
}

export type UserRole =
  | 'ADMIN'
  | 'RECEPTION'
  | 'PHLEBOTOMY'
  | 'TECHNOLOGIST'
  | 'PATHOLOGIST'

export interface AuthTokens {
  access: string
  refresh: string
}

export interface LoginResponse {
  access: string
  refresh: string
  user: User
}

// Patient types
export interface Patient {
  id: number
  mrn: string
  cnic?: string | null
  phone: string
  full_name: string
  father_name?: string
  sex: 'M' | 'F' | 'O'
  dob: string | null
  age_years?: number | null
  age_months?: number | null
  age_days?: number | null
  address?: string
  origin_terminal?: number | null
  is_offline_entry?: boolean
  synced_at?: string | null
  created_at: string
  updated_at: string
}

// Catalog types
export interface Test {
  id: number
  code: string
  name: string
  price: number
  specimen: string
  department: string
  result_type: 'numeric' | 'text' | 'option'
  unit?: string
  reference_range?: string
  is_active: boolean
}

export interface TestCatalog {
  id: number
  code: string
  name: string
  description?: string
  category: string
  sample_type: string
  price: number
  turnaround_time_hours: number
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface TestCatalogFormData {
  code: string
  name: string
  description?: string
  category: string
  sample_type: string
  price: number
  turnaround_time_hours: number
  is_active: boolean
}

// Terminal types
export interface LabTerminal {
  id: number
  code: string
  name: string
  offline_range_start: number
  offline_range_end: number
  offline_current: number
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface LabTerminalFormData {
  code: string
  name: string
  offline_range_start: number
  offline_range_end: number
  is_active: boolean
}

// Order types
export type OrderStatus =
  | 'NEW'
  | 'COLLECTED'
  | 'IN_PROCESS'
  | 'VERIFIED'
  | 'PUBLISHED'
  | 'CANCELLED'

export type OrderPriority = 'ROUTINE' | 'URGENT' | 'STAT'

export interface OrderItem {
  id: number
  test: TestCatalog
  test_detail?: TestCatalog
  status: OrderStatus
  created_at: string
  updated_at: string
}

export interface Order {
  id: number
  order_no: string
  patient: Patient
  patient_detail?: Patient
  items: OrderItem[]
  priority: OrderPriority
  status: OrderStatus
  notes?: string
  created_at: string
  updated_at: string
  created_by?: User
}

// Sample types
export type SampleStatus = 'PENDING' | 'COLLECTED' | 'RECEIVED' | 'REJECTED'

export interface Sample {
  id: number
  order_item: number
  barcode: string
  status: SampleStatus
  sample_type: string
  collected_at?: string
  collected_by?: number
  received_at?: string
  received_by?: number
  rejection_reason?: string
  notes?: string
  created_at: string
  updated_at: string
}

// Result types
export type ResultStatus = 'DRAFT' | 'ENTERED' | 'VERIFIED' | 'PUBLISHED'

export interface Result {
  id: number
  order_item: number
  status: ResultStatus
  value: string
  unit?: string
  reference_range?: string
  flags?: string
  entered_at?: string
  entered_by?: number
  verified_at?: string
  verified_by?: number
  published_at?: string
  notes?: string
  created_at: string
  updated_at: string
}

// Report types
export interface Report {
  id: number
  order: Order
  pdf_file: string
  generated_at: string
  generated_by: User
}

// Dashboard types
export interface DashboardQuickTiles {
  total_orders_today: number
  reports_published_today: number
}

export interface OrdersPerDay {
  date: string
  count: number
}

export interface SampleStatusDistribution {
  pending: number
  collected: number
  received: number
  rejected: number
}

export interface ResultStatusDistribution {
  draft: number
  entered: number
  verified: number
  published: number
}

export interface DashboardAnalytics {
  quick_tiles: DashboardQuickTiles
  orders_per_day: OrdersPerDay[]
  sample_status: SampleStatusDistribution
  result_status: ResultStatusDistribution
  avg_tat_hours: number
}
