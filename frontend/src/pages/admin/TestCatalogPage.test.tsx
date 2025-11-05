import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { TestCatalogPage } from './TestCatalogPage'
import { catalogService } from '../../services/catalog'
import type { TestCatalog } from '../../types'

vi.mock('../../services/catalog')

const mockTests: TestCatalog[] = [
  {
    id: 1,
    code: 'CBC',
    name: 'Complete Blood Count',
    description: 'Blood test',
    category: 'Hematology',
    sample_type: 'Blood',
    price: 500,
    turnaround_time_hours: 24,
    is_active: true,
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
  },
]

describe('TestCatalogPage', () => {
  beforeEach(() => {
    vi.resetAllMocks()
  })

  it('renders test catalog page', async () => {
    vi.mocked(catalogService.getAll).mockResolvedValue(mockTests)

    render(
      <BrowserRouter>
        <TestCatalogPage />
      </BrowserRouter>
    )

    expect(screen.getByText('Test Catalog')).toBeInTheDocument()
    expect(screen.getByText('Add Test')).toBeInTheDocument()
  })

  it('displays loading state initially', () => {
    vi.mocked(catalogService.getAll).mockReturnValue(new Promise(() => {}))

    render(
      <BrowserRouter>
        <TestCatalogPage />
      </BrowserRouter>
    )

    expect(screen.getByText('Loading tests...')).toBeInTheDocument()
  })

  it('displays tests when loaded', async () => {
    vi.mocked(catalogService.getAll).mockResolvedValue(mockTests)

    render(
      <BrowserRouter>
        <TestCatalogPage />
      </BrowserRouter>
    )

    await waitFor(() => {
      expect(screen.getByText('CBC')).toBeInTheDocument()
      expect(screen.getByText('Complete Blood Count')).toBeInTheDocument()
    })
  })

  it('displays error message on fetch failure', async () => {
    vi.mocked(catalogService.getAll).mockRejectedValue(
      new Error('Network error')
    )

    render(
      <BrowserRouter>
        <TestCatalogPage />
      </BrowserRouter>
    )

    await waitFor(() => {
      expect(screen.getByText(/Network error/)).toBeInTheDocument()
    })
  })
})
