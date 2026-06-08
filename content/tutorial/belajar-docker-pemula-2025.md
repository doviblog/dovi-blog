---
title: "Belajar Docker untuk Pemula (Tutorial Lengkap 2025)"
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

Docker itu intimidating banget buat pemula. Tapi sebenernya simple kok.

## Docker Itu Apa?

Bayangin kamu punya aplikasi yang jalan di laptop. Tapi pas dipindah ke server, error karena environment beda.

Docker solve masalah itu dengan packaging aplikasi + dependencies jadi satu unit.

## Install Docker

### Windows/macOS
Download Docker Desktop

### Linux
```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
```

## Hello World

```bash
docker run hello-world
```

## Dockerfile

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["node", "index.js"]
```

## Build & Run

```bash
docker build -t my-app .
docker run -d -p 3000:3000 my-app
```

## Docker Compose

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
  db:
    image: postgres:15
    environment:
      - POSTGRES_PASSWORD=***
```

## Basic Commands

```bash
docker ps                  # List containers
docker stop my-container   # Stop
docker rm my-container     # Remove
docker logs my-container   # Logs
```

## Conclusion

Docker dalam 15 menit. Practice: Containerize aplikasi kamu sekarang!

**Pertanyaan?** Komen di bawah!
