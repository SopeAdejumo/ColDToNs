# ColDToNs Deployment Checklist

Use this checklist to ensure your ColDToNs application is ready for deployment to Render.

## Pre-Deployment Checklist

### ✅ Repository Setup
- [ ] All code is committed to your Git repository
- [ ] Repository is pushed to GitHub/GitLab/Bitbucket
- [ ] Repository is public or you have connected your Git provider to Render
- [ ] `.gitignore` file excludes `node_modules/`, `frontend/dist/`, and other build artifacts

### ✅ Project Structure
- [ ] `package.json` exists in root directory
- [ ] `build.sh` and `start.sh` scripts exist and are executable
- [ ] `Procfile` exists for alternative deployment methods
- [ ] `DEPLOYMENT.md` documentation is complete
- [ ] `backend/main.py` contains the Flask application
- [ ] `backend/requirements.txt` lists all Python dependencies
- [ ] `frontend/package.json` contains all Node.js dependencies
- [ ] `frontend/vite.config.js` is configured for production builds

### ✅ Code Configuration
- [ ] Flask app is configured to serve static files from `../frontend/dist`
- [ ] Flask routes handle both API endpoints (`/api/*`) and frontend routing
- [ ] CORS is properly configured for production
- [ ] Environment variables are used for configuration (PORT, etc.)
- [ ] No hardcoded localhost URLs in production code

### ✅ Dependencies
- [ ] All Python dependencies are listed in `backend/requirements.txt`
- [ ] All Node.js dependencies are listed in `frontend/package.json`
- [ ] Dependency versions are pinned or use compatible ranges
- [ ] No development-only dependencies in production requirements

### ✅ Build Process
- [ ] `build.sh` script installs frontend dependencies
- [ ] `build.sh` script builds the frontend successfully
- [ ] `build.sh` script installs Python dependencies
- [ ] Frontend build outputs to `frontend/dist/` directory
- [ ] Build process completes without errors locally

### ✅ Testing
- [ ] Run `python test-build.py` and all tests pass
- [ ] Frontend builds successfully with `npm run build`
- [ ] Backend starts successfully and serves static files
- [ ] API endpoints respond correctly
- [ ] Health check endpoint (`/api/health`) works
- [ ] Application works when accessing built version locally

## Render Deployment Steps

### 1. Create Web Service
- [ ] Log into [Render Dashboard](https://dashboard.render.com/)
- [ ] Click "New +" → "Web Service"
- [ ] Connect your Git repository
- [ ] Select the ColDToNs repository

### 2. Configure Service Settings
- [ ] **Name**: Choose a unique service name (e.g., `coldtons-app`)
- [ ] **Environment**: Python 3
- [ ] **Region**: Select appropriate region
- [ ] **Branch**: `main` or your default branch
- [ ] **Root Directory**: Leave empty (uses repository root)
- [ ] **Build Command**: `./build.sh`
- [ ] **Start Command**: `./start.sh`

### 3. Environment Variables (if needed)
- [ ] Set `PYTHON_VERSION` if you need a specific version
- [ ] Set `NODE_VERSION` if you need a specific version
- [ ] Add any application-specific environment variables

### 4. Advanced Settings
- [ ] **Auto-Deploy**: Enable for automatic deployments
- [ ] **Health Check Path**: `/api/health`
- [ ] **Instance Type**: Start with free tier, upgrade if needed

### 5. Deploy
- [ ] Click "Create Web Service"
- [ ] Monitor build logs for any errors
- [ ] Wait for deployment to complete (usually 5-15 minutes)

## Post-Deployment Verification

### ✅ Basic Functionality
- [ ] Application loads at your Render URL
- [ ] Frontend interface displays correctly
- [ ] No console errors in browser developer tools
- [ ] Health check endpoint responds: `https://your-app.onrender.com/api/health`

### ✅ API Testing
- [ ] Menu configuration loads: `/api/menu-config`
- [ ] ATNF parameters load: `/api/atnf-parameters`
- [ ] ADTN catalog search works: `/api/tools/adtn-catalog/data`
- [ ] File download functionality works: `/api/tools/adtn-catalog/download`

### ✅ Frontend Features
- [ ] Menu navigation works
- [ ] Sidebar tools display correctly
- [ ] Workspace components load
- [ ] ADTN Catalog tool functions properly
- [ ] Data can be searched and filtered
- [ ] Data can be downloaded in different formats

### ✅ Performance
- [ ] Initial page load is reasonable (< 10 seconds on free tier)
- [ ] API responses are timely
- [ ] No memory or timeout errors in logs

## Troubleshooting Common Issues

### Build Failures
- [ ] Check build logs in Render dashboard
- [ ] Verify all dependencies are correctly specified
- [ ] Ensure build scripts have proper permissions
- [ ] Test build process locally first

### Runtime Errors
- [ ] Check application logs in Render dashboard
- [ ] Verify environment variables are set correctly
- [ ] Check that all required files are in the repository
- [ ] Test the start command locally

### Static File Issues
- [ ] Verify frontend build completed successfully
- [ ] Check that `frontend/dist/` directory exists after build
- [ ] Ensure Flask static folder configuration is correct
- [ ] Test static file serving locally

### API Issues
- [ ] Verify API routes are correctly prefixed with `/api/`
- [ ] Check CORS configuration
- [ ] Test API endpoints directly with curl or Postman
- [ ] Review Flask application logs

## Maintenance

### Regular Tasks
- [ ] Monitor application logs for errors
- [ ] Check health endpoint periodically
- [ ] Update dependencies regularly
- [ ] Monitor resource usage and performance

### Updates
- [ ] Test changes locally before deploying
- [ ] Use feature branches for major changes
- [ ] Monitor deployment logs after updates
- [ ] Have a rollback plan for critical issues

## Performance Optimization

### Free Tier Considerations
- [ ] Service will sleep after 15 minutes of inactivity
- [ ] Cold starts take 10-30 seconds
- [ ] 750 hours per month limit

### Optimization Strategies
- [ ] Use UptimeRobot or similar to keep service warm
- [ ] Optimize frontend bundle size
- [ ] Implement caching where appropriate
- [ ] Consider upgrading to paid tier for better performance

## Security

### Best Practices
- [ ] Use environment variables for sensitive data
- [ ] Keep dependencies updated
- [ ] Use HTTPS (automatically provided by Render)
- [ ] Implement proper error handling
- [ ] Don't expose sensitive information in logs

---

## Quick Reference

### Useful URLs
- **Render Dashboard**: https://dashboard.render.com/
- **Your App**: `https://your-service-name.onrender.com`
- **Health Check**: `https://your-service-name.onrender.com/api/health`

### Useful Commands
```bash
# Test build locally
python test-build.py

# Setup development environment
python setup.py

# Build frontend only
cd frontend && npm run build

# Start backend only
cd backend && python main.py

# View logs (if using Render CLI)
render logs your-service-name
```

### Support Resources
- [Render Documentation](https://render.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)