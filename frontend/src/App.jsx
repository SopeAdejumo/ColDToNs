import { useState, useEffect } from 'react'
import axios from 'axios'
import MenuBar from './components/MenuBar'
import Sidebar from './components/Sidebar'
import Workspace from './components/Workspace'

function App() {
  const [menuConfig, setMenuConfig] = useState({})
  const [currentMenu, setCurrentMenu] = useState(null)
  const [currentTool, setCurrentTool] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Fetch menu configuration from backend
    const fetchMenuConfig = async () => {
      try {
        const response = await axios.get('/api/menu-config')
        setMenuConfig(response.data)
        setLoading(false)
      } catch (error) {
        console.error('Failed to fetch menu configuration:', error)
        setLoading(false)
      }
    }

    fetchMenuConfig()
  }, [])

  const handleMenuChange = (menuKey) => {
    setCurrentMenu(menuKey)
    setCurrentTool(null) // Reset tool when menu changes
  }

  const handleToolChange = (toolId) => {
    setCurrentTool(toolId)
  }

  if (loading) {
    return (
      <div className="bg-gray-900 text-white h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-lg">Loading ColDToNs...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-gray-900 text-gray-100 font-sans overflow-hidden h-screen">
      {/* Menu Bar */}
      <MenuBar 
        menuConfig={menuConfig}
        currentMenu={currentMenu}
        onMenuChange={handleMenuChange}
      />

      {/* Main Container */}
      <div className="flex h-screen" style={{ height: 'calc(100vh - 2.5rem)' }}>
        {/* Sidebar */}
        <Sidebar 
          menuConfig={menuConfig}
          currentMenu={currentMenu}
          currentTool={currentTool}
          onToolChange={handleToolChange}
        />

        {/* Workspace */}
        <Workspace 
          menuConfig={menuConfig}
          currentMenu={currentMenu}
          currentTool={currentTool}
        />
      </div>
    </div>
  )
}

export default App