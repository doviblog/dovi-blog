---
title: "Cara Install dan Setup Cursor AI di VS Code (2025)"
date: 2025-12-16
draft: false
slug: "install-setup-cursor-ai-2025"
description: "Tutorial lengkap install dan setup Cursor AI di VS Code. Tips productivity dan comparison dengan Copilot."
categories: ['Tutorial']
tags: ['cursor', 'ai', 'vs-code', 'productivity']
ShowShareButtons: true
ShowReadingTime: true
ShowToc: true
---

Cursor AI itu game-changer banget untuk developer. Basically VS Code dengan AI built-in yang lebih powerful dari Copilot.

Di tutorial ini aku bakal ngejelasin cara install dan setup Cursor biar workflow kamu makin produktif.

## Apa itu Cursor?

Cursor itu fork dari VS Code dengan AI integration native. Bedanya sama VS Code biasa:

- **AI Chat** - Tanya-tanya langsung di editor
- **Code completion** - Suggestion lebih akurat
- **Codebase understanding** - AI paham整个 project
- **Apply edits** - AI bisa edit file langsung

## Cara Install

### Windows

1. Download dari [cursor.sh](https://cursor.sh)
2. Run installer
3. Login dengan GitHub/Google account
4. Import VS Code settings (otomatis)

### macOS

```bash
# Via Homebrew
brew install --cask cursor

# Atau download langsung dari cursor.sh
```

### Linux

```bash
# Download .deb/.AppImage dari cursor.sh
# Install
sudo dpkg -i cursor_*.deb
```

## Setup Pertama

### 1. Import Extensions

Cursor otomatis detect extensions dari VS Code. Tapi kalau belum muncul:

1. Buka Extensions panel (`Ctrl+Shift+X`)
2. Search extension yang kamu punya di VS Code
3. Install satu-satu

### 2. Setup AI

1. Klik icon AI di sidebar (atau `Ctrl+L`)
2. Login dengan account Cursor
3. Pilih model (default: Claude Sonnet)

### 3. Keyboard Shortcuts

Default shortcuts:
- `Ctrl+L` - Open AI chat
- `Ctrl+K` - Quick edit
- `Ctrl+I` - Inline edit
- `Ctrl+Shift+L` - Add file to context

**Customize:** `File > Preferences > Keyboard Shortcuts`

## Fitur Unggulan

### 1. AI Chat

Buka panel chat (`Ctrl+L`) dan tanya apa aja:

```
You: Jelaskan flow authentication di project ini
AI: [Analyses codebase and explains]
```

**Pro tips:**
- Tambahin file ke context (`@filename`)
- Tanya spesifik, jangan general
- Follow up questions diperbolehkan

### 2. Quick Edit

Highlight kode, tekan `Ctrl+K`, kasih instruksi:

```
Make this function async and add error handling
```

AI bakal suggest edit, kamu tinggal accept/reject.

### 3. Codebase Indexing

Cursor index整个 project kamu:

1. Buka Command Palette (`Ctrl+Shift+P`)
2. Ketik "Cursor: Index Codebase"
3. Tunggu selesai (5-10 menit untuk project gede)

Setelah itu AI bisa reference semua file di project.

### 4. Multi-File Edits

AI bisa edit beberapa file sekaligus:

```
You: Create a new auth middleware and update all route files to use it
AI: [Creates middleware.js, updates routes/auth.js, routes/user.js]
```

## Tips Productivity

### 1. Context Management

**Tambahin file ke context:**
- Drag & drop file ke chat
- Atau ketik `@` + nama file

**Pilih code section:**
- Highlight kode dulu
- Baru buka AI chat
- Kode otomatis masuk context

### 2. Writing Good Prompts

**Bad prompt:** "Fix this code"
**Good prompt:** "This function throws TypeError when user is null. Add null check and return appropriate error message."

### 3. Iterative Development

```
1. Ask AI to generate initial code
2. Review and test
3. Ask for specific improvements
4. Repeat until满意
```

### 4. Code Review

```
You: Review this function for security issues and suggest improvements
AI: [Lists potential issues and suggests fixes]
```

## Comparison: Cursor vs Copilot

| Feature | Cursor | Copilot |
|---------|--------|---------|
| AI Chat | ✓ | ✗ |
| Code completion | ✓ | ✓ |
| Codebase understanding | ✓ | Limited |
| Multi-file edits | ✓ | ✗ |
| Price | $20/mo (Pro) | $10/mo |

**Kesimpulan:** Cursor lebih powerful untuk complex workflows. Copilot lebih murah untuk basic code completion.

## Troubleshooting

**AI gak nyala?**
- Cek internet connection
- Login ulang ke Cursor account
- Restart editor

**Index lambat?**
- Exclude folder besar (node_modules, .git)
- Check RAM usage
- Close heavy extensions

**Suggestion jelek?**
- Kasih lebih banyak context
- Specify language/framework
- Use `.cursorrules` file

## .cursorrules

Buat file `.cursorrules` di root project:

```markdown
# Project Guidelines

- Use TypeScript
- Follow ESLint rules
- Use functional components
- Prefer const over let
- Add JSDoc comments
```

AI bakal follow rules ini di semua suggestions.

## Conclusion

Cursor AI bisa increase productivity 2-3x kalau dipake bener. Kuncinya:

1. Master keyboard shortcuts
2. Learn effective prompting
3. Use codebase indexing
4. Iterate and refine

**Butuh bantuan setup?** DM di Telegram!
