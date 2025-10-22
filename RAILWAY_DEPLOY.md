# Railway Deployment Guide (Recommended)

Railway is the **recommended platform** for deploying this Flask application because it supports:
- ✅ Persistent filesystem (SQLite works perfectly)
- ✅ Global state (traditional server architecture)
- ✅ File uploads and storage
- ✅ Simple deployment process
- ✅ Free tier available

## Quick Deploy to Railway

### Option 1: One-Click Deploy (Easiest)

1. Click this button: [![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/new)

2. Or visit: https://railway.app/new

3. Select "Deploy from GitHub repo"

4. Choose `VerifiedError/vault_audit_redone`

5. Railway will automatically:
   - Detect it's a Python project
   - Install dependencies from `requirements.txt`
   - Start the Flask application

### Option 2: CLI Deploy

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login to Railway
railway login

# Link to your project (or create new)
railway link

# Deploy
railway up

# Get the deployment URL
railway domain
```

## Configuration

Railway should auto-detect everything, but you can create a `railway.json` if needed:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "cd vault_audit && python app.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

Or use a `Procfile`:

```
web: cd vault_audit && python app.py
```

## Environment Variables

No environment variables needed for basic deployment. The app runs on port 5000 by default.

If you want to customize:

```bash
# Set Flask environment
railway variables set FLASK_ENV=production

# Set port (Railway uses $PORT automatically)
railway variables set PORT=5000
```

## Database Persistence

Railway provides **persistent storage** by default:
- SQLite database will persist across deployments
- Uploaded files remain available
- No configuration needed

## Monitoring

Access your deployment:

```bash
# View logs
railway logs

# Open in browser
railway open
```

## Custom Domain

1. Go to your Railway project dashboard
2. Click "Settings"
3. Add your custom domain
4. Update DNS records as instructed

## Cost

- **Free Tier**: $5 free credits per month
- Perfect for development and small production apps
- Sufficient for most small-to-medium traffic

## Troubleshooting

### App won't start

Check logs:
```bash
railway logs
```

Ensure start command is correct in Railway dashboard:
```
cd vault_audit && python app.py
```

### Database resets

If using the wrong storage, ensure you're using Railway's persistent volume.

### Port issues

Flask should bind to `0.0.0.0:5000`. Update `app.py` if needed:

```python
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

## Next Steps

After deployment:
1. Visit your Railway URL
2. Upload a container Excel file
3. Start scanning labels
4. Export reports

Your database and uploads will persist across deployments!
