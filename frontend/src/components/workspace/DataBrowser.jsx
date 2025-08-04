import { useState } from 'react'

const DataBrowser = () => {
  const [searchTerm, setSearchTerm] = useState('')

  const datasets = [
    { name: 'Pulsar Catalog J2000', entries: 2500 },
    { name: 'Magnetar Database', entries: 30 },
    { name: 'X-ray Binary Systems', entries: 180 }
  ]

  const filteredDatasets = datasets.filter(dataset =>
    dataset.name.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Data Browser</h2>
      <div className="space-y-4">
        <div className="border border-gray-600 rounded-lg p-4">
          <input
            type="text"
            placeholder="Search datasets..."
            className="w-full p-2 border border-gray-600 rounded bg-gray-800 text-gray-100 mb-4"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          <div className="grid grid-cols-1 gap-2">
            {filteredDatasets.map((dataset, index) => (
              <div
                key={index}
                className="p-3 border border-gray-600 rounded hover:bg-gray-800 cursor-pointer"
              >
                <strong>{dataset.name}</strong> - {dataset.entries} entries
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default DataBrowser