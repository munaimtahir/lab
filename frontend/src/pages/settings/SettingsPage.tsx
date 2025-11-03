import { Link } from 'react-router-dom'

interface SettingsTileProps {
  title: string
  description: string
  to?: string
  isImplemented?: boolean
}

function SettingsTile({ title, description, to, isImplemented = false }: SettingsTileProps) {
  const content = (
    <>
      <h3 className="text-lg font-semibold text-gray-800 mb-2">{title}</h3>
      <p className="text-sm text-gray-600">{description}</p>
      {!isImplemented && (
        <p className="text-xs text-orange-600 mt-2">Coming soon</p>
      )}
    </>
  )

  if (to && isImplemented) {
    return (
      <Link
        to={to}
        className="block bg-white rounded-lg shadow p-6 border-2 border-gray-200 hover:border-blue-500 hover:shadow-lg transition-all cursor-pointer"
      >
        {content}
      </Link>
    )
  }

  return (
    <div className={`block bg-white rounded-lg shadow p-6 border-2 border-gray-200 ${!isImplemented ? 'opacity-60' : ''}`}>
      {content}
    </div>
  )
}

export function SettingsPage() {
  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Settings</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <SettingsTile
          title="User Management"
          description="Manage users, roles, and permissions"
          isImplemented={false}
        />
        
        <SettingsTile
          title="Branches"
          description="Configure lab branches and locations"
          isImplemented={false}
        />
        
        <SettingsTile
          title="Departments"
          description="Manage test departments"
          isImplemented={false}
        />
        
        <SettingsTile
          title="Doctors"
          description="Doctor information and signatures"
          isImplemented={false}
        />
        
        <SettingsTile
          title="System Settings"
          description="General system configuration"
          isImplemented={false}
        />
        
        <SettingsTile
          title="Page Headers"
          description="Customize report headers and branding"
          isImplemented={false}
        />
      </div>
      
      <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
        <p className="text-sm text-blue-800">
          <strong>Note:</strong> Settings pages are currently stubs. Backend endpoints exist for user management,
          branches, and departments. Full CRUD interfaces can be implemented as needed.
        </p>
      </div>
    </div>
  )
}

