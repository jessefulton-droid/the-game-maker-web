# Deployment Guide - Render

This guide will help you deploy The Game Maker to Render.

## Prerequisites

1. A Render account (free tier works great!)
2. Your Anthropic API key
3. Git repository (GitHub, GitLab, or Bitbucket)

## Quick Deploy to Render

### Option 1: Automatic Deploy (Recommended)

1. **Push to Git Repository**
   ```bash
   cd the-game-maker-web
   git init
   git add .
   git commit -m "Initial commit - The Game Maker v2.0"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Connect to Render**
   - Go to [https://render.com](https://render.com)
   - Click "New +" → "Blueprint"
   - Connect your Git repository
   - Render will automatically detect `render.yaml`

3. **Set Environment Variables**
   - Render will prompt you to set `ANTHROPIC_API_KEY`
   - Add your API key
   - All other env vars are auto-configured!

4. **Deploy!**
   - Click "Apply"
   - Wait 5-10 minutes for initial build
   - Your app will be live at `https://the-game-maker.onrender.com`

### Option 2: Manual Web Service Deploy

If you prefer manual setup:

1. **Create Web Service**
   - Dashboard → "New +" → "Web Service"
   - Connect your repository

2. **Configure Build**
   - **Name**: `the-game-maker`
   - **Runtime**: Python 3
   - **Build Command**:
     ```bash
     pip install --upgrade pip && pip install -r backend/requirements.txt
     ```
   - **Start Command**:
     ```bash
     gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --chdir backend app:app
     ```

3. **Set Environment Variables**
   In the "Environment" tab, add:
   - `ANTHROPIC_API_KEY` = your API key
   - `FLASK_ENV` = production
   - `SECRET_KEY` = (generate a random secure string)
   - `PYTHON_VERSION` = 3.11.0

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment

## Environment Variables Explained

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | ✅ Yes | Your Anthropic (Claude) API key |
| `FLASK_ENV` | No | Set to `production` for production |
| `SECRET_KEY` | ✅ Yes | Secret key for session encryption |
| `SESSION_TYPE` | No | Session storage type (default: filesystem) |
| `LOG_LEVEL` | No | Logging level (default: INFO) |
| `PYTHON_VERSION` | No | Python version (default: 3.11.0) |

## Post-Deployment Configuration

### 1. Custom Domain (Optional)

- Go to Settings → Custom Domain
- Add your domain: `gameMaker.yourdomain.com`
- Update DNS records as instructed

### 2. Auto-Deploy on Push

- Enabled by default with Blueprint deploy
- Every git push to `main` will auto-deploy

### 3. Monitoring

Render provides built-in monitoring:
- CPU usage
- Memory usage
- Request logs
- Health check status

Access via: Dashboard → Your Service → Metrics

## Testing Your Deployment

1. **Health Check**
   ```bash
   curl https://your-app.onrender.com/api/health
   # Should return: {"status":"healthy","service":"the-game-maker","version":"2.0"}
   ```

2. **Start a Session**
   ```bash
   curl -X POST https://your-app.onrender.com/api/start_session \
     -H "Content-Type: application/json"
   # Should return session data
   ```

3. **Open in Browser**
   - Navigate to `https://your-app.onrender.com`
   - You should see the chat interface
   - Try the voice input!

## Troubleshooting

### Build Fails

**Issue**: Dependencies won't install
```bash
# Check requirements.txt syntax
# Ensure all packages are available on PyPI
# Check Python version compatibility
```

**Solution**: Review build logs in Render dashboard

### App Won't Start

**Issue**: Gunicorn fails to start
```bash
# Check that app.py is in backend/ directory
# Verify gunicorn is in requirements.txt
```

**Solution**: Check logs for specific error

### API Key Issues

**Issue**: "ANTHROPIC_API_KEY not set"
- Go to Environment tab
- Add the variable
- Redeploy (or Render will auto-restart)

### Session Errors

**Issue**: Sessions not persisting
- This is expected on free tier (restarts daily)
- For production, consider Redis for sessions

## Free Tier Limitations

Render Free Tier includes:
- ✅ 750 hours/month (enough for one service)
- ✅ Automatic SSL
- ✅ Custom domains
- ⚠️ Spins down after 15 minutes of inactivity
- ⚠️ 512MB RAM
- ⚠️ Slower CPU

**First request after spin-down**: ~30-60 seconds to wake up

## Upgrading to Paid Tier

For production use, consider:
- **Starter Plan** ($7/month)
  - Always on (no spin-down)
  - More CPU/RAM
  - Faster builds

## Production Optimizations

### 1. Enable Compression

In `app.py`, add Flask-Compress:
```python
from flask_compress import Compress
Compress(app)
```

### 2. Add Rate Limiting

Install Flask-Limiter:
```bash
pip install flask-limiter
```

### 3. Use Redis for Sessions

For multi-instance deployments:
```python
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis_url
```

### 4. Add Monitoring

Integrate with services like:
- Sentry (error tracking)
- LogTail (log aggregation)
- Better Uptime (monitoring)

## Scaling

When your app grows:

1. **Horizontal Scaling**
   - Increase instances in render.yaml
   - Requires paid plan

2. **Vertical Scaling**
   - Upgrade to higher plan
   - More RAM/CPU per instance

3. **Add Services**
   - Separate Redis service
   - Background workers for game generation
   - CDN for static assets

## Backup & Recovery

Render handles infrastructure, but you should:
- Keep Git repository as source of truth
- Back up environment variables
- Document any manual configurations

## Security Checklist

Before going live:
- [ ] ANTHROPIC_API_KEY is set and secure
- [ ] SECRET_KEY is random and strong
- [ ] HTTPS is enabled (automatic on Render)
- [ ] CORS is configured for your domain
- [ ] Rate limiting is enabled
- [ ] Input validation is in place

## Cost Estimation

**Free Tier**: $0/month
- Perfect for personal use, demos, portfolio

**Starter**: $7/month
- Good for low-traffic production
- ~100-1000 users/month

**Standard**: $25/month+
- Production with consistent traffic
- Multiple instances
- Background workers

## Support & Resources

- **Render Docs**: https://render.com/docs
- **Render Community**: https://community.render.com
- **This Project**: See README.md for detailed docs

## Next Steps

After deployment:
1. Test all features thoroughly
2. Share the URL with users!
3. Monitor logs for any issues
4. Consider adding analytics
5. Iterate based on feedback

---

## Quick Reference Commands

```bash
# Check deployment status
render services list

# View logs
render logs the-game-maker

# Trigger manual deploy
render deploy the-game-maker

# SSH into service (paid plans)
render shell the-game-maker
```

---

**Congratulations!** 🎉

Your Game Maker is now live on the internet!

Share your URL and let people create games from their favorite books!

---

*Last Updated: October 17, 2025*  
*Deployment Platform: Render*  
*Version: 2.0*

