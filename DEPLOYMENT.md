# Deployment Guide

## ⚠️ IMPORTANT: Vercel Limitations

This Flask application has **significant limitations** when deployed to Vercel:

### Issues with Vercel

1. **Ephemeral Filesystem**:
   - SQLite database will **NOT persist** across deployments
   - Uploaded files will be **lost** when the serverless function restarts
   - Database resets on every deployment

2. **Global State**:
   - Flask app uses global variables (`container_data`, `auditor`, `last_audit_result`)
   - Serverless architecture doesn't support persistent global state
   - Each request may hit a different serverless instance

3. **File Storage**:
   - `uploads/` and `exports/` directories won't persist
   - Files uploaded will disappear after serverless function terminates

### Recommended Hosting Alternatives

For this application, consider these platforms instead:

#### 1. **Railway** (Recommended)
```bash
# Install Railway CLI
npm i -g @railway/cli

# Deploy
railway login
railway init
railway up
```
- Persistent filesystem
- SQLite works perfectly
- Easy deployment
- Free tier available

#### 2. **Render**
- Create a new Web Service
- Connect your GitHub repository
- Set build command: `pip install -r requirements.txt`
- Set start command: `cd vault_audit && python app.py`
- Add persistent disk for database

#### 3. **PythonAnywhere**
- Upload code via web interface or git
- Configure WSGI file
- Perfect for Flask + SQLite
- Free tier available

#### 4. **Traditional VPS** (DigitalOcean, Linode, AWS EC2)
- Full control
- Persistent storage
- Install Python, run Flask
- Use systemd or supervisor for process management

## If You Must Use Vercel

You would need to make these changes:

1. **Replace SQLite** with a cloud database:
   - PostgreSQL (Supabase, Neon, Railway)
   - MySQL (PlanetScale)
   - MongoDB (Atlas)

2. **Replace File Storage** with cloud storage:
   - AWS S3
   - Cloudflare R2
   - Vercel Blob Storage

3. **Remove Global State**:
   - Store session data in database
   - Use JWT tokens for state
   - Implement stateless architecture

This would require **significant refactoring** of the codebase.

## Quick Start for Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
start.bat  # Windows
# OR
cd vault_audit && python app.py
```

Visit `http://localhost:5000`

## Current Deployment Status

- ✅ GitHub: Ready to push
- ⚠️ Vercel: Not recommended (see above)
- ✅ Railway: Recommended
- ✅ Render: Recommended
- ✅ PythonAnywhere: Recommended
