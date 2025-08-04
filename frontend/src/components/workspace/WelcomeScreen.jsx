const WelcomeScreen = () => {
  return (
    <div className="h-full flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-100 mb-4">ColDToNs</h1>
        <p className="text-gray-300 text-lg mb-2">
          Collection of Data and Tools for Neutron Stars
        </p>
        <p className="text-gray-400 text-sm mb-8 max-w-2xl mx-auto">
          A unified toolkit for the study and visualization of neutron star
          data. Designed for both amateur astronomers and professional
          astrophysicists to democratize access to cutting-edge research.
        </p>
        <div className="text-gray-500 text-sm">
          Select a menu item above to get started
        </div>
      </div>
    </div>
  )
}

export default WelcomeScreen