import WelcomeScreen from './workspace/WelcomeScreen'
import ADTNCatalog from './workspace/ADTNCatalog'
import DataImport from './workspace/DataImport'
import DataExport from './workspace/DataExport'
import DataBrowser from './workspace/DataBrowser'
import StatisticalAnalysis from './workspace/StatisticalAnalysis'

const Workspace = ({ menuConfig, currentMenu, currentTool }) => {
  // Component mapping for different tools
  const toolComponents = {
    'adtn-catalog': ADTNCatalog,
    'data-import': DataImport,
    'data-export': DataExport,
    'data-browser': DataBrowser,
    'statistical-analysis': StatisticalAnalysis,
  }

  const renderContent = () => {
    if (!currentTool) {
      return <WelcomeScreen />
    }

    const ToolComponent = toolComponents[currentTool]
    if (ToolComponent) {
      return <ToolComponent />
    }

    // Fallback for tools without specific components
    return (
      <div className="p-6">
        <h2 className="text-2xl font-bold mb-4">Tool: {currentTool}</h2>
        <p className="text-gray-400">This tool is under development.</p>
      </div>
    )
  }

  return (
    <div className="flex-1 bg-gray-900 relative overflow-hidden">
      <div className="workspace-content h-full overflow-y-auto">
        {renderContent()}
      </div>
    </div>
  )
}

export default Workspace