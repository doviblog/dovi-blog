---
title: "RAG 101: Build AI yang Bisa Akses Database Kamu"
date: 2026-04-01
draft: false
slug: "rag-retrieval-augmented-generation"
description: "Tutorial Retrieval Augmented Generation untuk AI yang lebih cerdas. Bikin chatbot yang jawab berdasarkan data kamu sendiri."
categories: [Ai Agent]
tags: ['rag', 'vector-db', 'embeddings', 'python', 'langchain', 'chromadb']
ShowShareLinks: true
ShowReadingTime: true
ShowToc: true
---

Aku pernah bikin chatbot untuk customer service toko online. Pakai GPT-4 langsung — jawabannya bagus, tapi... salah semua. Chatbot-nya ngarang info produk, harga, dan stok. Customer marah, boss tanya kenapa.

Masalahnya jelas: LLM gak tau data produk kita. Dia cuma bisa jawab dari training data-nya yang udah outdated.

Solusinya? **RAG — Retrieval Augmented Generation.**

## RAG Itu Apa?

RAG itu konsep simple: sebelum AI jawab pertanyaan, dia cari dulu informasi relevan dari database/dokumen kita, terus pakai info itu sebagai context buat jawab.

Alurnya:

```
User: "Berapa harga iPhone 15 Pro di toko kamu?"

1. RETRIEVE: Cari di database → "iPhone 15 Pro, harga Rp 18.999.000, stok 5 unit"
2. AUGMENT: Tambahin context ke prompt AI
3. GENERATE: AI jawab berdasarkan data real
```

Bukan ngarang lagi — jawabannya berdasarkan data asli.

**Kenapa RAG daripada fine-tuning?**

- RAG: Update data tinggal update database. Gak perlu retrain.
- Fine-tuning: Data berubah = retrain ulang, mahal dan lama.
- RAG: Bisa trace jawaban ke sumber data. 
- Fine-tuning: Gak bisa explain dari mana jawabannya.

## Arsitektur RAG

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Documents   │────▶│  Embedding   │────▶│  Vector DB  │
│  (PDF/DB/    │     │  Model       │     │  (Chroma/   │
│   Web)       │     │              │     │   Pinecone) │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
                                                │ Similarity Search
                                                │
┌─────────────┐     ┌──────────────┐     ┌──────▼──────┐
│   User       │────▶│  Prompt +    │────▶│    LLM      │
│   Query      │     │  Context     │     │  (GPT-4)    │
└─────────────┘     └──────────────┘     └─────────────┘
```

## Prerequisites

```bash
pip install langchain langchain-openai chromadb openai tiktoken pypdf
```

Dan set env variable:

```bash
export OPENAI_API_KEY="sk-xxxx"
```

## Step 1: Load Documents

```python
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    DirectoryLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Option A: Load dari folder PDF
loader = DirectoryLoader(
    "./docs",
    glob="**/*.pdf",
    loader_cls=PyPDFLoader,
    show_progress=True
)
documents = loader.load()

# Option B: Load dari file teks
loader = TextLoader("./product_catalog.txt")
documents = loader.load()

print(f"Loaded {len(documents)} documents")

# Split jadi chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,       # 1000 karakter per chunk
    chunk_overlap=200,     # Overlap 200 karakter biar konteks gak putus
    length_function=len,
    separators=["\n\n", "\n", ". ", " ", ""]
)

chunks = text_splitter.split_documents(documents)
print(f"Split into {len(chunks)} chunks")
```

**Kenapa harus di-split?**

LLM punya context window terbatas (walaupun udah gede). Selain itu, chunk yang kecil bikin retrieval lebih presisi. Kalau kamu kirim 50 halaman dokumen, AI bakal overwhelmed. Tapi kalau kamu kirim 3 paragraf yang relevan, dia bisa jawab dengan fokus.

## Step 2: Create Embeddings & Vector Store

```python
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# Inisialisasi embedding model
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-small"  # Bagus, murah
)

# Simpan ke Chroma (local, gak perlu install apapun)
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory="./chroma_db",
    collection_name="product_docs"
)

print(f"Indexed {vectorstore._collection.count()} chunks")
```

Kalau mau pakai Pinecone (cloud, lebih scalable):

```python
from langchain_community.vectorstores import Pinecone
from pinecone import Pinecone

pc = Pinecone(api_key="your-pinecone-key")

vectorstore = Pinecone.from_documents(
    documents=chunks,
    embedding=embedding_model,
    index_name="product-docs",
    namespace="default"
)
```

## Step 3: Build RAG Chain

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.2  # RAG jawabannya harus akurat, jangan kreatif
)

# Format retrieved docs
def format_docs(docs):
    return "\n\n".join([
        f"[Sumber: {doc.metadata.get('source', 'unknown')}, "
        f"Halaman: {doc.metadata.get('page', 'N/A')}]\n{doc.page_content}"
        for doc in docs
    ])

# Prompt
RAG_PROMPT = ChatPromptTemplate.from_template("""
Kamu adalah asisten yang menjawab berdasarkan dokumen yang tersedia.

Aturan:
1. HANYA jawab berdasarkan context yang diberikan
2. Kalau informasi tidak ada di context, bilang "Data ini tidak tersedia di database kami"
3. Sebutkan sumber (nama file/halaman) saat memberikan jawaban
4. Jawab dalam bahasa Indonesia, gaya kasual

Context:
{context}

Pertanyaan: {question}

Jawaban:
""")

# Retriever — ambil top 3 chunks paling relevan
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

# RAG Chain
rag_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    }
    | RAG_PROMPT
    | llm
    | StrOutputParser()
)

# Test!
answer = rag_chain.invoke("Berapa harga MacBook Pro M3?")
print(answer)
```

Output-nya bakal kayak gini:

```
Berdasarkan katalog produk kami, MacBook Pro M3 dijual dengan harga
Rp 27.999.000 untuk varian 14 inch (RAM 18GB, Storage 512GB).

Sumber: product_catalog.pdf, Halaman: 3
```

Cakep kan? Sekarang AI jawabnya berdasarkan data real kita, bukan ngarang.

## Step 4: Bikin Chat Interface

```python
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage

st.title("🤖 Toko AI Assistant")
st.write("Tanya apapun soal produk kami!")

# Session state untuk chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chain = rag_chain

# Tampilkan chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
if prompt := st.chat_input("Ketik pertanyaanmu..."):
    # Tampilkan user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Mencari jawaban..."):
            response = st.session_state.chain.invoke(prompt)
            st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

# Jalankan: streamlit run app.py
```

## Tips: Bikin RAG-nya Lebih Bagus

Setelah trial and error berbulan-bulan, ini tips yang beneran bikin beda:

### 1. Optimasi Chunk Size

Chunk terlalu kecil = kehilangan konteks. Chunk terlalu besar = retrieval gak presisi. Sweet spot yang aku temukan:

```python
# Untuk dokumen teknis/formal
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)

# Untuk percakapan/chat logs
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=100
)

# Untuk kode/programming docs
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=300,
    separators=["\n\ndef ", "\nclass ", "\n\n", "\n", " "]
)
```

### 2. Pakai Metadata

```python
# Tambah metadata pas indexing
for doc in chunks:
    doc.metadata["category"] = "pricing"
    doc.metadata["last_updated"] = "2025-04-01"

# Filter retrieval berdasarkan metadata
retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 3,
        "filter": {"category": "pricing"}  # Hanya cari di pricing
    }
)
```

### 3. Hybrid Search

Gabungkan keyword search + semantic search:

```python
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

# Keyword-based retriever
bm25_retriever = BM25Retriever.from_documents(chunks)
bm25_retriever.k = 3

# Semantic retriever
semantic_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Ensemble — best of both worlds
ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, semantic_retriever],
    weights=[0.3, 0.7]  # Semantic lebih diprioritasin
)
```

### 4. Re-ranking

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain_cohere import CohereRerank

# Re-rank hasil retrieval untuk hasil lebih akurat
reranker = CohereRerank(
    model="rerank-v3.5",
    top_n=3
)

compression_retriever = ContextualCompressionRetriever(
    base_compressor=reranker,
    base_retriever=semantic_retriever
)
```

### 5. Multi-Query Retrieval

Kalau pertanyaan user ambigu, generate beberapa versi query:

```python
from langchain.retrievers.multi_query import MultiQueryRetriever

multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(),
    llm=ChatOpenAI(model="gpt-4", temperature=0.5),
    include_original=True
)

# Query: "yang murah" → generate query:
# "produk harga terjangkau"
# "diskon dan promo"
# "budget friendly"
```

## Pitfalls yang Sering Membuat RAG Jelek

**1. Data yang belum di-clean**
Garbage in, garbage out. Pastikan data yang dimasukkan bersih dari HTML tags, duplicate, dan noise.

```python
import re

def clean_text(text):
    # Hapus HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Hapus multiple spaces
    text = re.sub(r'\s+', ' ', text)
    # Hapus special characters yang gak perlu
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    return text.strip()
```

**2. Gak ada Grounding Check**
AI masih bisa hallucinate meskipun pakai RAG. Tambahin guard:

```python
def grounded_check(question, context, answer):
    """Cek apakah jawaban benar-benar dari context"""
    prompt = f"""Apakah jawaban ini didukung oleh context yang diberikan?

Context: {context}
Pertanyaan: {question}
Jawaban: {answer}

Jawab HANYA dengan: SUPPORTED atau NOT_SUPPORTED"""
    
    result = llm.invoke(prompt).content.strip()
    return "SUPPORTED" in result
```

**3. Stale Data**
Data lama masih ada di vector store setelah di-update. Implement periodic reindexing.

**4. Gak handle follow-up questions**
Pertanyaan follow-up kayak "itu yang tadi harganya berapa?" butuh chat history. Tambahin conversation memory:

```python
from langchain_core.prompts import MessagesPlaceholder

chat_history = []

CONDENSE_PROMPT = ChatPromptTemplate.from_template("""
Diberikan chat history dan pertanyaan terbaru, buatlah standalone question.

Chat History:
{chat_history}

Pertanyaan terbaru: {question}

Standalone question:
""")

def condense_question(question, history):
    response = llm.invoke(
        CONDENSE_PROMPT.format(
            chat_history=history,
            question=question
        )
    )
    return response.content.strip()

# Saat user bertanya
standalone_q = condense_question(
    "Yang warna merah ada gak?",
    chat_history
)
# → "Apakah ada produk berwarna merah yang tersedia?"
```

## Biaya Estimasi

Real talk: RAG punya cost.

- Embedding (text-embedding-3-small): ~$0.02 per 1M tokens
- Retrieval: Gratis (local) atau ~$0.1/1M ops (Pinecone)
- LLM call: ~$0.01-0.03 per query (GPT-4)

Untuk 1000 query per hari, estimasi ~$30-50/bulan. Cukup reasonable untuk production app.

## RAG Framework Comparison

Kalau kamu mau lebih cepat, ada framework yang bisa dipakai:

- **LangChain** — Paling banyak fitur, tapi complex
- **LlamaIndex** — Paling gampang buat RAG dedicated
- **Haystack** — Bagus untuk enterprise, production-ready

(Bandingin detail ketiganya di artikel [LangChain vs LlamaIndex vs Haystack](/tech-review/framework-ai-python-perbandingan/))

## Conclusion

RAG itu game-changer untuk bikin AI yang beneran useful. Dengan langkah-langkah di atas, kamu udah bisa bikin chatbot yang jawabnya based on data real, bukan ngarang.

Next steps yang aku rekomendasiin:
1. Implement di project kamu
2. Eksperimen dengan chunk size dan retrieval method
3. Monitor quality jawaban (bikin test set!)
4. Scale ke production

Mau sharing RAG project kamu? Chat aku di [kontak@dovi.my.id](mailto:kontak@dovi.my.id), seru kalau bisa bahas bareng!
