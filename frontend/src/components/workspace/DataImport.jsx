import { useState } from 'react'

const DataImport = () => {
  const [file, setFile] = useState(null)
  const [databaseUrl, setDatabaseUrl] = useState('')
  const [uploading, setUploading] = useState(false)
  const [connecting, setConnecting] = useState(false)

  const handleFileChange = (e) => {
    setFile(e.target.files[0])
  }

  const handleUpload = async () => {
    if (!file) return
    
    setUploading(true)
    // Simulate upload process
    setTimeout(() => {
      console.log('File uploaded:', file.name)
      setUploading(false)
      setFile(null)
    }, 2000)
  }

  const handleConnect = async () => {
    if (!databaseUrl) return
    
    setConnecting(true)
    // Simulate connection process
    setTimeout(() => {
      console.log('Connected to database:', databaseUrl)
      setConnecting(false)
    }, 1500)
  }

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Data Import</h2>
      <div className="space-y-4">
        {/* File Upload */}
        <div className="border border-gray-600 rounded-lg p-4">
          <h3 className="text-lg font-semibold mb-2">Upload Data File</h3>
          <input
            type="file"
            className="w-full p-2 border border-gray-600 rounded bg-gray-800 text-gray-100 mb-2"
            accept=".csv,.json,.txt"
            onChange={handleFileChange}
          />
          {file && (
            <p className="text-sm text-gray-400 mb-2">
              Selected: {file.name} ({(file.size / 1024).toFixed(1)} KB)
            </p>
          )}
          <button
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
            onClick={handleUpload}
            disabled={!file || uploading}
          >
            {uploading ? 'Uploading...' : 'Upload'}
          </button>
        </div>

        {/* Database Connection */}
        <div className="border border-gray-600 rounded-lg p-4">
          <h3 className="text-lg font-semibold mb-2">Connect to Database</h3>
          <input
            type="text"
            placeholder="Database URL"
            className="w-full p-2 border border-gray-600 rounded bg-gray-800 text-gray-100 mb-2"
            value={databaseUrl}
            onChange={(e) => setDatabaseUrl(e.target.value)}
          />
          <button
            className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 disabled:opacity-50"
            onClick={handleConnect}
            disabled={!databaseUrl || connecting}
          >
            {connecting ? 'Connecting...' : 'Connect'}
          </button>
        </div>
      </div>
    </div>
  )
}

export default DataImport