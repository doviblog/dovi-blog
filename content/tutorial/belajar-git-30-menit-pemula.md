---
title: "Belajar Git dalam 30 Menit (Tutorial untuk Pemula)"
date: 2026-01-24
draft: false
slug: "belajar-git-30-menit-pemula"
description: "Tutorial Git untuk pemula. Belajar dari nol sampai bisa collaborate dalam 30 menit."
categories: ['Tutorial']
tags: ['git', 'version-control', 'pemula', 'tutorial']
ShowShareButtons: true
ShowReadingTime: true
ShowToc: true
---

Git itu intimidating banget buat pemula. Tapi tenang, di tutorial ini aku bakal jelasin Git dari nol.

## Git Itu Apa?

Git itu version control system. Bayangin punya "save point" di game, tapi untuk kode.

## Install Git

### Windows
Download dari git-scm.com

### macOS
```bash
xcode-select --install
```

### Linux
```bash
sudo apt install git
```

## Basic Commands

```bash
git init                    # Buat repo baru
git add .                   # Add semua ke staging
git commit -m "msg"         # Commit
git status                  # Check status
git log                     # History
git branch                  # List branches
git checkout -b name        # New branch
git merge name              # Merge branch
git push                    # Push ke remote
git pull                    # Pull dari remote
```

## Cheat Sheet

| Command | Fungsi |
|---------|--------|
| `git init` | Buat repo baru |
| `git add .` | Add semua ke staging |
| `git commit -m "msg"` | Commit |
| `git status` | Check status |
| `git log` | History |
| `git push` | Push ke remote |
| `git pull` | Pull dari remote |

## Best Practices

1. **Atomic commits** - Satu commit = satu fitur/fix
2. **Good commit messages** - Jelas dan deskriptif
3. **Branch per fitur**
4. **Pull before push**
5. **.gitignore** - Exclude file gak perlu

## Conclusion

Dalam 30 menit, kamu udah belajar basic Git. Practice makes perfect!

**Ada pertanyaan?** Komen di bawah!
