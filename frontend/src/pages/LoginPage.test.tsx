import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { LoginPage } from './LoginPage'

describe('LoginPage', () => {
  it('renders login form', () => {
    const mockLogin = vi.fn()
    render(<LoginPage onLogin={mockLogin} />)

    expect(screen.getByText('Al-Shifa Laboratory')).toBeInTheDocument()
    expect(screen.getByLabelText('Username')).toBeInTheDocument()
    expect(screen.getByLabelText('Password')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Login' })).toBeInTheDocument()
  })

  it('calls onLogin with username on submit', () => {
    const mockLogin = vi.fn()
    render(<LoginPage onLogin={mockLogin} />)

    const usernameInput = screen.getByLabelText('Username')
    const passwordInput = screen.getByLabelText('Password')
    const loginButton = screen.getByRole('button', { name: 'Login' })

    fireEvent.change(usernameInput, { target: { value: 'testuser' } })
    fireEvent.change(passwordInput, { target: { value: 'testpass' } })
    fireEvent.click(loginButton)

    expect(mockLogin).toHaveBeenCalledWith('testuser')
  })

  it('shows demo credentials', () => {
    const mockLogin = vi.fn()
    render(<LoginPage onLogin={mockLogin} />)

    expect(screen.getByText('Demo credentials:')).toBeInTheDocument()
    expect(screen.getByText('admin / admin123')).toBeInTheDocument()
  })

  it('requires username and password', () => {
    const mockLogin = vi.fn()
    render(<LoginPage onLogin={mockLogin} />)

    const usernameInput = screen.getByLabelText('Username') as HTMLInputElement
    const passwordInput = screen.getByLabelText('Password') as HTMLInputElement

    expect(usernameInput.required).toBe(true)
    expect(passwordInput.required).toBe(true)
  })
})
