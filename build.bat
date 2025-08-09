@echo off
echo Starting ColDToNs build process...

echo Installing frontend dependencies...
cd frontend
call npm ci
if %errorlevel% neq 0 exit /b %errorlevel%

echo Building frontend...
call npm run build
if %errorlevel% neq 0 exit /b %errorlevel%

echo Frontend build completed!

cd ..

echo Installing Python dependencies...
pip install -r backend/requirements.txt
if %errorlevel% neq 0 exit /b %errorlevel%

echo Build process completed successfully!