---
title: "Cara Membuat AI Agent Pertama Kamu dari Nol (Tutorial Lengkap)"
date: 2025-10-25
draft: false
slug: "cara-membuat-ai-agent-pertama"
description: "Tutorial lengkap membuat AI agent dari nol menggunakan Python dan OpenAI API. Cocok untuk pemula yang mau belajar AI."
categories: ['AI Agent', 'Tutorial']
tags: ['ai-agent', 'python', 'openai', 'tutorial']
ShowShareButtons: true
ShowReadingTime: true
ShowToc: true
---

Pernah kebayang gak sih punya AI agent yang bisa ngerjain tugas-tugas kamu secara otomatis? Kayak punya asisten pribadi yang gak pernah capek dan bisa kerja 24 jam non-stop.

Nah, di tutorial kali ini, aku bakal ngejelasin cara bikin AI agent dari nol. Gak perlu jadi expert coding kok, yang penting mau belajar. Tutorial ini dibuat buat developer Indonesia yang mau masuk ke dunia AI agent tanpa ribet.

## AI Agent Itu Apa Sih?

Jadi gini, AI agent itu program yang bisa ngambil keputusan sendiri berdasarkan input yang dia terima. Bedanya sama chatbot biasa, AI agent itu bisa:

- **Ngeksekusi tugas** langsung (bukan cuma ngasih jawaban)
- **Ngehubungin sama tools lain** (API, database, file system)
- **Nge-learn dari interaksi** sebelumnya
- **Bikin keputusan** secara otonom berdasarkan konteks

Contoh simple: kalau chatbot cuma bisa jawab "cara reset password itu klik link di email", AI agent bisa langsung trigger reset password email ke user. Gak cuma jawab pertanyaan, tapi langsung ngasih solusi.

Kalau kamu penasaran tentang berbagai framework yang bisa dipakai untuk bikin AI agent, baca [5 framework AI agent terbaik](/ai-agent/5-framework-ai-agent-terbaik-2025/) yang udah aku review sebelumnya.

### Jenis-Jenis AI Agent

Sebelum mulai coding, penting buat tau bahwa ada beberapa jenis AI agent:

1. **Simple Reflex Agent** — Respon langsung berdasarkan input. Paling sederhana, seperti chatbot sederhana yang memberi jawaban dari keyword tertentu.
2. **Model-Based Agent** — Punya internal state dan konteks. Dia bisa ingat percakapan sebelumnya dan mempertimbangkan history.
3. **Goal-Based Agent** — Punya tujuan spesifik dan cari cara untuk mencapainya. Lebih canggih karena bisa break down goal jadi langkah-langkah kecil.
4. **Utility-Based Agent** — Punya sistem evaluasi sendiri. Dia bisa menimbang beberapa pilihan dan memilih yang paling optimal.
5. **Learning Agent** — Bisa belajar dari experience dan improve performa seiring waktu.

Di tutorial ini, kita bakal bikin jenis Goal-Based Agent yang paling umum dipakai di production.

## Persiapan Sebelum Mulai

Sebelum coding, siapin dulu beberapa hal:

1. **Python 3.9+** — Install kalau belum ada. Cek dengan `python --version`
2. **API Key OpenAI/Anthropic** — Buat akun dulu di platform masing-masing. Khusus OpenAI, kamu butuh kredit minimal $5 (sekitar Rp 78.000) untuk mulai pakai API-nya.
3. **Code Editor** — VS Code dengan [extension Python](/tutorial/setup-vs-code-web-development-2025/) yang udah di-setup, atau Cursor AI yang sudah ada AI built-in. Baca [tutorial setup Cursor AI](/tutorial/install-setup-cursor-ai-2025/) kalau mau coba.
4. **Terminal/Command Prompt** — Untuk jalankan script

### Biaya yang Dibutuhkan

Sebelum lanjut, penting buat tau biaya yang bakal kamu keluarkan:

- **OpenAI API:** GPT-4 sekitar $0.03 per 1K input tokens, $0.06 per 1K output tokens. Untuk tutorial ini, estimasi $0.50 - $2.00 (Rp 8.000 - Rp 31.000) tergantung panjang percakapan.
- **Anthropic API:** Claude sedikit lebih mahal, tapi punya context window yang lebih besar.
- **Alternatif hemat:** Pakai OpenAI GPT-3.5-turbi yang 10x lebih murah dari GPT-4. Cukup buat belajar dan prototyping.

## Step 1: Setup Environment

Buat folder project baru:

```bash
mkdir my-first-agent
cd my-first-agent
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

Kenapa pakai virtual environment? Supaya dependencies project ini gak clash sama project Python lain di komputer kamu. Ini best practice yang wajib dipakai di setiap project Python.

Install dependencies:

```bash
pip install openai python-dotenv
```

Buat file `.env`:

```
OPENAI_API_KEY=your-api-key-here
```

**Penting:** Jangan pernah commit file `.env` ke Git! Tambahkan ke `.gitignore`:

```bash
echo ".env" >> .gitignore
```

## Step 2: Buat Agent Basic

Buat file `agent.py`:

```python
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def chat_with_agent(message, history=None):
    if history is None:
        history = []
    
    history.append({"role": "user", "content": message})
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=history,
        temperature=0.7
    )
    
    assistant_message = response.choices[0].message.content
    history.append({"role": "assistant", "content": assistant_message})
    
    return assistant_message

# Test agent
if __name__ == "__main__":
    print("AI Agent siap! Ketik pesan (ketik 'exit' untuk keluar)")
    history = []
    while True:
        user_input = input("Kamu: ")
        if user_input.lower() == 'exit':
            break
        response = chat_with_agent(user_input, history)
        print(f"Agent: {response}")
```

Jalankan:

```bash
python agent.py
```

Sekarang kamu udah punya basic chatbot yang bisa mempertahankan konteks percakapan. Coba ajak ngobrol beberapa kali — dia bakal ingat apa yang kamu sebutin sebelumnya karena kita pakai `history` parameter.

Tapi ini belum AI agent sejati. Yang bikin AI agent berbeda dari chatbot biasa adalah kemampuan menggunakan tools. Yuk lanjut.

## Step 3: Tambahin Tools

Nah ini bagian serunya. Kita bikin agent bisa pake tools. Konsep ini yang disebut "function calling" — agent bisa memutuskan kapan dan bagaimana cara menggunakan tools yang tersedia.

```python
import json
import requests
import os
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Definisi tools yang bisa dipakai agent
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Dapatkan waktu sekarang",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Cari informasi di internet",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Kata kunci pencarian"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Hitung operasi matematika",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Ekspresi matematika, contoh: '2 + 3 * 4'"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def search_web(query):
    """Search menggunakan DuckDuckGo (tanpa API key)"""
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json"
        response = requests.get(url, timeout=10)
        data = response.json()
        abstract = data.get("Abstract", "Tidak ditemukan hasil spesifik")
        related = [r["Text"] for r in data.get("RelatedTopics", [])[:3] if "Text" in r]
        return json.dumps({"summary": abstract, "related_topics": related})
    except Exception as e:
        return json.dumps({"error": str(e)})

def calculate(expression):
    """Hitung ekspresi matematika dengan aman"""
    try:
        allowed_chars = set("0123456789+-*/.() ")
        if not all(c in allowed_chars for c in expression):
            return json.dumps({"error": "Ekspresi mengandung karakter tidak valid"})
        result = eval(expression)
        return json.dumps({"result": result})
    except Exception as e:
        return json.dumps({"error": str(e)})
```

## Step 4: Agent Loop dengan Tool Execution

Sekarang kita bikin loop yang memungkinkan agent memanggil tools secara otomatis:

```python
def run_agent(user_message, history=None):
    if history is None:
        history = [
            {
                "role": "system",
                "content": (
                    "Kamu adalah AI assistant yang helpful. Kamu bisa menggunakan tools "
                    "untuk membantu user. Gunakan tools yang tersedia untuk menjawab pertanyaan. "
                    "Selalu jawab dalam Bahasa Indonesia."
                )
            }
        ]
    
    history.append({"role": "user", "content": user_message})
    
    # Step 1: Kirim ke model dan lihat apakah dia mau pakai tools
    response = client.chat.completions.create(
        model="gpt-4",
        messages=history,
        tools=tools,
        tool_choice="auto"
    )
    
    assistant_message = response.choices[0].message
    
    # Step 2: Cek apakah ada tool calls
    if assistant_message.tool_calls:
        # Tambahkan response assistant ke history
        history.append(assistant_message)
        
        # Step 3: Eksekusi setiap tool call
        for tool_call in assistant_message.tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            
            print(f"  [Agent memanggil tool: {function_name}]")
            
            # Panggil function yang sesuai
            if function_name == "get_current_time":
                result = get_current_time()
            elif function_name == "search_web":
                result = search_web(arguments.get("query", ""))
            elif function_name == "calculate":
                result = calculate(arguments.get("expression", ""))
            else:
                result = json.dumps({"error": f"Tool {function_name} tidak ditemukan"})
            
            # Tambahkan result ke history
            history.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })
        
        # Step 4: Kirim ulang ke model dengan hasil tool
        second_response = client.chat.completions.create(
            model="gpt-4",
            messages=history
        )
        final_message = second_response.choices[0].message.content
        history.append({"role": "assistant", "content": final_message})
        return final_message
    else:
        # Gak ada tool call, langsung return response
        final_message = assistant_message.content
        history.append({"role": "assistant", "content": final_message})
        return final_message


if __name__ == "__main__":
    print("=== AI Agent with Tools ===")
    print("Ketik 'exit' untuk keluar\n")
    print("Contoh pertanyaan:")
    print("  - Jam berapa sekarang?")
    print("  - Cari info tentang Python programming")
    print("  - Berapa hasil dari 123 * 456?\n")
    
    history = [
        {
            "role": "system",
            "content": (
                "Kamu adalah AI assistant yang helpful. Kamu bisa menggunakan tools "
                "untuk membantu user. Gunakan tools yang tersedia untuk menjawab pertanyaan. "
                "Selalu jawab dalam Bahasa Indonesia."
            )
        }
    ]
    
    while True:
        user_input = input("Kamu: ")
        if user_input.lower() == 'exit':
            print("Sampai jumpa!")
            break
        response = run_agent(user_input, history)
        print(f"Agent: {response}\n")
```

## Step 5: Tambahin Memory yang Persistent

Agent baru-baru saja kita bikin cuma punya short-term memory — hilang begitu program ditutup. Untuk bikin agent yang lebih canggih, kita bisa tambahin persistent memory pakai SQLite:

```python
import sqlite3

def setup_memory():
    """Setup database untuk simpan percakapan"""
    conn = sqlite3.connect('agent_memory.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return conn

def save_message(conn, session_id, role, content):
    conn.execute(
        "INSERT INTO conversations (session_id, role, content) VALUES (?, ?, ?)",
        (session_id, role, content)
    )
    conn.commit()

def load_history(conn, session_id, limit=20):
    cursor = conn.execute(
        "SELECT role, content FROM conversations WHERE session_id = ? "
        "ORDER BY id DESC LIMIT ?",
        (session_id, limit)
    )
    messages = [{"role": row[0], "content": row[1]} for row in cursor.fetchall()]
    messages.reverse()
    return messages
```

Dengan persistent memory, agent kamu bisa "ingat" percakapan sebelumnya walaupun program sudah ditutup dan dijalankan ulang. Ini sangat berguna untuk use case seperti customer service bot atau personal assistant.

## Tips Biar Agent Lebih Cerdik

Setelah bikin agent basic, ada beberapa hal yang bisa kamu lakukan untuk bikin agent lebih pintar dan reliable:

1. **System Prompt yang Jelas** — Kasih instruksi spesifik ke agent tentang siapa dia, apa yang dia bisa lakukan, dan apa yang dia gak boleh lakukan. System prompt yang bagus bisa beda banget hasilnya. Contoh:

```python
system_prompt = """
Kamu adalah assistant untuk tim engineering. 
Kamu bisa:
- Menjawab pertanyaan teknis tentang codebase
- Mencari dokumentasi
- Menghitung estimasi waktu

Kamu TIDAK BOLEH:
- Menghapus file tanpa konfirmasi
- Mengakses database production
- Membagikan informasi sensitif
"""
```

2. **Tool Selection yang Tepat** — Pilih tools yang relevan sama use case kamu. Jangan kasih terlalu banyak tools karena bisa bikin agent bingung. Lebih baik 3-5 tools yang well-defined dibanding 20 tools yang setengah-setengah.

3. **Error Handling yang Robust** — Jangan lupa handle error di setiap tool function. Kalau ada error di satu tool, agent harus bisa handle graceful dan inform user. Jangan crash.

4. **Token Usage Monitoring** — Cek usage API kamu secara berkala di dashboard OpenAI. Kalau percakapan mulai panjang, pertimbangkan untuk compress history. Kamu bisa ambil N pesan terakhir saja, atau summarize pesan-pesan lama.

5. **Testing dengan Berbagai Skenario** — Test agent kamu dengan pertanyaan yang aneh, ambiguous, dan edge cases. Ini yang paling sering dilupakan tapi paling penting.

## Deploy AI Agent ke Production

Kalau kamu udah puas dengan agent kamu dan mau deploy ke production, ada beberapa opsi:

- **Railway** — Paling gampang, deploy langsung dari GitHub. Baca [perbandingan hosting](/tech-review/review-railway-vs-render-vs-flyio-2025/) untuk detail.
- **Docker** — Lebih portable dan predictable. Baca [tutorial Docker untuk pemula](/tutorial/belajar-docker-pemula-2025/) dan [deploy AI agent ke production](/ai-agent/deploy-ai-agent-production-docker-railway/).
- **Telegram Bot** — Kalau kamu mau agent yang accessible lewat chat, bikin Telegram bot. Baca [tutorial bikin Telegram bot pakai AI](/tutorial/cara-build-telegram-bot-ai-nodejs/).

Biaya hosting di Railway mulai dari $5/bulan (sekitar Rp 78.000), termasuk lumayan terjangkau buat developer Indonesia yang baru mulai.

## FAQ

**Berapa biaya API OpenAI per bulan untuk AI agent?**

Sangat tergantung usage. Untuk usage ringan (50-100 percakapan/hari pakai GPT-3.5-turbo), estimasi $5-15/bulan (Rp 78.000 - Rp 234.000). Kalau pakai GPT-4, bisa 10x lebih mahal. Untuk menekan biaya, pakai GPT-3.5-turbo untuk task sederhana dan GPT-4 hanya untuk yang kompleks.

**Bisa gak pakai model AI gratis?**

Bisa! Pakai Ollama untuk menjalankan model open source lokal (seperti Llama 2, Mistral). Gak perlu bayar API, tapi butuh komputer dengan RAM minimal 8GB. Cocok buat belajar dan development.

**AI agent vs chatbot, apa bedanya?**

Chatbot itu respon dari input ke output. AI agent bisa ambil keputusan, pakai tools, maintain memory, dan eksekusi task kompleks secara otonom. Chatbot itu subset dari AI agent.

**Gimana cara bikin AI agent yang bisa baca PDF?**

Kamu bisa gunakan library seperti PyPDF2 atau PDFplumber untuk extract text dari PDF, lalu feed ke LLM. Tutorial lengkapnya ada di [tutorial AI agent baca PDF](/ai-agent/tutorial-ai-agent-baca-pdf-summary/).

**Apakah aman kasih AI agent akses ke API dan database?**

Hati-hati! Mulai dengan akses yang sangat terbatas (read-only). Gunakan environment variable untuk API keys. Jangan pernah hardcode credentials. Kalau untuk production, pasang rate limiting dan audit log untuk semua action yang dilakukan agent.

**Model AI apa yang paling cocok untuk agent?**

GPT-4 atau Claude paling powerful untuk complex reasoning. GPT-3.5-turbo bagus untuk task sederhana karena lebih murah. Model open source seperti Mixtral dan Llama 3 juga mulai bisa bersaing untuk use case tertentu.

---

Membuat AI agent itu gak serumit yang dibayangkan. Dengan dasar Python dan API yang tepat, kamu udah bisa bikin agent yang useful dan powerful. Mulai dari yang sederhana, iterate, dan tambahkan complexity seiring berjalannya waktu.

Langkah selanjutnya, coba tambahin lebih banyak tools dan integrasi sama platform lain. Atau kalau mau langsung praktik, baca tutorial [cara bikin Telegram bot pakai AI](/tutorial/cara-build-telegram-bot-ai-nodejs/) untuk deploy agent kamu ke platform chat yang populer.

**Pertanyaan?** Komen di bawah atau langsung chat aku di Telegram!
