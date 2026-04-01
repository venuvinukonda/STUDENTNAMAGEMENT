# Production Deployment Guide

## Pre-Deployment Checklist

### Backend Setup
- [ ] `DEBUG = False` in `settings.py`
- [ ] Update `ALLOWED_HOSTS` with your domain
- [ ] Set `SECRET_KEY` to a secure value
- [ ] Use PostgreSQL instead of SQLite
- [ ] Configure environment variables
- [ ] Run database migrations: `python manage.py migrate`
- [ ] Create superuser: `python manage.py createsuperuser`

### Frontend / CSS Setup
- [ ] Build Tailwind CSS: `npm run build:prod`
- [ ] Verify `static/css/output.css` is generated
- [ ] Run `python manage.py collectstatic`
- [ ] Test all pages for styling

### Security
- [ ] Set `CSRF_TRUSTED_ORIGINS`
- [ ] Enable `SECURE_SSL_REDIRECT = True`
- [ ] Set `SECURE_HSTS_SECONDS`
- [ ] Configure CORS if needed
- [ ] Use HTTPS only

---

## Step-by-Step Deployment

### 1. Prepare Django Settings

Create `settings_production.py`:

```python
from .settings import *

DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Database - PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', 5432),
    }
}

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = '/path/to/staticfiles'

# CloudFront or CDN
# STATIC_URL = 'https://cdn.example.com/static/'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = '/path/to/media'
```

### 2. Build Tailwind CSS for Production

```bash
npm run build:prod
```

This creates an optimized, minified `output.css`.

### 3. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 4. Run Migrations

```bash
python manage.py migrate --noinput
```

### 5. Set Environment Variables

Create `.env` file:
```
DEBUG=False
SECRET_KEY=your-very-long-secret-key
DB_ENGINE=django.db.backends.postgresql
DB_NAME=snapservice
DB_USER=db_user
DB_PASSWORD=secure_password
DB_HOST=db.example.com
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### 6. Use Gunicorn as WSGI Server

Install Gunicorn:
```bash
pip install gunicorn
```

Run with Gunicorn:
```bash
gunicorn SNAPSERVICE.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### 7. Setup Nginx as Reverse Proxy

Example `nginx.conf`:

```nginx
upstream snapservice {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL certificates
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;

    # Gzip compression
    gzip on;
    gzip_types text/css application/javascript application/json;

    # Proxy to Gunicorn
    location / {
        proxy_pass http://snapservice;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }

    # Static files
    location /static/ {
        alias /path/to/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /path/to/media/;
        expires 7d;
    }
}
```

### 8. Setup Systemd Service

Create `/etc/systemd/system/snapservice.service`:

```ini
[Unit]
Description=SNAPSERVICE Django Application
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/var/www/snapservice
ExecStart=/var/www/snapservice/venv/bin/gunicorn \
    --workers 4 \
    --bind unix:/var/www/snapservice/gunicorn.sock \
    SNAPSERVICE.wsgi:application
Restart=always
RestartSec=3
StandardOutput=journal
StandardError=journal
SyslogIdentifier=snapservice

[Install]
WantedBy=multi-user.target
```

Start service:
```bash
sudo systemctl start snapservice
sudo systemctl enable snapservice
```

### 9. Setup SSL with Let's Encrypt

```bash
sudo apt-get install certbot python3-certbot-nginx

sudo certbot certonly --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo systemctl enable certbot.timer
```

### 10. Database Backup

Schedule daily backups:

```bash
#!/bin/bash
# backup.sh
pg_dump -U db_user -h localhost snapservice | \
  gzip > /backups/snapservice_$(date +%Y-%m-%d).sql.gz

# Keep only last 30 days
find /backups -name "snapservice_*.sql.gz" -mtime +30 -delete
```

Add to crontab: `0 2 * * * /path/to/backup.sh`

---

## Docker Deployment (Optional)

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Install Node.js for Tailwind
FROM node:18-slim as node-builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY static/css/tailwind.css ./static/css/
RUN npm run build:prod

# Copy application
COPY . /app/

# Run Django
CMD ["gunicorn", "SNAPSERVICE.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: snapservice
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    command: >
      sh -c "python manage.py migrate &&
             python manage.py createsuperuser --noinput --username admin --email admin@example.com &&
             gunicorn SNAPSERVICE.wsgi:application --bind 0.0.0.0:8000"
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      DEBUG: false
      DATABASE_URL: postgresql://user:password@db:5432/snapservice

volumes:
  postgres_data:
```

Run with Docker:
```bash
docker-compose build
docker-compose up -d
```

---

## Performance Optimization

### Database
```python
# settings.py
DATABASES = {
    'default': {
        'CONN_MAX_AGE': 600,  # Connection pooling
        ...
    }
}
```

### Cache
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### Compression
```python
MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    ...
]
```

### Query Optimization
```python
# Use select_related() and prefetch_related()
students = Student.objects.select_related('program').all()
```

---

## Monitoring & Logging

### Application Logging
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/snapservice.log',
            'maxBytes': 1024*1024*10,
            'backupCount': 5,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },
}
```

### Error Tracking with Sentry

```bash
pip install sentry-sdk
```

```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.1,
)
```

---

## Monitoring Tools

- **Uptime**: Uptimerobot.com
- **Performance**: New Relic, DataDog
- **Error Tracking**: Sentry
- **Log Management**: ELK Stack, Splunk
- **Application**: PM2, Supervisor

---

## Maintenance

### Regular Tasks
- [ ] Monitor error logs
- [ ] Update dependencies: `pip list --outdated`
- [ ] Clean old sessions: `python manage.py clearsessions`
- [ ] Backup database daily
- [ ] Monitor disk space
- [ ] Check SSL certificate expiry

### Updates
```bash
# Update Django
pip install --upgrade Django

# Update all packages
pip install --upgrade -r requirements.txt

# Update Tailwind
npm update
npm run build:prod
```

---

## Troubleshooting

**Static files not loading:**
```bash
python manage.py collectstatic --clear --noinput
```

**Database connection issues:**
```bash
python manage.py dbshell
```

**Permission denied on static files:**
```bash
sudo chown -R www-data:www-data /var/www/snapservice/staticfiles
```

---

## Resources

- Django Deployment: https://docs.djangoproject.com/en/stable/howto/deployment/
- Gunicorn: https://gunicorn.org/
- Nginx: https://nginx.org/
- Docker: https://www.docker.com/

---

**Ready for production!** 🚀
