#!/bin/bash

# Start script for Render deployment
echo "Starting ColDToNs application..."

# Change to backend directory and start the Flask app with Gunicorn
cd backend
exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 0 main:app