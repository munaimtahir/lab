import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { AuthProvider, useAuth } from './hooks/useAuth'
import { ProtectedRoute } from './components/ProtectedRoute'
import { MainLayout } from './layouts/MainLayout'
import { LoginPage } from './pages/LoginPage'
import { HomePage } from './pages/home/HomePage'
import { LabHomePage } from './pages/lab/LabHomePage'
import { NewLabSlipPage } from './pages/lab/NewLabSlipPage'
import { LabWorklistPage } from './pages/lab/LabWorklistPage'
import { OrderDetailPage } from './pages/lab/OrderDetailPage'
import { SettingsPage } from './pages/settings/SettingsPage'
import { ROUTES } from './utils/constants'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
})

function AppRoutes() {
  const { user, isAuthenticated, login, logout } = useAuth()

  return (
    <Routes>
      {!isAuthenticated ? (
        <>
          <Route path={ROUTES.LOGIN} element={<LoginPage onLogin={login} />} />
          <Route path="*" element={<Navigate to={ROUTES.LOGIN} replace />} />
        </>
      ) : (
        <Route
          element={
            <MainLayout
              user={user ? { username: user.username, role: user.role } : null}
              onLogout={logout}
            />
          }
        >
          <Route path={ROUTES.HOME} element={<HomePage />} />
          <Route path={ROUTES.LAB} element={<LabHomePage />} />
          <Route path={ROUTES.LAB_NEW} element={<NewLabSlipPage />} />
          <Route
            path={ROUTES.LAB_WORKLIST}
            element={
              <ProtectedRoute
                allowedRoles={['ADMIN', 'PHLEBOTOMY', 'TECHNOLOGIST', 'PATHOLOGIST']}
              >
                <LabWorklistPage />
              </ProtectedRoute>
            }
          />
          <Route path={ROUTES.LAB_ORDER} element={<OrderDetailPage />} />
          <Route
            path={ROUTES.SETTINGS}
            element={
              <ProtectedRoute allowedRoles={['ADMIN']}>
                <SettingsPage />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<Navigate to={ROUTES.HOME} replace />} />
        </Route>
      )}
    </Routes>
  )
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <BrowserRouter>
          <AppRoutes />
        </BrowserRouter>
      </AuthProvider>
    </QueryClientProvider>
  )
}

export default App
