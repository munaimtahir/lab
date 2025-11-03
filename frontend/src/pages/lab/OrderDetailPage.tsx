import { useParams } from 'react-router-dom'

export function OrderDetailPage() {
  const { id } = useParams<{ id: string }>()

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Order Detail - {id}</h1>
      
      <div className="bg-white rounded-lg shadow p-6">
        <p className="text-gray-600">
          Order detail page with tabs (Summary, Samples, Results, Report) will be implemented in Stage F3.
        </p>
      </div>
    </div>
  )
}
