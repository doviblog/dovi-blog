---
title: "Cara Deploy AI Agent ke Production (Docker + Railway)"
date: 2026-01-13
draft: false
slug: "deploy-ai-agent-production-docker-railway"
description: "Tutorial deploy AI agent ke production menggunakan Docker dan Railway. Step-by-step dari local ke live."
categories: ['AI Agent', 'Tutorial']
tags: ['ai-agent', 'docker', 'railway', 'deploy', 'production']
ShowShareButtons: true
ShowReadingTime: true
ShowToc: true
---

Local development udah beres? Sekarang saatnya deploy ke production biar bisa dipake orang lain.

## Kenapa Railway?

- **Free tier** tersedia
- **Auto-deploy** dari GitHub
- **No infra management**
- **Support Docker**

## Step 1: Dockerize AI Agent

Buat `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "main.py"]
```

Buat `requirements.txt`:

```
openai==1.3.0
flask==3.0.0
python-dotenv==1.0.0
gunicorn==21.2.0
```

## Step 2: Web API Wrapper

```python
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message')
    
    if not message:
        return jsonify({'error': 'Message required'}), 400
    
    try:
        response = generate_response(message)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
```

## Step 3: Deploy ke Railway

1. Push ke GitHub
2. Login ke railway.app
3. New Project > Deploy from GitHub repo
4. Set environment variables
5. Auto-deploy!

## Cost Breakdown

**Railway Free Tier:**
- 500 hours/month
- 1GB RAM
- Sufficient untuk testing

**Railway Pro:** $5/month
- Unlimited hours
- 8GB RAM

## Conclusion

Deploy AI agent ke production gak serumit yang dibayangkan. Dengan Docker + Railway, kamu bisa live dalam 30 menit.

**Butuh bantuan deploy?** DM di Telegram!
