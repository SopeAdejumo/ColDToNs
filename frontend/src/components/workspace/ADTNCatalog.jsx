import { useState, useEffect } from 'react'
import axios from 'axios'

const ADTNCatalog = () => {
  const [pulsarNames, setPulsarNames] = useState('')
  const [atnfParams, setAtnfParams] = useState([])
  const [selectedParams, setSelectedParams] = useState([])
  const [searchFilter, setSearchFilter] = useState('')
  const [selectAll, setSelectAll] = useState(false)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    // Fetch ATNF parameters from backend
    const fetchParams = async () => {
      try {
        const response = await axios.get('/api/atnf-parameters')
        setAtnfParams(response.data)
      } catch (error) {
        console.error('Failed to fetch ATNF parameters:', error)
      }
    }
    fetchParams()
  }, [])

  const filteredParams = atnfParams.filter(param =>
    param.toLowerCase().includes(searchFilter.toLowerCase())
  )

  const handleParamToggle = (param) => {
    setSelectedParams(prev =>
      prev.includes(param)
        ? prev.filter(p => p !== param)
        : [...prev, param]
    )
  }

  const handleSelectAll = () => {
    if (selectAll) {
      setSelectedParams([])
    } else {
      setSelectedParams([...filteredParams])
    }
    setSelectAll(!selectAll)
  }

  const handleQuery = async () => {
    setLoading(true)
    try {
      const response = await axios.post('/api/tools/adtn-catalog/data', {
        pulsarNames: pulsarNames.split(',').map(name => name.trim()).filter(name => name),
        parameters: selectedParams
      })
      console.log('Query result:', response.data)
      // Handle the response data here
    } catch (error) {
      console.error('Query failed:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">ADTN Catalog</h2>
      <div className="space-y-4">
        {/* Pulsar Selection */}
        <div className="border border-gray-600 rounded-lg p-4">
          <label htmlFor="pulsar-jnames" className="block text-lg font-semibold mb-2">
            Pulsar Selection
          </label>
          <textarea
            id="pulsar-jnames"
            rows="3"
            placeholder="J0534+2200, J1939+2134"
            className="w-full p-2 border border-gray-600 rounded bg-gray-800 text-gray-100 mb-2 resize-y"
            value={pulsarNames}
            onChange={(e) => setPulsarNames(e.target.value)}
          />
          <p className="text-sm text-gray-400 mb-2">
            Enter a comma-separated list of pulsar JNAMES (e.g., 'J0534+2200, J1939+2134'). 
            Leave blank to query all pulsars.
          </p>
        </div>

        {/* Parameter Selection */}
        <div className="border border-gray-600 rounded-lg p-4">
          <label className="block text-lg font-semibold mb-2">Select Parameters</label>
          
          {/* Select All */}
          <div className="mb-2">
            <input
              type="checkbox"
              id="select-all-params"
              className="mr-2"
              checked={selectAll}
              onChange={handleSelectAll}
            />
            <label htmlFor="select-all-params" className="text-sm font-medium cursor-pointer">
              Select All
            </label>
          </div>

          {/* Search Filter */}
          <input
            type="text"
            placeholder="Search parameters..."
            className="w-full p-2 border border-gray-600 rounded bg-gray-800 text-gray-100 mb-2"
            value={searchFilter}
            onChange={(e) => setSearchFilter(e.target.value)}
          />

          {/* Parameter List */}
          <div className="max-h-40 overflow-y-auto border border-gray-600 rounded bg-gray-900 p-2 space-y-1">
            {filteredParams.map((param) => (
              <div key={param}>
                <input
                  type="checkbox"
                  id={`param-${param}`}
                  value={param}
                  className="mr-2"
                  checked={selectedParams.includes(param)}
                  onChange={() => handleParamToggle(param)}
                />
                <label htmlFor={`param-${param}`} className="cursor-pointer">
                  {param}
                </label>
              </div>
            ))}
          </div>

          <p className="text-sm text-gray-400 mt-2">
            Choose the catalogue parameters to retrieve (e.g., JNAME, RAJ, DECJ, P0, DM).
          </p>

          {/* Query Button */}
          <button
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
            onClick={handleQuery}
            disabled={loading || selectedParams.length === 0}
          >
            {loading ? 'Querying...' : 'Query Catalog'}
          </button>
        </div>
      </div>
    </div>
  )
}

export default ADTNCatalog