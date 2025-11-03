import { useState } from 'react'
import './App.css'

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-blue-600 text-white p-4">
        <div className="container mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-bold">Al Shifa LIMS</h1>
          {isLoggedIn ? (
            <button
              onClick={() => setIsLoggedIn(false)}
              className="bg-white text-blue-600 px-4 py-2 rounded hover:bg-gray-100"
            >
              Logout
            </button>
          ) : (
            <button
              onClick={() => setIsLoggedIn(true)}
              className="bg-white text-blue-600 px-4 py-2 rounded hover:bg-gray-100"
            >
              Login
            </button>
          )}
        </div>
      </nav>

      <main className="container mx-auto p-8">
        {isLoggedIn ? (
          <div>
            <h2 className="text-3xl font-bold mb-6">Welcome to Al Shifa LIMS</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
                <h3 className="text-xl font-semibold mb-2">Patients</h3>
                <p className="text-gray-600 mb-4">Register and search patients</p>
                <button className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
                  Manage Patients
                </button>
              </div>

              <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
                <h3 className="text-xl font-semibold mb-2">Orders</h3>
                <p className="text-gray-600 mb-4">Create and view test orders</p>
                <button className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
                  Manage Orders
                </button>
              </div>

              <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
                <h3 className="text-xl font-semibold mb-2">Reports</h3>
                <p className="text-gray-600 mb-4">View and download reports</p>
                <button className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700">
                  View Reports
                </button>
              </div>
            </div>
          </div>
        ) : (
          <div className="max-w-md mx-auto bg-white p-8 rounded-lg shadow">
            <h2 className="text-2xl font-bold mb-6 text-center">Login to LIMS</h2>
            <form className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Username</label>
                <input
                  type="text"
                  className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Enter username"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Password</label>
                <input
                  type="password"
                  className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Enter password"
                />
              </div>
              <button
                type="button"
                onClick={() => setIsLoggedIn(true)}
                className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
              >
                Login
              </button>
            </form>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
