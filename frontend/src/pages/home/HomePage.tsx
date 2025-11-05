export function HomePage() {
  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Quick Stats - Placeholder */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-700 mb-2">
            Today's Orders
          </h3>
          <p className="text-3xl font-bold text-blue-600">--</p>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-700 mb-2">
            Pending Samples
          </h3>
          <p className="text-3xl font-bold text-yellow-600">--</p>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-700 mb-2">
            Results Ready
          </h3>
          <p className="text-3xl font-bold text-green-600">--</p>
        </div>
      </div>

      <div className="mt-8">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Quick Actions</h2>
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-600">
            Quick action shortcuts will appear here based on your role.
          </p>
        </div>
      </div>
    </div>
  )
}
