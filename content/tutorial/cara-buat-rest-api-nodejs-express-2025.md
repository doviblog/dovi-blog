---
title: "Cara Buat REST API dengan Node.js dan Express (2025)"
date: 2026-02-13
draft: false
slug: "cara-buat-rest-api-nodejs-express-2025"
description: "Tutorial lengkap membuat REST API dengan Node.js dan Express. Dari setup sampai production-ready."
categories: ['Tutorial']
tags: ['nodejs', 'express', 'rest-api', 'backend', 'tutorial']
ShowShareButtons: true
ShowReadingTime: true
ShowToc: true
---

REST API itu backbone dari hampir semua aplikasi modern. Di tutorial ini aku bakal jelasin cara bikin dari nol.

## Setup Project

```bash
mkdir my-api && cd my-api
npm init -y
npm install express dotenv cors helmet morgan
```

## Basic Server

```javascript
const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.get('/', (req, res) => {
  res.json({ message: 'API is running!' });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

## CRUD Operations

```javascript
// GET all
app.get('/api/users', (req, res) => {
  res.json(users);
});

// GET single
app.get('/api/users/:id', (req, res) => {
  const user = users.find(u => u.id === parseInt(req.params.id));
  if (!user) return res.status(404).json({ error: 'Not found' });
  res.json(user);
});

// POST create
app.post('/api/users', (req, res) => {
  const newUser = { id: nextId++, ...req.body };
  users.push(newUser);
  res.status(201).json(newUser);
});

// PUT update
app.put('/api/users/:id', (req, res) => {
  const index = users.findIndex(u => u.id === parseInt(req.params.id));
  if (index === -1) return res.status(404).json({ error: 'Not found' });
  users[index] = { ...users[index], ...req.body };
  res.json(users[index]);
});

// DELETE
app.delete('/api/users/:id', (req, res) => {
  const index = users.findIndex(u => u.id === parseInt(req.params.id));
  if (index === -1) return res.status(404).json({ error: 'Not found' });
  users.splice(index, 1);
  res.status(204).send();
});
```

## Best Practices

1. **Versioning** - `/api/v1/users`
2. **Pagination** - `?page=1&limit=10`
3. **Error handling**
4. **Input validation**
5. **Rate limiting**

## Conclusion

Dalam 1 jam, kamu udah punya REST API yang functional.

**Butuh bantuan?** DM di Telegram!
