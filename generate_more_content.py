#!/usr/bin/env python3
"""
Generate additional articles to reach 30+ total
"""

import os

BASE_DIR = os.path.expanduser("~/dovi-blog/content")

ADDITIONAL_ARTICLES = [
    {
        "category": "ai-agent",
        "title": "Tutorial: Bikin AI Agent yang Baca PDF dan Kasih Summary",
        "slug": "tutorial-ai-agent-baca-pdf-summary",
        "date": "2025-03-05",
        "categories": ["AI Agent", "Tutorial"],
        "tags": ["ai-agent", "pdf", "summary", "python"],
        "description": "Tutorial lengkap membuat AI agent yang bisa baca PDF dan generate summary otomatis menggunakan Python.",
        "content": "Punya tumpukan PDF yang gak kebaca? Di tutorial ini aku bakal ngejelasin cara bikin AI agent yang bisa baca PDF dan kasih summary dalam hitungan detik.\n\n## Kenapa Butuh AI PDF Reader?\n\nBayangin kamu punya 100 dokumen research paper. Manual baca butuh berhari-hari. Pakai AI? 30 menit beres.\n\n**Use cases:**\n- Research paper analysis\n- Legal document review\n- Business report summarization\n- Academic literature review\n\n## Persiapan\n\n1. Python 3.9+\n2. OpenAI API key\n3. Library: PyPDF2, langchain, openai\n\nInstall dependencies:\n\n```bash\npip install PyPDF2 langchain openai tiktoken\n```\n\n## Step 1: PDF Parser\n\nBuat fungsi untuk extract text dari PDF:\n\n```python\nimport PyPDF2\nfrom typing import List\n\ndef extract_text_from_pdf(pdf_path: str) -> str:\n    text = \"\"\n    with open(pdf_path, 'rb') as file:\n        reader = PyPDF2.PdfReader(file)\n        for page in reader.pages:\n            text += page.extract_text() + \"\\n\"\n    return text\n\ndef chunk_text(text: str, chunk_size: int = 4000) -> List[str]:\n    words = text.split()\n    chunks = []\n    current_chunk = []\n    current_size = 0\n    \n    for word in words:\n        current_chunk.append(word)\n        current_size += len(word) + 1\n        \n        if current_size >= chunk_size:\n            chunks.append(' '.join(current_chunk))\n            current_chunk = []\n            current_size = 0\n    \n    if current_chunk:\n        chunks.append(' '.join(current_chunk))\n    \n    return chunks\n```\n\n## Step 2: AI Summarizer\n\n```python\nfrom openai import OpenAI\n\nclient = OpenAI()\n\ndef summarize_chunk(chunk: str, prompt: str = None) -> str:\n    if not prompt:\n        prompt = \"\"\"Summarize the following text in Indonesian. \n        Focus on key points, main arguments, and conclusions.\n        Keep it concise but comprehensive.\"\"\"\n    \n    response = client.chat.completions.create(\n        model=\"gpt-4\",\n        messages=[\n            {\"role\": \"system\", \"content\": prompt},\n            {\"role\": \"user\", \"content\": chunk}\n        ],\n        temperature=0.3\n    )\n    \n    return response.choices[0].message.content\n```\n\n## Step 3: Main Agent\n\n```python\ndef summarize_pdf(pdf_path: str, output_format: str = \"bullet\") -> str:\n    print(f\"Reading PDF: {pdf_path}\")\n    text = extract_text_from_pdf(pdf_path)\n    \n    if not text.strip():\n        return \"Error: Could not extract text from PDF\"\n    \n    chunks = chunk_text(text)\n    print(f\"Found {len(chunks)} chunks\")\n    \n    summaries = []\n    for i, chunk in enumerate(chunks):\n        print(f\"Summarizing chunk {i+1}/{len(chunks)}...\")\n        summary = summarize_chunk(chunk)\n        summaries.append(summary)\n    \n    combined = \"\\n\\n\".join(summaries)\n    \n    if len(summaries) > 1:\n        print(\"Generating final summary...\")\n        final_prompt = f\"\"\"Combine these summaries into one comprehensive summary.\n        Format: {output_format}\n        Language: Indonesian\"\"\"\n        final = summarize_chunk(combined, final_prompt)\n    else:\n        final = summaries[0]\n    \n    return final\n```\n\n## Tips Production-Ready\n\n1. **Use embeddings** - Untuk find relevant chunks lebih akurat\n2. **Cache results** - Simpan summary biar gak re-process\n3. **Handle large PDFs** - Implement streaming\n4. **Error handling** - PDF corrupt, encrypted\n5. **Rate limiting** - Respect OpenAI rate limits\n\n## Conclusion\n\nBikin AI PDF reader itu straightforward. Dengan Python dan OpenAI API, kamu bisa automate document analysis.\n\n**Next steps:**\n- Build web interface\n- Add multi-PDF support\n- Implement vector search untuk Q&A\n\n**Butuh bantuan?** Chat aku di Telegram!"
    },
    {
        "category": "ai-agent",
        "title": "Cara Deploy AI Agent ke Production (Docker + Railway)",
        "slug": "deploy-ai-agent-production-docker-railway",
        "date": "2025-03-10",
        "categories": ["AI Agent", "Tutorial"],
        "tags": ["ai-agent", "docker", "railway", "deploy", "production"],
        "description": "Tutorial deploy AI agent ke production menggunakan Docker dan Railway. Step-by-step dari local ke live.",
        "content": "Local development udah beres? Sekarang saatnya deploy ke production biar bisa dipake orang lain.\n\n## Kenapa Railway?\n\n- **Free tier** tersedia\n- **Auto-deploy** dari GitHub\n- **No infra management**\n- **Support Docker**\n\n## Step 1: Dockerize AI Agent\n\nBuat `Dockerfile`:\n\n```dockerfile\nFROM python:3.11-slim\n\nWORKDIR /app\n\nRUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*\n\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\n\nCOPY . .\n\nEXPOSE 8080\n\nCMD [\"python\", \"main.py\"]\n```\n\nBuat `requirements.txt`:\n\n```\nopenai==1.3.0\nflask==3.0.0\npython-dotenv==1.0.0\ngunicorn==21.2.0\n```\n\n## Step 2: Web API Wrapper\n\n```python\nfrom flask import Flask, request, jsonify\nimport os\n\napp = Flask(__name__)\n\n@app.route('/health')\ndef health():\n    return jsonify({'status': 'ok'})\n\n@app.route('/chat', methods=['POST'])\ndef chat():\n    data = request.json\n    message = data.get('message')\n    \n    if not message:\n        return jsonify({'error': 'Message required'}), 400\n    \n    try:\n        response = generate_response(message)\n        return jsonify({'response': response})\n    except Exception as e:\n        return jsonify({'error': str(e)}), 500\n\nif __name__ == '__main__':\n    port = int(os.getenv('PORT', 8080))\n    app.run(host='0.0.0.0', port=port)\n```\n\n## Step 3: Deploy ke Railway\n\n1. Push ke GitHub\n2. Login ke railway.app\n3. New Project > Deploy from GitHub repo\n4. Set environment variables\n5. Auto-deploy!\n\n## Cost Breakdown\n\n**Railway Free Tier:**\n- 500 hours/month\n- 1GB RAM\n- Sufficient untuk testing\n\n**Railway Pro:** $5/month\n- Unlimited hours\n- 8GB RAM\n\n## Conclusion\n\nDeploy AI agent ke production gak serumit yang dibayangkan. Dengan Docker + Railway, kamu bisa live dalam 30 menit.\n\n**Butuh bantuan deploy?** DM di Telegram!"
    },
    {
        "category": "tutorial",
        "title": "Belajar Git dalam 30 Menit (Tutorial untuk Pemula)",
        "slug": "belajar-git-30-menit-pemula",
        "date": "2025-03-15",
        "categories": ["Tutorial"],
        "tags": ["git", "version-control", "pemula", "tutorial"],
        "description": "Tutorial Git untuk pemula. Belajar dari nol sampai bisa collaborate dalam 30 menit.",
        "content": "Git itu intimidating banget buat pemula. Tapi tenang, di tutorial ini aku bakal jelasin Git dari nol.\n\n## Git Itu Apa?\n\nGit itu version control system. Bayangin punya \"save point\" di game, tapi untuk kode.\n\n## Install Git\n\n### Windows\nDownload dari git-scm.com\n\n### macOS\n```bash\nxcode-select --install\n```\n\n### Linux\n```bash\nsudo apt install git\n```\n\n## Basic Commands\n\n```bash\ngit init                    # Buat repo baru\ngit add .                   # Add semua ke staging\ngit commit -m \"msg\"         # Commit\ngit status                  # Check status\ngit log                     # History\ngit branch                  # List branches\ngit checkout -b name        # New branch\ngit merge name              # Merge branch\ngit push                    # Push ke remote\ngit pull                    # Pull dari remote\n```\n\n## Cheat Sheet\n\n| Command | Fungsi |\n|---------|--------|\n| `git init` | Buat repo baru |\n| `git add .` | Add semua ke staging |\n| `git commit -m \"msg\"` | Commit |\n| `git status` | Check status |\n| `git log` | History |\n| `git push` | Push ke remote |\n| `git pull` | Pull dari remote |\n\n## Best Practices\n\n1. **Atomic commits** - Satu commit = satu fitur/fix\n2. **Good commit messages** - Jelas dan deskriptif\n3. **Branch per fitur**\n4. **Pull before push**\n5. **.gitignore** - Exclude file gak perlu\n\n## Conclusion\n\nDalam 30 menit, kamu udah belajar basic Git. Practice makes perfect!\n\n**Ada pertanyaan?** Komen di bawah!"
    },
    {
        "category": "tutorial",
        "title": "Cara Setup VS Code untuk Web Development (2025)",
        "slug": "setup-vs-code-web-development-2025",
        "date": "2025-03-20",
        "categories": ["Tutorial"],
        "tags": ["vs-code", "setup", "web-development", "productivity"],
        "description": "Tutorial setup VS Code untuk web development. Extensions, themes, dan shortcuts yang wajib ada.",
        "content": "VS Code itu editor paling populer di 2025. Di tutorial ini aku bakal share setup yang aku pake.\n\n## Extensions Wajib\n\n1. **ES7+ React Snippets**\n2. **Prettier** - Auto-format\n3. **ESLint** - Code linting\n4. **GitLens** - Git supercharged\n5. **Auto Rename Tag**\n6. **Path Intellisense**\n7. **Thunder Client** - REST API client\n8. **Error Lens** - Inline errors\n9. **indent-rainbow**\n10. **Material Icon Theme**\n\n## Theme Recommendation\n\n- **Light:** GitHub Light Default\n- **Dark:** One Dark Pro\n\n## Keyboard Shortcuts\n\n- `Ctrl+P` - Quick open file\n- `Ctrl+Shift+P` - Command palette\n- `Ctrl+D` - Select next occurrence\n- `Alt+Up/Down` - Move line\n- `Ctrl+Shift+K` - Delete line\n- `Ctrl+/` - Toggle comment\n\n## Conclusion\n\nSetup VS Code yang bener bisa save waktu 30-60 menit per hari.\n\n**Ada tips lain?** Share di komentar!"
    },
    {
        "category": "tutorial",
        "title": "Belajar Docker untuk Pemula (Tutorial Lengkap 2025)",
        "slug": "belajar-docker-pemula-2025",
        "date": "2025-03-25",
        "categories": ["Tutorial"],
        "tags": ["docker", "container", "devops", "pemula"],
        "description": "Tutorial Docker untuk pemula. Dari install sampai deploy containerized application.",
        "content": "Docker itu intimidating banget buat pemula. Tapi sebenernya simple kok.\n\n## Docker Itu Apa?\n\nBayangin kamu punya aplikasi yang jalan di laptop. Tapi pas dipindah ke server, error karena environment beda.\n\nDocker solve masalah itu dengan packaging aplikasi + dependencies jadi satu unit.\n\n## Install Docker\n\n### Windows/macOS\nDownload Docker Desktop\n\n### Linux\n```bash\ncurl -fsSL https://get.docker.com | sh\nsudo usermod -aG docker $USER\n```\n\n## Hello World\n\n```bash\ndocker run hello-world\n```\n\n## Dockerfile\n\n```dockerfile\nFROM node:18-alpine\n\nWORKDIR /app\n\nCOPY package*.json ./\nRUN npm install\n\nCOPY . .\n\nEXPOSE 3000\n\nCMD [\"node\", \"index.js\"]\n```\n\n## Build & Run\n\n```bash\ndocker build -t my-app .\ndocker run -d -p 3000:3000 my-app\n```\n\n## Docker Compose\n\n```yaml\nversion: '3.8'\nservices:\n  app:\n    build: .\n    ports:\n      - \"3000:3000\"\n  db:\n    image: postgres:15\n    environment:\n      - POSTGRES_PASSWORD=***\n```\n\n## Basic Commands\n\n```bash\ndocker ps                  # List containers\ndocker stop my-container   # Stop\ndocker rm my-container     # Remove\ndocker logs my-container   # Logs\n```\n\n## Conclusion\n\nDocker dalam 15 menit. Practice: Containerize aplikasi kamu sekarang!\n\n**Pertanyaan?** Komen di bawah!"
    },
    {
        "category": "tutorial",
        "title": "Cara Buat REST API dengan Node.js dan Express (2025)",
        "slug": "cara-buat-rest-api-nodejs-express-2025",
        "date": "2025-04-01",
        "categories": ["Tutorial"],
        "tags": ["nodejs", "express", "rest-api", "backend", "tutorial"],
        "description": "Tutorial lengkap membuat REST API dengan Node.js dan Express. Dari setup sampai production-ready.",
        "content": "REST API itu backbone dari hampir semua aplikasi modern. Di tutorial ini aku bakal jelasin cara bikin dari nol.\n\n## Setup Project\n\n```bash\nmkdir my-api && cd my-api\nnpm init -y\nnpm install express dotenv cors helmet morgan\n```\n\n## Basic Server\n\n```javascript\nconst express = require('express');\nconst app = express();\nconst PORT = process.env.PORT || 3000;\n\napp.use(express.json());\n\napp.get('/', (req, res) => {\n  res.json({ message: 'API is running!' });\n});\n\napp.listen(PORT, () => {\n  console.log(`Server running on port ${PORT}`);\n});\n```\n\n## CRUD Operations\n\n```javascript\n// GET all\napp.get('/api/users', (req, res) => {\n  res.json(users);\n});\n\n// GET single\napp.get('/api/users/:id', (req, res) => {\n  const user = users.find(u => u.id === parseInt(req.params.id));\n  if (!user) return res.status(404).json({ error: 'Not found' });\n  res.json(user);\n});\n\n// POST create\napp.post('/api/users', (req, res) => {\n  const newUser = { id: nextId++, ...req.body };\n  users.push(newUser);\n  res.status(201).json(newUser);\n});\n\n// PUT update\napp.put('/api/users/:id', (req, res) => {\n  const index = users.findIndex(u => u.id === parseInt(req.params.id));\n  if (index === -1) return res.status(404).json({ error: 'Not found' });\n  users[index] = { ...users[index], ...req.body };\n  res.json(users[index]);\n});\n\n// DELETE\napp.delete('/api/users/:id', (req, res) => {\n  const index = users.findIndex(u => u.id === parseInt(req.params.id));\n  if (index === -1) return res.status(404).json({ error: 'Not found' });\n  users.splice(index, 1);\n  res.status(204).send();\n});\n```\n\n## Best Practices\n\n1. **Versioning** - `/api/v1/users`\n2. **Pagination** - `?page=1&limit=10`\n3. **Error handling**\n4. **Input validation**\n5. **Rate limiting**\n\n## Conclusion\n\nDalam 1 jam, kamu udah punya REST API yang functional.\n\n**Butuh bantuan?** DM di Telegram!"
    },
    {
        "category": "tutorial",
        "title": "Cara Bikin Portfolio Website dalam 1 Hari (Next.js + Tailwind)",
        "slug": "cara-bikin-portfolio-website-nextjs-tailwind",
        "date": "2025-04-25",
        "categories": ["Tutorial"],
        "tags": ["portfolio", "nextjs", "tailwind", "web-development"],
        "description": "Tutorial bikin portfolio website profesional dalam 1 hari menggunakan Next.js dan Tailwind CSS.",
        "content": "Portfolio website itu kartu nama digital kamu. Di tutorial ini aku bakal jelasin cara bikin dalam 1 hari.\n\n## Setup\n\n```bash\nnpx create-next-app@latest my-portfolio\ncd my-portfolio\n```\n\n## Components to Build\n\n1. **Navbar** - Navigation\n2. **Hero** - Landing section\n3. **About** - About me\n4. **Projects** - Portfolio showcase\n5. **Contact** - Contact form\n6. **Footer** - Links & copyright\n\n## Deploy\n\n1. Push ke GitHub\n2. Import ke Vercel\n3. Add custom domain\n\nDone! Portfolio live dalam 1 hari.\n\n## Tips\n\n1. Keep it simple\n2. Fast loading\n3. Mobile responsive\n4. Show best work\n5. Clear CTA\n\n**Butuh bantuan?** DM di Telegram!"
    },
    {
        "category": "tech-review",
        "title": "Review: 5 Hosting Terbaik untuk Developer Indonesia (2025)",
        "slug": "review-5-hosting-terbaik-developer-indonesia-2025",
        "date": "2025-04-05",
        "categories": ["Tech Review"],
        "tags": ["hosting", "review", "indonesia", "web-hosting"],
        "description": "Review 5 hosting terbaik untuk developer Indonesia. Perbandingan harga, performance, dan support.",
        "content": "Pilih hosting itu confusing banget. Setelah coba belasan hosting, ini 5 yang recommended.\n\n## 1. Cloudways ($14/bln)\n\nBest overall untuk production. Managed cloud hosting.\n\n## 2. Niagahoster (Rp 10rb/bln)\n\nBest budget option. Server lokal Indonesia.\n\n## 3. Hostinger ($2.99/bln)\n\nBest value. Interface bagus untuk pemula.\n\n## 4. DigitalOcean ($4/bln)\n\nBest untuk developers. Full control.\n\n## 5. Vercel (Free)\n\nBest untuk frontend. Deploy dari GitHub.\n\n## Rekomendasi\n\n- **Personal Blog:** Niagahoster\n- **Startup:** Cloudways\n- **Portfolio:** Vercel\n- **Full Control:** DigitalOcean\n\n**Punya pengalaman hosting lain?** Share di komentar!"
    },
    {
        "category": "tech-review",
        "title": "Cursor vs Copilot vs Codeium: AI Code Assistant Terbaik 2025",
        "slug": "cursor-vs-copilot-vs-codeium-2025",
        "date": "2025-04-10",
        "categories": ["Tech Review"],
        "tags": ["ai", "coding", "comparison", "productivity"],
        "description": "Perbandingan 3 AI code assistant terbaik: Cursor, GitHub Copilot, dan Codeium.",
        "content": "AI code assistant udah jadi tools wajib developer di 2025. Mana yang paling bagus?\n\n## Cursor ($20/bln)\n- AI-native code editor\n- Multi-file editing\n- Codebase understanding\n\n## Copilot ($10/bln)\n- GitHub integration\n- Fast suggestions\n- Good for boilerplate\n\n## Codeium (Free)\n- Free!\n- Decent quality\n- Good for learning\n\n## Verdict\n\n- **Best Overall:** Cursor\n- **Best Value:** Codeium (gratis!)\n- **Best Middle Ground:** Copilot\n\n**Kamu pakai yang mana?**"
    },
    {
        "category": "tech-review",
        "title": "Review Jujur: Railway vs Render vs Fly.io (Platform PaaS 2025)",
        "slug": "review-railway-vs-render-vs-flyio-2025",
        "date": "2025-04-15",
        "categories": ["Tech Review"],
        "tags": ["paas", "deploy", "cloud", "comparison"],
        "description": "Review jujur 3 platform PaaS terbaik: Railway, Render, dan Fly.io.",
        "content": "Deploy aplikasi seharusnya gampang. Pilih platform yang bener itu yang bikin pusing.\n\n## Railway (Pro $5/bln)\n- Best DX\n- Simple pricing\n- Fast deploy\n\n## Render ($7/bln Starter)\n- Very reliable\n- Good for production\n- Predictable costs\n\n## Fly.io (Pay-as-you-go)\n- Edge deployment\n- Flexible pricing\n- Global\n\n## Verdict\n\n- **Beginners:** Railway\n- **Production:** Render\n- **Global:** Fly.io\n\n**Kamu pakai platform mana?**"
    }
]

def generate_article(article_data, output_dir):
    content = f"""---
title: "{article_data['title']}"
date: {article_data['date']}
draft: false
slug: "{article_data['slug']}"
description: "{article_data['description']}"
categories: {article_data['categories']}
tags: {article_data['tags']}
ShowShareButtons: true
ShowReadingTime: true
ShowToc: true
---

{article_data['content']}
"""
    filepath = os.path.join(output_dir, f"{article_data['slug']}.md")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return filepath

def main():
    total = 0
    for article in ADDITIONAL_ARTICLES:
        category = article['category']
        output_dir = os.path.join(BASE_DIR, category)
        os.makedirs(output_dir, exist_ok=True)
        filepath = generate_article(article, output_dir)
        total += 1
        print(f"✓ [{category}] {article['slug']}.md")
    print(f"\n✅ Generated {total} additional articles")

if __name__ == "__main__":
    main()
