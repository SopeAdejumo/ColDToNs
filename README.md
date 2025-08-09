# ColDToNs (Collection of Data and Tools for Neutron Stars)
ColDToNs is a unified toolkit for the study and visualization of neutron star data. It combines several existing powerful scientific tools and libraries into one user-friendly, cross-platform web application. Designed for both amateur astronomers and professional astrophysicists, ColDToNs aims to democratize access to cutting-edge research and enhance the understanding of these extreme cosmic objects.

### Find the live prototype here: [https://coldtons.onrender.com](https://coldtons.onrender.com)

## 🚀 Quick Start

### Local Development
```bash
# Install dependencies
npm run install-deps

# Build frontend
npm run build-frontend

# Start the application
npm start
```

For development mode with hot reloading:
```bash
# Terminal 1 - Backend
npm run dev-backend

# Terminal 2 - Frontend
npm run dev-frontend
```
## Functions
The toolkit's functionalities are organized to provide a comprehensive suite of tools for exploring, analyzing, and visualizing neutron stars.

### Neutron Star Database and Catalog Browser
A searchable, filterable database of known neutron stars (pulsars, X-ray binaries, isolated neutron stars). Users can search by name, coordinates, or other parameters, and view properties such as mass, radius, magnetic field strength, spin period, spin-down rate, flux, and associated binary parameters. Data can be downloaded in various formats.

### Equation of State Library
A collection of reputable equations of state (EoS) that describe how the density and pressure of neutron stars vary under extreme conditions. These EoSs are fundamental inputs for various calculations performed within the toolkit.

### Neutron Star Property Calculator
Given a neutron star's mass and an Equation of State selected from the integrated library, this function calculates fundamental inferred properties such as the star's radius, average density, moment of inertia, surface gravity, and escape velocity.

### Light Curve and Spectra Plotter
Visualizes generic light curves (intensity as a function of time) and spectra (intensity as a function of energy or wavelength) for different neutron star phenomena (e.g., idealized pulsar pulses, X-ray burst profiles, thermal emission spectra). Future versions may allow users to upload and plot their own basic observational data.

### Pulsar Timing and Ephemeris Viewer
Displays current ephemerides (precise spin period, spin-down rate, sky position) for selected pulsars. Users can input a specific date and time to calculate the expected pulse phase, useful for planning observations or understanding timing data.

### Mass-Radius Relation Plotter
Plots the Mass-Radius (M-R) relations for various theoretical equations of state. It allows the user to overlay real observational constraints (e.g., inferred M-R contours from NICER observations, tidal deformability limits from gravitational wave events like GW170817) to assess which EoS models are consistent with current data.

### Pulsar Dispersion and Faraday Rotation Calculator
Calculates the effects of the interstellar medium on pulsar signals, specifically Dispersion Measure (DM) and Faraday Rotation Measure (RM). Users can input observed DM/RM values to estimate average electron density or magnetic field strength along the line of sight to a pulsar.

### Interactive 3D Conceptual Neutron Star Modeler
Provides an interactive 3D visualization of a conceptual neutron star. Users can rotate, zoom, and toggle illustrative elements such as jets, magnetic field lines, inferred surface hot spots (from X-ray data), or a simplified cross-section showing internal layers.

### X-ray Pulse Profile Modeler (Simplified Forward Model)
Allows users to input basic neutron star parameters (mass, radius, spin, assumed hotspot size/location) and simulate a simplified X-ray pulse profile. This demonstrates the effects of strong gravity (light bending) and relativistic Doppler boosting on the observed signal.

### Gravitational Waveform Viewer (Binary Neutron Star Mergers)
Displays pre-computed gravitational waveform templates from binary neutron star inspirals and mergers. Users can adjust parameters like component masses, spins, and viewing angle to observe how these affect the waveform's morphology. An option to "audify" the waveform may be included.

### Numerical Relativity Simulation Playback
Enables loading and interactive playback of pre-rendered animations or 3D volumetric datasets from numerical relativity simulations of binary neutron star mergers. Users can explore the evolution of density, temperature, or magnetic fields in 3D spacetime.

### Custom EoS Input & TOV Solver
Designed for advanced users, this function allows the input of custom Equation of State (EoS) data (e.g., a table of pressure vs. density). The toolkit then uses a built-in Tolman-Oppenheimer-Volkoff (TOV) solver to compute and display the corresponding mass-radius curve and other stellar properties for that custom EoS.

### Data Sharing & Collaboration Features
Allows users to securely save their analysis sessions, share generated plots or models with other users, or potentially collaborate on specific projects (e.g., shared EoS parameter sets, comparative analysis results). This feature would leverage cloud storage.

## Documentation of tools

### Searchable Neutron Star Database
This tool makes use of the ATNF Pulsar Catalogue, and the psrqpy Python package to query it. It provides a simple interface where you can enter keywords or filters to find information about neutron stars, seaarching them based on names or coordinates, as well as various parameters.

"The ATNF Pulsar Catalogue," by Manchester et al. (2005)  at https://www.atnf.csiro.au/research/pulsar/psrcat/