import { useState } from 'react'
import { Link, Outlet, useLocation } from 'react-router-dom'
import { ROUTES, COLORS } from '../utils/constants'

interface NavItem {
  path: string
  label: string
  roles?: string[]
}

const navItems: NavItem[] = [
  { path: ROUTES.HOME, label: 'Home' },
  { path: ROUTES.LAB, label: 'Lab' },
  {
    path: ROUTES.LAB_WORKLIST,
    label: 'Worklist',
    roles: ['ADMIN', 'PHLEBOTOMY', 'TECHNOLOGIST', 'PATHOLOGIST'],
  },
  { path: ROUTES.SETTINGS, label: 'Settings', roles: ['ADMIN'] },
]

interface MainLayoutProps {
  user?: { username: string; role: string } | null
  onLogout?: () => void
}

export function MainLayout({ user, onLogout }: MainLayoutProps) {
  const location = useLocation()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const isNavItemVisible = (item: NavItem) => {
    if (!item.roles) return true
    if (!user) return false
    return item.roles.includes(user.role)
  }

  const closeMobileMenu = () => {
    setMobileMenuOpen(false)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className={`${COLORS.header.bg} ${COLORS.header.text} shadow-lg`}>
        <div className="container mx-auto px-4">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-8">
              <h1 className="text-xl md:text-2xl font-bold">
                Al-Shifa Laboratory
              </h1>

              {/* Desktop Navigation */}
              {user && (
                <nav className="hidden md:flex space-x-1">
                  {navItems.filter(isNavItemVisible).map(item => {
                    const isActive =
                      location.pathname === item.path ||
                      (item.path !== ROUTES.HOME &&
                        location.pathname.startsWith(item.path))

                    return (
                      <Link
                        key={item.path}
                        to={item.path}
                        className={`px-4 py-2 rounded transition-colors ${
                          isActive
                            ? 'bg-red-800 text-white'
                            : 'text-red-100 hover:bg-red-800 hover:text-white'
                        }`}
                      >
                        {item.label}
                      </Link>
                    )
                  })}
                </nav>
              )}
            </div>

            {/* Right side: User Info & Mobile Menu Button */}
            {user && (
              <div className="flex items-center space-x-2 md:space-x-4">
                <div className="text-right hidden sm:block">
                  <div className="text-sm font-medium">{user.username}</div>
                  <div className="text-xs text-red-200">{user.role}</div>
                </div>

                {/* Logout Button - Desktop */}
                {onLogout && (
                  <button
                    onClick={onLogout}
                    className="hidden md:block bg-red-800 hover:bg-red-700 px-4 py-2 rounded transition-colors text-sm font-medium"
                  >
                    Logout
                  </button>
                )}

                {/* Mobile Menu Button */}
                <button
                  onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                  className="md:hidden p-2 rounded hover:bg-red-800 focus:outline-none focus:ring-2 focus:ring-red-300"
                  aria-label="Toggle mobile menu"
                  aria-expanded={mobileMenuOpen}
                >
                  {mobileMenuOpen ? (
                    // Close icon (X)
                    <svg
                      className="w-6 h-6"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M6 18L18 6M6 6l12 12"
                      />
                    </svg>
                  ) : (
                    // Hamburger icon
                    <svg
                      className="w-6 h-6"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M4 6h16M4 12h16M4 18h16"
                      />
                    </svg>
                  )}
                </button>
              </div>
            )}
          </div>

          {/* Mobile Navigation Menu */}
          {user && mobileMenuOpen && (
            <nav className="md:hidden border-t border-red-800 py-2">
              <div className="flex flex-col space-y-1">
                {navItems.filter(isNavItemVisible).map(item => {
                  const isActive =
                    location.pathname === item.path ||
                    (item.path !== ROUTES.HOME &&
                      location.pathname.startsWith(item.path))

                  return (
                    <Link
                      key={item.path}
                      to={item.path}
                      onClick={closeMobileMenu}
                      className={`px-4 py-3 rounded transition-colors ${
                        isActive
                          ? 'bg-red-800 text-white'
                          : 'text-red-100 hover:bg-red-800 hover:text-white'
                      }`}
                    >
                      {item.label}
                    </Link>
                  )
                })}

                {/* User info in mobile menu */}
                <div className="px-4 py-3 border-t border-red-800 mt-2">
                  <div className="text-sm font-medium">{user.username}</div>
                  <div className="text-xs text-red-200">{user.role}</div>
                </div>

                {/* Logout button in mobile menu */}
                {onLogout && (
                  <button
                    onClick={() => {
                      closeMobileMenu()
                      onLogout()
                    }}
                    className="mx-4 mb-2 px-4 py-2 bg-red-800 hover:bg-red-700 rounded transition-colors text-sm font-medium text-center"
                  >
                    Logout
                  </button>
                )}
              </div>
            </nav>
          )}
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-6">
        <Outlet />
      </main>
    </div>
  )
}
