---
title: "Cara Pasang ChatGPT di WhatsApp (Tutorial 2025)"
date: 2025-11-16
draft: false
slug: "cara-pasang-chatgpt-whatsapp"
description: "Tutorial lengkap cara pasang ChatGPT di WhatsApp 2025. 3 cara: bot siap pakai, bot sendiri, dan no-code platform."
categories: ['Tutorial']
tags: ['chatgpt', 'whatsapp', 'bot', 'tutorial']
ShowShareButtons: true
ShowReadingTime: true
ShowToc: true
---

Siapa yang gak mau ChatGPT langsung di WhatsApp? Ribet harus buka browser atau app terpisah.

Nah, di tutorial ini aku bakal ngejelasin cara pasang ChatGPT di WhatsApp. Gampang banget, cuma butuh 15 menit.

Aku sendiri udah coba semua metode yang aku bahas di sini, dan masing-masing punya kelebihan serta kekurangan tergantung kebutuhan kamu. Kalau cuma butuh jawaban cepat偶尔, pakai bot siap pakai udah cukup. Tapi kalau mau full control dan fitur custom, bikin bot sendiri jauh lebih worth it di long run.

## Yang Perlu Disiapin

Sebelum mulai, pastikan semua ini udah ready:

1. **HP Android/iOS** - Pastiin WhatsApp udah update ke versi terbaru
2. **Akun OpenAI** - Daftar gratis di platform.openai.com
3. **API Key** - Dapet dari dashboard OpenAI setelah daftar
4. **Node.js** (opsional) - Untuk setup bot sendiri, download dari nodejs.org
5. **VPS/Server** (opsional) - Kalau mau bot jalan 24/7, bisa pakai VPS murah sekitar Rp 50.000-100.000/bulan

### Soal Biaya OpenAI API

Banyak yang nanya soal ini. OpenAI API itu bayar pakai kredit, bukan subscription bulanan. Kamu deposit dulu (mulai dari $5 atau sekitar Rp 78.000), terus dipotong per pemakaian. Untuk bot WhatsApp ringan, Rp 50.000 bisa tahan sebulan lebih kalau gak spam.

Kalau mau yang beneran gratis, ada opsi pakai model open-source seperti Llama atau Mistral lewat provider seperti Together AI atau Groq. Tapi kualitasnya tentu beda sama GPT-4.

## Cara 1: Pakai Bot Siap Pakai (Gampang)

Ini cara paling cepat buat kamu yang cuma mau coba-coba atau butuh ChatGPT di WhatsApp tanpa ribet setup.

### Langkah-langkah:

1. **Save nomor bot** - Tambahin kontak: +1 (XXX) XXX-XXXX (contoh: TEFBOTS atau bot lain yang tersedia)
2. **Buka WhatsApp** - Kirim pesan ke nomor bot yang udah disave
3. **Ketik `/start`** - Untuk mulai sesi chat
4. **Ikuti instruksi** - Bot bakal guide kamu step by step
5. **Mulai chat** - Kirim pertanyaan apa aja, bot bakal respon pakai AI

**Kelebihan:**
- Gratis (ada limit harian, biasanya 10-50 pesan/hari)
- Gak perlu coding sama sekali
- Langsung dipakai dalam 2 menit
- Cocok buat coba-coba dulu sebelum commitment

**Kekurangan:**
- Rate limit ketat, kadang cuma 10 pesan/hari
- Kadang slow karena banyak user sharing server
- Fitur terbatas, gak bisa custom system prompt
- Data kamu di-process di server orang lain
- Bot bisa tiba-tiba mati kalau provider tutup

**Tips:** Kalau mau pakai cara ini, jangan pakai bot yang minta data pribadi berlebihan. Cukup yang minta nomor WhatsApp aja. Kalau ada yang minta password atau data bank, langsung skip.

## Cara 2: Bikin Bot Sendiri (Lebih Bebas)

Ini cara yang aku recommend kalau mau serius. Kamu punya full control: bisa custom prompt, set limit sendiri, bahkan tambahin fitur kayak voice message atau image recognition.

### Step 1: Setup Project

Buka terminal, ketik:

```bash
mkdir chatgpt-whatsapp
cd chatgpt-whatsapp
npm init -y
npm install @whiskeysockets/baileys openai qrcode-terminal dotenv
```

Pastikan Node.js versi 18 atau lebih baru udah terinstall. Kalau belum, download dulu dari [nodejs.org](https://nodejs.org).

### Step 2: Buat Bot

Buat file `bot.js` di dalam folder project:

```javascript
const { Boom } = require('@hapi/boom');
const { default: makeWASocket, useMultiFileAuthState, DisconnectReason } = require('@whiskeysockets/baileys');
const OpenAI = require('openai');
const qrcode = require('qrcode-terminal');
require('dotenv').config();

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

// Simpan conversation history per user
const conversations = new Map();

async function startBot() {
    const { state, saveCreds } = await useMultiFileAuthState('auth_info');
    
    const sock = makeWASocket({
        auth: state,
        printQRInTerminal: true,
        // Limit biar gak spam
        maxCachedMessages: 5
    });
    
    sock.ev.on('creds.update', saveCreds);
    
    sock.ev.on('connection.update', (update) => {
        const { connection, lastDisconnect, qr } = update;
        if (qr) {
            console.log('Scan QR code ini pakai WhatsApp kamu:');
            qrcode.generate(qr, { small: true });
        }
        if (connection === 'close') {
            const shouldReconnect = (lastDisconnect?.error)?.output?.statusCode !== DisconnectReason.loggedOut;
            console.log('Connection closed. Reconnecting:', shouldReconnect);
            if (shouldReconnect) {
                startBot();
            }
        } else if (connection === 'open') {
            console.log('Bot connected! Siap menerima pesan.');
        }
    });
    
    sock.ev.on('messages.upsert', async ({ messages }) => {
        const msg = messages[0];
        if (!msg.key.fromMe && msg.message?.conversation) {
            const userMessage = msg.message.conversation;
            const userId = msg.key.remoteJid;
            
            // Handle command /clear
            if (userMessage === '/clear') {
                conversations.delete(userId);
                await sock.sendMessage(userId, { text: '✅ History dihapus!' });
                return;
            }
            
            // Handle command /help
            if (userMessage === '/help') {
                const helpText = '🤖 *ChatGPT Bot*\n\n' +
                    'Ketik pesan apa aja untuk chat.\n' +
                    '/clear - Hapus history\n' +
                    '/help - Tampilkan bantuan';
                await sock.sendMessage(userId, { text: helpText });
                return;
            }
            
            // Initialize conversation
            if (!conversations.has(userId)) {
                conversations.set(userId, []);
            }
            
            // Tambah user message ke history
            const history = conversations.get(userId);
            history.push({ role: 'user', content: userMessage });
            
            // Keep hanya 10 pesan terakhir biar gak kehabisan token
            if (history.length > 10) {
                history.splice(0, history.length - 10);
            }
            
            try {
                const completion = await openai.chat.completions.create({
                    model: 'gpt-3.5-turbo',
                    messages: [
                        { role: 'system', content: 'Kamu adalah asisten AI yang helpful. Jawab dalam Bahasa Indonesia.' },
                        ...history
                    ],
                    max_tokens: 500,
                    temperature: 0.7
                });
                
                const reply = completion.choices[0].message.content;
                
                // Simpan reply ke history
                history.push({ role: 'assistant', content: reply });
                
                await sock.sendMessage(userId, { text: reply });
                console.log(`[OK] ${userId}: ${userMessage.substring(0, 50)}...`);
            } catch (error) {
                console.error('Error:', error.message);
                await sock.sendMessage(userId, { text: '❌ Maaf, ada error. Coba lagi nanti.' });
            }
        }
    });
}

startBot();
```

### Step 3: Setup Environment

Buat file `.env` di root project:

```
OPENAI_API_KEY=sk-your-api-key-here
```

Ganti `sk-your-api-key-here` dengan API key dari dashboard OpenAI. **Jangan pernah commit file .env ke GitHub.** Tambahin `.env` ke file `.gitignore`.

### Step 4: Jalankan Bot

```bash
node bot.js
```

Scan QR code yang muncul di terminal pakai WhatsApp kamu. Caranya: buka WhatsApp > klik tiga titik > Linked Devices > Link a Device.

Kalau QR code udah di-scan, bot bakal langsung nyala dan siap nerima pesan.

### Step 5: Deploy ke Server (Biar 24/7 Online)

Kalau cuma dijalankan di laptop, bot bakal mati kalau laptop dimatikan. Untuk bot yang selalu online, deploy ke VPS:

**Pakai PM2 (Recommended):**
```bash
npm install -g pm2
pm2 start bot.js --name "chatgpt-wa"
pm2 save
pm2 startup
```

**Pakai Docker:**
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
CMD ["node", "bot.js"]
```

VPS murah yang bisa dipakai: DigitalOcean (mulai $6/bulan ≈ Rp 94.000), atau provider lokal seperti Biznet Gio (mulai Rp 50.000/bulan).

Kalau kamu tertarik bikin bot yang lebih canggih, coba juga tutorial [cara build Telegram bot AI](/tutorial/cara-build-telegram-bot-ai-nodejs) di blog ini.

## Cara 3: Pakai Platform No-Code

Kalau gak mau coding sama sekali, beberapa platform bisa bantu kamu bikin bot tanpa nulis kode:

1. **Botpress** - Visual flow builder, free tier tersedia. Cocok untuk bot yang butuh decision tree.
2. **WATI** - WhatsApp Business API official partner. Mulai dari Rp 500.000/bulan, cocok untuk bisnis.
3. **Landbot** - Drag and drop builder dengan WhatsApp integration. Free trial tersedia.
4. **Chatfuel** - Popular untuk e-commerce, mulai dari $15/bulan (≈ Rp 235.000).

**Kelebihan:** Gak perlu coding sama sekali, bisa langsung jadi dalam hitungan jam.
**Kekurangan:** Biasanya bayar (mulai Rp 200.000-500.000/bulan), fitur terbatas, dan kamu gak punya full control atas data.

## Tips Penting

### 1. Rate Limit dan Biaya

OpenAI punya rate limit yang harus diperhatiin:

- **GPT-3.5-turbo:** 3 RPM (requests per minute), 200 RPM per account
- **GPT-4:** 10 RPM, 10.000 RPM per account

Kalau kelewatan, kamu kena error 429. Artinya request kamu ditolak sementara.

Soal biaya (per 2025):
- GPT-3.5-turbo: $0.0005 / 1K tokens input, $0.0015 / 1K tokens output
- GPT-4o: $2.50 / 1M tokens input, $10 / 1M tokens output
- GPT-4o-mini: $0.15 / 1M tokens input, $0.60 / 1M tokens output

Rata-rata chat WhatsApp: 100-200 tokens. Kalau pakai GPT-4o-mini, biaya per chat cuma sekitar Rp 0.1-0.3. Sangat murah!

Untuk bot pribadi yang dipake sendiri atau keluarga, budget Rp 20.000-50.000/bulan udah lebih dari cukup.

### 2. Privacy dan Keamanan

Ini penting banget. Semua pesan yang kamu kirim ke bot bakal diproses di server OpenAI:

- **Jangan share** data sensitif: nomor kartu kredit, password, data rekening
- **Jangan kirim** foto KTP atau dokumen penting ke bot
- **Bisa nonaktif** training data di dashboard OpenAI (Settings > Data Controls > Improve model)
- Kalau bot sendiri, pertimbangin pakai **self-hosted model** seperti Ollama untuk privasi maksimal

### 3. Error Handling yang Proper

Selalu handle error biar bot gak crash mendadak:

```javascript
try {
    const reply = await getChatGPTReply(message);
    await sendMessage(reply);
} catch (error) {
    console.error('Error:', error);
    if (error.status === 429) {
        await sendMessage('⏳ Terlalu banyak request. Tunggu 1 menit ya.');
    } else if (error.status === 500) {
        await sendMessage('🔧 OpenAI lagi maintenance. Coba lagi nanti.');
    } else {
        await sendMessage('❌ Maaf, ada masalah. Coba lagi nanti.');
    }
}
```

### 4. Custom System Prompt

Salah satu kelebihan bikin bot sendiri adalah bisa custom system prompt. Ini contoh yang aku pakai:

```javascript
const systemPrompt = `Kamu adalah asisten AI bernama "Dovi Bot".

Karakter:
- Ramah dan helpful
- Jawab dalam Bahasa Indonesia kecuali diminta bahasa lain
- Kasih jawaban yang singkat dan to the point untuk WhatsApp
- Kalau ditanya sesuatu yang gak kamu tahu, bilang aja jujur

Kamu dibuat oleh developer Indonesia. Jangan pakai emoji berlebihan.`;
```

Dengan custom prompt, bot kamu jadi punya personality sendiri dan gak generic kayak bot bawaan.

## Troubleshooting

**Bot gak nyala?**
- Cek API key bener (ada `sk-` di depannya)
- Pastiin WhatsApp version update ke versi terbaru
- Restart bot: `Ctrl+C` lalu `node bot.js` lagi
- Cek余额 OpenAI di dashboard

**QR code gak muncul?**
- Delete folder `auth_info` lalu jalankan ulang
- Pastiin koneksi internet stabil
- Coba pakai terminal yang beda

**Response lambat?**
- Ganti model ke GPT-4o-mini (lebih cepat dari GPT-4)
- Cek koneksi internet di server/laptop
- Reduce `max_tokens` di API call (misal dari 1000 ke 500)
- Kalau pakai VPS, cek apakah server lagi load tinggi

**Bot disconnect dari WhatsApp?**
- Biasanya terjadi kalau pakai WhatsApp di HP yang sama
- Re-scan QR code
- Pastiin gak ada device lain yang login ke akun yang sama

## FAQ

**Q: Apakah pakai bot ini legal?**
A: Secara teknis, pakai unofficial API WhatsApp melanggar ToS WhatsApp. Tapi untuk penggunaan pribadi, risikonya kecil. Kalau untuk bisnis, pertimbangin pakai WhatsApp Business API official.

**Q: Berapa biaya bulanan untuk bot pribadi?**
A: Untuk pemakaian ringan (10-20 chat/hari), sekitar Rp 15.000-30.000/bulan pakai GPT-4o-mini. Kalau pakai GPT-4, bisa Rp 100.000-200.000/bulan.

**Q: Bisa dipakai di grup WhatsApp?**
A: Bisa, tapi perlu modifikasi kode. Tambahin pengecekan `msg.key.remoteJid.endsWith('@g.us')` untuk detect grup. Perlu hati-hati biar bot gak spam di grup.

**Q: Model AI apa yang recommended?**
A: Untuk WhatsApp, GPT-4o-mini balance paling bagus antara kualitas dan biaya. Kalau butuh jawaban lebih cerdas, pakai GPT-4o.

**Q: Apakah pesan saya disimpan OpenAI?**
A: Secara default, ya. Tapi kamu bisa nonaktifkan di Settings > Data Controls > "Improve the model for everyone." Kalau privacy concern, pertimbangin pakai model self-hosted.

## Kesimpulan

Cara paling gampang pakai ChatGPT di WhatsApp itu pakai bot siap pakai. Tapi kalau mau lebih bebas, bikin bot sendiri lebih worth it di long run. Dengan budget Rp 50.000/bulan, kamu udah bisa punya AI assistant pribadi langsung di WhatsApp.

Kalau tertarik bikin bot di platform lain, coba juga tutorial [cara build Telegram bot AI](/tutorial/cara-build-telegram-bot-ai-nodejs) yang udah aku tulis di blog ini.

**Butuh bantuan?** Chat aku di Telegram [@dovi](kontak@dovi.my.id)
