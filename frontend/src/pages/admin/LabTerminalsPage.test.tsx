import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { LabTerminalsPage } from './LabTerminalsPage'
import { terminalService } from '../../services/terminals'
import type { LabTerminal } from '../../types'

vi.mock('../../services/terminals')

const mockTerminals: LabTerminal[] = [
  {
    id: 1,
    code: 'LAB1-PC',
    name: 'Lab 1 PC',
    offline_range_start: 1000,
    offline_range_end: 1999,
    offline_current: 0,
    is_active: true,
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
  },
]

describe('LabTerminalsPage', () => {
  beforeEach(() => {
    vi.resetAllMocks()
  })

  it('renders lab terminals page', async () => {
    vi.mocked(terminalService.getAll).mockResolvedValue(mockTerminals)

    render(
      <BrowserRouter>
        <LabTerminalsPage />
      </BrowserRouter>
    )

    expect(screen.getByText('Lab Terminals')).toBeInTheDocument()
    expect(screen.getByText('Add Terminal')).toBeInTheDocument()
  })

  it('displays loading state initially', () => {
    vi.mocked(terminalService.getAll).mockReturnValue(new Promise(() => {}))

    render(
      <BrowserRouter>
        <LabTerminalsPage />
      </BrowserRouter>
    )

    expect(screen.getByText('Loading terminals...')).toBeInTheDocument()
  })

  it('displays terminals when loaded', async () => {
    vi.mocked(terminalService.getAll).mockResolvedValue(mockTerminals)

    render(
      <BrowserRouter>
        <LabTerminalsPage />
      </BrowserRouter>
    )

    await waitFor(() => {
      expect(screen.getByText('LAB1-PC')).toBeInTheDocument()
      expect(screen.getByText('Lab 1 PC')).toBeInTheDocument()
    })
  })

  it('displays error message on fetch failure', async () => {
    vi.mocked(terminalService.getAll).mockRejectedValue(new Error('Network error'))

    render(
      <BrowserRouter>
        <LabTerminalsPage />
      </BrowserRouter>
    )

    await waitFor(() => {
      expect(screen.getByText(/Network error/)).toBeInTheDocument()
    })
  })
})
