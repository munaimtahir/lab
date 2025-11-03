import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from './App'

// Mock all page components to simplify testing
vi.mock('./pages/LoginPage', () => ({
  LoginPage: ({ onLogin }: { onLogin: (u: string) => void }) => (
    <div data-testid="login-page">
      <button onClick={() => onLogin('test')}>Mock Login</button>
    </div>
  ),
}))

vi.mock('./layouts/MainLayout', () => ({
  MainLayout: ({ user }: { user: { username: string; role: string } | null }) => (
    <div data-testid="main-layout">
      {user ? `Logged in as ${user.username}` : 'Not logged in'}
    </div>
  ),
}))

describe('App', () => {
  it('renders without crashing', () => {
    render(<App />)
    // Should render either login or main layout
    expect(
      screen.getByTestId('login-page') || screen.getByTestId('main-layout')
    ).toBeInTheDocument()
  })

  it('shows login page when not authenticated', () => {
    render(<App />)
    expect(screen.getByTestId('login-page')).toBeInTheDocument()
  })
})
