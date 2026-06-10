---
title: "Tutorial LangChain Python untuk AI Agent"
date: 2026-06-10
draft: false
slug: "cara-pakai-langchain-python"
description: "Tutorial lengkap LangChain Python untuk membangun AI Agent. Dari instalasi sampai deploy, dengan contoh kode real-world."
categories: [AI Agent]
tags: ['langchain', 'python', 'ai', 'ai-agent', 'openai', 'llm']
ShowShareButtons: true
ShowReadingTime: true
ShowToc: true
---

LangChain jadi salah satu framework paling populer buat build AI Agent di Python. Di tutorial ini, aku bakal guide kamu dari nol sampai bisa bikin agent yang bisa search web, baca dokumen, dan maintain conversation context.

Kenapa LangChain? Karena dia handle banyak complexity di balik layar — memory management, tool orchestration, prompt chaining — jadi kamu bisa fokus ke logic bisnis.

## Apa itu LangChain?

LangChain adalah framework Python yang memudahkan pengembangan aplikasi yang menggunakan Large Language Models (LLM). Dia provide abstractions untuk:

- **Chains** — Rangkaian prompt dan LLM calls yang terstruktur
- **Agents** — LLM yang bisa pilih tools dan ambil keputusan
- **Memory** — Simpan dan kelola konteks percakapan
- **Retrieval** — Ambil informasi dari dokumen/database

Bayangin LangChain sebagai "middleware" antara aplikasi kamu dan LLM. Dia handle semua plumbing supaya kamu bisa build fitur canggih dengan kode minimal.

## Instalasi dan Setup

### Requirements

- Python 3.9+
- OpenAI API key (atau provider lain)
- Virtual environment (recommended)

### Step 1: Buat Virtual Environment

```bash
# Buat project directory
mkdir my-langchain-agent
cd my-langchain-agent

# Buat virtual environment
python -m venv venv

# Aktifkan
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

### Step 2: Install Dependencies

```bash
pip install langchain langchain-openai langchain-community python-dotenv
```

### Step 3: Setup Environment

Buat file `.env`:

```env
OPENAI_API_KEY=sk-your-api-key-here
```

Load di Python:

```python
from dotenv import load_dotenv
import os

load_dotenv()
# Sekarang os.environ["OPENAI_API_KEY"] sudah tersedia
```

## Hello World: Chain Pertama

Mulai dari yang paling simpel — buat chain yang menerima input dan menghasilkan output:

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Inisialisasi LLM
llm = ChatOpenAI(model="gpt-4", temperature=0.7)

# Buat prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "Kamu adalah expert Python developer. Jawab dengan singkat dan praktis."),
    ("user", "{question}")
])

# Buat chain
chain = prompt | llm | StrOutputParser()

# Jalankan
result = chain.invoke({"question": "Apa itu LangChain?"})
print(result)
```

Penjelasan:
- `ChatOpenAI` — Inisialisasi LLM dengan model tertentu
- `ChatPromptTemplate` — Template prompt yang bisa menerima variabel
- `StrOutputParser` — Parse output LLM ke string biasa
- `|` (pipe) — Operator untuk menggabungkan components jadi chain

## Menambah Tools ke Agent

Agent tanpa tools itu kayak developer tanpa keyboard. Di LangChain, tools adalah fungsi Python yang bisa dipanggil agent berdasarkan konteks.

### Definisikan Tools

```python
from langchain_core.tools import tool
import requests

@tool
def search_web(query: str) -> str:
    """Search the web for current information."""
    # Contoh sederhana — di production pakai API search beneran
    response = requests.get(
        f"https://api.search.example/search?q={query}"
    )
    return response.json()["results"]

@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression safely."""
    try:
        # Hanya izinkan operasi matematika dasar
        allowed = set("0123456789+-*/.() ")
        if all(c in allowed for c in expression):
            result = eval(expression)
            return str(result)
        return "Error: Invalid expression"
    except Exception as e:
        return f"Error: {e}"

@tool
def read_file(filepath: str) -> str:
    """Read content of a local text file."""
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: File '{filepath}' not found"
```

### Buat Agent dengan Tools

```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

# Setup LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Daftar tools
tools = [search_web, calculate, read_file]

# Prompt untuk agent
prompt = ChatPromptTemplate.from_messages([
    ("system", "Kamu adalah helpful assistant. Gunakan tools yang tersedia untuk menjawab pertanyaan user."),
    ("user", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

# Buat agent
agent = create_tool_calling_agent(llm, tools, prompt)

# Bungkus dengan executor
executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,  # Print proses reasoning
    max_iterations=5  # Batasi loop
)

# Jalankan
result = executor.invoke({"input": "Berapa hasil dari 123 * 456 + 789?"})
print(result["output"])
```

Agent akan:
1. Menerima pertanyaan
2. Memutuskan tool mana yang dipanggil (`calculate`)
3. Menjalankan tool dengan argumen yang tepat
4. Mengolah hasil dan memberikan jawaban

## Memory: Simpan Konteks Percakapan

Tanpa memory, agent kamu amnesia setiap turn. LangChain provide beberapa tipe memory:

### ConversationBufferMemory

Simpan semua percakapan:

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True  # Return sebagai message objects
)

# Tambah manual (untuk testing)
memory.save_context(
    {"input": "Halo, nama aku Dovi"},
    {"output": "Halo Dovi! Ada yang bisa aku bantu?"}
)

# Load memory
memory.load_memory_variables({})
```

### ConversationSummaryMemory

Ringkas percakapan lama untuk hemat token:

```python
from langchain.memory import ConversationSummaryMemory

memory = ConversationSummaryMemory(
    llm=llm,
    memory_key="chat_history",
    return_messages=True
)
```

### Integrasi dengan Agent

```python
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.memory import ConversationBufferMemory

# Setup memory
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# Buat agent (sama seperti sebelumnya)
agent = create_tool_calling_agent(llm, tools, prompt)

# Tambah memory ke executor
executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True
)

# Sekarang agent ingat konteks
executor.invoke({"input": "Nama aku Dovi"})
executor.invoke({"input": "Siapa nama aku?"})  # Akan ingat "Dovi"
```

## Retrieval: Agent yang Baca Dokumen

Ini fitur paling powerful — agent yang bisa baca dan cari informasi dari dokumen kamu.

### Setup Document Loader

```python
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load semua .txt dari folder
loader = DirectoryLoader("./docs/", glob="**/*.txt", loader_cls=TextLoader)
documents = loader.load()

# Split jadi chunks kecil
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = text_splitter.split_documents(documents)

print(f"Loaded {len(documents)} docs, split into {len(chunks)} chunks")
```

### Setup Vector Store

```python
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Buat embeddings
embeddings = OpenAIEmbeddings()

# Buat vector store dari chunks
vectorstore = FAISS.from_documents(chunks, embeddings)

# Buat retriever
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}  # Return 3 hasil paling relevan
)
```

### Buat RAG Agent

```python
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# Prompt untuk RAG
rag_prompt = ChatPromptTemplate.from_messages([
    ("system", "Jawab berdasarkan konteks berikut:\n\n{context}"),
    ("user", "{input}")
])

# Document chain
doc_chain = create_stuff_documents_chain(llm, rag_prompt)

# Retrieval chain
rag_chain = create_retrieval_chain(retriever, doc_chain)

# Jalankan
result = rag_chain.invoke({"input": "Apa isi dokumen tentang deployment?"})
print(result["answer"])
```

## Contoh Real-World: Customer Support Agent

Gabungkan semua konsep jadi satu agent yang utuh:

```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool

# LLM
llm = ChatOpenAI(model="gpt-4", temperature=0.3)

# Tools
@tool
def lookup_order(order_id: str) -> str:
    """Look up order status by order ID."""
    orders = {
        "ORD-001": "Processing",
        "ORD-002": "Shipped",
        "ORD-003": "Delivered"
    }
    return orders.get(order_id, "Order not found")

@tool
def escalate_to_human(reason: str) -> str:
    """Escalate complex issues to human support team."""
    return f"Escalated to human support. Reason: {reason}. Tim support akan menghubungi dalam 1x24 jam."

# Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", """Kamu adalah customer support agent. 
    - Jawab dengan sopan dan helpful
    - Gunakan tools untuk lookup informasi
    - Escalate ke human jika masalah terlalu kompleks
    - Selalu konfirmasi informasi ke user"""),
    ("user", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

# Memory (hanya simpan 10 turn terakhir)
memory = ConversationBufferWindowMemory(
    k=10,
    memory_key="chat_history",
    return_messages=True
)

# Agent
tools = [lookup_order, escalate_to_human]
agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    max_iterations=3
)

# Simulasi percakapan
print(executor.invoke({"input": "Halo, mau tanya status order ORD-002"}))
print(executor.invoke({"input": "Kapan sampainya?"}))
```

## Best Practices

### 1. Handle Errors Gracefully

```python
try:
    result = executor.invoke({"input": user_input})
except Exception as e:
    result = {"output": "Maaf, terjadi error. Coba lagi atau hubungi support."}
```

### 2. Limit Token Usage

```python
# Di prompt, tambahkan instruksi
system_prompt = """...Jawab dalam maksimal 200 kata..."""

# Atau set max_tokens di LLM
llm = ChatOpenAI(model="gpt-4", max_tokens=500)
```

### 3. Test Tools Secara Terpisah

```python
# Unit test tools
assert calculate("2 + 2") == "4"
assert lookup_order("ORD-001") == "Processing"
```

### 4. Monitor Penggunaan

```python
# Callback untuk tracking
from langchain.callbacks import get_openai_callback

with get_openai_callback() as cb:
    result = executor.invoke({"input": "test"})
    print(f"Tokens: {cb.total_tokens}")
    print(f"Cost: ${cb.total_cost:.4f}")
```

## Troubleshooting

**Error: "Could not import langchain"**
```bash
pip install --upgrade langchain langchain-openai
```

**Error: "API key not found"**
```python
import os
os.environ["OPENAI_API_KEY"] = "sk-..."
# Atau pakai .env + load_dotenv()
```

**Agent terlalu banyak iterasi**
```python
executor = AgentExecutor(..., max_iterations=3, early_stopping_method="generate")
```

**Memory terlalu besar**
```python
# Pakai window memory
memory = ConversationBufferWindowMemory(k=5, ...)
# Atau summary memory
memory = ConversationSummaryMemory(llm=llm, ...)
```

## FAQ

### Berapa biaya pakai LangChain?

LangChain itu **gratis** (open source). Yang bayar adalah LLM provider (OpenAI, Anthropic, dll). Biaya tergantung usage — untuk development/testing, biasanya <$1/bulan.

### LangChain vs LlamaIndex?

LangChain lebih general-purpose (agents, chains, tools). LlamaIndex lebih fokus ke retrieval dan indexing dokumen. Kalau fokusnya RAG, LlamaIndex lebih optimized. Kalau butuh agents dengan tools, LangChain lebih fleksibel.

### Bisa pakai selain OpenAI?

Bisa! LangChain support banyak provider:
- Anthropic (Claude)
- Google (Gemini)
- Ollama (local models)
- HuggingFace
- Dan banyak lagi

```python
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model="claude-3-opus-20240229")
```

### Aman untuk production?

LangChain sendiri aman, tapi perlu perhatikan:
- API key management (jangan hardcode)
- Rate limiting
- Error handling
- Cost monitoring

## Kesimpulan

LangChain bikin build AI Agent jadi jauh lebih mudah. Dengan konsep Chains, Agents, Memory, dan Retrieval, kamu bisa bikin aplikasi AI yang sophisticated tanpa harus handle semua complexity dari nol.

Mulai dari yang simpel, tambah fitur satu per satu, dan test thoroughly sebelum deploy.

Ada pertanyaan atau mau request tutorial lain? Email aku di [kontak@dovi.my.id](mailto:kontak@dovi.my.id). Jangan lupa share ke temen-temen yang butuh!

**Selamat mencoba!** 🚀
