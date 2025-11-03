import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { orderService } from '../../services/orders'
import type { Order } from '../../types'
import { ROUTES, COLORS } from '../../utils/constants'
import { formatDateTime, formatCurrency } from '../../utils/validators'
import { useAuth } from '../../hooks/useAuth'

type TabType = 'summary' | 'samples' | 'results' | 'report'

export function OrderDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { user } = useAuth()
  
  const [order, setOrder] = useState<Order | null>(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<TabType>('summary')

  useEffect(() => {
    if (id) {
      fetchOrder(Number(id))
    }
  }, [id])

  const fetchOrder = async (orderId: number) => {
    setLoading(true)
    try {
      const data = await orderService.getById(orderId)
      setOrder(data)
    } catch (error) {
      console.error('Failed to fetch order:', error)
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status: string) => {
    return COLORS.status[status as keyof typeof COLORS.status] || 'bg-gray-100 text-gray-800'
  }

  const canCollectSamples = user && ['ADMIN', 'PHLEBOTOMY'].includes(user.role)
  const canReceiveSamples = user && ['ADMIN', 'TECHNOLOGIST', 'PATHOLOGIST'].includes(user.role)
  const canEnterResults = user && ['ADMIN', 'TECHNOLOGIST'].includes(user.role)
  const canVerifyResults = user && ['ADMIN', 'PATHOLOGIST'].includes(user.role)

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-blue-600 border-r-transparent"></div>
        <p className="mt-2 text-gray-600">Loading order...</p>
      </div>
    )
  }

  if (!order) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600">Order not found</p>
        <button
          onClick={() => navigate(ROUTES.LAB_WORKLIST)}
          className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          Back to Worklist
        </button>
      </div>
    )
  }

  return (
    <div>
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">Order Detail</h1>
          <p className="text-gray-600">{order.order_number}</p>
        </div>
        <button
          onClick={() => navigate(ROUTES.LAB_WORKLIST)}
          className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50"
        >
          Back to Worklist
        </button>
      </div>

      {/* Status Badge */}
      <div className="mb-6">
        <span className={`inline-block px-4 py-2 rounded-lg text-sm font-medium ${getStatusColor(order.status)}`}>
          Status: {order.status}
        </span>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow">
        <div className="border-b border-gray-200">
          <nav className="flex -mb-px">
            <button
              onClick={() => setActiveTab('summary')}
              className={`px-6 py-3 border-b-2 font-medium text-sm ${
                activeTab === 'summary'
                  ? 'border-blue-600 text-blue-600'
                  : 'border-transparent text-gray-600 hover:text-gray-800 hover:border-gray-300'
              }`}
            >
              Summary
            </button>
            <button
              onClick={() => setActiveTab('samples')}
              className={`px-6 py-3 border-b-2 font-medium text-sm ${
                activeTab === 'samples'
                  ? 'border-blue-600 text-blue-600'
                  : 'border-transparent text-gray-600 hover:text-gray-800 hover:border-gray-300'
              }`}
            >
              Samples
            </button>
            <button
              onClick={() => setActiveTab('results')}
              className={`px-6 py-3 border-b-2 font-medium text-sm ${
                activeTab === 'results'
                  ? 'border-blue-600 text-blue-600'
                  : 'border-transparent text-gray-600 hover:text-gray-800 hover:border-gray-300'
              }`}
            >
              Results
            </button>
            <button
              onClick={() => setActiveTab('report')}
              className={`px-6 py-3 border-b-2 font-medium text-sm ${
                activeTab === 'report'
                  ? 'border-blue-600 text-blue-600'
                  : 'border-transparent text-gray-600 hover:text-gray-800 hover:border-gray-300'
              }`}
            >
              Report
            </button>
          </nav>
        </div>

        <div className="p-6">
          {/* Summary Tab */}
          {activeTab === 'summary' && (
            <div className="space-y-6">
              {/* Patient Info */}
              <div>
                <h3 className="text-lg font-semibold text-gray-800 mb-3">Patient Information</h3>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm">
                  <div>
                    <span className="text-gray-600">Name:</span>
                    <p className="font-medium">{order.patient.full_name}</p>
                  </div>
                  <div>
                    <span className="text-gray-600">MRN:</span>
                    <p className="font-medium">{order.patient.mrn}</p>
                  </div>
                  <div>
                    <span className="text-gray-600">Gender:</span>
                    <p className="font-medium">{order.patient.gender === 'M' ? 'Male' : order.patient.gender === 'F' ? 'Female' : 'Other'}</p>
                  </div>
                  <div>
                    <span className="text-gray-600">Age:</span>
                    <p className="font-medium">{order.patient.age} {order.patient.age_unit}</p>
                  </div>
                  <div>
                    <span className="text-gray-600">Phone:</span>
                    <p className="font-medium">{order.patient.phone}</p>
                  </div>
                  <div>
                    <span className="text-gray-600">CNIC:</span>
                    <p className="font-medium">{order.patient.cnic}</p>
                  </div>
                </div>
              </div>

              {/* Order Info */}
              <div>
                <h3 className="text-lg font-semibold text-gray-800 mb-3">Order Information</h3>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm">
                  <div>
                    <span className="text-gray-600">Order Number:</span>
                    <p className="font-medium">{order.order_number}</p>
                  </div>
                  <div>
                    <span className="text-gray-600">Created:</span>
                    <p className="font-medium">{formatDateTime(order.created_at)}</p>
                  </div>
                  <div>
                    <span className="text-gray-600">Created By:</span>
                    <p className="font-medium">{order.created_by.username}</p>
                  </div>
                  <div>
                    <span className="text-gray-600">Status:</span>
                    <p className="font-medium">{order.status}</p>
                  </div>
                </div>
              </div>

              {/* Test Items */}
              <div>
                <h3 className="text-lg font-semibold text-gray-800 mb-3">Ordered Tests</h3>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b border-gray-200">
                        <th className="text-left py-2 px-3 text-sm font-medium text-gray-700">Test Name</th>
                        <th className="text-left py-2 px-3 text-sm font-medium text-gray-700">Code</th>
                        <th className="text-left py-2 px-3 text-sm font-medium text-gray-700">Specimen</th>
                        <th className="text-right py-2 px-3 text-sm font-medium text-gray-700">Price</th>
                        <th className="text-center py-2 px-3 text-sm font-medium text-gray-700">Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      {order.items.map(item => (
                        <tr key={item.id} className="border-b border-gray-100">
                          <td className="py-2 px-3">{item.test.name}</td>
                          <td className="py-2 px-3 text-sm text-gray-600">{item.test.code}</td>
                          <td className="py-2 px-3 text-sm text-gray-600">{item.test.specimen}</td>
                          <td className="py-2 px-3 text-right font-medium">{formatCurrency(item.test.price)}</td>
                          <td className="py-2 px-3 text-center">
                            <span className={`px-2 py-1 rounded text-xs font-medium ${getStatusColor(item.status)}`}>
                              {item.status}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Billing */}
              <div>
                <h3 className="text-lg font-semibold text-gray-800 mb-3">Billing</h3>
                <div className="bg-gray-50 p-4 rounded-lg">
                  <div className="flex justify-between mb-2">
                    <span>Bill Amount:</span>
                    <span className="font-medium">{formatCurrency(order.bill_amount)}</span>
                  </div>
                  <div className="flex justify-between mb-2">
                    <span>Discount:</span>
                    <span className="font-medium">{formatCurrency(order.discount)}</span>
                  </div>
                  <div className="flex justify-between border-t pt-2">
                    <span className="font-semibold">Amount Paid:</span>
                    <span className="font-semibold text-blue-600">{formatCurrency(order.amount_paid)}</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Samples Tab */}
          {activeTab === 'samples' && (
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Sample Management</h3>
              <div className="bg-blue-50 border border-blue-200 p-4 rounded-lg">
                <p className="text-sm text-blue-800">
                  Sample collection and receiving workflow will be fully implemented here.
                  {canCollectSamples && <span className="block mt-2 font-medium">You can collect samples.</span>}
                  {canReceiveSamples && <span className="block mt-2 font-medium">You can receive samples.</span>}
                </p>
              </div>
            </div>
          )}

          {/* Results Tab */}
          {activeTab === 'results' && (
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Results Entry</h3>
              <div className="bg-blue-50 border border-blue-200 p-4 rounded-lg">
                <p className="text-sm text-blue-800">
                  Results entry and verification workflow will be fully implemented here.
                  {canEnterResults && <span className="block mt-2 font-medium">You can enter results.</span>}
                  {canVerifyResults && <span className="block mt-2 font-medium">You can verify and publish results.</span>}
                </p>
              </div>
            </div>
          )}

          {/* Report Tab */}
          {activeTab === 'report' && (
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Report Generation</h3>
              <div className="text-center py-8">
                <p className="text-gray-600 mb-4">Generate and download PDF report</p>
                <button
                  className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700"
                  onClick={() => console.log('Generate report for order:', order.id)}
                >
                  Generate PDF Report
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

