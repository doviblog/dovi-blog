#!/usr/bin/env python3
import os

BASE_DIR = os.path.expanduser("~/dovi-blog/content")

articles = [
    {"cat": "ai-agent", "slug": "multi-agent-orchestration-guide", "title": "Guide: Multi-Agent Orchestration untuk Complex Tasks", "date": "2025-05-01", "desc": "Cara setup multiple AI agents yang bekerja sama menyelesaikan task kompleks.", "tags": ["multi-agent", "orchestration", "advanced"]},
    {"cat": "ai-agent", "slug": "rag-retrieval-augmented-generation", "title": "RAG 101: Build AI yang Bisa Akses Database Kamu", "date": "2025-05-05", "desc": "Tutorial Retrieval Augmented Generation untuk AI yang lebih cerdas.", "tags": ["rag", "vector-db", "embeddings"]},
    {"cat": "tutorial", "slug": "cara-setup-ci-cd-github-actions", "title": "Cara Setup CI/CD dengan GitHub Actions (Gratis)", "date": "2025-05-10", "desc": "Tutorial setup CI/CD pipeline menggunakan GitHub Actions. Automate testing dan deployment.", "tags": ["ci-cd", "github-actions", "automation"]},
    {"cat": "tutorial", "slug": "belajar-typescript-dari-nol", "title": "Belajar TypeScript dari Nol (2025)", "date": "2025-05-15", "desc": "Tutorial TypeScript untuk JavaScript developer. Dari basic types sampai generics.", "tags": ["typescript", "javascript", "tutorial"]},
    {"cat": "tutorial", "slug": "cara-pakai-postman-api-testing", "title": "Cara Pakai Postman untuk API Testing (Lengkap)", "date": "2025-05-20", "desc": "Tutorial Postman untuk testing API. Collections, environments, dan automated tests.", "tags": ["postman", "api", "testing"]},
    {"cat": "tutorial", "slug": "setup-linux-server-dari-nol", "title": "Setup Linux Server dari Nol untuk Web App", "date": "2025-05-25", "desc": "Tutorial setup Linux server production-ready. Nginx, SSL, firewall, monitoring.", "tags": ["linux", "server", "devops"]},
    {"cat": "tech-review", "slug": "brower-ai-terbaik-2025", "title": "5 Browser AI Terbaik di 2025 (Review)", "date": "2025-06-01", "desc": "Review 5 browser dengan fitur AI terbaik: Arc, Sigma, Brave, dan lainnya.", "tags": ["browser", "ai", "review"]},
    {"cat": "tech-review", "slug": "framework-ai-python-perbandingan", "title": "LangChain vs LlamaIndex vs Haystack: Framework AI Python", "date": "2025-06-05", "desc": "Perbandingan 3 framework AI Python populer untuk RAG dan agents.", "tags": ["python", "ai-framework", "comparison"]},
    {"cat": "tech-review", "slug": "no-code-ai-tools-review-2025", "title": "Review: 5 No-Code AI Tools untuk Non-Programmer", "date": "2025-06-10", "desc": "Review no-code AI tools: Dify, Flowise, Botpress, dan lainnya.", "tags": ["no-code", "ai-tools", "review"]},
    {"cat": "tutorial", "slug": "cara-monetize-blog-adsense", "title": "Cara Monetize Blog dengan AdSense (Step-by-Step)", "date": "2025-06-15", "desc": "Tutorial lengkap monetize blog dengan Google AdSense. Dari setup sampai optimize revenue.", "tags": ["adsense", "monetize", "blogging"]}
]

for a in articles:
    content = f'''---
title: "{a['title']}"
date: {a['date']}
draft: false
slug: "{a['slug']}"
description: "{a['desc']}"
categories: [{a['cat'].replace('-', ' ').title()}]
tags: {a['tags']}
ShowShareLinks: true
ShowReadingTime: true
ShowToc: true
---

Artikel coming soon. Stay tuned!

Kunjungi [Telegram](https://t.me/dovi) untuk update terbaru.
'''
    outdir = os.path.join(BASE_DIR, a['cat'])
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, f"{a['slug']}.md")
    with open(path, 'w') as f:
        f.write(content)
    print(f"✓ {a['cat']}/{a['slug']}.md")

print(f"\n✅ Generated {len(articles)} articles")
