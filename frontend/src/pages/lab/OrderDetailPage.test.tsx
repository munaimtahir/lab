import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { OrderDetailPage } from './OrderDetailPage'
import { orderService } from '../../services/orders'
import { AuthProvider } from '../../hooks/useAuth'
import type { User } from '../../types'

vi.mock('../../services/orders')
vi.mock('../../services/auth', () => ({
  authService: {
    getCurrentUser: () => ({ id: 1, username: 'admin', role: 'ADMIN' }),
    isAuthenticated: () => true,
  },
}))

const mockOrder = {
  id: 1,
  order_number: 'ORD-001',
  patient: {
    id: 1,
    mrn: 'PAT-001',
    full_name: 'John Doe',
    gender: 'M' as const,
    age: 30,
    age_unit: 'years' as const,
    cnic: '12345-1234567-1',
    phone: '03001234567',
    date_of_birth: '1994-01-01',
    created_at: '2024-01-01T00:00:00Z',
  },
  items: [
    {
      id: 1,
      test: {
        id: 1,
        code: 'CBC',
        name: 'Complete Blood Count',
        price: 500,
        specimen: 'Blood',
        department: 'Hematology',
        result_type: 'numeric' as const,
        is_active: true,
      },
      status: 'NEW' as const,
    },
  ],
  status: 'NEW' as const,
  created_at: '2024-01-01T00:00:00Z',
  created_by: { id: 1, username: 'admin', role: 'ADMIN' } as unknown as User,
  bill_amount: 500,
  discount: 0,
  amount_paid: 500,
}

describe('OrderDetailPage', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('shows loading state', () => {
    vi.mocked(orderService.getById).mockImplementation(() => new Promise(() => {}))

    render(
      <MemoryRouter initialEntries={['/lab/orders/1']}>
        <AuthProvider>
          <Routes>
            <Route path="/lab/orders/:id" element={<OrderDetailPage />} />
          </Routes>
        </AuthProvider>
      </MemoryRouter>
    )

    expect(screen.getByText('Loading order...')).toBeInTheDocument()
  })

  it('renders page with tabs', async () => {
    vi.mocked(orderService.getById).mockResolvedValue(mockOrder)

    render(
      <MemoryRouter initialEntries={['/lab/orders/1']}>
        <AuthProvider>
          <Routes>
            <Route path="/lab/orders/:id" element={<OrderDetailPage />} />
          </Routes>
        </AuthProvider>
      </MemoryRouter>
    )

    await waitFor(() => {
      expect(screen.getByRole('button', { name: 'Summary' })).toBeInTheDocument()
    }, { timeout: 5000 })
  })
})
