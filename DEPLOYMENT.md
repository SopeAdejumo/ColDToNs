# ColDToNs Deployment Guide

This guide explains how to deploy ColDToNs as a single web service on Render.

## Architecture Overview

ColDToNs is now configured as a unified web application where:
- The Flask backend serves both the API endpoints and the built React frontend
- The React frontend is built during deployment and served as static files
- All requests are handled by a single web service

## Prerequisites

- A GitHub repository containing your ColDToNs code
- A Render account (free tier available)
- Node.js 18+ and Python 3.8+ (handled automatically by Render)

## Deployment Steps

### 1. Prepare Your Repository

Ensure your repository has the following structure:
```
ColDToNs/
├── backend/
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── vite.config.js
│   └── ...
├── package.json
├── build.sh
├── start.sh
├── Procfile
└── DEPLOYMENT.md
```

### 2. Deploy to Render

1. **Connect Your Repository**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" and select "Web Service"
   - Connect your GitHub repository
   - Select the ColDToNs repository

2. **Configure the Web Service**
   - **Name**: `coldtons` (or your preferred name)
   - **Environment**: `Python 3`
   - **Region**: Choose the closest to your users
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: Leave empty (uses repository root)
   - **Build Command**: `./build.sh`
   - **Start Command**: `./start.sh`

3. **Environment Variables** (Optional)
   - `PORT`: Automatically set by Render
   - `PYTHON_VERSION`: `3.11.0` (or your preferred version)
   - `NODE_VERSION`: `18.17.0` (or your preferred version)

4. **Advanced Settings**
   - **Auto-Deploy**: Enable for automatic deployments on git push
   - **Health Check Path**: `/api/health`

### 3. Deploy

1. Click "Create Web Service"
2. Render will automatically:
   - Install Node.js dependencies
   - Build the React frontend
   - Install Python dependencies
   - Start the Flask application with Gunicorn

### 4. Access Your Application

Once deployed, your application will be available at:
`https://your-service-name.onrender.com`

## Local Development

### Prerequisites
- Node.js 18+
- Python 3.8+
- pip

### Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd ColDToNs

# Install frontend dependencies
cd frontend
npm install
cd ..

# Install backend dependencies
cd backend
pip install -r requirements.txt
cd ..
```

### Development Mode
```bash
# Option 1: Run both frontend and backend separately
# Terminal 1 - Backend
cd backend
python main.py

# Terminal 2 - Frontend (in development mode with proxy)
cd frontend
npm run dev

# Option 2: Run both with concurrently (requires npm install in root)
npm install
npm run dev
```

### Production Build (Local Testing)
```bash
# Build frontend
cd frontend
npm run build
cd ..

# Start backend (serves built frontend)
cd backend
python main.py
```

## Troubleshooting

### Common Issues

1. **Build Fails**
   - Check that `build.sh` has execute permissions
   - Verify Node.js and Python versions in Render settings
   - Check build logs for specific error messages

2. **Application Won't Start**
   - Verify `start.sh` has execute permissions
   - Check that all dependencies are listed in `requirements.txt`
   - Review application logs in Render dashboard

3. **Static Files Not Loading**
   - Ensure frontend build completed successfully
   - Check that `dist` folder exists in `frontend/` after build
   - Verify Flask static folder configuration in `main.py`

4. **API Endpoints Not Working**
   - Check that API routes are prefixed with `/api/`
   - Verify CORS configuration if needed
   - Test API endpoints directly: `https://your-app.onrender.com/api/health`

### Logs and Monitoring

- **Build Logs**: Available during deployment in Render dashboard
- **Application Logs**: Real-time logs in Render dashboard
- **Health Check**: Monitor at `/api/health` endpoint

## Performance Considerations

### Render Free Tier Limitations
- Services spin down after 15 minutes of inactivity
- 750 hours per month (sufficient for most use cases)
- Cold start time: 10-30 seconds

### Optimization Tips
1. **Keep Services Warm**: Use a service like UptimeRobot to ping your app
2. **Optimize Build**: Remove unnecessary dependencies
3. **Static Assets**: Consider using a CDN for large assets
4. **Database**: Use Render's PostgreSQL for persistent data

## Scaling

### Upgrading from Free Tier
- **Starter Plan**: $7/month, no sleep, faster builds
- **Standard Plan**: $25/month, more resources, better performance

### Horizontal Scaling
- Increase worker count in Gunicorn configuration
- Use Render's load balancing for multiple instances

## Security

### Environment Variables
Store sensitive data as environment variables in Render:
- Database URLs
- API keys
- Secret keys

### HTTPS
- Automatically provided by Render
- Custom domains supported with SSL certificates

## Monitoring and Maintenance

### Health Checks
The application includes a health check endpoint at `/api/health` that returns:
```json
{
  "status": "healthy",
  "message": "ColDToNs API is running"
}
```

### Updates
1. Push changes to your connected GitHub repository
2. Render will automatically rebuild and deploy (if auto-deploy is enabled)
3. Monitor deployment logs for any issues

## Support

For deployment issues:
- Check Render's [documentation](https://render.com/docs)
- Review application logs in Render dashboard
- Test locally first to isolate deployment-specific issues

For application issues:
- Check the main README.md for application-specific documentation
- Review API endpoints and frontend functionality