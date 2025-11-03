import { useState } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { MainLayout } from './layouts/MainLayout'
import { LoginPage } from './pages/LoginPage'
import { HomePage } from './pages/home/HomePage'
import { LabHomePage } from './pages/lab/LabHomePage'
import { NewLabSlipPage } from './pages/lab/NewLabSlipPage'
import { LabWorklistPage } from './pages/lab/LabWorklistPage'
import { OrderDetailPage } from './pages/lab/OrderDetailPage'
import { SettingsPage } from './pages/settings/SettingsPage'
import { ROUTES } from './utils/constants'

function App() {
  // Temporary mock auth state - will be replaced with proper auth in F1
  const [user, setUser] = useState<{ username: string; role: string } | null>(null)

  const handleLogin = (username: string) => {
    // Mock login - will be replaced with real API call in F1
    setUser({
      username,
      role: 'ADMIN', // Mock role
    })
  }

  const handleLogout = () => {
    setUser(null)
  }

  return (
    <BrowserRouter>
      <Routes>
        {!user ? (
          <>
            <Route path={ROUTES.LOGIN} element={<LoginPage onLogin={handleLogin} />} />
            <Route path="*" element={<Navigate to={ROUTES.LOGIN} replace />} />
          </>
        ) : (
          <Route element={<MainLayout user={user} onLogout={handleLogout} />}>
            <Route path={ROUTES.HOME} element={<HomePage />} />
            <Route path={ROUTES.LAB} element={<LabHomePage />} />
            <Route path={ROUTES.LAB_NEW} element={<NewLabSlipPage />} />
            <Route path={ROUTES.LAB_WORKLIST} element={<LabWorklistPage />} />
            <Route path={ROUTES.LAB_ORDER} element={<OrderDetailPage />} />
            <Route path={ROUTES.SETTINGS} element={<SettingsPage />} />
            <Route path="*" element={<Navigate to={ROUTES.HOME} replace />} />
          </Route>
        )}
      </Routes>
    </BrowserRouter>
  )
}

export default App
