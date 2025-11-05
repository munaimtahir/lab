import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { UserManagementPage } from './UserManagementPage'
import { userService } from '../../services/users'
import type { User } from '../../types'

vi.mock('../../services/users')

const mockUsers: User[] = [
  {
    id: 1,
    username: 'admin',
    email: 'admin@example.com',
    role: 'ADMIN',
    first_name: 'Admin',
    last_name: 'User',
    is_active: true,
  },
  {
    id: 2,
    username: 'tech',
    email: 'tech@example.com',
    role: 'TECHNOLOGIST',
    first_name: 'Tech',
    last_name: 'User',
    is_active: true,
  },
]

describe('UserManagementPage', () => {
  beforeEach(() => {
    vi.resetAllMocks()
  })

  it('renders user management page', async () => {
    vi.mocked(userService.getAll).mockResolvedValue(mockUsers)

    render(
      <BrowserRouter>
        <UserManagementPage />
      </BrowserRouter>
    )

    expect(screen.getByText('User Management')).toBeInTheDocument()
    expect(screen.getByText('Add User')).toBeInTheDocument()
  })

  it('displays loading state initially', () => {
    vi.mocked(userService.getAll).mockReturnValue(new Promise(() => {}))

    render(
      <BrowserRouter>
        <UserManagementPage />
      </BrowserRouter>
    )

    expect(screen.getByText('Loading users...')).toBeInTheDocument()
  })

  it('displays users when loaded', async () => {
    vi.mocked(userService.getAll).mockResolvedValue(mockUsers)

    render(
      <BrowserRouter>
        <UserManagementPage />
      </BrowserRouter>
    )

    await waitFor(() => {
      expect(screen.getByText('admin')).toBeInTheDocument()
      expect(screen.getByText('tech')).toBeInTheDocument()
    })
  })

  it('displays error message on fetch failure', async () => {
    vi.mocked(userService.getAll).mockRejectedValue(new Error('Network error'))

    render(
      <BrowserRouter>
        <UserManagementPage />
      </BrowserRouter>
    )

    await waitFor(() => {
      expect(screen.getByText(/Network error/)).toBeInTheDocument()
    })
  })
})
