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

Di tutorial ini aku bakal ngejelasin cara bikin Telegram bot pakai Node.js dan OpenAI API.

## Persiapan

1. **Telegram Bot Token** - Dapet dari @BotFather
2. **OpenAI API Key** - Dari platform.openai.com
3. **Node.js 18+** - Sudah terinstall
4. **Code Editor** - VS Code atau sejenisnya

## Step 1: Buat Bot di Telegram

1. Buka Telegram, cari **@BotFather**
2. Kirim `/newbot`
3. Kasih nama bot (misal: "My AI Bot")
4. Kasih username (harus unik, diakhiri 'bot')
5. Simpan token yang dikasih

## Step 2: Setup Project

```bash
mkdir my-ai-bot
cd my-ai-bot
npm init -y
npm install node-telegram-bot-api openai dotenv
```

Buat file `.env`:

```
TELEGRAM_BOT_TOKEN=your-telegram-token
OPENAI_API_KEY=sk-your-openai-key
```

## Step 3: Coding Bot

Buat file `bot.js`:

```javascript
require('dotenv').config();
const TelegramBot = require('node-telegram-bot-api');
const OpenAI = require('openai');

// Initialize
const bot = new TelegramBot(process.env.TELEGRAM_BOT_TOKEN, { polling: true });
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

// Storage for conversation history (per user)
const conversations = {};

// Handle /start command
bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;
    conversations[chatId] = [];
    bot.sendMessage(chatId, 
        'Halo! 👋 Aku AI Bot. Kirim pesan apa aja dan aku akan jawab pakai AI.

' +
        'Ketik /clear untuk clear history.'
    );
});

// Handle /clear command
bot.onText(/\/clear/, (msg) => {
    const chatId = msg.chat.id;
    conversations[chatId] = [];
    bot.sendMessage(chatId, '✅ History cleared!');
});

// Handle all messages
bot.on('message', async (msg) => {
    const chatId = msg.chat.id;
    const userMessage = msg.text;
    
    // Skip commands
    if (userMessage.startsWith('/')) return;
    
    // Initialize conversation history
    if (!conversations[chatId]) {
        conversations[chatId] = [];
    }
    
    // Add user message to history
    conversations[chatId].push({ role: 'user', content: userMessage });
    
    // Keep only last 10 messages to avoid token limit
    if (conversations[chatId].length > 10) {
        conversations[chatId] = conversations[chatId].slice(-10);
    }
    
    try {
        // Show typing indicator
        bot.sendChatAction(chatId, 'typing');
        
        // Call OpenAI API
        const completion = await openai.chat.completions.create({
            model: 'gpt-4',
            messages: [
                { role: 'system', content: 'Kamu adalah asisten AI yang helpful dan ramah. Jawab dalam Bahasa Indonesia.' },
                ...conversations[chatId]
            ],
            temperature: 0.7,
            max_tokens: 1000
        });
        
        const reply = completion.choices[0].message.content;
        
        // Add reply to history
        conversations[chatId].push({ role: 'assistant', content: reply });
        
        // Send reply
        bot.sendMessage(chatId, reply);
        
    } catch (error) {
        console.error('OpenAI Error:', error);
        bot.sendMessage(chatId, '❌ Maaf, ada error. Coba lagi nanti.');
    }
});

console.log('🤖 Bot is running...');
```

## Step 4: Jalankan Bot

```bash
node bot.js
```

Buka Telegram, cari bot kamu, dan mulai chat!

## Fitur Tambahan

### 1. Image Generation

```javascript
bot.onText(/\/image (.+)/, async (msg, match) => {
    const chatId = msg.chat.id;
    const prompt = match[1];
    
    try {
        const image = await openai.images.generate({
            model: "dall-e-3",
            prompt: prompt,
            n: 1,
            size: "1024x1024"
        });
        
        bot.sendPhoto(chatId, image.data[0].url);
    } catch (error) {
        bot.sendMessage(chatId, '❌ Gagal generate image.');
    }
});
```

### 2. Code Highlighting

```javascript
bot.onText(/\/code (.+)/, async (msg, match) => {
    const chatId = msg.chat.id;
    const request = match[1];
    
    try {
        const completion = await openai.chat.completions.create({
            model: 'gpt-4',
            messages: [
                { role: 'system', content: 'Generate code based on request. Wrap in ```codeblock.' },
                { role: 'user', content: request }
            ]
        });
        
        bot.sendMessage(chatId, completion.choices[0].message.content, { parse_mode: 'Markdown' });
    } catch (error) {
        bot.sendMessage(chatId, '❌ Error generating code.');
    }
});
```

### 3. Rate Limiting

```javascript
const rateLimit = {};

function checkRateLimit(userId) {
    const now = Date.now();
    if (!rateLimit[userId]) {
        rateLimit[userId] = [];
    }
    
    // Remove messages older than 1 minute
    rateLimit[userId] = rateLimit[userId].filter(t => now - t < 60000);
    
    if (rateLimit[userId].length >= 5) {
        return false; // Rate limited
    }
    
    rateLimit[userId].push(now);
    return true; // OK
}

// Use in message handler:
if (!checkRateLimit(msg.from.id)) {
    bot.sendMessage(chatId, '⚠️ Rate limit! Tunggu 1 menit.');
    return;
}
```

## Deploy ke Production

### Pakai PM2

```bash
npm install -g pm2
pm2 start bot.js --name "ai-bot"
pm2 save
pm2 startup
```

### Pakai Docker

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
CMD ["node", "bot.js"]
```

```bash
docker build -t ai-bot .
docker run -d --restart unless-stopped --name ai-bot ai-bot
```

## Tips Penting

1. **Jangan spam** - Telegram bisa ban bot yang spam
2. **Handle error** - Selalu wrap API call di try-catch
3. **Clear history** - Kasih command `/clear` biar user bisa reset
4. **Logging** - Log semua request untuk debugging
5. **Environment variables** - Jangan hardcode token di code

## Troubleshooting

**Bot gak respon?**
- Cek token bener
- Pastiin polling active
- Check OpenAI credit

**Error 429 (Rate Limit)?**
- Kurangi request frequency
- Implement rate limiting
- Upgrade OpenAI plan

**Token limit exceeded?**
- Keep conversation history minimal
- Use `max_tokens` parameter
- Summarize old messages

## Kesimpulan

Membuat Telegram bot dengan AI itu straightforward. Dalam 30 menit kamu udah punya bot yang functional.

Next steps:
- Tambahin lebih banyak commands
- Integrate sama tools lain (weather, news, etc.)
- Deploy ke cloud biar 24/7 online

**Need help?** DM aku di Telegram [@dovi](https://t.me/dovi)
