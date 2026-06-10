---
title: "Tutorial: Bikin AI Agent yang Baca PDF dan Kasih Summary"
date: 2026-01-06
draft: false
slug: "tutorial-ai-agent-baca-pdf-summary"
description: "Tutorial lengkap membuat AI agent yang bisa baca PDF dan generate summary otomatis menggunakan Python."
categories: ['AI Agent', 'Tutorial']
tags: ['ai-agent', 'pdf', 'summary', 'python']
ShowShareButtons: true
ShowReadingTime: true
ShowToc: true
---

Punya tumpukan PDF yang gak kebaca? Di tutorial ini aku bakal ngejelasin cara bikin AI agent yang bisa baca PDF, kasih summary, bahkan jawab pertanyaan berdasarkan isi dokumen — semua dalam hitungan detik.

Kita bakal cover semuanya dari nol: parsing PDF, nyimpen ke vector database, bikin RAG pipeline, sampai deploy ke production. Siap? Let's go! 🚀

## Kenapa Butuh AI PDF Reader?

Bayangin kamu punya 100 dokumen research paper, laporan keuangan, atau kontrak hukum. Manual baca? Butuh berhari-hari. Pakai AI agent yang properly built? 30 menit beres, dan hasilnya konsisten.

**Real-world use cases:**
- Research paper analysis
- Legal document review
- Business report summarization
- Academic literature review
- Chat with your PDF (ask questions about the document)
- Compliance audit automation
- Invoice and receipt processing

Yang kita bangun di tutorial ini bukan cuma summary generator biasa. Kita bikin full AI agent yang punya kemampuan RAG, artinya dia bisa retrieve informasi spesifik dari dokumen dan jawab pertanyaan berdasarkan isi PDF. Ini beda jauh sama approach lama yang cuma nge-push seluruh teks ke LLM — yang bisa meledak kalau dokumennya gede.

Oke, tanpa banyak basa-basi, langsung ke teknis. 🛠️

## Persiapan

Sebelum mulai coding, pastikan environment kamu ready:

**Requirements:**
1. Python 3.9 atau lebih baru
2. OpenAI API key (atau API key LLM provider lain)
3. Minimal 4GB RAM (untuk processing PDF besar)
4. Terminal / code editor (VS Code recommended)

**Install semua dependencies sekaligus:**

```bash
pip install PyPDF2 pdfplumber langchain langchain-openai langchain-chroma openai tiktoken chromadb fastapi uvicorn
```

## Step 1: PDF Parser

Ada beberapa library PDF parsing di Python. Ini perbandingannya:

- **PyPDF2** — Ringan dan cepat, tapi kurang akurat di complex layout
- **pdfplumber** — Lebih akurat, support table extraction
- **PyMuPDF (fitz)** — Sangat cepat dan akurat, tapi dependencies agak besar
- **Unstructured.io** — Auto-detect format, tapi overkill untuk simple PDF

Untuk tutorial ini, kita pakai **PyPDF2** untuk simplicity dan **pdfplumber** sebagai alternatif yang lebih akurat.

### Versi PyPDF2 (Basic):

```python
import PyPDF2
from typing import List

def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        print(f"Total halaman: {len(reader.pages)}")
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text
```

### Versi pdfplumber (Recommended untuk Production):

```python
import pdfplumber
from typing import List

def extract_text_with_pdfplumber(pdf_path: str) -> str:
    """Extract text lebih akurat, termasuk tabel."""
    full_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            # Extract text biasa
            text = page.extract_text()
            if text:
                full_text.append(f"--- Halaman {i+1} ---\n{text}")

            # Bonus: extract tabel juga
            tables = page.extract_tables()
            for table in tables:
                table_text = "\n".join(
                    [" | ".join(str(cell or "") for cell in row) for row in table]
                )
                full_text.append(f"[Tabel]:\n{table_text}")

    return "\n\n".join(full_text)
```

### Chunking: Pecah Teks Jadi Bagian Kecil

Kenapa harus di-chunk? Karena LLM punya context window terbatas. Kita pecah teks jadi potongan-potongan yang masuk akal:

```python
def chunk_text(text: str, chunk_size: int = 3000, overlap: int = 200) -> List[str]:
    """Chunking dengan overlap untuk menjaga konteks antar bagian."""
    words = text.split()
    chunks = []
    current_chunk = []
    current_size = 0

    for word in words:
        current_chunk.append(word)
        current_size += len(word) + 1

        if current_size >= chunk_size:
            chunks.append(' '.join(current_chunk))
            # Overlap: simpen beberapa kata terakhir buat konteks
            current_chunk = current_chunk[-overlap//5:] if overlap > 0 else []
            current_size = sum(len(w) + 1 for w in current_chunk)

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    print(f"Total chunks: {len(chunks)}, rata-rata {chunk_size} kata per chunk")
    return chunks
```

**Kenapa overlap penting?** Tanpa overlap, informasi di batas chunk bisa hilang begitu saja. Bayangin ada kalimat penting yang terpotong antara chunk 5 dan chunk 6 — tanpa overlap, konteksnya hilang. Dengan overlap 200 kata, informasi yang ada di perbatasan tetap terjaga di kedua chunk. Ini simple trick tapi dampaknya besar banget ke kualitas output akhir.

## Step 2: Setup Vector Database dengan ChromaDB

Vector database itu jantungnya RAG pipeline. Dia nyimpen embedding dari setiap chunk dan bikin pencarian semantic jadi super cepat.

Kenapa **ChromaDB**? Karena ringan, open-source, dan bisa jalan lokal tanpa setup server. Cocok buat yang baru mulai.

```python
import chromadb
from chromadb.utils import embedding_functions
import os

def setup_vector_db(persist_dir: str = "./chroma_db"):
    """Setup ChromaDB client dengan OpenAI embeddings."""
    client = chromadb.PersistentClient(path=persist_dir)

    # Gunakan OpenAI embeddings (atau ganti ke local model biar hemat API)
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name="text-embedding-3-small"
    )

    # Buat atau ambil collection yang sudah ada
    collection = client.get_or_create_collection(
        name="pdf_documents",
        embedding_function=openai_ef,
        metadata={"hnsw:space": "cosine"}
    )

    return client, collection

def store_chunks_in_db(collection, chunks: List[str], pdf_name: str):
    """Simpen chunks ke vector database."""
    ids = [f"{pdf_name}_chunk_{i}" for i in range(len(chunks))]

    # Batch insert untuk efisiensi (ChromaDB max 5461 per batch)
    batch_size = 500
    for i in range(0, len(chunks), batch_size):
        batch_chunks = chunks[i:i+batch_size]
        batch_ids = ids[i:i+batch_size]
        collection.add(
            documents=batch_chunks,
            ids=batch_ids,
            metadatas=[{"source": pdf_name}] * len(batch_chunks)
        )

    print(f"Stored {len(chunks)} chunks dari '{pdf_name}' ke database")
```

**Alternatif Vector DB:**
- **Pinecone**: Managed service, cocok buat production scale
- **Weaviate**: GraphQL API, support hybrid search
- **FAISS** (Meta): Ultra-fast, tapi in-memory aja
- **Qdrant**: Rust-based, performa tinggi

Kalau cuma buat personal project atau prototyping, ChromaDB udah lebih dari cukup. Tapi kalau targetnya production scale dengan jutaan dokumen, pertimbangkan Pinecone atau Qdrant yang bisa handle distribusi.

## Step 3: RAG Pipeline

RAG (Retrieval-Augmented Generation) adalah technique di mana kita retrieve context relevan dari database dulu, baru dikasih ke LLM buat generate jawaban. Ini jauh lebih akurat daripada langsung nge-push seluruh dokumen ke LLM.

Alurnya: **User Query → Embedding → Search Vector DB → Ambil Top-K Results → Gabung ke Prompt → LLM Generate Jawaban**

Kenapa ini penting? Karena tanpa RAG, kamu harus nge-push seluruh konten PDF ke prompt LLM. Kalau PDF-nya 500 halaman, itu bakal exceed context window dan biaya API-nya juga gila-gilaan. Dengan RAG, cuma bagian yang relevan aja yang masuk ke prompt — hemat token, hemat duit, dan jawabannya lebih akurat karena fokus.

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

def search_similar_chunks(collection, query: str, n_results: int = 5) -> List[str]:
    """Cari chunks yang paling relevan dengan query."""
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results["documents"][0]

def build_rag_chain(collection):
    """Build RAG chain menggunakan LangChain."""
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.2,
        max_tokens=2000
    )

    def retrieve_context(query: str) -> str:
        chunks = search_similar_chunks(collection, query)
        return "\n\n---\n\n".join(chunks)

    prompt = ChatPromptTemplate.from_template("""
    Kamu adalah assistant ahli yang membantu menganalisis dokumen PDF.

    Gunakan context berikut untuk menjawab pertanyaan user.
    Jika jawaban tidak ada di context, katakan "Maaf, informasi ini
    tidak ditemukan di dokumen."
    Selalu cantumkan referensi dari mana informasi diambil.

    Context:
    {context}

    Pertanyaan: {question}

    Jawaban (dalam Bahasa Indonesia yang jelas dan terstruktur):
    """)

    def rag_query(question: str) -> str:
        context = retrieve_context(question)
        chain = prompt | llm | StrOutputParser()
        return chain.invoke({"context": context, "question": question})

    return rag_query
```

## Step 4: AI Summarizer (Full Pipeline)

Gabungin semua komponen jadi satu pipeline yang jalan:

```python
from openai import OpenAI
import os

client = OpenAI()

def summarize_chunk(chunk: str, custom_prompt: str = None) -> str:
    """Summarize satu chunk menggunakan OpenAI."""
    if not custom_prompt:
        custom_prompt = (
            "Kamu adalah expert summarizer. Ringkas teks berikut "
            "dalam Bahasa Indonesia. Fokus pada: poin-poin utama, "
            "argumen/klaim, data penting, dan kesimpulan. "
            "Gunakan format bullet point yang rapi dan mudah dibaca. "
            "Jangan menambahkan informasi yang tidak ada di teks asli."
        )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": custom_prompt},
            {"role": "user", "content": chunk}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content
```

## Step 5: Main Agent

Ini fungsi utama yang ngegabungin semuanya:

```python
from pathlib import Path

def process_pdf(pdf_path: str, mode: str = "summarize") -> str:
    """
    Main agent function.
    mode: 'summarize' untuk summary, 'index' untuk simpen ke vector DB,
          'ask' untuk tanya ke PDF.
    """
    pdf_name = Path(pdf_path).stem
    print(f"📄 Processing: {pdf_path}")

    text = extract_text_with_pdfplumber(pdf_path)

    if not text.strip():
        return "❌ Error: Tidak bisa extract text dari PDF."

    chunks = chunk_text(text)

    if mode == "index":
        _, collection = setup_vector_db()
        store_chunks_in_db(collection, chunks, pdf_name)
        return f"✅ '{pdf_name}' berhasil di-index! {len(chunks)} chunks tersimpan."

    elif mode == "ask":
        _, collection = setup_vector_db()
        question = input("Masukkan pertanyaan kamu: ")
        rag_chain = build_rag_chain(collection)
        return rag_chain(question)

    else:  # summarize
        summaries = []
        for i, chunk in enumerate(chunks):
            print(f"📝 Summarizing chunk {i+1}/{len(chunks)}...")
            summary = summarize_chunk(chunk)
            summaries.append(summary)

        combined = "\n\n".join(summaries)

        if len(summaries) > 1:
            print("🔄 Generating final combined summary...")
            final_prompt = (
                "Gabungkan semua ringkasan berikut jadi satu summary "
                "komprehensif. Format: heading untuk topik utama, "
                "bullet point untuk detail. Bahasa: Indonesia. "
                "Panjang: 500-800 kata"
            )
            final = summarize_chunk(combined, final_prompt)
        else:
            final = summaries[0]

        return final


# === Cara Pakai ===
if __name__ == "__main__":
    import sys

    pdf_file = sys.argv[1] if len(sys.argv) > 1 else "sample.pdf"
    mode = sys.argv[2] if len(sys.argv) > 2 else "summarize"

    result = process_pdf(pdf_file, mode)
    print("\n" + "=" * 60)
    print(result)
    print("=" * 60)
```

## Step 6: Prompt Engineering Tips

Prompt engineering itu seni yang sering di-overlook. Beberapa tips dari pengalaman aku:

### 1. Selalu Kasih Role yang Spesifik

```python
# ❌ Bad
"Summarize this text"

# ✅ Good
"Kamu adalah analis riset senior. Ringkas dokumen akademik berikut
dengan fokus pada metodologi, hasil utama, dan limitasi studi."
```

### 2. Pakai Structured Output Format

```python
prompt = """Analisis dokumen ini dan jawab dalam format:

## Ringkasan Eksekutif
[2-3 kalimat]

## Poin-Poin Utama
- [bullet point]
- [bullet point]

## Data/Kutipan Penting
[angka, statistik, atau quote relevan]

## Kesimpulan
[1 paragraf]
"""
```

### 3. Temperature Setting yang Tepat

- **0.0-0.2** — Untuk factual tasks (summary, extraction)
- **0.5-0.7** — Untuk creative writing atau brainstorming
- **0.8-1.0** — Untuk experimental/creative output

### 4. Handle Edge Cases di Prompt

```python
# Tambahkan instruksi edge case handling
"""
Jika informasi tidak ditemukan di dokumen, jawab:
"Informasi ini tidak tersedia di dokumen yang diberikan."
Jangan pernah mengarang atau hallucinate jawaban.
"""
```

### 5. Few-Shot Prompting untuk Output Konsisten

Kasih contoh output yang kamu mau langsung di prompt. LLM bakal follow formatnya dengan lebih konsisten daripada hanya kasih instruksi. Misalnya, kalau kamu mau summary dengan format tertentu, kasih satu contoh summary lengkap di prompt. Hasilnya jauh lebih predictable dan konsisten di setiap run.

## Step 7: Deploy ke Production

Nah, ini bagian yang sering dilupakan. Bikin jalan di localhost itu gampang, tapi production-ready itu beda cerita. 😅

Banyak developer cuma sampai di tahap "udah jalan di terminal" terus langsung pamer ke Twitter. Tapi kalau mau dipake orang lain — atau bahkan cuma buat diri sendiri secara konsisten — ada beberapa hal yang harus dipersiapin.

### Opsi 1: FastAPI Server

Bikin REST API biar bisa dipanggil dari mana aja:

```python
# app.py - FastAPI server
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import tempfile
import os

app = FastAPI(title="PDF AI Agent API")

@app.post("/summarize")
async def summarize_endpoint(file: UploadFile = File(...)):
    """Upload PDF dan dapatkan summary."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        result = process_pdf(tmp_path, mode="summarize")
        return {"status": "success", "summary": result}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    finally:
        os.unlink(tmp_path)

@app.post("/ask")
async def ask_endpoint(file: UploadFile = File(...), question: str = ""):
    """Upload PDF dan tanya sesuatu."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        process_pdf(tmp_path, mode="index")
        _, collection = setup_vector_db()
        rag_chain = build_rag_chain(collection)
        answer = rag_chain(question)
        return {"status": "success", "answer": answer}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    finally:
        os.unlink(tmp_path)

# Jalankan: uvicorn app:app --host 0.0.0.0 --port 8000
```

### Opsi 2: Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Tips Deployment Production

- **Rate Limiting** — Pasang limit biar API gak ke-abuse. Bisa pakai `slowapi` atau `fastapi-limiter`.
- **Error Handling** — PDF corrupt, file terlalu besar, API key habis — handle semua itu dengan graceful error messages.
- **Logging** — Pakai `structlog` atau `loguru` biar bisa debug kalau ada error di production.
- **Caching** — Kalau PDF yang sama di-request berulang kali, cache hasilnya di Redis biar gak re-process.
- **Monitoring** — Pasang health check endpoint dan monitor API usage.
- **Security** — Validasi file upload (hanya terima `.pdf`, max size 50MB), sanitasi input, dan jangan hardcode API key!

```bash
# Deploy dengan Docker Compose (production-ready)
docker compose up -d --build
```

## Pertanyaan yang Sering Ditanyakan (FAQ)

**Q: PDF yang scanned (hasil scan/gambar) bisa diproses gak?**
A: Bisa, tapi butuh OCR dulu. Pakai library `pytesseract` atau `PaddleOCR` buat convert image ke text baru diproses. Atau pakai model GPT-4o yang sudah support vision langsung.

**Q: Berapa biaya OpenAI API buat proses 100 PDF?**
A: Tergantung ukuran PDF. Rata-rata 1 PDF (10-20 halaman) butuh ~5-15K tokens. Dengan `text-embedding-3-small` ($0.02/1M tokens) dan `gpt-4o` ($2.50/1M input tokens), estimasi biaya untuk 100 PDF sekitar $15-30. Bisa lebih hemat pakai model open-source seperti Llama 3 via Ollama.

**Q: Bisa gak pakai LLM local biar hemat?**
A: Bisa banget! Pakai Ollama + Llama 3. Tinggal ganti `ChatOpenAI` jadi `ChatOllama` di LangChain. Tapi butuh GPU minimal 8GB VRAM buat Llama 3 8B.

**Q: PDF dengan tabel dan gambar kompleks gimana?**
A: Pakai `pdfplumber` atau `Unstructured.io` yang lebih handal untuk complex layout. Untuk gambar/grafik, bisa pakai GPT-4o vision untuk deskripsi otomatis.

**Q: Berapa besar vector database yang dihasilkan?**
A: Rata-rata 1 PDF (20 halaman) menghasilkan sekitar 100-200 chunks. Dengan embedding 1536 dimensi (OpenAI), storage per chunk ~6KB. Jadi 1 PDF ≈ 1MB storage di ChromaDB.

**Q: Bisa dipake untuk PDF berbahasa non-Inggris?**
A: Ya, langsung aja! LLM seperti GPT-4o mendukung 100+ bahasa. Tinggal sesuaikan prompt-nya. Tutorial ini pakai Bahasa Indonesia sebagai default.

## Kesimpulan

Bikin AI agent yang bisa baca PDF itu sekarang jauh lebih accessible daripada 2-3 tahun lalu. Dengan kombinasi Python, OpenAI API, ChromaDB untuk vector storage, dan LangChain untuk orchestration, kamu bisa bangun sistem yang powerful dalam waktu singkat.

Yang penting diinget:

1. **Pilih PDF parser yang tepat** — PyPDF2 untuk quick tasks, pdfplumber untuk accuracy
2. **Chunking dengan overlap** — Penting banget buat menjaga konteks antar potongan
3. **RAG > raw prompting** — Selalu retrieve dulu, baru generate jawaban
4. **Prompt engineering matters** — Prompt yang baik = hasil yang konsisten
5. **Production ≠ localhost** — Error handling, logging, caching itu wajib

**Next steps yang bisa kamu explore:**
- Build web interface (Streamlit / Gradio)
- Multi-PDF support dengan folder indexing
- Hybrid search (keyword + semantic)
- Auto-classification document types
- Integration dengan tools lain (Notion, Google Drive, Slack)

Kalau ada pertanyaan atau stuck di step tertentu, jangan ragu buat tanya di Telegram aku ya! Happy coding! 💻🔥

---

*Tutorial ini ditulis dengan Python 3.11, OpenAI API v1.x, LangChain v0.2, dan ChromaDB v0.5. Update terakhir: Januari 2026.*
