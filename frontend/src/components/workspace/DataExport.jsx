import { useState } from 'react'

const DataExport = () => {
  const [exportFormat, setExportFormat] = useState('CSV')
  const [exporting, setExporting] = useState(false)

  const formats = ['CSV', 'JSON', 'Excel', 'HDF5']

  const handleExport = async () => {
    setExporting(true)
    // Simulate export process
    setTimeout(() => {
      console.log('Data exported as:', exportFormat)
      setExporting(false)
    }, 2000)
  }

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Data Export</h2>
      <div className="space-y-4">
        <div className="border border-gray-600 rounded-lg p-4">
          <h3 className="text-lg font-semibold mb-2">Export Format</h3>
          <select
            className="w-full p-2 border border-gray-600 rounded bg-gray-800 text-gray-100 mb-2"
            value={exportFormat}
            onChange={(e) => setExportFormat(e.target.value)}
          >
            {formats.map(format => (
              <option key={format} value={format}>{format}</option>
            ))}
          </select>
          <button
            className="px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700 disabled:opacity-50"
            onClick={handleExport}
            disabled={exporting}
          >
            {exporting ? 'Exporting...' : 'Export Data'}
          </button>
        </div>
      </div>
    </div>
  )
}

export default DataExport