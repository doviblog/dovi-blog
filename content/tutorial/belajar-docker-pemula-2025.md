---
title: "Belajar Docker untuk Pemula (Tutorial Lengkap 2026)"
date: 2026-02-06
draft: false
slug: "belajar-docker-pemula-2025"
description: "Tutorial Docker untuk pemula. Dari install sampai deploy containerized application."
categories: ['Tutorial']
tags: ['docker', 'container', 'devops', 'pemula']
ShowShareButtons: true
ShowReadingTime: true
ShowToc: true
---

Docker itu intimidating banget buat pemula. Istilah-istilah seperti container, image, volume, dan orchestration terdengar rumit. Tapi kalau dipelajari step-by-step, Docker sebenarnya konsepnya sederhana — dan manfaatnya luar biasa untuk workflow development kamu.

Tutorial ini bakal bawa kamu dari nol sampai bisa containerize aplikasi dan deploy ke server. Semua penjelasan pakai analogi yang mudah dipahami, dengan code examples yang langsung bisa dicoba.

## Docker Itu Apa, Sebenarnya?

Bayangin kamu punya aplikasi Node.js yang jalan sempurna di laptop. Semua dependency terinstall, environment variables sudah di-set, database sudah connected. Tapi begitu dipindah ke server production, error. Kenapa?

Karena environment di server beda:
- Versi Node.js beda
- Package yang terinstall beda
- OS dan konfigurasi beda
- Environment variables belum di-set

Masalah klasik yang developer Indonesia sering hadapi: "kok di laptopku jalan, di server error?" — a.k.a. "works on my machine" problem.

**Docker solve masalah ini** dengan packaging aplikasi + semua dependencies + konfigurasi jadi satu unit yang disebut **container**. Container ini bisa jalan di mana saja — laptop kamu, server teman, cloud production — dengan hasil yang persis sama.

### Analogi Sederhana

Bayangin Docker container itu seperti **kotak bekal (bento box)**:
- **Image** = resep masakan (template untuk bikin bekal)
- **Container** = kotak bekal yang sudah jadi (instance dari image)
- **Dockerfile** = instruksi memasak (langkah-langkah bikin image)
- **Volume** = bumbu cadangan (data yang persist meski container dihapus)
- **Docker Hub** = toko bekal online (repository untuk share images)

Satu image bisa menghasilkan banyak container, sama seperti satu resep bisa dibikin berulang kali.

## Install Docker

### Windows

1. Download Docker Desktop dari [docker.com](https://www.docker.com/products/docker-desktop/)
2. Jalankan installer
3. Restart komputer setelah install
4. Pastikan **WSL 2 backend** diaktifkan (Docker Desktop akan guide kamu)

### macOS

```bash
# Via Homebrew (recommended)
brew install --cask docker

# Atau download .dmg dari docker.com
```

Buka Docker Desktop setelah install. Tunggu sampai icon Docker di menu bar berubah jadi "running".

### Linux (Ubuntu/Debian)

```bash
# Install Docker Engine
curl -fsSL https://get.docker.com | sh

# Tambahkan user ke docker group (biar gak perlu sudo setiap kali)
sudo usermod -aG docker $USER

# Apply perubahan group tanpa logout
newgrp docker

# Verify installation
docker --version
```

### Verifikasi

Setelah install, jalankan command ini untuk pastikan Docker jalan:

```bash
docker --version
# Output: Docker version 24.x.x, build xxxxxxx

docker compose version
# Output: Docker Compose version v2.x.x
```

## Hello World — Container Pertama

Sekarang coba jalankan container pertama kamu:

```bash
docker run hello-world
```

Apa yang terjadi di balik layar:

1. Docker cari image `hello-world` di local — tidak ketemu
2. Docker download image dari Docker Hub
3. Docker bikin container dari image tersebut
4. Container jalan, print pesan, lalu berhenti

Output-nya kurang lebih:

```
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

Selamat, Docker kamu sudah berjalan! Sekarang coba sesuatu yang lebih menarik:

```bash
# Jalankan container interaktif Ubuntu
docker run -it ubuntu bash

# Di dalam container, kamu sekarang di environment Ubuntu
cat /etc/os-release
ls
exit  # Keluar dari container
```

## Konsep Penting Docker

### Image vs Container

- **Image**: Blueprint/template yang read-only. Seperti file `.iso` untuk install OS.
- **Container**: Instance yang jalan dari image. Bisa start, stop, restart, delete.

```bash
# List images yang sudah di-download
docker images

# List container yang sedang jalan
docker ps

# List SEMUA container (termasuk yang sudah stop)
docker ps -a
```

### Layers

Docker image terdiri dari layers. Setiap instruksi di Dockerfile bikin satu layer. Layers yang sama bisa di-share antar images, jadi hemat storage.

```bash
# Lihat layers dari sebuah image
docker history node:18-alpine
```

### Port Mapping

Container punya network sendiri. Untuk mengakses aplikasi di container dari luar, perlu port mapping:

```bash
# Format: -p host_port:container_port
docker run -p 3000:3000 my-app
# Artinya: port 3000 di laptop → port 3000 di container

docker run -p 8080:3000 my-app
# Artinya: port 8080 di laptop → port 3000 di container
```

## Membuat Dockerfile

Dockerfile adalah instruksi untuk bikin image. Ini inti dari Docker workflow.

### Contoh: Dockerfile untuk Node.js App

Misalnya kamu punya project Express.js sederhana. Buat file bernama `Dockerfile` (tanpa ekstensi) di root project:

```dockerfile
# Base image
FROM node:18-alpine

# Set working directory di dalam container
WORKDIR /app

# Copy package files dulu (biar caching lebih efisien)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Port yang akan dipakai aplikasi
EXPOSE 3000

# Command untuk menjalankan aplikasi
CMD ["node", "index.js"]
```

### Penjelasan Setiap Instruksi

**`FROM node:18-alpine`**
Base image. Alpine artinya image yang sangat kecil (sekitar 50MB dibanding 900MB untuk image full). Selalu pakai Alpine kalau ada opsi.

**`WORKDIR /app`**
Set working directory. Semua command setelah ini jalan di folder `/app` di dalam container.

**`COPY package*.json ./`**
Copy `package.json` dan `package-lock.json` ke container. Kenapa copy ini duluan? Karena Docker cache layers. Kalau source code berubah tapi package.json tidak, Docker tidak perlu install ulang dependencies.

**`RUN npm install`**
Install dependencies di dalam container. Hasilnya tersimpan di layer ini.

**`COPY . .`**
Copy semua file dari project ke container. Taruh di akhir karena source code sering berubah, dan kamu mau layer-cache dependency tetap dipakai.

**`EXPOSE 3000`**
Deklarasi bahwa container akan pakai port 3000. Ini cuma dokumentasi, tidak benar-benar membuka port.

**`CMD ["node", "index.js"]`**
Command yang dijalankan saat container start. Hanya boleh satu CMD per Dockerfile.

### Multi-Stage Build

Untuk production, pakai multi-stage build supaya image lebih kecil:

```dockerfile
# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package*.json ./
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

Image production hanya berisi file yang dibutuhkan, tanpa source code, dev dependencies, atau build tools.

### .dockerignore

Buat file `.dockerignore` di root project (mirip `.gitignore`):

```
node_modules
npm-debug.log
.git
.gitignore
.env
.env.local
dist
build
coverage
*.md
.vscode
```

Ini mencegah file yang tidak perlu masuk ke image, bikin build lebih cepat dan image lebih kecil.

## Build & Run

### Build Image

```bash
# Build dengan tag (nama) image
docker build -t my-app .

# Build dengan versi
docker build -t my-app:v1.0 .

# Lihat proses build
docker build -t my-app . --no-cache  # Force rebuild tanpa cache
```

### Run Container

```bash
# Run di foreground (terminal ter-block)
docker run -p 3000:3000 my-app

# Run di background (detached mode)
docker run -d -p 3000:3000 --name my-app-container my-app

# Run dengan environment variables
docker run -d -p 3000:3000 \
  -e NODE_ENV=production \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  --name my-app-container my-app
```

### Manage Container

```bash
# Lihat container yang jalan
docker ps

# Stop container
docker stop my-app-container

# Start container yang sudah stop
docker start my-app-container

# Restart
docker restart my-app-container

# Lihat logs
docker logs my-app-container
docker logs -f my-app-container  # Follow/stream logs

# Masuk ke dalam container (debugging)
docker exec -it my-app-container sh

# Hapus container
docker rm my-app-container

# Hapus image
docker rmi my-app
```

## Docker Compose

Docker Compose memungkinkan kamu menjalankan **beberapa container sekaligus** dengan satu command. Ini sangat penting untuk aplikasi yang butuh database, cache, dan layanan lainnya.

### docker-compose.yml

Buat file `docker-compose.yml` di root project:

```yaml
version: '3.8'

services:
  # Aplikasi Node.js
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://postgres:password@db:5432/myapp
      - REDIS_URL=redis://cache:6379
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_started
    restart: unless-stopped
    volumes:
      - ./uploads:/app/uploads  # Persist uploads

  # PostgreSQL Database
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache
  cache:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### Docker Compose Commands

```bash
# Start semua services
docker compose up -d

# Lihat logs semua services
docker compose logs -f

# Lihat logs specific service
docker compose logs -f app

# Stop semua services
docker compose down

# Stop dan HAPUS volumes (data hilang!)
docker compose down -v

# Rebuild image setelah perubahan Dockerfile
docker compose up -d --build

# Lihat status services
docker compose ps
```

### Kenapa Docker Compose Penting?

Tanpa Docker Compose, kamu harus jalankan command manual untuk setiap container:

```bash
# Tanpa Compose — ribet
docker run -d --name db -e POSTGRES_PASSWORD=pass postgres:15
docker run -d --name cache redis:7
docker run -d --name app -p 3000:3000 --link db --link cache my-app
```

Dengan Compose:
```bash
# Dengan Compose — satu command
docker compose up -d
```

Untuk contoh penggunaan Docker di project nyata, lihat juga [tutorial deploy AI agent ke production](/ai-agent/deploy-ai-agent-production-docker-railway/) yang pakai Docker Compose.

## Volumes — Persist Data

Container bersifat ephemeral — kalau dihapus, data di dalamnya hilang. Untuk persist data, pakai volumes:

### Named Volumes

```bash
# Buat volume
docker volume create my-data

# Pakai volume di container
docker run -d -v my-data:/app/data my-app

# Lihat semua volumes
docker volume ls

# Hapus volume
docker volume rm my-data
```

### Bind Mounts

Bind mount map folder di host ke container:

```bash
# Map folder local ke container
docker run -d -v $(pwd)/src:/app/src my-app

# Readonly mount
docker run -d -v $(pwd)/config:/app/config:ro my-app
```

Bind mounts sangat berguna untuk development — kamu edit file di VS Code, perubahan langsung ter-refleksi di container.

## Networking

Container bisa berkomunikasi satu sama lain lewat Docker network:

```bash
# Docker Compose otomatis bikin network untuk semua services
# Di dalam container, service bisa dipanggil pakai nama service
# Contoh: app bisa connect ke db pakai hostname "db" (bukan localhost)
```

Ini yang bikin `DATABASE_URL=postgresql://postgres:password@db:5432/myapp` di docker-compose.yml bekerja — `db` adalah nama service yang bisa di-resolve sebagai hostname.

## Praktik Terbaik

### 1. Selalu Pakai .dockerignore
Jangan copy `node_modules`, `.git`, atau file sensitif ke image.

### 2. Gunakan Multi-Stage Build
Bikin image production sekecil mungkin. Perbedaan bisa drastis — dari 1GB jadi 100MB.

### 3. Pin Version
```dockerfile
# JANGAN
FROM node:latest

# LAKUKAN
FROM node:18.19-alpine
```
Hindari `latest` karena bisa bikin build tidak reproducible.

### 4. Jangan Run as Root
```dockerfile
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
```

### 5. Scan for Vulnerabilities
```bash
docker scout quickview my-app
```

### 6. Pakai Health Checks
Tambahkan health check di Dockerfile:
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:3000/health || exit 1
```

## Debugging Container

### Container Tidak Mau Start

```bash
# Cek logs
docker logs my-container

# Masuk ke container dengan shell (kalau image punya shell)
docker run -it my-app sh

# Override entrypoint untuk debugging
docker run -it --entrypoint sh my-app
```

### Container Tiba-tiba Stop

```bash
# Cek exit code
docker ps -a  # Lihat STATUS column

# Exit code 0 = normal exit
# Exit code 1 = error
# Exit code 137 = OOM killed (kehabisan memory)
```

### Aplikasi Tidak Bisa Diakses

```bash
# Pastikan port mapping benar
docker port my-container

# Cek container berjalan
docker ps

# Test dari dalam container
docker exec -it my-container curl http://localhost:3000
```

## Deploy ke Server

Setelah aplikasi ter-containerize, deploy ke server jadi gampang:

### Push ke Docker Hub

```bash
# Login ke Docker Hub
docker login

# Tag image
docker tag my-app username/my-app:v1.0

# Push
docker push username/my-app:v1.0
```

### Deploy di Server

```bash
# Pull image di server
docker pull username/my-app:v1.0

# Jalankan
docker run -d -p 80:3000 username/my-app:v1.0
```

Atau lebih praktis, copy `docker-compose.yml` ke server dan jalankan:

```bash
docker compose up -d
```

Untuk server management, baca [tutorial setup Linux server dari nol](/tutorial/setup-linux-server-dari-nol/).

## Docker vs Alternatif

**Docker vs VM (Virtual Machine):**
- Docker lebih ringan — share kernel host, tidak perlu full OS
- Startup dalam milidetik, bukan menit
- Ukuran image MB, bukan GB

**Docker vs Podman:**
- Podman daemonless, Docker punya daemon
- Podman lebih secure secara default (rootless)
- Docker ekosistem lebih besar

**Docker vs Nix:**
- Nix fokus pada reproducible builds
- Docker lebih populer dan fleksibel
- Untuk pemula, Docker lebih mudah dipelajari

## FAQ

### Apakah Docker gratis?
Docker Engine (CLI) gratis dan open source. Docker Desktop juga gratis untuk individual developer dan small business. Untuk perusahaan besar (>250 karyawan atau >$10M revenue), Docker Desktop butuh subscription berbayar.

### Berapa RAM yang dibutuhkan Docker?
Docker Desktop di Windows/Mac butuh minimal 4GB RAM untuk Docker VM. Di Linux, Docker langsung pakai kernel host, jadi lebih hemat. Untuk development normal, alokasikan 4-8GB untuk Docker Desktop.

### Docker atau langsung install di OS?
Untuk development, pilihanmu. Tapi untuk production, Docker sangat direkomendasikan. Konsistensi environment antara development dan production mengurangi "works on my machine" problem secara drastis.

### Apakah semua aplikasi perlu di-Docker-kan?
Tidak. Aplikasi sederhana yang cuma satu file mungkin tidak perlu Docker. Tapi kalau aplikasinya punya banyak dependency, database, dan service lain, Docker bikin setup jauh lebih simpel.

### Bagaimana cara update aplikasi di Docker?
Build image baru, push ke registry, pull di server, jalankan container baru. Dengan Docker Compose: update `docker-compose.yml`, jalankan `docker compose up -d --build`.

### Apakah Docker aman untuk production?
Docker sendiri aman, tapi konfigurasi yang salah bisa bikin vulnerability. Tips: jangan run as root, scan image untuk CVE, pakai official base images, dan update base image secara berkala.

---

Docker dalam 15 menit. Sekarang waktunya practice: containerize aplikasi kamu! Mulai dari yang sederhana — bungkus project Node.js atau Python kamu dalam Docker. Begitu terbiasa, kamu bakal heran kenapa dulu tidak pakai Docker dari awal.

**Pertanyaan?** Komen di bawah!
