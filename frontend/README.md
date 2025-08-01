# ColDToNs Frontend

This is the frontend interface for the ColDToNs (Collection of Data and Tools for Neutron Stars) application.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Build the CSS (one-time):
```bash
npm run build
```

3. For development with auto-rebuild on changes:
```bash
npm run dev
```

## Project Structure

```
frontend/
├── src/
│   └── input.css          # Tailwind CSS source file
├── dist/
│   └── output.css         # Generated CSS file (do not edit)
├── index.html             # Main HTML file
├── package.json           # Node.js dependencies and scripts
└── tailwind.config.js     # Tailwind CSS configuration
```

## Available Scripts

- `npm run build-css` - Build CSS from source
- `npm run watch-css` - Watch for changes and rebuild CSS automatically
- `npm run build` - Alias for build-css
- `npm run dev` - Alias for watch-css

## Styling

The project uses Tailwind CSS with custom color themes for the neutron star research interface. All custom styles are defined in `src/input.css` and compiled to `dist/output.css`.

## Opening the Application

Simply open `index.html` in your web browser. The styling will work offline since Tailwind CSS is now installed locally.