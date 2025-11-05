import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { patientService } from '../../services/patients'
import { catalogService } from '../../services/catalog'
import { orderService } from '../../services/orders'
import type { Patient, Test } from '../../types'
import {
  validateCNIC,
  validatePhone,
  validateDOB,
  formatCNIC,
  formatPhone,
  calculateAge,
  formatCurrency,
} from '../../utils/validators'
import { ROUTES } from '../../utils/constants'

interface PatientFormData {
  cnic: string
  phone: string
  full_name: string
  patient_id: string
  gender: 'M' | 'F' | 'O'
  date_of_birth: string
  age: number
  age_unit: 'years' | 'months' | 'days'
}

export function NewLabSlipPage() {
  const navigate = useNavigate()

  // Patient form state
  const [patientData, setPatientData] = useState<PatientFormData>({
    cnic: '',
    phone: '',
    full_name: '',
    patient_id: '',
    gender: 'M',
    date_of_birth: '',
    age: 0,
    age_unit: 'years',
  })

  const [existingPatient, setExistingPatient] = useState<Patient | null>(null)
  const [patientSuggestions, setPatientSuggestions] = useState<Patient[]>([])

  // Test selection state
  const [testSearch, setTestSearch] = useState('')
  const [testSuggestions, setTestSuggestions] = useState<Test[]>([])
  const [selectedTests, setSelectedTests] = useState<Test[]>([])

  // Billing state
  const [discount, setDiscount] = useState(0)
  const [amountPaid, setAmountPaid] = useState(0)
  const [reportDate, setReportDate] = useState(
    new Date().toISOString().split('T')[0]
  )
  const [reportTime, setReportTime] = useState(
    new Date().toTimeString().slice(0, 5)
  )

  // UI state
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [isSubmitting, setIsSubmitting] = useState(false)

  // Search for existing patients by CNIC or phone
  useEffect(() => {
    const searchPatients = async () => {
      if (patientData.cnic.length >= 5 || patientData.phone.length >= 5) {
        const query = patientData.cnic || patientData.phone
        const patients = await patientService.search(query)
        setPatientSuggestions(patients)
      } else {
        setPatientSuggestions([])
      }
    }

    const debounce = setTimeout(searchPatients, 300)
    return () => clearTimeout(debounce)
  }, [patientData.cnic, patientData.phone])

  // Search tests
  useEffect(() => {
    const searchTests = async () => {
      if (testSearch.length >= 2) {
        const tests = await catalogService.search(testSearch)
        setTestSuggestions(
          tests.filter(t => !selectedTests.find(s => s.id === t.id))
        )
      } else {
        setTestSuggestions([])
      }
    }

    const debounce = setTimeout(searchTests, 300)
    return () => clearTimeout(debounce)
  }, [testSearch, selectedTests])

  // Calculate age from DOB
  useEffect(() => {
    if (patientData.date_of_birth && validateDOB(patientData.date_of_birth)) {
      const { age, unit } = calculateAge(patientData.date_of_birth)
      setPatientData(prev => ({ ...prev, age, age_unit: unit }))
    }
  }, [patientData.date_of_birth])

  const handlePatientChange = (field: keyof PatientFormData, value: string) => {
    let formattedValue = value

    if (field === 'cnic') {
      formattedValue = formatCNIC(value)
    } else if (field === 'phone') {
      formattedValue = formatPhone(value)
    }

    setPatientData(prev => ({ ...prev, [field]: formattedValue }))
    setExistingPatient(null)
    setErrors(prev => ({ ...prev, [field]: '' }))
  }

  const selectPatient = (patient: Patient) => {
    setExistingPatient(patient)
    setPatientData({
      cnic: patient.cnic,
      phone: patient.phone,
      full_name: patient.full_name,
      patient_id: patient.mrn,
      gender: patient.gender,
      date_of_birth: patient.date_of_birth,
      age: patient.age || 0,
      age_unit: patient.age_unit || 'years',
    })
    setPatientSuggestions([])
  }

  const addTest = (test: Test) => {
    setSelectedTests(prev => [...prev, test])
    setTestSearch('')
    setTestSuggestions([])
  }

  const removeTest = (testId: number) => {
    setSelectedTests(prev => prev.filter(t => t.id !== testId))
  }

  const billAmount = selectedTests.reduce((sum, test) => sum + test.price, 0)
  const netAmount = billAmount - discount
  const change = amountPaid - netAmount

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {}

    if (!patientData.full_name.trim()) {
      newErrors.full_name = 'Full name is required'
    }
    if (!patientData.cnic || !validateCNIC(patientData.cnic)) {
      newErrors.cnic = 'Valid CNIC is required (e.g., 12345-1234567-1)'
    }
    if (!patientData.phone || !validatePhone(patientData.phone)) {
      newErrors.phone = 'Valid phone number is required'
    }
    if (!patientData.date_of_birth || !validateDOB(patientData.date_of_birth)) {
      newErrors.date_of_birth = 'Valid date of birth is required'
    }
    if (selectedTests.length === 0) {
      newErrors.tests = 'At least one test must be selected'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (printImmediately: boolean) => {
    if (!validateForm()) return

    setIsSubmitting(true)
    try {
      // Create or use existing patient
      let patientId = existingPatient?.id

      if (!patientId) {
        const newPatient = await patientService.create({
          cnic: patientData.cnic,
          phone: patientData.phone,
          full_name: patientData.full_name,
          gender: patientData.gender,
          date_of_birth: patientData.date_of_birth,
        })
        patientId = newPatient.id
      }

      // Create order
      const order = await orderService.create({
        patient_id: patientId,
        test_ids: selectedTests.map(t => t.id),
        bill_amount: billAmount,
        discount,
        amount_paid: amountPaid,
        report_date: reportDate,
        report_time: reportTime,
      })

      if (printImmediately) {
        // TODO: Trigger PDF generation and download
        console.log('Print order:', order.id)
      }

      // Navigate to order detail or lab home
      navigate(ROUTES.LAB_ORDER_DETAIL(order.id))
    } catch (error) {
      console.error('Failed to create order:', error)
      setErrors({ submit: 'Failed to create order. Please try again.' })
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">New Lab Slip</h1>

      {errors.submit && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-800">{errors.submit}</p>
        </div>
      )}

      {/* Patient Information Section */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-xl font-semibold text-blue-700 mb-4">
          Patient Information
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {/* CNIC */}
          <div className="relative">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              CNIC <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              value={patientData.cnic}
              onChange={e => handlePatientChange('cnic', e.target.value)}
              className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 ${
                errors.cnic
                  ? 'border-red-500 focus:ring-red-500'
                  : 'border-gray-300 focus:ring-blue-500'
              }`}
              placeholder="12345-1234567-1"
            />
            {errors.cnic && (
              <p className="text-xs text-red-500 mt-1">{errors.cnic}</p>
            )}

            {/* Patient suggestions */}
            {patientSuggestions.length > 0 && (
              <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg max-h-40 overflow-y-auto">
                {patientSuggestions.map(patient => (
                  <button
                    key={patient.id}
                    type="button"
                    onClick={() => selectPatient(patient)}
                    className="w-full px-3 py-2 text-left hover:bg-blue-50 border-b border-gray-100 last:border-0"
                  >
                    <div className="font-medium">{patient.full_name}</div>
                    <div className="text-xs text-gray-600">
                      {patient.cnic} - {patient.phone}
                    </div>
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Mobile */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Mobile <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              value={patientData.phone}
              onChange={e => handlePatientChange('phone', e.target.value)}
              className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 ${
                errors.phone
                  ? 'border-red-500 focus:ring-red-500'
                  : 'border-gray-300 focus:ring-blue-500'
              }`}
              placeholder="03001234567"
            />
            {errors.phone && (
              <p className="text-xs text-red-500 mt-1">{errors.phone}</p>
            )}
          </div>

          {/* Full Name */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Full Name <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              value={patientData.full_name}
              onChange={e => handlePatientChange('full_name', e.target.value)}
              className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 ${
                errors.full_name
                  ? 'border-red-500 focus:ring-red-500'
                  : 'border-gray-300 focus:ring-blue-500'
              }`}
              placeholder="Enter full name"
            />
            {errors.full_name && (
              <p className="text-xs text-red-500 mt-1">{errors.full_name}</p>
            )}
          </div>

          {/* Patient ID (read-only) */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Patient ID
            </label>
            <input
              type="text"
              value={patientData.patient_id}
              readOnly
              className="w-full px-3 py-2 border border-gray-300 rounded-lg bg-gray-50"
              placeholder="Auto-generated"
            />
          </div>

          {/* Gender */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Gender
            </label>
            <select
              value={patientData.gender}
              onChange={e => handlePatientChange('gender', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="M">Male</option>
              <option value="F">Female</option>
              <option value="O">Other</option>
            </select>
          </div>

          {/* DOB */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Date of Birth <span className="text-red-500">*</span>
            </label>
            <input
              type="date"
              value={patientData.date_of_birth}
              max={new Date().toISOString().split('T')[0]}
              onChange={e =>
                handlePatientChange('date_of_birth', e.target.value)
              }
              className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 ${
                errors.date_of_birth
                  ? 'border-red-500 focus:ring-red-500'
                  : 'border-gray-300 focus:ring-blue-500'
              }`}
            />
            {errors.date_of_birth && (
              <p className="text-xs text-red-500 mt-1">
                {errors.date_of_birth}
              </p>
            )}
          </div>

          {/* Age (calculated) */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Age
            </label>
            <div className="flex gap-2">
              <input
                type="number"
                value={patientData.age}
                readOnly
                className="w-20 px-3 py-2 border border-gray-300 rounded-lg bg-gray-50"
              />
              <select
                value={patientData.age_unit}
                disabled
                className="flex-1 px-3 py-2 border border-gray-300 rounded-lg bg-gray-50"
              >
                <option value="years">Years</option>
                <option value="months">Months</option>
                <option value="days">Days</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* Test Selection Section */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-xl font-semibold text-blue-700 mb-4">
          Test Selection
        </h2>

        {/* Test Search */}
        <div className="mb-4 relative">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Search Tests
          </label>
          <input
            type="text"
            value={testSearch}
            onChange={e => setTestSearch(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Search by test name or code"
          />
          {errors.tests && (
            <p className="text-xs text-red-500 mt-1">{errors.tests}</p>
          )}

          {/* Test suggestions */}
          {testSuggestions.length > 0 && (
            <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg max-h-60 overflow-y-auto">
              {testSuggestions.map(test => (
                <button
                  key={test.id}
                  type="button"
                  onClick={() => addTest(test)}
                  className="w-full px-3 py-2 text-left hover:bg-blue-50 border-b border-gray-100 last:border-0"
                >
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="font-medium">{test.name}</div>
                      <div className="text-xs text-gray-600">
                        {test.code} - {test.specimen}
                      </div>
                    </div>
                    <div className="text-sm font-semibold text-blue-600">
                      {formatCurrency(test.price)}
                    </div>
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Selected Tests Table */}
        {selectedTests.length > 0 && (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-2 px-3 text-sm font-medium text-gray-700">
                    Test Name
                  </th>
                  <th className="text-left py-2 px-3 text-sm font-medium text-gray-700">
                    Code
                  </th>
                  <th className="text-left py-2 px-3 text-sm font-medium text-gray-700">
                    Specimen
                  </th>
                  <th className="text-right py-2 px-3 text-sm font-medium text-gray-700">
                    Price
                  </th>
                  <th className="text-center py-2 px-3 text-sm font-medium text-gray-700">
                    Action
                  </th>
                </tr>
              </thead>
              <tbody>
                {selectedTests.map(test => (
                  <tr key={test.id} className="border-b border-gray-100">
                    <td className="py-2 px-3">{test.name}</td>
                    <td className="py-2 px-3 text-sm text-gray-600">
                      {test.code}
                    </td>
                    <td className="py-2 px-3 text-sm text-gray-600">
                      {test.specimen}
                    </td>
                    <td className="py-2 px-3 text-right font-medium">
                      {formatCurrency(test.price)}
                    </td>
                    <td className="py-2 px-3 text-center">
                      <button
                        type="button"
                        onClick={() => removeTest(test.id)}
                        className="text-red-600 hover:text-red-800 text-sm"
                      >
                        Remove
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Billing Section */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-xl font-semibold text-blue-700 mb-4">
          Billing & Report Details
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div className="flex justify-between items-center py-2 border-b">
              <span className="text-gray-700">Bill Amount:</span>
              <span className="font-semibold text-lg">
                {formatCurrency(billAmount)}
              </span>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Discount
              </label>
              <input
                type="number"
                min="0"
                max={billAmount}
                value={discount}
                onChange={e => setDiscount(Number(e.target.value))}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div className="flex justify-between items-center py-2 border-b border-gray-400">
              <span className="text-gray-700 font-medium">Net Amount:</span>
              <span className="font-bold text-xl text-blue-600">
                {formatCurrency(netAmount)}
              </span>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Amount Paid
              </label>
              <input
                type="number"
                min="0"
                value={amountPaid}
                onChange={e => setAmountPaid(Number(e.target.value))}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div className="flex justify-between items-center py-2">
              <span className="text-gray-700">Change:</span>
              <span
                className={`font-semibold ${change >= 0 ? 'text-green-600' : 'text-red-600'}`}
              >
                {formatCurrency(Math.abs(change))}
              </span>
            </div>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Report Date
              </label>
              <input
                type="date"
                value={reportDate}
                onChange={e => setReportDate(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Report Time
              </label>
              <input
                type="time"
                value={reportTime}
                onChange={e => setReportTime(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex gap-4 justify-end">
        <button
          type="button"
          onClick={() => navigate(ROUTES.LAB)}
          disabled={isSubmitting}
          className="px-6 py-3 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 disabled:opacity-50"
        >
          Cancel
        </button>
        <button
          type="button"
          onClick={() => handleSubmit(false)}
          disabled={isSubmitting}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          {isSubmitting ? 'Saving...' : 'Save Only'}
        </button>
        <button
          type="button"
          onClick={() => handleSubmit(true)}
          disabled={isSubmitting}
          className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
        >
          {isSubmitting ? 'Saving...' : 'Save & Print'}
        </button>
      </div>
    </div>
  )
}
