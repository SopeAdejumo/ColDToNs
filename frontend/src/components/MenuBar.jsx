import { useState, useEffect } from 'react'

const MenuBar = ({ menuConfig, currentMenu, onMenuChange }) => {
  const [ripples, setRipples] = useState([])

  const menuItems = [
    { key: 'database', icon: 'fas fa-database', label: 'Database' },
    { key: 'analysis', icon: 'fas fa-calculator', label: 'Analysis' },
    { key: 'visualization', icon: 'fas fa-chart-line', label: 'Visualization' },
    { key: 'modeling', icon: 'fas fa-cube', label: 'Modeling' },
    { key: 'simulation', icon: 'fas fa-atom', label: 'Simulation' },
    { key: 'collaboration', icon: 'fas fa-share-alt', label: 'Collaboration' },
    { key: 'help', icon: 'fas fa-question-circle', label: 'Help' }
  ]

  const handleMenuClick = (menuKey, event) => {
    onMenuChange(menuKey)
    
    // Add ripple effect
    const rect = event.currentTarget.getBoundingClientRect()
    const size = Math.max(rect.width, rect.height)
    const x = event.clientX - rect.left - size / 2
    const y = event.clientY - rect.top - size / 2
    
    const newRipple = {
      id: Date.now(),
      x,
      y,
      size
    }
    
    setRipples(prev => [...prev, newRipple])
    
    // Remove ripple after animation
    setTimeout(() => {
      setRipples(prev => prev.filter(ripple => ripple.id !== newRipple.id))
    }, 600)
  }

  return (
    <div className="flex bg-gray-800 px-3 h-10 items-center border-b border-gray-700 shadow-lg">
      {menuItems.map((item) => (
        <span
          key={item.key}
          className={`
            menu-item px-4 py-1 cursor-pointer text-sm select-none 
            transition-all duration-200 rounded-md hover:bg-gray-600 hover:text-white
            relative overflow-hidden
            ${currentMenu === item.key ? 'menu-item-active' : ''}
          `}
          onClick={(e) => handleMenuClick(item.key, e)}
        >
          <i className={`${item.icon} mr-2`}></i>
          {item.label}
          
          {/* Ripple effects */}
          {ripples.map((ripple) => (
            <span
              key={ripple.id}
              className="ripple"
              style={{
                left: ripple.x,
                top: ripple.y,
                width: ripple.size,
                height: ripple.size
              }}
            />
          ))}
        </span>
      ))}
    </div>
  )
}

export default MenuBar