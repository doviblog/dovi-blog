---
title: "Cara Build Telegram Bot dengan AI (Node.js + OpenAI)"
date: 2025-12-01
draft: false
slug: "cara-build-telegram-bot-ai-nodejs"
description: "Tutorial lengkap membuat Telegram bot dengan AI menggunakan Node.js dan OpenAI API. Cocok untuk pemula."
categories: ['Tutorial']
tags: ['telegram', 'bot', 'ai', 'nodejs', 'openai']
ShowShareButtons: true
ShowReadingTime: true
ShowToc: true
---

Telegram bot itu powerful banget, apalagi kalau dikasih AI. Bayangin punya bot yang bisa jawab pertanyaan, summarize artikel, bahkan nulis kode.

Di tutorial ini aku bakal ngejelasin cara bikin Telegram bot pakai Node.js dan OpenAI API. Dari nol sampai deploy ke server. Gak perlu pengalaman bikin bot sebelumnya — yang penting kamu familiar dengan JavaScript dasar.

Tutorial ini based on pengalaman aku bikin bot untuk komunitas developer Indonesia. Banyak yang pake bot semacam ini untuk customer support, virtual assistant, bahkan bot edukasi di grup-grup belajar coding.

## Kenapa Telegram Bot?

Sebelum lanjut, kenapa Telegram?

1. **API-nya gratis dan gampang** - BotFather bikin setup butuh 2 menit, gak perlu approval
2. **Gratis selamanya** - Gak kayak WhatsApp yang butuh WhatsApp Business API (bayar $500/bulan)
3. **Developer-friendly** - Webhook dan polling support, rich message format
4. **User base besar di Indonesia** - Banyak komunitas tech pakai Telegram
5. **Group support** - Bisa dipakai di grup, bukan cuma 1-on-1 chat
6. **Inline query** - User bisa manggil bot dari chat lain

Kalau kamu tertarik bikin bot juga di platform lain, cek tutorial [cara pasang ChatGPT di WhatsApp](/tutorial/cara-pasang-chatgpt-whatsapp) yang aku tulis sebelumnya.

## Persiapan

Sebelum mulai coding, siapkan semua ini:

1. **Telegram Bot Token** - Dapet dari @BotFather di Telegram
2. **OpenAI API Key** - Daftar di platform.openai.com, deposit kredit minimal $5 (sekitar Rp 78.000)
3. **Node.js 18+** - Download dari nodejs.org, pilih LTS version
4. **Code Editor** - VS Code, [Cursor AI](/tutorial/install-setup-cursor-ai-2025), atau editor apapun
5. **Terminal** - Command Prompt (Windows) atau Terminal (macOS/Linux)

### Biaya yang Dibutuhkan

Untuk tutorial ini, estimasi biaya:
- **Telegram Bot Token:** Rp 0 (gratis)
- **OpenAI API:** Rp 78.000 deposit, bisa tahan 2-4 bulan untuk bot pribadi
- **Hosting (opsional):** Rp 0-100.000/bulan tergantung provider
- **Total:** Rp 78.000 untuk mulai

Gak mahal. Cocok buat belajar dan prototyping.

## Step 1: Buat Bot di Telegram

Proses bikin bot cuma butuh 2 menit:

1. Buka Telegram, cari **@BotFather** (akun official Telegram untuk bikin bot)
2. Kirim perintah `/newbot`
3. BotFather minta **nama display** — ketik apa aja, misalnya "My AI Bot"
4. BotFather minta **username** — harus unik dan diakhiri dengan 'bot', misalnya "myaiassistant_bot"
5. **Simpan token** yang dikasih — format-nya kayak gini: `123456789:ABCdefGHIjklMNOpqrSTUvwxYZ`

Jangan share token ini ke siapapun. Siapa yang punya token bisa kendaliin bot kamu.

**Bonus commands yang berguna:**
- `/setdescription` — Kasih deskripsi bot (muncul saat user buka bot pertama kali)
- `/setabouttext` — Teks di halaman profil bot
- `/setuserpic` — Upload foto bot
- `/setcommands` — Daftar command yang user bisa lihat

Contoh setup commands:
```
start - Mulai chat dengan bot
clear - Hapus history chat
help - Tampilkan bantuan
image - Generate gambar dari teks
code - Generate code snippet
```

## Step 2: Setup Project

Buka terminal, jalankan perintah berikut:

```bash
mkdir my-ai-bot
cd my-ai-bot
npm init -y
npm install node-telegram-bot-api openai dotenv
```

**Penjelasan dependencies:**
- `node-telegram-bot-api` — Library untuk bikin Telegram bot (simple, promise-based)
- `openai` — Official OpenAI Node.js SDK
- `dotenv` — Load environment variables dari file `.env`

Buat file `.env` di root project:

```
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrSTUvwxYZ
OPENAI_API_KEY=sk-anti `sk-ant-xxx` dengan key dari OpenAI. **Wajib pakai .env, jangan hardcode di code.**

Buat `.gitignore`:
```
node_modules/
.env
```

## Step 3: Coding Bot

Buat file `bot.js` di root project:

```javascript
require('dotenv').config();
const TelegramBot = require('node-telegram-bot-api');
const OpenAI = require('openai');

// Initialize Telegram bot dengan polling mode
const bot = new TelegramBot(process.env.TELEGRAM_BOT_TOKEN, { polling: true });

// Initialize OpenAI client
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

// Storage untuk conversation history per user
// Di production, ganti ini dengan database (Redis/MongoDB)
const conversations = new Map();

// System prompt - personality bot kamu
const SYSTEM_PROMPT = `Kamu adalah asisten AI bernama "Dovi Bot".

Karakter:
- Ramah dan helpful, suka bantu orang
- Jawab dalam Bahasa Indonesia kecuali diminta bahasa lain
- Kasih jawaban yang jelas dan terstruktur
- Kalau ditanya coding, kasih contoh kode yang bisa langsung dipake
- Kalau gak tahu jawabannya, bilang jujur
- Jangan terlalu formal, tapi tetap sopan
- Pake sesedikit mungkin emoji`;

// ====== COMMAND HANDLERS ======

// Handle /start command
bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;
    const firstName = msg.from.first_name || 'User';
    
    // Initialize conversation
    conversations.set(chatId, []);
    
    const welcomeText = `Halo ${firstName}! 👋

Aku adalah AI Bot yang powered by ChatGPT.

*Command yang tersedia:*
/start - Mulai bot (reset history)
/clear - Hapus history chat
/help - Tampilkan bantuan
/image [prompt] - Generate gambar dari teks
/code [request] - Generate code snippet
/model [model] - Ganti model AI

Tinggal ketik pesan biasa untuk mulai chat! 🚀`;
    
    bot.sendMessage(chatId, welcomeText, { parse_mode: 'Markdown' });
    console.log(`[START] User ${firstName} (${chatId}) started the bot`);
});

// Handle /clear command
bot.onText(/\/clear/, (msg) => {
    const chatId = msg.chat.id;
    conversations.set(chatId, []);
    bot.sendMessage(chatId, '✅ History chat dihapus! Mulai dari awal.');
    console.log(`[CLEAR] History cleared for ${chatId}`);
});

// Handle /help command
bot.onText(/\/help/, (msg) => {
    const chatId = msg.chat.id;
    const helpText = `🤖 *Bantuan Bot*

*Cara pakai:*
Ketik pesan apa aja, dan AI bakal jawab.

*Commands:*
/start - Mulai ulang bot
/clear - Hapus history
/image [prompt] - Generate gambar
/code [request] - Generate kode
/model [model] - Ganti model (gpt-4o, gpt-4o-mini)

*Tips:*
- Ketik spesifik untuk hasil terbaik
- Bot ingat percakapan terakhir (10 pesan)
- Kirim /clear kalau mau mulai dari awal`;
    
    bot.sendMessage(chatId, helpText, { parse_mode: 'Markdown' });
});

// ====== MAIN MESSAGE HANDLER ======

bot.on('message', async (msg) => {
    const chatId = msg.chat.id;
    const userMessage = msg.text;
    
    // Skip commands (yang udah di-handle di atas)
    if (!userMessage || userMessage.startsWith('/')) return;
    
    // Initialize conversation history kalau belum ada
    if (!conversations.has(chatId)) {
        conversations.set(chatId, []);
    }
    
    // Tambah user message ke history
    const history = conversations.get(chatId);
    history.push({ role: 'user', content: userMessage });
    
    // Keep hanya 10 pesan terakhir (5 pasang user+assistant)
    // Ini buat hemat token dan hindari rate limit
    while (history.length > 10) {
        history.shift();
    }
    
    try {
        // Kirim typing indicator biar user tau bot lagi mikir
        bot.sendChatAction(chatId, 'typing');
        
        // Call OpenAI API
        const completion = await openai.chat.completions.create({
            model: 'gpt-4o-mini',
            messages: [
                { role: 'system', content: SYSTEM_PROMPT },
                ...history
            ],
            temperature: 0.7,
            max_tokens: 1000
        });
        
        const reply = completion.choices[0].message.content;
        const tokensUsed = completion.usage.total_tokens;
        
        // Simpan reply ke history
        history.push({ role: 'assistant', content: reply });
        
        // Kirim reply ke user
        // Telegram punya limit 4096 karakter per pesan
        if (reply.length > 4096) {
            // Split pesan panjang
            for (let i = 0; i < reply.length; i += 4096) {
                await bot.sendMessage(chatId, reply.substring(i, i + 4096), { parse_mode: 'Markdown' });
            }
        } else {
            await bot.sendMessage(chatId, reply, { parse_mode: 'Markdown' });
        }
        
        // Log untuk debugging
        console.log(`[OK] ${chatId} | Tokens: ${tokensUsed} | Msg: ${userMessage.substring(0, 50)}...`);
        
    } catch (error) {
        console.error('OpenAI Error:', error.message);
        
        // Handle error spesifik
        if (error.status === 429) {
            bot.sendMessage(chatId, '⏳ Terlalu banyak request. Tunggu 1 menit ya.');
        } else if (error.status === 500 || error.status === 503) {
            bot.sendMessage(chatId, '🔧 OpenAI lagi maintenance. Coba lagi nanti.');
        } else {
            bot.sendMessage(chatId, '❌ Maaf, ada error. Coba lagi nanti.');
        }
    }
});

console.log('🤖 Bot is running...');
console.log('Press Ctrl+C to stop');
```

### Penjelasan Code

Beberapa hal penting yang perlu dipahami:

1. **Polling vs Webhook:** Kita pakai polling (bot nanya ke Telegram server tiap beberapa detik). Simpler untuk development. Webhook lebih efisien tapi butuh HTTPS server.

2. **Conversation history:** Disimpan di memory (Map object). Ini hilang kalau bot restart. Untuk production, pakai database.

3. **Token limit:** Kita keep hanya 10 pesan terakhir. Ini hemat token OpenAI dan hindari error context window exceeded.

4. **Error handling:** Semua error ditangkap dengan pesan user-friendly. Error 429 (rate limit) beda handling-nya dari error lain.

## Step 4: Jalankan Bot

```bash
node bot.js
```

Kalau sukses, kamu bakal lihat:
```
🤖 Bot is running...
Press Ctrl+C to stop
```

Buka Telegram, cari bot kamu (pakai username yang tadi dibuat), dan mulai chat! Coba ketik "Halo" atau tanya sesuatu.

## Fitur Tambahan

### 1. Image Generation (/image command)

Tambahin command untuk generate gambar pakai DALL-E:

```javascript
bot.onText(/\/image (.+)/, async (msg, match) => {
    const chatId = msg.chat.id;
    const prompt = match[1];
    
    try {
        bot.sendChatAction(chatId, 'upload_photo');
        bot.sendMessage(chatId, '🎨 Generating gambar...');
        
        const image = await openai.images.generate({
            model: "dall-e-3",
            prompt: prompt,
            n: 1,
            size: "1024x1024",
            quality: "standard"
        });
        
        await bot.sendPhoto(chatId, image.data[0].url, {
            caption: `🎨 Generated: "${prompt}"`
        });
        
        console.log(`[IMAGE] ${chatId}: ${prompt}`);
    } catch (error) {
        console.error('Image Error:', error.message);
        if (error.status === 400) {
            bot.sendMessage(chatId, '❌ Prompt terlalu sensitif. Coba prompt yang lain.');
        } else {
            bot.sendMessage(chatId, '❌ Gagal generate image. Coba lagi.');
        }
    }
});
```

Biaya DALL-E 3: $0.04 per gambar (≈ Rp 630). Cukup murah untuk usage biasa.

### 2. Code Generation (/code command)

```javascript
bot.onText(/\/code (.+)/, async (msg, match) => {
    const chatId = msg.chat.id;
    const request = match[1];
    
    try {
        bot.sendChatAction(chatId, 'typing');
        
        const completion = await openai.chat.completions.create({
            model: 'gpt-4o-mini',
            messages: [
                {
                    role: 'system',
                    content: `Generate clean, well-commented code based on the request. 
                    Wrap code in markdown code blocks with language identifier.
                    Include brief explanation in Bahasa Indonesia.`
                },
                { role: 'user', content: request }
            ],
            max_tokens: 2000
        });
        
        const reply = completion.choices[0].message.content;
        
        // Split kalau terlalu panjang
        if (reply.length > 4096) {
            for (let i = 0; i < reply.length; i += 4096) {
                await bot.sendMessage(chatId, reply.substring(i, i + 4096), { parse_mode: 'Markdown' });
            }
        } else {
            await bot.sendMessage(chatId, reply, { parse_mode: 'Markdown' });
        }
    } catch (error) {
        bot.sendMessage(chatId, '❌ Error generating code.');
    }
});
```

### 3. Rate Limiting

Untuk bot yang dipakai banyak orang, rate limiting wajib:

```javascript
const rateLimit = new Map();

function checkRateLimit(userId, maxRequests = 10, windowMs = 60000) {
    const now = Date.now();
    
    if (!rateLimit.has(userId)) {
        rateLimit.set(userId, []);
    }
    
    // Hapus request yang udah expired
    const timestamps = rateLimit.get(userId).filter(t => now - t < windowMs);
    rateLimit.set(userId, timestamps);
    
    if (timestamps.length >= maxRequests) {
        return false; // Rate limited
    }
    
    timestamps.push(now);
    return true; // OK
}

// Tambahin di awal message handler:
// if (!checkRateLimit(msg.from.id)) {
//     bot.sendMessage(chatId, '⚠️ Terlalu banyak request! Tunggu 1 menit.');
//     return;
// }
```

Rate limit 10 pesan per menit per user itu fair untuk bot personal. Sesuaikan kalau butuh.

## Deploy ke Production

### Pakai PM2 (Recommended untuk VPS)

PM2 bikin bot jalan terus, auto-restart kalau crash, dan manage logs.

```bash
# Install PM2 globally
npm install -g pm2

# Jalankan bot
pm2 start bot.js --name "ai-telegram-bot"

# Lihat status
pm2 status

# Lihat logs
pm2 logs ai-telegram-bot

# Auto-start saat server restart
pm2 startup
pm2 save
```

### Pakai Docker

Kalau prefer containerized deployment:

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
CMD ["node", "bot.js"]
```

```bash
# Build image
docker build -t ai-telegram-bot .

# Jalankan container
docker run -d \
  --restart unless-stopped \
  --name ai-telegram-bot \
  --env-file .env \
  ai-telegram-bot
```

### Pilihan Hosting

Untuk developer Indonesia, beberapa pilihan:

1. **VPS DigitalOcean** — $6/bulan (≈ Rp 94.000), simple dan reliable
2. **Vultr** — $6/bulan, server di Singapur (latency rendah ke Indonesia)
3. **Biznet Gio** — Mulai Rp 50.000/bulan, provider Indonesia
4. **Rumahweb** — VPS Indonesia mulai Rp 60.000/bulan
5. **Oracle Cloud Free Tier** — GRATIS selamanya (1 OCPU + 1GB RAM), cukup untuk bot kecil

Rekomendasi aku: mulai dengan **Oracle Cloud Free Tier** karena gratis dan powerful enough untuk bot personal. Upgrade ke paid VPS kalau bot-nya dipakai banyak orang.

## Monitoring dan Logging

Untuk production, tambahin logging yang proper:

```javascript
const fs = require('fs');

function log(level, message, data = {}) {
    const timestamp = new Date().toISOString();
    const logEntry = {
        timestamp,
        level,
        message,
        ...data
    };
    
    console.log(JSON.stringify(logEntry));
    
    // Simpan ke file (opsional)
    fs.appendFileSync('bot.log', JSON.stringify(logEntry) + '\n');
}

// Pakai di mana-mana:
// log('info', 'Message received', { userId: chatId, message: userMessage });
// log('error', 'OpenAI failed', { error: error.message, status: error.status });
```

## Tips Penting

1. **Jangan spam** - Telegram bisa ban bot yang kirim terlalu banyak pesan. Max 30 pesan per detik ke chat berbeda, 20 pesan per menit ke grup yang sama.

2. **Handle error dengan grace** - Selalu wrap API call di try-catch. User gak perlu tau technical detail error.

3. **Clear history** - Kasih command `/clear` biar user bisa reset. Berguna kalau bot mulai ngasih jawaban gak relevan karena context lama.

4. **Logging** - Log semua request untuk debugging. Tapi jangan log data sensitif.

5. **Environment variables** - Jangan hardcode token di code. Selalu pakai `.env` file.

6. **Database untuk production** - Map object hilang saat restart. Pakai Redis atau SQLite untuk persistence.

7. **Graceful shutdown** - Handle SIGINT/SIGTERM untuk cleanup:
```javascript
process.on('SIGINT', () => {
    console.log('Bot shutting down...');
    process.exit(0);
});
```

## Troubleshooting

**Bot gak respon?**
- Cek token di `.env` bener (ada angka + colon + huruf)
- Pastiin polling: `{ polling: true }`
- Cek OpenAI credit di dashboard (mungkin habis)
- Lihat terminal untuk error message

**Error 429 (Rate Limit)?**
- Kurangi request frequency
- Implement rate limiting (lihat code di atas)
- Upgrade OpenAI plan di platform.openai.com
- Pakai model yang lebih murah (gpt-4o-mini)

**Token limit exceeded / Error 400?**
- Kurangi conversation history (ubah limit dari 10 ke 6)
- Kurangi `max_tokens` di API call
- Summarize old messages (advanced)

**Bot kena banned Telegram?**
- Jangan spam ke user yang gak approve
- Jangan kirim promotional messages
- Ikuti Telegram Bot Policy

**Markdown gak render?**
- Pastiin `parse_mode: 'Markdown'` di sendMessage
- Escape special characters: `_`, `*`, `[`, `` ` ``
- Untuk code block, pakai triple backtick

## FAQ

**Q: Berapa biaya bulanan untuk bot personal?**
A: Untuk 1-2 user dengan pemakaian wajar (20-50 chat/hari), sekitar Rp 15.000-30.000/bulan pakai GPT-4o-mini. Hosting bisa pakai Oracle Cloud Free Tier = Rp 0. Total: Rp 15.000-30.000/bulan.

**Q: Bisa dipakai di grup Telegram?**
A: Bisa! Tapi bot perlu di-add ke grup dulu, dan di-set privacy ke false lewat @BotFather. Tambahin pengecekan `if (msg.chat.type === 'group')` untuk handle grup berbeda dari 1-on-1.

**Q: Bisa pakai model selain OpenAI?**
A: Bisa. Ganti SDK OpenAI dengan provider lain: Anthropic (Claude), Google (Gemini), atau model open-source lewat Together AI / Groq. API-nya mirip-mirip format-nya.

**Q: Apakah data chat disimpan oleh OpenAI?**
A: Secara default, data dipakai untuk training. Kamu bisa nonaktifkan di Settings → Data Controls. Untuk privacy lebih baik, self-host model pakai Ollama.

**Q: Bisa deploy di shared hosting?**
A: Gak recommended. Telegram bot butuh process yang jalan terus. Pakai VPS atau platform kayak Railway ($5/bulan) atau Fly.io (free tier ada).

**Q: Gimana cara update bot tanpa downtime?**
A: Pakai PM2 cluster mode, atau Docker rolling update. Untuk simple: `pm2 restart ai-telegram-bot` — restart cuma butuh 2-3 detik.

## Kesimpulan

Membuat Telegram bot dengan AI itu straightforward. Dalam 30 menit kamu udah punya bot yang functional dan bisa dipakai.

**Kunci sukses:**
1. Mulai simple, fitur dasar dulu
2. Tambahin fitur bertahap (image gen, code gen, dll)
3. Deploy ke server biar 24/7 online
4. Monitor logs dan handle error dengan baik
5. Investasi di rate limiting dan security

Bot ini bukan cuma untuk belajar — bisa jadi real product. Beberapa developer Indonesia udah monetize bot-nya dengan model langganan (Rp 20.000-50.000/bulan per user). Pasar untuk bahasa Indonesia belum se-saturated bahasa Inggris.

Next steps:
- Tambahin fitur voice message → speech-to-text
- Integrate sama tools lain (weather API, news API)
- Buat admin panel untuk manage users
- Tambahin subscription model untuk monetize

**Need help?** DM aku di Telegram [@dovi](https://t.me/dovi)
