@echo off
echo Starting ColDToNs application...

cd backend
if not defined PORT set PORT=5000
python main.py