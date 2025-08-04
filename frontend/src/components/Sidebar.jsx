const Sidebar = ({ menuConfig, currentMenu, currentTool, onToolChange }) => {
  if (!currentMenu || !menuConfig[currentMenu]) {
    return (
      <div className="w-64 bg-gray-800 text-gray-100 shadow-lg sidebar-scroll overflow-y-auto"
           style={{ height: 'calc(100vh - 2.5rem)' }}>
        <div className="p-4 text-center text-gray-400">
          <p>Select a menu item to view tools</p>
        </div>
      </div>
    )
  }

  const menuData = menuConfig[currentMenu]

  const handleToolClick = (toolId) => {
    onToolChange(toolId)
  }

  return (
    <div className="w-64 bg-gray-800 text-gray-100 shadow-lg sidebar-scroll overflow-y-auto"
         style={{ height: 'calc(100vh - 2.5rem)' }}>
      {/* Header */}
      <div className="p-4 border-b border-gray-700">
        <h2 className="text-lg font-semibold text-gray-100">
          {menuData.title}
        </h2>
      </div>

      {/* Tools */}
      <div className="p-2">
        {menuData.tools.map((tool) => (
          <div
            key={tool.id}
            className={`
              tool-item p-4 mb-3 rounded-lg cursor-pointer 
              transition-all duration-200 hover:bg-gray-700
              sidebar-item
              ${currentTool === tool.id ? 'bg-gray-700' : ''}
            `}
            onClick={() => handleToolClick(tool.id)}
          >
            <div className="flex items-center mb-2">
              <i className={`${tool.icon} mr-3 text-blue-400`}></i>
              <span className="font-medium">{tool.name}</span>
            </div>
            <p className="text-sm text-gray-400">{tool.description}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Sidebar