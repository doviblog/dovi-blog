---
title: "Cara Buat REST API dengan Node.js dan Express (2026)"
date: 2026-02-13
draft: false
slug: "cara-buat-rest-api-nodejs-express-2026"
description: "Tutorial lengkap membuat REST API dengan Node.js dan Express. Dari setup sampai production-ready."
categories: ['Tutorial']
tags: ['nodejs', 'express', 'rest-api', 'backend', 'tutorial']
ShowShareButtons: true
ShowReadingTime: true
ShowToc: true
---

REST API itu *backbone* dari hampir semua aplikasi modern yang kamu pakai sehari-hari—dari Instagram, Tokopedia, sampai Gojek. Setiap kali aplikasi mobile meminta data dari server, kemungkinan besar itu lewat REST API. Kalau kamu mau jadi backend developer di 2026, **wajib hukumnya** bisa bikin REST API sendiri dari nol.

Di tutorial ini aku bakal jelasin step-by-step cara bikin REST API production-ready pakai **Node.js** dan **Express.js**. Kita nggak cuma bikin endpoint CRUD biasa—tapi juga middleware, error handling, koneksi database, testing, dan security best practices. Semua pakai kode yang bisa langsung kamu copy-paste dan jalankan.

## Apa Itu REST API?

**REST** (Representational State Transfer) adalah arsitektur atau gaya desain untuk membangun web service. **API** (Application Programming Interface) adalah kontrak antara dua aplikasi yang mau komunikasi. Jadi REST API itu cara aplikasi client (mobile app, website, atau service lain) minta dan kirim data ke server menggunakan protokol HTTP.

Prinsip utama REST:

- **Stateless** — Setiap request harus berdiri sendiri, server nggak ingat request sebelumnya
- **Resource-based** — Semua data diperlakukan sebagai resource dengan URL unik (misal `/api/users/1`)
- **HTTP Methods** — GET (baca), POST (buat), PUT/PATCH (update), DELETE (hapus)
- **JSON format** — Data dikirim dan diterima dalam format JSON

Contoh sederhana: kalau kamu mau ambil data semua user, client mengirim `GET /api/users`. Kalau mau buat user baru, `POST /api/users` dengan body berisi data user. Intuitif dan konsisten—itu kekuatan REST.

## Setup Project Express

Buka terminal dan jalankan command berikut untuk membuat project baru:

```bash
mkdir my-api && cd my-api
npm init -y
npm install express dotenv cors helmet morgan
```

Penjelasan setiap package:

- **express** — Framework HTTP minimalis untuk Node.js
- **dotenv** — Load environment variables dari file `.env`
- **cors** — Enable Cross-Origin Resource Sharing
- **helmet** — Set security HTTP headers otomatis
- **morgan** — HTTP request logger

Buat file `.env` di root project:

```env
PORT=3000
NODE_ENV=development
DB_URL=mongodb://localhost:27017/myapi
```

## Membuat Server Dasar

Buat file `index.js` sebagai entry point:

```javascript
require('dotenv').config();
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware global
app.use(helmet());
app.use(cors());
app.use(morgan('dev'));
app.use(express.json({ limit: '10mb' }));

// Health check
app.get('/', (req, res) => {
  res.json({ status: 'ok', message: 'API is running!' });
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
```

Jalankan dengan `node index.js`. Kalau muncul pesan "Server running", berarti setup berhasil!

## CRUD Operations Lengkap

CRUD (Create, Read, Update, Delete) adalah empat operasi dasar yang wajib ada di setiap API. Kita akan bikin endpoint untuk resource `users`:

```javascript
// Data dummy (nanti diganti database)
let users = [
  { id: 1, name: 'Budi', email: 'budi@mail.com' },
  { id: 2, name: 'Ani', email: 'ani@mail.com' },
];
let nextId = 3;

// READ - Ambil semua user
app.get('/api/v1/users', (req, res) => {
  const { page = 1, limit = 10 } = req.query;
  const start = (page - 1) * limit;
  const paginated = users.slice(start, start + Number(limit));

  res.json({
    total: users.length,
    page: Number(page),
    limit: Number(limit),
    data: paginated,
  });
});

// READ - Ambil satu user berdasarkan ID
app.get('/api/v1/users/:id', (req, res) => {
  const user = users.find(u => u.id === parseInt(req.params.id));
  if (!user) {
    return res.status(404).json({ error: 'User tidak ditemukan' });
  }
  res.json(user);
});

// CREATE - Buat user baru
app.post('/api/v1/users', (req, res) => {
  const { name, email } = req.body;
  if (!name || !email) {
    return res.status(400).json({ error: 'Name dan email wajib diisi' });
  }
  const newUser = { id: nextId++, name, email };
  users.push(newUser);
  res.status(201).json(newUser);
});

// UPDATE - Edit user yang sudah ada
app.put('/api/v1/users/:id', (req, res) => {
  const index = users.findIndex(u => u.id === parseInt(req.params.id));
  if (index === -1) {
    return res.status(404).json({ error: 'User tidak ditemukan' });
  }
  users[index] = { ...users[index], ...req.body };
  res.json(users[index]);
});

// DELETE - Hapus user
app.delete('/api/v1/users/:id', (req, res) => {
  const index = users.findIndex(u => u.id === parseInt(req.params.id));
  if (index === -1) {
    return res.status(404).json({ error: 'User tidak ditemukan' });
  }
  users.splice(index, 1);
  res.status(204).send();
});
```

Perhatikan kita pakai versioning `/api/v1/` di URL. Ini best practice supaya kalau nanti ada breaking change, versi lama tetap bisa jalan.

## Middleware: Jantungnya Express

Middleware adalah function yang berjalan **sebelum** request sampai ke handler. Kamu bisa pakai middleware untuk logging, autentikasi, validasi, atau mengubah request/response.

Contoh custom middleware untuk validasi API key:

```javascript
function apiKeyAuth(req, res, next) {
  const apiKey = req.headers['x-api-key'];
  if (apiKey !== process.env.API_KEY) {
    return res.status(401).json({ error: 'API key tidak valid' });
  }
  next();
}

// Terapkan ke route tertentu
app.get('/api/v1/users', apiKeyAuth, (req, res) => {
  // Hanya bisa diakses dengan API key yang valid
});
```

Middleware juga bisa dibuat untuk request logging custom:

```javascript
function requestLogger(req, res, next) {
  const start = Date.now();
  res.on('finish', () => {
    const duration = Date.now() - start;
    console.log(`${req.method} ${req.url} - ${res.statusCode} (${duration}ms)`);
  });
  next();
}

app.use(requestLogger);
```

## Error Handling yang Robust

Error handling yang baik memisahkan logic bisnis dari penanganan error. Gunakan centralized error handler:

```javascript
// 404 handler - kalau route nggak ketemu
app.use((req, res) => {
  res.status(404).json({ error: 'Endpoint tidak ditemukan' });
});

// Global error handler
app.use((err, req, res, next) => {
  console.error(err.stack);
  const statusCode = err.statusCode || 500;
  res.status(statusCode).json({
    error: err.message || 'Terjadi kesalahan pada server',
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack }),
  });
});
```

Untuk async handler, gunakan wrapper supaya error nggak tenggelam:

```javascript
const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

// Contoh pemakaian
app.get('/api/v1/users', asyncHandler(async (req, res) => {
  const users = await User.find();
  res.json(users);
}));
```

## Koneksi Database dengan MongoDB

Sekarang ganti data dummy dengan database sungguhan. Kita pakai **MongoDB** dengan ODM **Mongoose**:

```bash
npm install mongoose
```

Buat file `db.js`:

```javascript
const mongoose = require('mongoose');

async function connectDB() {
  try {
    await mongoose.connect(process.env.DB_URL);
    console.log('MongoDB connected');
  } catch (err) {
    console.error('Database connection failed:', err.message);
    process.exit(1);
  }
}

module.exports = connectDB;
```

Buat model `User.js`:

```javascript
const mongoose = require('mongoose');

const userSchema = new mongoose.Schema(
  {
    name: { type: String, required: true, trim: true },
    email: { type: String, required: true, unique: true, lowercase: true },
  },
  { timestamps: true }
);

module.exports = mongoose.model('User', userSchema);
```

Lalu refactor route handler untuk pakai database:

```javascript
const User = require('./models/User');

app.get('/api/v1/users', asyncHandler(async (req, res) => {
  const { page = 1, limit = 10 } = req.query;
  const users = await User.find()
    .skip((page - 1) * limit)
    .limit(Number(limit));
  const total = await User.countDocuments();
  res.json({ total, page: Number(page), data: users });
}));
```

## Testing API dengan Postman

Setelah API jalan, kamu perlu test semua endpoint. **Postman** adalah tool terpopuler untuk ini.

Langkah testing:

1. Buka Postman, buat collection baru bernama "My API"
2. Tambahkan request `GET http://localhost:3000/api/v1/users`
3. Tambahkan request `POST` dengan body JSON:
```json
{
  "name": "Sari",
  "email": "sari@mail.com"
}
```
4. Test `PUT` dan `DELETE` dengan ID yang valid dan tidak valid
5. Coba kirim request tanpa field yang wajib untuk test error handling

Postman juga punya fitur **Collection Runner** dan **Automated Tests**. Kamu bisa tulis test script langsung di Postman:

```javascript
pm.test("Status code is 200", () => {
  pm.response.to.have.status(200);
});

pm.test("Response has data array", () => {
  const json = pm.response.json();
  pm.expect(json).to.have.property('data');
});
```

## Security Best Practices

API yang exposed ke internet wajib diamankan. Berikut checklist keamanan yang wajib kamu terapkan:

- **Rate Limiting** — Batasi jumlah request per IP untuk mencegah DDoS. Pakai package `express-rate-limit`:
```javascript
const rateLimit = require('express-rate-limit');
app.use('/api/', rateLimit({ windowMs: 15 * 60 * 1000, max: 100 }));
```
- **Input Validation** — Validasi semua input user pakai `joi` atau `zod`. Jangan percaya input dari client
- **Helmet Headers** — Sudah kita pasang di awal. Ini set security headers seperti X-Content-Type-Options, X-Frame-Options, dll
- **Environment Variables** — Simpan semua rahasia (API key, DB password) di `.env`, **jangan pernah** di-commit ke Git
- **HTTPS** — Selalu pakai HTTPS di production. Pakai reverse proxy Nginx atau deploy di platform yang support SSL otomatis
- **Authentication** — Untuk API yang butuh login, pakai JWT (JSON Web Tokens) atau OAuth 2.0

## Deployment ke Cloud

Setelah API kamu beres dan ter-test, saatnya deploy ke production. Ada beberapa pilihan platform yang cocok untuk Express API:

### Railway (Recommended untuk Pemula)

Railway adalah platform PaaS yang paling simpel untuk deploy Node.js app. Cukup push ke GitHub, connect repository, dan Railway auto-detect Dockerfile atau langsung build dengan `npm start`.

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login dan deploy
railway login
railway init
railway up
```

Kelebihan Railway: built-in database PostgreSQL, environment variables langsung dari dashboard, custom domain gratis, dan auto-deploy setiap push ke `main`.

### Render

Alternatif lain yang mirip. Render punya free tier untuk web service, tapi cold start-nya bisa lambat (sampai 30 detik di free tier). Untuk production serius, pakai paket bayar yang mulai dari $7/bulan.

### VPS Manual (DigitalOcean, Vultr, Linode)

Untuk full control, deploy ke VPS dengan Nginx sebagai reverse proxy:

```nginx
server {
    listen 80;
    server_name api.myapp.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Gunakan **PM2** sebagai process manager untuk menjaga app tetap berjalan:

```bash
npm install -g pm2
pm2 start src/index.js --name my-api
pm2 startup   # Auto-start saat server reboot
pm2 save
```

## Versioning dan Documentation

API yang baik punya versioning dan dokumentasi yang jelas. Kamu sudah melihat kita pakai `/api/v1/` di URL. Untuk dokumentasi, pertimbangkan pakai **Swagger/OpenAPI**:

```bash
npm install swagger-ui-express swagger-jsdoc
```

Swagger UI generate halaman interaktif di `/api-docs` yang bisa dipakai developer lain untuk explore dan test API kamu tanpa perlu tools tambahan.

## FAQ

**Node.js atau Python untuk bikin REST API?**
Dua-duanya bagus. Node.js unggul di real-time dan I/O heavy tasks. Python unggul di data processing dan machine learning. Kalau kamu sudah familiar JavaScript, Node.js + Express adalah pilihan paling cepat untuk mulai.

**Berapa lama belajar bikin REST API dari nol?**
Kalau sudah paham JavaScript dasar, dalam 1-2 hari kamu bisa bikin API CRUD lengkap. Untuk benar-benar production-ready (auth, testing, deployment), butuh sekitar 1-2 minggu.

**Express atau Fastify?**
Express lebih mature dan ecosystem-nya lebih besar. Fastify lebih cepat dan punya built-in schema validation. Untuk pemula, mulai dari Express dulu. Kalau sudah nyaman, coba Fastify.

**Apakah perlu pakai TypeScript?**
Sangat disarankan! TypeScript membantu catch error sebelum runtime dan bikin codebase lebih maintainable. Di 2026, hampir semua project baru pakai TypeScript.

**Bagaimana cara deploy REST API?**
Paling mudah: **Railway** atau **Render** (gratis untuk project kecil). Push ke GitHub, connect repository, auto-deploy. Untuk production serius, pakai AWS EC2, Google Cloud Run, atau DigitalOcean.

## Kesimpulan

Bikin REST API dengan Node.js dan Express itu ternyata nggak serumit yang dibayangkan. Dari setup sampai punya API yang functional, kamu cuma butuh waktu beberapa jam. Tapi ingat—API yang **baik** itu bukan cuma yang jalan, tapi yang juga aman, terdokumentasi, dan mudah di-maintain.

Mulai dari project kecil. Bikin API untuk to-do list, catatan harian, atau apapun yang kamu butuhkan. Yang penting **mulai** dan **konsisten belajar**. Setelah basic-nya kuat, naik level ke authentication, testing otomatis, dan deployment ke cloud.

Kalau ada pertanyaan atau stuck di step tertentu, jangan ragu buat email aku di [kontak@dovi.my.id](mailto:kontak@dovi.my.id). Happy coding! 🚀
