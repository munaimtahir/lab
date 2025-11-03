import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { MainLayout } from './MainLayout'

describe('MainLayout', () => {
  it('renders header with Al-Shifa Laboratory title', () => {
    render(
      <BrowserRouter>
        <MainLayout />
      </BrowserRouter>
    )

    expect(screen.getByText('Al-Shifa Laboratory')).toBeInTheDocument()
  })

  it('shows navigation when user is logged in', () => {
    const mockUser = { username: 'testuser', role: 'ADMIN' }
    
    render(
      <BrowserRouter>
        <MainLayout user={mockUser} />
      </BrowserRouter>
    )

    expect(screen.getByText('Home')).toBeInTheDocument()
    expect(screen.getByText('Lab')).toBeInTheDocument()
    expect(screen.getByText('Settings')).toBeInTheDocument()
  })

  it('displays user info when logged in', () => {
    const mockUser = { username: 'testuser', role: 'ADMIN' }
    
    render(
      <BrowserRouter>
        <MainLayout user={mockUser} />
      </BrowserRouter>
    )

    expect(screen.getByText('testuser')).toBeInTheDocument()
    expect(screen.getByText('ADMIN')).toBeInTheDocument()
  })

  it('hides navigation when user is not logged in', () => {
    render(
      <BrowserRouter>
        <MainLayout />
      </BrowserRouter>
    )

    expect(screen.queryByText('Home')).not.toBeInTheDocument()
    expect(screen.queryByText('Lab')).not.toBeInTheDocument()
  })

  it('shows logout button when user is logged in', () => {
    const mockUser = { username: 'testuser', role: 'ADMIN' }
    const mockLogout = () => {}
    
    render(
      <BrowserRouter>
        <MainLayout user={mockUser} onLogout={mockLogout} />
      </BrowserRouter>
    )

    expect(screen.getByText('Logout')).toBeInTheDocument()
  })

  it('filters navigation based on user role', () => {
    const mockUser = { username: 'testuser', role: 'RECEPTION' }
    
    render(
      <BrowserRouter>
        <MainLayout user={mockUser} />
      </BrowserRouter>
    )

    // Reception should see Home and Lab but not Settings
    expect(screen.getByText('Home')).toBeInTheDocument()
    expect(screen.getByText('Lab')).toBeInTheDocument()
    expect(screen.queryByText('Settings')).not.toBeInTheDocument()
  })
})
