import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { HomePage } from './HomePage'

describe('HomePage', () => {
  it('renders dashboard title', () => {
    render(
      <BrowserRouter>
        <HomePage />
      </BrowserRouter>
    )

    expect(screen.getByText('Dashboard')).toBeInTheDocument()
  })

  it('displays quick stats cards', () => {
    render(
      <BrowserRouter>
        <HomePage />
      </BrowserRouter>
    )

    expect(screen.getByText("Today's Orders")).toBeInTheDocument()
    expect(screen.getByText('Pending Samples')).toBeInTheDocument()
    expect(screen.getByText('Results Ready')).toBeInTheDocument()
  })

  it('displays quick actions section', () => {
    render(
      <BrowserRouter>
        <HomePage />
      </BrowserRouter>
    )

    expect(screen.getByText('Quick Actions')).toBeInTheDocument()
  })
})
