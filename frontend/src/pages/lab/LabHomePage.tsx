import { Link } from 'react-router-dom'
import { ROUTES } from '../../utils/constants'

interface TileProps {
  title: string
  description: string
  to?: string
  onClick?: () => void
  color?: string
}

function Tile({ title, description, to, onClick, color = 'blue' }: TileProps) {
  const colorClasses = {
    blue: 'bg-blue-50 border-blue-200 hover:bg-blue-100',
    green: 'bg-green-50 border-green-200 hover:bg-green-100',
    purple: 'bg-purple-50 border-purple-200 hover:bg-purple-100',
    teal: 'bg-teal-50 border-teal-200 hover:bg-teal-100',
    orange: 'bg-orange-50 border-orange-200 hover:bg-orange-100',
    red: 'bg-red-50 border-red-200 hover:bg-red-100',
  }[color]

  const content = (
    <>
      <h3 className="text-lg font-semibold text-gray-800 mb-2">{title}</h3>
      <p className="text-sm text-gray-600">{description}</p>
    </>
  )

  if (to) {
    return (
      <Link
        to={to}
        className={`block p-6 rounded-lg border-2 ${colorClasses} transition-colors cursor-pointer`}
      >
        {content}
      </Link>
    )
  }

  return (
    <div
      onClick={onClick}
      className={`block p-6 rounded-lg border-2 ${colorClasses} transition-colors ${onClick ? 'cursor-pointer' : 'cursor-default opacity-60'}`}
    >
      {content}
    </div>
  )
}

export function LabHomePage() {
  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Lab Home</h1>

      {/* Main Lab Actions */}
      <section className="mb-8">
        <h2 className="text-xl font-semibold text-gray-700 mb-4">Lab Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <Tile
            title="New Lab Slip"
            description="Create a new test order"
            to={ROUTES.LAB_NEW}
            color="blue"
          />
          <Tile
            title="Due Lab Slip"
            description="View pending orders"
            color="orange"
          />
          <Tile
            title="Refund Lab Slip"
            description="Process refunds"
            color="red"
          />
          <Tile
            title="Modify Lab Slip"
            description="Edit existing orders"
            color="purple"
          />
          <Tile
            title="Test Results Saving"
            description="Enter test results"
            color="green"
          />
          <Tile
            title="Results Upload Bulk"
            description="Bulk upload results"
            color="teal"
          />
          <Tile
            title="Manage Lab Tests"
            description="View test catalog"
            color="blue"
          />
        </div>
      </section>

      {/* Reports Section */}
      <section>
        <h2 className="text-xl font-semibold text-gray-700 mb-4">Reports</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <Tile
            title="Daily Reports"
            description="View daily statistics"
            color="green"
          />
          <Tile
            title="Monthly Summary"
            description="Monthly overview"
            color="blue"
          />
          <Tile
            title="Department Wise"
            description="Department statistics"
            color="purple"
          />
        </div>
      </section>
    </div>
  )
}
