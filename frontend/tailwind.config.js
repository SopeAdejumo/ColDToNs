/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        'dark': {
          'bg': '#1a1a1a',
          'surface': '#2d2d2d',
          'border': '#404040',
          'text': '#e5e5e5',
          'text-muted': '#a3a3a3'
        },
        'accent': {
          'blue': '#3b82f6',
          'green': '#10b981',
          'purple': '#8b5cf6',
          'orange': '#f59e0b',
          'red': '#ef4444'
        }
      }
    }
  },
  plugins: []
}