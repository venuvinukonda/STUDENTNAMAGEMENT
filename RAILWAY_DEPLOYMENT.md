# Deploying Student Management System to Railway

Railway is the **easiest way to deploy Django applications**. It auto-detects Python projects and handles PostgreSQL setup automatically.

---

## ✅ Prerequisites

- [x] GitHub repository created (already done ✓)
- [x] Railway account (free tier available)
- [x] All code pushed to GitHub

---

## 🚀 Step-by-Step Deployment

### Step 1: Sign Up on Railway

1. Go to [railway.app](https://railway.app)
2. Click **"Start Project"**
3. Sign up with GitHub (recommended - simpler auth)
4. Authorize Railway to access your GitHub account

---

### Step 2: Create New Project

1. Click **"Create New Project"** in Railway dashboard
2. Select **"Deploy from GitHub repo"**
3. Select your repository: `venuvinukonda/STUDENTNAMAGEMENT`
4. Click **"Deploy"**

Railway will auto-detect Django and start building! 🎉

---

### Step 3: Add PostgreSQL Database

1. In Railway project dashboard, click **"+ New Service"**
2. Click **"Database"** → **"PostgreSQL"**
3. Railway will create PostgreSQL and automatically set `DATABASE_URL` environment variable ✓

---

### Step 4: Configure Environment Variables

Railway auto-sets `DATABASE_URL`. You need to add:

1. In Railway dashboard, go to **Variables** tab
2. Click **"New Variable"** and add:

| Variable | Value |
|----------|-------|
| `DEBUG` | `False` |
| `SECRET_KEY` | Generate one: `python manage.py shell` → `from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())` |
| `ALLOWED_HOSTS` | Your Railway domain (gets auto-generated, e.g., `student-management-production-abcd.up.railway.app`) |

**Finding your Railway domain:**
1. Go to **Deployments** tab
2. Look for "Railway Custom Domain" or "Public URL"
3. Copy that domain and add to `ALLOWED_HOSTS` variable

---

### Step 5: Update SECRET_KEY

Generate a secure secret key:

```bash
python manage.py shell
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Copy the output and paste it in Railway's `SECRET_KEY` environment variable.

---

### Step 6: Run Database Migrations

Railway automatically runs commands in `Procfile` release phase, which includes:
```
release: python manage.py migrate
```

This runs automatically on each deployment! ✓

---

### Step 7: Create Superuser (Admin Account)

After first deployment, run the admin creation command:

1. In Railway dashboard, click on the **"Web Service"**
2. Go to **"Logs"** tab to view deployment logs
3. Once deployment is successful, you need to SSH into the app

**Via Railway CLI (easiest):**

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Connect to your project
railway link

# Run migrations and create superuser
railway run python manage.py migrate
railway run python manage.py createsuperuser
```

Follow the prompts to create admin account.

---

### Step 8: Verify Deployment

1. Go to Railway dashboard → **Deployments**
2. Click the **Public URL** link (usually something like `student-management-production-xxxx.up.railway.app`)
3. You should see your application! 🎉

---

## 📋 Deployment Checklist

- [ ] GitHub repository set up
- [ ] Railway project created
- [ ] PostgreSQL database added
- [ ] Environment variables configured:
  - [ ] `DEBUG=False`
  - [ ] `SECRET_KEY` set
  - [ ] `ALLOWED_HOSTS` set to your Railway domain
- [ ] Database migrations ran automatically
- [ ] Superuser created via `railway run`
- [ ] Application loads on public URL
- [ ] Admin panel accessible at `/admin/`
- [ ] All pages load with CSS styling

---

## 🔧 Troubleshooting

### Issue: "502 Bad Gateway"

**Solution:** Check logs:
```bash
railway logs
```

Common causes:
- `SECRET_KEY` not set
- `DEBUG=True` in production
- Database migrations not ran

### Issue: CSS/Static Files Not Loading

**Solution:** Already configured with WhiteNoise in `settings.py`:
- WhiteNoise middleware compresses and serves static files
- `STATICFILES_STORAGE` uses `CompressedManifestStaticFilesStorage`
- No need for `npm run build` - CSS loads from CDN

### Issue: Database Connection Error

**Solution:** Railway auto-sets `DATABASE_URL`. If still failing:
1. Verify PostgreSQL service is running in Railway dashboard
2. Check `DATABASE_URL` variable is set
3. Ensure URL format is correct: `postgresql://user:pass@host:port/dbname`

### Issue: Can't Create Superuser

```bash
# Try this:
railway run python manage.py shell
# Then in shell:
from django.contrib.auth.models import User
User.objects.create_superuser('admin', 'admin@example.com', 'password')
```

---

## 🌍 Custom Domain (Optional)

Rail already gives you a free `.up.railway.app` domain. To use custom domain:

1. Railway dashboard → **Settings**
2. Click **"Add Domain"**
3. Enter your domain (e.g., `studentmgmt.com`)
4. Follow DNS setup instructions for your domain provider

---

## 📊 Monitoring & Logs

**View real-time logs:**
```bash
railway logs
```

**View metrics (CPU, Memory, Disk):**
- Railway dashboard → **Metrics** tab

---

## 💾 Backup Database

Railway handles automatic daily backups for PostgreSQL. Access via:

1. Railway dashboard → PostgreSQL service
2. Click **"Backups"** tab
3. Download or restore backups

---

## 🔐 Security Best Practices

✅ **Already configured in `settings.py`:**
- HTTPS enforced (SECURE_SSL_REDIRECT = True)
- Secure cookies (SESSION_COOKIE_SECURE)
- HSTS enabled (HTTP Strict Transport Security)
- CSRF protection

✅ **Keep these safe:**
- Don't commit `.env` file
- Regenerate `SECRET_KEY` after deployment
- Use strong `ALLOWED_HOSTS`
- Enable 2FA on Railway account

---

## 📈 Performance Tips

1. **Use PostgreSQL** - Already set up ✓
2. **Enable caching** - Add Redis service in Railway for caching
3. **Compress assets** - WhiteNoise auto-compresses ✓
4. **Monitor performance** - Check Railway metrics regularly

---

## 💰 Cost Estimate (Railway Free Tier)

- **Web Service:** $5/month credit included
- **PostgreSQL:** $5/month credit included
- **Free tier:** $10/month included - Usually enough for dev/testing

For production scale, upgrade to paid plan.

---

## 🆘 Need Help?

- Railway Docs: https://docs.railway.app
- Django Deployment: https://docs.djangoproject.com/en/5.1/howto/deployment/
- Railway Discord: https://discord.gg/railway

---

**Your app is now ready for production! 🚀**
