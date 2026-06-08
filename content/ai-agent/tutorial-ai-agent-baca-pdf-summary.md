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

Punya tumpukan PDF yang gak kebaca? Di tutorial ini aku bakal ngejelasin cara bikin AI agent yang bisa baca PDF dan kasih summary dalam hitungan detik.

## Kenapa Butuh AI PDF Reader?

Bayangin kamu punya 100 dokumen research paper. Manual baca butuh berhari-hari. Pakai AI? 30 menit beres.

**Use cases:**
- Research paper analysis
- Legal document review
- Business report summarization
- Academic literature review

## Persiapan

1. Python 3.9+
2. OpenAI API key
3. Library: PyPDF2, langchain, openai

Install dependencies:

```bash
pip install PyPDF2 langchain openai tiktoken
```

## Step 1: PDF Parser

Buat fungsi untuk extract text dari PDF:

```python
import PyPDF2
from typing import List

def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def chunk_text(text: str, chunk_size: int = 4000) -> List[str]:
    words = text.split()
    chunks = []
    current_chunk = []
    current_size = 0
    
    for word in words:
        current_chunk.append(word)
        current_size += len(word) + 1
        
        if current_size >= chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_size = 0
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks
```

## Step 2: AI Summarizer

```python
from openai import OpenAI

client = OpenAI()

def summarize_chunk(chunk: str, prompt: str = None) -> str:
    if not prompt:
        prompt = """Summarize the following text in Indonesian. 
        Focus on key points, main arguments, and conclusions.
        Keep it concise but comprehensive."""
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": chunk}
        ],
        temperature=0.3
    )
    
    return response.choices[0].message.content
```

## Step 3: Main Agent

```python
def summarize_pdf(pdf_path: str, output_format: str = "bullet") -> str:
    print(f"Reading PDF: {pdf_path}")
    text = extract_text_from_pdf(pdf_path)
    
    if not text.strip():
        return "Error: Could not extract text from PDF"
    
    chunks = chunk_text(text)
    print(f"Found {len(chunks)} chunks")
    
    summaries = []
    for i, chunk in enumerate(chunks):
        print(f"Summarizing chunk {i+1}/{len(chunks)}...")
        summary = summarize_chunk(chunk)
        summaries.append(summary)
    
    combined = "\n\n".join(summaries)
    
    if len(summaries) > 1:
        print("Generating final summary...")
        final_prompt = f"""Combine these summaries into one comprehensive summary.
        Format: {output_format}
        Language: Indonesian"""
        final = summarize_chunk(combined, final_prompt)
    else:
        final = summaries[0]
    
    return final
```

## Tips Production-Ready

1. **Use embeddings** - Untuk find relevant chunks lebih akurat
2. **Cache results** - Simpan summary biar gak re-process
3. **Handle large PDFs** - Implement streaming
4. **Error handling** - PDF corrupt, encrypted
5. **Rate limiting** - Respect OpenAI rate limits

## Conclusion

Bikin AI PDF reader itu straightforward. Dengan Python dan OpenAI API, kamu bisa automate document analysis.

**Next steps:**
- Build web interface
- Add multi-PDF support
- Implement vector search untuk Q&A

**Butuh bantuan?** Chat aku di Telegram!
