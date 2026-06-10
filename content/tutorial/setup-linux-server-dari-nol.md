---
title: "Setup Linux Server dari Nol untuk Web App"
date: 2026-05-03
draft: false
slug: "setup-linux-server-dari-nol"
description: "Tutorial setup Linux server production-ready. Dari SSH setup, Nginx, SSL, firewall, sampai monitoring."
categories: [Tutorial]
tags: ['linux', 'server', 'devops', 'nginx', 'ubuntu', 'web-app']
ShowShareLinks: true
ShowReadingTime: true
ShowToc: true
---

Jadi ceritanya, aku baru beli VPS murah ($5/bulan) dari DigitalOcean. Fresh Ubuntu server, kosong melompong. Gak ada Nginx, gak ada SSL, gak ada security setup.

Banyak yang gak tau cara setup server dari nol. Padahal gak serumit yang dibayangin. Di tutorial ini, aku bakal jelasin step-by-step dari fresh server sampai production-ready.

Yang bakal kamu dapet di akhir tutorial:
- Server aman dari serangan
- Nginx reverse proxy
- SSL gratis dari Let's Encrypt
- Auto-renew SSL
- UFW firewall
- Basic monitoring

## Prerequisites

- VPS dengan Ubuntu 22.04/24.04 (DigitalOcean, Vultr, AWS, dll)
- Domain name yang sudah pointing ke IP server
- Terminal/SSH client

## Step 1: SSH ke Server

Kalau baru beli VPS, biasanya kamu dikasih root password via email.

```bash
ssh root@your-server-ip
```

Atau kalau pakai SSH key:

```bash
ssh root@your-server-ip -i ~/.ssh/your-key.pem
```

## Step 2: Initial Server Setup

### Update system

```bash
sudo apt update && sudo apt upgrade -y
```

### Buat non-root user

**JANGAN pakai root untuk daily use!** Itu security risk besar.

```bash
# Buat user baru
adduser deploy

# Kasih sudo privileges
usermod -aG sudo deploy

# Copy SSH keys ke user baru (supaya bisa SSH tanpa password)
rsync --archive --chown=deploy:deploy ~/.ssh /home/deploy
```

Test login dengan user baru:

```bash
# Buka terminal baru
ssh deploy@your-server-ip
```

Kalau udah bisa login, lanjut.

### Set timezone

```bash
sudo timedatectl set-timezone Asia/Jakarta
```

### Setup hostname

```bash
sudo hostnamectl set-hostname my-server
```

Edit `/etc/hosts`:

```bash
sudo nano /etc/hosts
```

Tambahin:

```
127.0.0.1   localhost
127.0.1.1   my-server
```

## Step 3: Security Hardening

### Enable firewall (UFW)

```bash
# Pastikan UFW aktif
sudo ufw status

# Allow SSH (PENTING! Kalau gak, kamu bisa lock out sendiri)
sudo ufw allow OpenSSH

# Allow HTTP & HTTPS
sudo ufw allow 'Nginx Full'

# Enable firewall
sudo ufw enable
```

Output:

```
Firewall is active and enabled on system startup
Status: active

To                         Action      From
--                         ------      ----
OpenSSH                    ALLOW       Anywhere
Nginx Full                 ALLOW       Anywhere
```

### Setup SSH security

Edit `/etc/ssh/sshd_config`:

```bash
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak  # Backup dulu!
sudo nano /etc/ssh/sshd_config
```

Ubah setting ini:

```
# Disable root login
PermitRootLogin no

# Disable password auth (pakai SSH key only)
PasswordAuthentication no

# Change default port (opsional tapi recommended)
Port 2222

# Limit login attempts
MaxAuthTries 3

# Set idle timeout (10 menit)
ClientAliveInterval 300
ClientAliveCountMax 2
```

Kalau ganti port SSH, jangan lupa update UFW:

```bash
sudo ufw allow 2222/tcp
sudo ufw reload
```

Restart SSH:

```bash
sudo systemctl restart sshd
```

### Install Fail2ban (anti brute force)

```bash
sudo apt install fail2ban -y

# Buat config lokal
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo nano /etc/fail2ban/jail.local
```

Config:

```ini
[DEFAULT]
bantime = 3600    # Ban 1 jam
findtime = 600    # Deteksi dalam 10 menit
maxretry = 5      # Max 5 gagal login

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
```

```bash
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

## Step 4: Install Nginx

```bash
sudo apt install nginx -y

# Enable dan start
sudo systemctl enable nginx
sudo systemctl start nginx

# Test — buka browser, akses IP server
# Harus muncul "Welcome to nginx!" page
```

### Basic Nginx Config

```bash
sudo nano /etc/nginx/sites-available/myapp
```

Untuk Node.js app:

```nginx
server {
    listen 80;
    server_name myapp.com www.myapp.com;

    # Untuk static files
    location / {
        root /var/www/myapp/dist;
        try_files $uri $uri/ /index.html;  # SPA support
    }

    # Proxy ke Node.js
    location /api {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_cache_bypass $http_upgrade;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml text/javascript;
}
```

Untuk Python/Django:

```nginx
server {
    listen 80;
    server_name myapp.com;

    location /static/ {
        alias /var/www/myapp/static/;
    }

    location /media/ {
        alias /var/www/myapp/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default  # Hapus default
sudo nginx -t  # Test config
sudo systemctl reload nginx
```

## Step 5: SSL dengan Let's Encrypt (Gratis!)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx -y

# Dapatkan SSL certificate
sudo certbot --nginx -d myapp.com -d www.myapp.com

# Ikuti prompt:
# - Enter email (untuk notifikasi expiry)
# - Agree to terms
# - Share email (opsional)
# - Pilih redirect (pilih 2: redirect HTTP → HTTPS)
```

Selesai! SSL udah aktif dan auto-redirect HTTP → HTTPS.

### Auto-Renew

Certbot udah setup auto-renew via cron. Cek:

```bash
sudo systemctl list-timers | grep certbot
```

Manual test:

```bash
sudo certbot renew --dry-run
```

Kalau gak error, auto-renew udah works.

## Step 6: Install Runtime

### Node.js (via nvm)

```bash
# Install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc

# Install Node.js LTS
nvm install 20
nvm use 20
nvm alias default 20
```

### Python

```bash
sudo apt install python3 python3-pip python3-venv -y

# Buat virtual environment
python3 -m venv /var/www/myapp/venv
source /var/www/myapp/venv/bin/activate
pip install -r requirements.txt
```

### PM2 untuk Node.js Process Management

```bash
npm install -g pm2

# Jalankan app
cd /var/www/myapp
pm2 start dist/index.js --name myapp
pm2 save
pm2 startup  # Auto-start saat server restart
```

### Supervisor untuk Python

```bash
sudo apt install supervisor -y
```

```ini
# /etc/supervisor/conf.d/myapp.conf
[program:myapp]
command=/var/www/myapp/venv/bin/gunicorn myapp.wsgi:application
 --bind 127.0.0.1:8000
 --workers 3
directory=/var/www/myapp
user=deploy
autostart=true
autorestart=true
stderr_logfile=/var/log/myapp/error.log
stdout_logfile=/var/log/myapp/access.log
environment=PYTHONUNBUFFERED="1"
```

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start myapp
```

## Step 7: Database

### PostgreSQL

```bash
sudo apt install postgresql postgresql-contrib -y

# Mulai service
sudo systemctl enable postgresql
sudo systemctl start postgresql
```

Buat database dan user:

```bash
sudo -u postgres psql
```

```sql
-- Di psql prompt
CREATE USER myuser WITH PASSWORD 'yang-kuat-banget-123';
CREATE DATABASE mydb OWNER myuser;
GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;
\q
```

Test connection:

```bash
psql -U myuser -d mydb -h localhost
```

### Redis (untuk caching)

```bash
sudo apt install redis-server -y
sudo systemctl enable redis-server

# Test
redis-cli ping
# PONG
```

## Step 8: Deployment Script

Bikin script untuk deploy yang smooth:

```bash
#!/bin/bash
# deploy.sh — Jalankan di server

set -e  # Stop on error

APP_DIR="/var/www/myapp"
BRANCH="main"

echo "🚀 Starting deployment..."

# Navigate
cd $APP_DIR

# Pull latest code
echo "📥 Pulling latest code..."
git pull origin $BRANCH

# Install dependencies
echo "📦 Installing dependencies..."
npm ci --production

# Build
echo "🔨 Building..."
npm run build

# Restart
echo "🔄 Restarting app..."
pm2 restart myapp

echo "✅ Deployment complete!"
echo "📊 App status:"
pm2 status
```

```bash
chmod +x deploy.sh
```

Sekarang tinggal `./deploy.sh` setiap kali mau deploy.

## Step 9: Basic Monitoring

### Simple health check script

```bash
#!/bin/bash
# health-check.sh

URL="https://myapp.com/api/health"
DISCORD_WEBHOOK="your-webhook-url"

RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" $URL)

if [ $RESPONSE -ne 200 ]; then
    curl -H "Content-Type: application/json" \
         -d "{\"content\":\"🔴 Server down! Status: $RESPONSE\"}" \
         $DISCORD_WEBHOOK
    echo "ALERT: Server returned $RESPONSE"

    # Auto-restart
    pm2 restart myapp
    echo "Auto-restarted myapp"
else
    echo "✅ Health check passed ($RESPONSE)"
fi
```

Add ke cron:

```bash
crontab -e
```

```
# Check setiap 5 menit
*/5 * * * * /home/deploy/health-check.sh >> /var/log/health-check.log 2>&1
```

### Install htop untuk monitoring

```bash
sudo apt install htop -y
htop  # Lihat CPU, RAM, processes
```

## Pitfalls yang Sering Bikin Bingung

**1. Gak bisa SSH setelah ganti port**
Pastiin UFW allow port baru SEBELUM restart SSH. Atau better, test di session baru dulu sambil session lama masih aktif.

**2. Nginx 502 Bad Gateway**
App belum jalan atau salah port. Cek:
```bash
pm2 status  # Pastikan app running
curl localhost:3000  # Test langsung
sudo tail -f /var/log/nginx/error.log
```

**3. SSL expired**
Biasanya karena auto-renew gagal. Cek:
```bash
sudo certbot renew --dry-run
# Kalau error, fix dulu, baru renew
sudo certbot renew
```

**4. Disk space habis**
```bash
df -h           # Cek disk usage
sudo du -sh /var/log/*  # Cek log sizes
sudo journalctl --vacuum-time=7d  # Clean old logs
sudo apt autoremove  # Hapus unused packages
```

## Bonus: Deploy with GitHub Actions

Gabungin CI/CD + server setup:

```yaml
name: Deploy to VPS

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /var/www/myapp
            ./deploy.sh
```

## Checklist Server Production

Sebelum go live, pastikan semua ini done:

- [ ] Non-root user dengan sudo
- [ ] SSH key only (disable password login)
- [ ] UFW firewall enabled
- [ ] Fail2ban active
- [ ] Nginx reverse proxy configured
- [ ] SSL certificate installed
- [ ] Auto-renew SSL tested
- [ ] Database configured dengan strong password
- [ ] App runs as service (PM2/Supervisor)
- [ ] Health check monitoring active
- [ ] Log rotation configured
- [ ] Backup strategy in place
- [ ] Domain pointing ke server IP

## Conclusion

Setup Linux server dari nol itu kayak masak rendang — banyak step, tapi hasilnya worth it banget. Dengan server yang properly secured dan configured, kamu bisa sleep tenang.

Jangan lupa: security itu process, bukan one-time setup. Update server secara berkala, monitor logs, dan review security config.

Ada pertanyaan soal server setup? Chat aku di [kontak@dovi.my.id](mailto:kontak@dovi.my.id), seru kalau bisa bahas bareng!
