#!/bin/bash

# Build script for Render deployment
echo "Starting ColDToNs build process..."

# Install Node.js dependencies and build frontend
echo "Installing frontend dependencies..."
cd frontend
npm ci

echo "Building frontend..."
npm run build

echo "Frontend build completed!"

# Go back to root directory
cd ..

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r backend/requirements.txt

echo "Build process completed successfully!"