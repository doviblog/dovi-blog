---
title: "Cara Buat REST API dengan Node.js dan Express (2026)"
date: 2026-02-13
draft: false
slug: "cara-buat-rest-api-nodejs-express-2025"
description: "Tutorial lengkap membuat REST API dengan Node.js dan Express. Dari setup sampai production-ready."
categories: ['Tutorial']
tags: ['nodejs', 'express', 'rest-api', 'backend', 'tutorial']
ShowShareButtons: true
ShowReadingTime: true
ShowToc: true
---

REST API itu backbone dari hampir semua aplikasi modern. Entah kamu bikin mobile app, web app, atau integrasi sama pihak ketiga — di balik semuanya pasti ada API. Di tutorial ini aku bakal jelasin cara bikin REST API dari nol pakai Node.js dan Express, dari setup sampai tips production-ready. Cocok banget buat kamu yang baru mulai belajar backend development.

Kalau kamu belum familiar sama Node.js, coba baca dulu [belajar Docker dari nol](/tutorial/belajar-docker-pemula-2025/) karena nanti di bagian deployment kamu butuh pengetahuan dasar Docker. Dan kalau kamu mau test API-nya pakai GUI, panduan [cara pakai Postman untuk API testing](/tutorial/cara-pakai-postman-api-testing/) bakal sangat membantu.

## Kenapa Harus Node.js + Express?

Banyak framework backend kayak Django (Python), Laravel (PHP), atau Spring Boot (Java). Tapi Node.js + Express punya beberapa kelebihan khusus untuk bikin REST API:

- **JavaScript everywhere** — Kamu udah paham JS di frontend, backend juga pakai bahasa yang sama. Gak perlu switch context.
- **Lightweight** — Express itu minimalist framework. Kamu cuma install yang kamu butuh, gak ada bloat.
- **Ekosistem NPM** — Ribuan package yang bisa langsung kamu install. Mulai dari database driver sampai authentication library.
- **Performance tinggi** — Node.js pakai event-driven, non-blocking I/O. Cocok banget untuk API yang handle banyak request simultan.
- **Banyak job opening** — Di Indonesia, banyak startup dan perusahaan tech yang pakai stack Node.js. Belajar Express itu investasi karir yang bagus.

Kalau dibandingkan sama framework lain, Express itu kayak pisau Swiss Army — sederhana tapi bisa handle banyak hal. Dan karena open source, komunitasnya gede banget. Kalau kamu stuck, pasti ada jawabannya di Stack Overflow atau documentation resmi.

## Setup Project

Langkah pertama, bikin folder project baru dan install dependencies yang dibutuhkan:

```bash
mkdir my-api && cd my-api
npm init -y
npm install express dotenv cors helmet morgan
npm install --save-dev nodemon
```

Kenapa install banyak package? Ini penjelasannya:

- **express** — Framework utama untuk bikin server dan handle routing
- **dotenv** — Buat baca environment variable dari file `.env`. Penting banget buat nyimpen API keys dan secrets.
- **cors** — Middleware untuk handle Cross-Origin Resource Sharing. Tanpa ini, browser frontend kamu gak akan bisa akses API.
- **helmet** — Middleware keamanan yang set header HTTP supaya lebih secure.
- **morgan** — HTTP request logger. Berguna banget pas debugging, karena kamu bisa lihat semua request yang masuk ke server.
- **nodemon** — Dev tool yang auto-restart server kalau ada perubahan file. Gak perlu manual restart setiap kali edit kode.

Buat file `.env` di root project:

```
PORT=3000
NODE_ENV=development
```

Dan tambahin script di `package.json`:

```json
{
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js"
  }
}
```

Sekarang jalankan `npm run dev` — server kamu udah jalan! Tapi belum ada endpoint sama sekali. Yuk kita bikin.

## Basic Server

Buat file `index.js` di root project:

```javascript
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(helmet());
app.use(cors());
app.use(morgan('combined'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Health check endpoint
app.get('/', (req, res) => {
  res.json({ message: 'API is running!', version: '1.0.0' });
});

// Health check untuk monitoring
app.get('/health', (req, res) => {
  res.json({ status: 'ok', uptime: process.uptime() });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

Jalankan `npm run dev`, lalu buka browser ke `http://localhost:3000`. Kamu bakal lihat response JSON. Selamat — API server kamu udah hidup!

Penjelasan singkat kenapa pakai middleware sebelum routes:

1. `helmet()` dijalankan dulu untuk set security headers di setiap response
2. `cors()` memastikan cross-origin request bisa diterima
3. `morgan()` log semua request untuk keperluan debugging
4. `express.json()` parse request body yang formatnya JSON

Urutan middleware itu penting. Kalau kamu taruh `express.json()` sebelum route, semua request body bakal ke-parse dengan benar.

## CRUD Operations

REST API itu pada dasarnya operasi CRUD — Create, Read, Update, Delete. Kita bakal bikin contoh lengkap pakai data users.

### Setup Data Dummy

```javascript
// Simpan di bagian atas file, sebelum routes
let users = [
  { id: 1, name: 'Budi Santoso', email: 'budi@example.com', role: 'developer' },
  { id: 2, name: 'Siti Rahayu', email: 'siti@example.com', role: 'designer' },
  { id: 3, name: 'Andi Pratama', email: 'andi@example.com', role: 'pm' },
];
let nextId = 4;
```

### GET — Ambil Semua Data

```javascript
// GET all users dengan pagination
app.get('/api/v1/users', (req, res) => {
  const page = parseInt(req.query.page) || 1;
  const limit = parseInt(req.query.limit) || 10;
  const startIndex = (page - 1) * limit;
  const endIndex = startIndex + limit;

  const results = users.slice(startIndex, endIndex);

  res.json({
    data: results,
    pagination: {
      total: users.length,
      page: page,
      limit: limit,
      totalPages: Math.ceil(users.length / limit)
    }
  });
});
```

### GET — Ambil Satu Data

```javascript
// GET single user by ID
app.get('/api/v1/users/:id', (req, res) => {
  const user = users.find(u => u.id === parseInt(req.params.id));
  if (!user) {
    return res.status(404).json({ error: 'User tidak ditemukan' });
  }
  res.json({ data: user });
});
```

### POST — Buat Data Baru

```javascript
// POST create new user dengan validasi
app.post('/api/v1/users', (req, res) => {
  const { name, email, role } = req.body;

  // Validasi input
  if (!name || !email) {
    return res.status(400).json({ error: 'Name dan email wajib diisi' });
  }

  // Cek duplikat email
  const existingUser = users.find(u => u.email === email);
  if (existingUser) {
    return res.status(409).json({ error: 'Email sudah terdaftar' });
  }

  const newUser = { id: nextId++, name, email, role: role || 'user' };
  users.push(newUser);
  res.status(201).json({ data: newUser, message: 'User berhasil dibuat' });
});
```

### PUT — Update Data

```javascript
// PUT update user
app.put('/api/v1/users/:id', (req, res) => {
  const index = users.findIndex(u => u.id === parseInt(req.params.id));
  if (index === -1) {
    return res.status(404).json({ error: 'User tidak ditemukan' });
  }

  users[index] = { ...users[index], ...req.body, id: users[index].id };
  res.json({ data: users[index], message: 'User berhasil diupdate' });
});
```

### DELETE — Hapus Data

```javascript
// DELETE user
app.delete('/api/v1/users/:id', (req, res) => {
  const index = users.findIndex(u => u.id === parseInt(req.params.id));
  if (index === -1) {
    return res.status(404).json({ error: 'User tidak ditemukan' });
  }

  users.splice(index, 1);
  res.status(204).send();
});
```

Kalau kamu mau test semua endpoint ini pakai GUI, panduan [cara pakai Postman](/tutorial/cara-pakai-postman-api-testing/) bakal sangat berguna. Atau langsung test pakai curl:

```bash
# Create user
curl -X POST http://localhost:3000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Dewi Lestari", "email": "dewi@example.com", "role": "developer"}'

# Get all users
curl http://localhost:3000/api/v1/users?page=1&limit=10
```

## Error Handling yang Proper

Salah satu kesalahan paling umum di REST API adalah error handling yang buruk. Kalau server error dan cuma return 500 tanpa pesan yang jelas, debugging jadi mimpi buruk. Mari kita bikin error handling yang proper:

```javascript
// Global error handler middleware — taruh di paling akhir sebelum app.listen
app.use((err, req, res, next) => {
  console.error(err.stack);

  res.status(err.status || 500).json({
    error: {
      message: err.message || 'Internal Server Error',
      status: err.status || 500,
      ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
    }
  });
});

// 404 handler untuk routes yang tidak ada
app.use((req, res) => {
  res.status(404).json({
    error: {
      message: `Route ${req.originalUrl} tidak ditemukan`,
      status: 404
    }
  });
});
```

Tips penting: di production, jangan pernah expose stack trace ke client karena bisa bocorkan informasi sensitif tentang struktur aplikasi kamu. Makanya ada pengecekan `NODE_ENV === 'development'`.

## Input Validation

Jangan pernah percaya input dari client! Validasi setiap data yang masuk. Untuk project yang lebih serius, pakai library seperti `joi` atau `express-validator`:

```javascript
const { body, validationResult } = require('express-validator');

// Validasi saat create user
app.post('/api/v1/users',
  [
    body('name').trim().notEmpty().withMessage('Nama wajib diisi'),
    body('email').isEmail().withMessage('Format email tidak valid'),
    body('role').optional().isIn(['admin', 'user', 'developer', 'designer'])
      .withMessage('Role tidak valid')
  ],
  (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const newUser = { id: nextId++, ...req.body };
    users.push(newUser);
    res.status(201).json({ data: newUser });
  }
);
```

Install express-validator terlebih dahulu: `npm install express-validator`.

## Structuring Project yang Rapi

Kalau semua kode taruh di satu file `index.js`, bakal jadi file yang ribet dan susah di-maintain. Untuk project yang lebih besar, split jadi beberapa file:

```
my-api/
├── index.js           # Entry point
├── routes/
│   └── users.js       # Routes untuk users
├── middleware/
│   └── auth.js        # Authentication middleware
├── models/
│   └── user.js        # Data model
├── .env
├── package.json
```

Contoh routes terpisah:

```javascript
// routes/users.js
const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
  // ... logic get all users
});

router.get('/:id', (req, res) => {
  // ... logic get single user
});

module.exports = router;
```

```javascript
// index.js (clean version)
const usersRouter = require('./routes/users');
app.use('/api/v1/users', usersRouter);
```

Ini bikin kode lebih modular, mudah di-maintain, dan gampang di-scale. Kalau kamu udah familiar dengan struktur project seperti ini, langkah selanjutnya adalah mempelajari [deployment ke production pakai Docker](/tutorial/belajar-docker-pemula-2025/).

## Best Practices untuk REST API

Kalau kamu mau API kamu dianggap profesional dan production-ready, ikuti best practices berikut:

1. **Versioning selalu pakai URL path** — Pakai `/api/v1/` bukan `/api/`. Kalau nanti ada breaking changes, kamu bisa bikin `/api/v2/` tanpa ngebreak versi lama.

2. **Pagination wajib untuk list endpoint** — Jangan pernah return semua data sekaligus. Pakai query parameter `?page=1&limit=10`. Ini hemat bandwidth dan lebih cepat.

3. **HTTP status code yang benar** — 200 untuk success, 201 untuk created, 400 untuk bad request, 404 untuk not found, 500 untuk server error. Jangan asal pakai 200 untuk semua.

4. **Rate limiting** — Pasang `express-rate-limit` supaya API kamu gak di-spam. Untuk server di Indonesia, pakai hosting yang support rate limiting di layer nginx juga bisa.

5. **Documentation** — Pakai Swagger/OpenAPI untuk auto-generate docs. Developer lain (atau kamu sendiri 3 bulan lagi) bakal makasih banget.

6. **CORS yang ketat** — Jangan wildcard CORS di production. Tentukan domain mana yang boleh akses API kamu.

7. **HTTPS wajib** — Jangan pernah jalankan API production tanpa HTTPS. Kalau kamu butuh SSL certificate gratis, baca [review 5 hosting terbaik untuk developer Indonesia](/tech-review/5-hosting-terbaik-developer-indonesia-2025/) yang kebanyakan udah support auto SSL.

## Deployment ke Production

Kalau API kamu udah siap, saatnya deploy. Beberapa opsi hosting yang cocok untuk Node.js API di Indonesia:

- **Railway** — Gratis tier yang cukup untuk project kecil. Deploy langsung dari GitHub. Baca [perbandingan Railway vs Render vs Fly.io](/tech-review/review-railway-vs-render-vs-flyio-2025/) untuk detail lengkap.
- **Vercel** — Meskipun dikenal untuk frontend, Vercel juga support API routes.
- **DigitalOcean** — VPS mulai dari $5/bulan (sekitar Rp 78.000). Cocok kalau kamu butuh full control.

Kalau mau pakai VPS, panduan [setup Linux server dari nol](/tutorial/setup-linux-server-dari-nol/) bakal bantu kamu dari awal. Dan untuk CI/CD pipeline supaya otomatis deploy tiap push ke GitHub, cek [tutorial GitHub Actions](/tutorial/cara-setup-ci-cd-github-actions/).

## FAQ

**Apakah Express masih relevan di 2026?**

Masih sangat relevan. Express tetap jadi framework paling populer untuk Node.js backend. Banyak perusahaan besar seperti Netflix, PayPal, dan Uber masih pakai Express. Komunitasnya besar, banyak tutorial, dan ekosistem package-nya stabil.

**Berapa salary backend developer Node.js di Indonesia?**

Berdasarkan data dari beberapa job portal, Junior Node.js developer di Jakarta bisa dapat Rp 6-10 juta/bulan. Mid-level sekitar Rp 12-20 juta/bulan. Senior bisa tembus Rp 25-40 juta/bulan tergantung perusahaan dan skill.

**Express vs Fastify, mana yang lebih bagus?**

Fastify memang lebih cepat dari Express dalam hal performance. Tapi Express punya komunitas lebih besar dan lebih banyak dokumentasi. Untuk beginner, Express lebih recommended. Kalau kamu udah advanced dan butuh performance ekstra, coba Fastify.

**Database apa yang cocok dipasangkan dengan Express?**

Untuk project kecil dan menengah, PostgreSQL atau MySQL pakai ORM seperti Prisma atau Sequelize. Untuk NoSQL, MongoDB pakai Mongoose sangat populer di ecosystem Node.js. Kalau butuh guidance lebih lanjut, cek artikel tentang [5 framework AI agent terbaik](/ai-agent/5-framework-ai-agent-terbaik-2025/) yang juga bahas integrasi database untuk AI application.

**Gimana cara handle authentication di Express?**

Paling umum pakai JWT (JSON Web Tokens). Install `jsonwebtoken` dan `bcryptjs`, lalu implementasi login endpoint yang return JWT. Token ini client kirim di header Authorization setiap request. Untuk project production, pertimbangkan pakai library seperti `passport.js` yang support berbagai strategi auth.

---

Dalam waktu singkat, kamu udah punya REST API yang functional dengan Express. Dari setup, CRUD operations, error handling, sampai project structure yang rapi — semua udah kamu pelajari. Tinggal practice dan explore lebih lanjut.

Kalau kamu tertarik bikin API yang lebih advanced dengan AI integration, cek juga tutorial [cara membuat AI agent pertama](/ai-agent/cara-membuat-ai-agent-pertama/) yang bisa kamu integrasikan sama API yang baru kamu bikin ini.

**Butuh bantuan?** Email aku di [kontak@dovi.my.id](mailto:kontak@dovi.my.id)!
