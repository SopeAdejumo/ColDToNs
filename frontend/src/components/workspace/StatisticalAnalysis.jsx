import { useState } from 'react'

const StatisticalAnalysis = () => {
  const [analysisType, setAnalysisType] = useState('Correlation Analysis')
  const [running, setRunning] = useState(false)

  const analysisTypes = [
    'Correlation Analysis',
    'Distribution Analysis',
    'Regression Analysis',
    'Time Series Analysis'
  ]

  const handleRunAnalysis = async () => {
    setRunning(true)
    setTimeout(() => {
      console.log('Analysis completed:', analysisType)
      setRunning(false)
    }, 3000)
  }

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Statistical Analysis</h2>
      <div className="space-y-4">
        <div className="border border-gray-600 rounded-lg p-4">
          <h3 className="text-lg font-semibold mb-2">Analysis Type</h3>
          <select
            className="w-full p-2 border border-gray-600 rounded bg-gray-800 text-gray-100 mb-2"
            value={analysisType}
            onChange={(e) => setAnalysisType(e.target.value)}
          >
            {analysisTypes.map(type => (
              <option key={type} value={type}>{type}</option>
            ))}
          </select>
          <button
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
            onClick={handleRunAnalysis}
            disabled={running}
          >
            {running ? 'Running Analysis...' : 'Run Analysis'}
          </button>
        </div>
      </div>
    </div>
  )
}

export default StatisticalAnalysis