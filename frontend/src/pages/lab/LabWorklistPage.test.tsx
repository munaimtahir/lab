import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { LabWorklistPage } from './LabWorklistPage'
import { orderService } from '../../services/orders'
import type { User } from '../../types'

vi.mock('../../services/orders')

describe('LabWorklistPage', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the worklist page', () => {
    vi.mocked(orderService.getAll).mockResolvedValue([])

    render(
      <BrowserRouter>
        <LabWorklistPage />
      </BrowserRouter>
    )

    expect(screen.getByText('Lab Worklist')).toBeInTheDocument()
  })

  it('displays filter controls', () => {
    vi.mocked(orderService.getAll).mockResolvedValue([])

    render(
      <BrowserRouter>
        <LabWorklistPage />
      </BrowserRouter>
    )

    expect(screen.getByText(/From Date/i)).toBeInTheDocument()
    expect(screen.getByText(/To Date/i)).toBeInTheDocument()
    expect(screen.getAllByText(/Status/i)[0]).toBeInTheDocument()
    expect(screen.getByText(/Patient Search/i)).toBeInTheDocument()
  })

  it('shows loading state', () => {
    vi.mocked(orderService.getAll).mockImplementation(() => new Promise(() => {}))

    render(
      <BrowserRouter>
        <LabWorklistPage />
      </BrowserRouter>
    )

    expect(screen.getByText('Loading orders...')).toBeInTheDocument()
  })

  it('displays orders in cards', async () => {
    const mockOrders = [
      {
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
      },
    ]

    vi.mocked(orderService.getAll).mockResolvedValue(mockOrders)

    render(
      <BrowserRouter>
        <LabWorklistPage />
      </BrowserRouter>
    )

    await waitFor(() => {
      expect(screen.getByText('ORD-001')).toBeInTheDocument()
      expect(screen.getByText('John Doe')).toBeInTheDocument()
      expect(screen.getByText('Complete Blood Count')).toBeInTheDocument()
    })
  })

  it('shows empty state when no orders', async () => {
    vi.mocked(orderService.getAll).mockResolvedValue([])

    render(
      <BrowserRouter>
        <LabWorklistPage />
      </BrowserRouter>
    )

    await waitFor(() => {
      expect(screen.getByText(/No orders found/i)).toBeInTheDocument()
    })
  })
})
