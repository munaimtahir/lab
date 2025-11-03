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
  { path: ROUTES.LAB_WORKLIST, label: 'Worklist', roles: ['ADMIN', 'PHLEBOTOMY', 'TECHNOLOGIST', 'PATHOLOGIST'] },
  { path: ROUTES.SETTINGS, label: 'Settings', roles: ['ADMIN'] },
]

interface MainLayoutProps {
  user?: { username: string; role: string } | null
  onLogout?: () => void
}

export function MainLayout({ user, onLogout }: MainLayoutProps) {
  const location = useLocation()

  const isNavItemVisible = (item: NavItem) => {
    if (!item.roles) return true
    if (!user) return false
    return item.roles.includes(user.role)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className={`${COLORS.header.bg} ${COLORS.header.text} shadow-lg`}>
        <div className="container mx-auto px-4">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-8">
              <h1 className="text-2xl font-bold">Al-Shifa Laboratory</h1>
              
              {/* Main Navigation */}
              {user && (
                <nav className="hidden md:flex space-x-1">
                  {navItems.filter(isNavItemVisible).map((item) => {
                    const isActive = location.pathname === item.path || 
                      (item.path !== ROUTES.HOME && location.pathname.startsWith(item.path))
                    
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

            {/* User Info & Logout */}
            {user && (
              <div className="flex items-center space-x-4">
                <div className="text-right hidden sm:block">
                  <div className="text-sm font-medium">{user.username}</div>
                  <div className="text-xs text-red-200">{user.role}</div>
                </div>
                {onLogout && (
                  <button
                    onClick={onLogout}
                    className="bg-red-800 hover:bg-red-700 px-4 py-2 rounded transition-colors text-sm font-medium"
                  >
                    Logout
                  </button>
                )}
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-6">
        <Outlet />
      </main>
    </div>
  )
}
