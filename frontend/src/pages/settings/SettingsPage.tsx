export function SettingsPage() {
  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Settings</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div className="bg-white rounded-lg shadow p-6 border-2 border-gray-200">
          <h3 className="text-lg font-semibold text-gray-800 mb-2">User Management</h3>
          <p className="text-sm text-gray-600">Manage users and roles</p>
        </div>
        
        <div className="bg-white rounded-lg shadow p-6 border-2 border-gray-200 opacity-60">
          <h3 className="text-lg font-semibold text-gray-800 mb-2">Branches</h3>
          <p className="text-sm text-gray-600">Configure lab branches</p>
        </div>
        
        <div className="bg-white rounded-lg shadow p-6 border-2 border-gray-200 opacity-60">
          <h3 className="text-lg font-semibold text-gray-800 mb-2">Departments</h3>
          <p className="text-sm text-gray-600">Manage departments</p>
        </div>
        
        <div className="bg-white rounded-lg shadow p-6 border-2 border-gray-200 opacity-60">
          <h3 className="text-lg font-semibold text-gray-800 mb-2">Doctors</h3>
          <p className="text-sm text-gray-600">Doctor information</p>
        </div>
        
        <div className="bg-white rounded-lg shadow p-6 border-2 border-gray-200 opacity-60">
          <h3 className="text-lg font-semibold text-gray-800 mb-2">System Settings</h3>
          <p className="text-sm text-gray-600">General configuration</p>
        </div>
        
        <div className="bg-white rounded-lg shadow p-6 border-2 border-gray-200 opacity-60">
          <h3 className="text-lg font-semibold text-gray-800 mb-2">Page Headers</h3>
          <p className="text-sm text-gray-600">Customize page headers</p>
        </div>
      </div>
      
      <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
        <p className="text-sm text-blue-800">
          Settings pages will be fully implemented in Stage F4.
        </p>
      </div>
    </div>
  )
}
