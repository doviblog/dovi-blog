---
title: "Cara Setup CI/CD dengan GitHub Actions (Gratis)"
date: 2026-04-09
draft: false
slug: "cara-setup-ci-cd-github-actions"
description: "Tutorial setup CI/CD pipeline menggunakan GitHub Actions. Automate testing dan deployment dari nol."
categories: [Tutorial]
tags: ['ci-cd', 'github-actions', 'automation', 'devops', 'deployment']
ShowShareLinks: true
ShowReadingTime: true
ShowToc: true
---

Dulu aku masih manual-deploy. Push code ke GitHub, SSH ke server, pull, restart. Setiap kali. Tiap update kecil aja, 10 menit habis buat proses deploy.

Teman aku bilang: "Lu belum pakai CI/CD?" — aku langsung malu.

Setelah setup GitHub Actions, sekarang tinggal push ke main branch dan... beres. Tests jalan otomatis, deploy otomatis, notifikasi kalau gagal. Gak pernah balik ke manual lagi.

## CI/CD Itu Apa?

- **CI (Continuous Integration)**: Setiap push code, otomatis run tests dan build. Kalau ada error, langsung ketauan.
- **CD (Continuous Deployment/Delivery)**: Kalau tests pass, otomatis deploy ke server/staging/production.

GitHub Actions jadi pilihan utama karena:
- **Gratis** untuk public repo (2000 menit/bulan untuk private)
- **Native** — langsung di GitHub, gak perlu setup tool lain
- **Mudah** — pakai YAML, bukan config ribet
- **Flexible** — bisa deploy ke mana aja (VPS, AWS, Vercel, Railway)

## Step 0: Persiapan

Yang kamu butuhin:
- GitHub repo dengan project (Node.js, Python, dll)
- GitHub account (pastinya)
- Target deployment server (aku pakai VPS dan Railway)

## Step 1: Project Structure

Aku asumsiin kamu punya project Node.js kayak gini:

```
my-app/
├── src/
│   ├── index.js
│   └── utils.js
├── tests/
│   └── app.test.js
├── package.json
├── .env.example
└── README.md
```

package.json kamu harus ada test script:

```json
{
  "name": "my-app",
  "version": "1.0.0",
  "scripts": {
    "test": "jest --coverage",
    "lint": "eslint src/",
    "build": "next build",
    "start": "node src/index.js"
  },
  "devDependencies": {
    "jest": "^29.7.0",
    "eslint": "^8.50.0"
  }
}
```

## Step 2: Buat Workflow Pertama

Buat folder dan file ini di repo kamu:

```bash
mkdir -p .github/workflows
touch .github/workflows/ci.yml
```

Basic CI workflow:

```yaml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

      - name: Run tests
        run: npm test
```

Push ke GitHub:

```bash
git add .
git commit -m "Add CI pipeline"
git push
```

Buka tab **Actions** di repo GitHub kamu. Pipeline langsung jalan!

## Step 3: Advanced CI — Matrix Testing

Test di multiple Node versions:

```yaml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        node-version: [18, 20, 22]

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'

      - run: npm ci
      - run: npm run lint
      - run: npm test

      - name: Upload coverage
        if: matrix.node-version == 20
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
```

Dengan matrix, tests jalan di 3 versi Node sekaligus. Kalau ada breaking change di salah satu versi, langsung ketauan.

## Step 4: Deploy ke VPS via SSH

Ini yang paling sering ditanya. Deploy ke VPS (Ubuntu) pakai SSH:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm test

  deploy:
    needs: test  # Hanya deploy kalau tests pass
    runs-on: ubuntu-latest

    steps:
      - name: Deploy via SSH
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          port: 22
          script: |
            cd /var/www/my-app
            git pull origin main
            npm ci --production
            npm run build
            pm2 restart my-app
            echo "Deployed at $(date)" >> deploy.log
```

**Set up secrets** di GitHub:

1. Buka repo → Settings → Secrets and variables → Actions
2. Tambahin:
   - `SERVER_HOST` — IP server kamu (contoh: 123.45.67.89)
   - `SERVER_USER` — SSH user (contoh: deploy)
   - `SSH_PRIVATE_KEY` — isi dari `cat ~/.ssh/id_ed25519`

Generate SSH key khusus untuk deploy (jangan pakai key personal):

```bash
# Di local machine
ssh-keygen -t ed25519 -C "github-actions-deploy" -f ~/.ssh/deploy_key

# Copy public key ke server
ssh-copy-id -i ~/.ssh/deploy_key.pub user@server

# Copy private key ke GitHub Secrets
cat ~/.ssh/deploy_key
# Paste ke SSH_PRIVATE_KEY secret
```

## Step 5: Deploy ke Railway / Vercel

Kalau pakai Railway, lebih gampang lagi:

```yaml
name: Deploy to Railway

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Railway CLI
        run: npm install -g @railway/cli

      - name: Deploy
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
        run: railway up --service=my-app
```

Atau deploy Docker image ke Railway:

```yaml
- name: Login to Railway Registry
  run: railway login --token ${{ secrets.RAILWAY_TOKEN }}

- name: Build & Deploy Docker
  run: |
    docker build -t my-app .
    railway up --docker-image my-app --service my-app
```

Untuk Vercel:

```yaml
name: Deploy to Vercel

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
```

## Step 6: Python Project CI/CD

Buat Python, workflow-nya mirip:

```yaml
name: Python CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Lint with ruff
        run: ruff check .

      - name: Type check with mypy
        run: mypy src/

      - name: Run tests
        run: pytest tests/ -v --cov=src --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          file: coverage.xml
```

## Step 7: Docker Build & Push

Build Docker image dan push ke Docker Hub:

```yaml
name: Build & Push Docker Image

on:
  push:
    tags:
      - 'v*'  # Trigger saat tag release (v1.0.0, v1.1.0, dll)

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Extract version
        id: version
        run: echo "VERSION=${GITHUB_REF#refs/tags/}" >> $GITHUB_OUTPUT

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            yourusername/my-app:latest
            yourusername/my-app:${{ steps.version.outputs.VERSION }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

## Step 8: Notifications

Biar tau kalau pipeline gagal:

```yaml
  notify:
    needs: [test, deploy]
    if: failure()
    runs-on: ubuntu-latest
    steps:
      - name: Send Telegram notification
        uses: appleboy/telegram-action@v1
        with:
          to: ${{ secrets.TELEGRAM_CHAT_ID }}
          token: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          message: |
            ❌ Deploy gagal!
            Repo: ${{ github.repository }}
            Branch: ${{ github.ref }}
            Commit: ${{ github.event.head_commit.message }}
            Author: ${{ github.event.head_commit.author.name }}
            Workflow: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
```

Atau pakai Slack/Discord — cari action-nya di GitHub Marketplace.

## Step 9: Caching & Optimasi

Biar pipeline lebih cepat:

```yaml
- name: Cache Node modules
  uses: actions/cache@v4
  with:
    path: |
      node_modules
      ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-

- name: Cache Python packages
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
```

Tapi kalau pakai `actions/setup-node@v4` dengan `cache: 'npm'`, caching udah otomatis kok.

## Pitfalls yang Pernah Bikin Aku Kesel

**1. Lupa set permissions**
Deploy ke server gagal karena SSH key gak punya permission yang tepat. Pastikan user di server punya permission ke folder target.

```bash
# Di server
sudo chown -R deploy:deploy /var/www/my-app
sudo usermod -aG docker deploy  # Kalau pakai Docker
```

**2. Secrets leak di log**
JANGAN print secrets di workflow log. GitHub otomatis mask secrets, tapi kalau kamu encode/base64, bisa tembus.

```yaml
# JANGAN gini:
- run: echo ${{ secrets.MY_SECRET }}

# GitHub bakal mask, tapi better gak ada sama sekali
```

**3. Workflow gak trigger**
Sering banget push tapi workflow gak jalan. Cek:
- Branch name bener? (main vs master)
- YAML syntax valid?
- Actions di-enable di repo settings?

**4. Timeout**
Default timeout 6 jam. Biasanya kebanyakan. Set lebih rendah:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15  # Cukup buat most cases
```

**5. Docker build lambat**
Pakai BuildKit cache:

```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3

- name: Build with cache
  uses: docker/build-push-action@v5
  with:
    context: .
    push: true
    tags: my-app:latest
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

## Complete Real-World Example

Ini workflow lengkap yang aku pakai di production:

```yaml
name: Full CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: '20'
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # ========== TESTS ==========
  lint-and-test:
    runs-on: ubuntu-latest
    timeout-minutes: 10

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - run: npm ci
      - run: npm run lint
      - run: npm test -- --coverage

      - name: Upload coverage
        if: github.event_name == 'pull_request'
        uses: codecov/codecov-action@v4

  # ========== BUILD & DEPLOY ==========
  deploy:
    needs: lint-and-test
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    timeout-minutes: 20

    steps:
      - uses: actions/checkout@v4

      - name: Deploy via SSH
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /var/www/my-app
            git pull origin main
            npm ci --production
            npm run build
            pm2 restart my-app

  # ========== NOTIFY ==========
  notify:
    needs: [lint-and-test, deploy]
    if: always()
    runs-on: ubuntu-latest

    steps:
      - name: Notify result
        uses: appleboy/telegram-action@v1
        with:
          to: ${{ secrets.TELEGRAM_CHAT_ID }}
          token: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          message: |
            ${{ needs.deploy.result == 'success' && '✅' || '❌' }} Deploy ${{ needs.deploy.result }}
            Commit: ${{ github.event.head_commit.message }}
```

## Cost GitHub Actions

- **Public repo**: Unlimited minutes, GRATIS
- **Private repo Free**: 2000 menit/bulan
- **Pro ($4/bulan)**: 3000 menit/bulan
- **Organization ($4/user/bulan)**: 3000 menit/bulan

Untuk project personal, free tier lebih dari cukup. Aku pakai ~400 menit/bulan untuk 3-4 repo aktif.

## Conclusion

CI/CD itu investasi yang worth it banget. 30 menit setup, tapi hemat ratusan jam dalam jangka panjang. Plus, code quality naik drastis karena ada automated testing.

Mulai dari simple workflow dulu (test + lint), terus tambahin deploy steps. Gak harus langsung perfect.

Mau nanya soal setup CI/CD di project kamu? Chat aku di [Telegram](https://t.me/dovi)!
