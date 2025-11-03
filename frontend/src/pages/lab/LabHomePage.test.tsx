import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { LabHomePage } from './LabHomePage'

describe('LabHomePage', () => {
  it('renders lab home title', () => {
    render(
      <BrowserRouter>
        <LabHomePage />
      </BrowserRouter>
    )

    expect(screen.getByText('Lab Home')).toBeInTheDocument()
  })

  it('displays lab action tiles', () => {
    render(
      <BrowserRouter>
        <LabHomePage />
      </BrowserRouter>
    )

    expect(screen.getByText('New Lab Slip')).toBeInTheDocument()
    expect(screen.getByText('Due Lab Slip')).toBeInTheDocument()
    expect(screen.getByText('Refund Lab Slip')).toBeInTheDocument()
    expect(screen.getByText('Modify Lab Slip')).toBeInTheDocument()
    expect(screen.getByText('Test Results Saving')).toBeInTheDocument()
    expect(screen.getByText('Results Upload Bulk')).toBeInTheDocument()
    expect(screen.getByText('Manage Lab Tests')).toBeInTheDocument()
  })

  it('displays reports section', () => {
    render(
      <BrowserRouter>
        <LabHomePage />
      </BrowserRouter>
    )

    expect(screen.getByText('Reports')).toBeInTheDocument()
    expect(screen.getByText('Daily Reports')).toBeInTheDocument()
    expect(screen.getByText('Monthly Summary')).toBeInTheDocument()
    expect(screen.getByText('Department Wise')).toBeInTheDocument()
  })

  it('new lab slip tile links to correct route', () => {
    render(
      <BrowserRouter>
        <LabHomePage />
      </BrowserRouter>
    )

    const newLabSlipLink = screen.getByText('New Lab Slip').closest('a')
    expect(newLabSlipLink).toHaveAttribute('href', '/lab/new')
  })
})
