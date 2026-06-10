---
title: "Cara Setup VS Code untuk Web Development (2026)"
date: 2026-01-30
draft: false
slug: "setup-vs-code-web-development-2025"
description: "Tutorial setup VS Code untuk web development. Extensions, themes, dan shortcuts yang wajib ada."
categories: ['Tutorial']
tags: ['vs-code', 'setup', 'web-development', 'productivity']
ShowShareButtons: true
ShowReadingTime: true
ShowToc: true
---

Visual Studio Code adalah editor paling populer untuk web development di 2026. Menurut survey Stack Overflow, lebih dari 70% developer pakai VS Code sebagai editor utama. Tapi install VS Code doang belum cukup — tanpa setup yang benar, kamu bakal kehilangan banyak waktu setiap hari.

Di tutorial ini, aku bakal share setup VS Code yang aku pakai sehari-hari. Mulai dari extensions wajib, theme, settings.json configuration, sampai keyboard shortcuts yang bisa naikin produktivitas signifikan. Semua sudah tested di workflow real project, bukan sekadar rekomendasi teori.

## Install VS Code

### Download

Download langsung dari [code.visualstudio.com](https://code.visualstudio.com/). Tersedia untuk Windows, macOS, dan Linux.

### Linux (Ubuntu/Debian)

Kalau pakai Ubuntu atau distro Debian-based:

```bash
# Via snap (recommended)
sudo snap install code --classic

# Atau via apt
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list'
sudo apt update && sudo apt install code
```

### macOS

```bash
# Via Homebrew (recommended)
brew install --cask visual-studio-code
```

Atau download `.dmg` file dari website resmi.

### Post-Install

Setelah install, langsung buka terminal di VS Code (`Ctrl+`` ` ``) dan verifikasi:

```bash
code --version
```

Tambahkan `code` ke PATH agar bisa buka file/folder dari terminal:

```bash
# Buka Command Palette (Ctrl+Shift+P), ketik "Shell Command: Install 'code' command in PATH"
```

## Extensions Wajib

Ini 10 extensions yang wajib ada di VS Code kamu untuk web development. Setiap extension aku jelaskan fungsinya supaya kamu tahu kenapa penting.

### 1. ES7+ React/Redux/React-Native Snippets

Extension ini menambahkan snippet untuk React yang sangat mempercepat coding. Contoh:

- `rafce` → React Arrow Function Component with Export
- `usf` → useState snippet
- `uef` → useEffect snippet
- `nf` → Next.js functional component

Tanpa snippet, bikin satu komponen React butuh 30 detik. Dengan snippet, 5 detik.

### 2. Prettier - Code Formatter

Auto-format kode setiap kali save. Ini wajib banget, terutama kalau kerja team. Konsistensi formatting menghindari "format war" di code review.

Install, lalu tambahkan ke settings.json:

```json
{
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true,
  "prettier.singleQuote": true,
  "prettier.trailingComma": "es5",
  "prettier.tabWidth": 2,
  "prettier.semi": true,
  "prettier.printWidth": 80
}
```

Buat file `.prettierrc` di root project untuk override per-project:

```json
{
  "singleQuote": true,
  "trailingComma": "es5",
  "tabWidth": 2,
  "semi": true
}
```

### 3. ESLint

Static analysis untuk JavaScript dan TypeScript. Bantuin detect bug sebelum runtime. Wajib banget untuk project TypeScript.

Pastikan project kamu sudah install ESLint:

```bash
npm install -D eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin
```

Settings VS Code untuk ESLint:

```json
{
  "eslint.validate": [
    "javascript",
    "javascriptreact",
    "typescript",
    "typescriptreact"
  ],
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"
  }
}
```

### 4. GitLens

GitLens bikin Git experience di VS Code jauh lebih powerful. Fitur yang paling sering aku pakai:

- **Inline blame**: Lihat siapa yang terakhir edit baris tertentu, langsung di editor
- **Git history**: Browse file history tanpa keluar VS Code
- **Compare**: Perbandingan antar branch atau commit
- **Blame annotations**: Hover di atas kode untuk lihat detail commit

GitLens gratis untuk fitur dasar. Untuk team features ada versi Pro.

### 5. Auto Rename Tag

Rename tag HTML/JSX pembuka, tag penutup otomatis ikut berubah. Sepele tapi sangat menghemat waktu, especially saat refactor komponen besar.

### 6. Path Intellisense

Auto-complete untuk file path saat import. Kamu ketik `import Component from './com'` dan dia suggest `./components/`. Sangat helpful di project dengan struktur folder yang dalam.

### 7. Thunder Client

REST API client built-in di VS Code. Alternatif Postman yang lebih ringan. Kamu bisa test API endpoint langsung dari editor tanpa switch window.

Fitur-fitur:
- Buat collection untuk group API requests
- Environment variables untuk staging/production
- Import dari Postman collection
- GraphQL support

Kalau kamu lebih sering pakai Postman, baca juga [tutorial cara pakai Postman untuk API testing](/tutorial/cara-pakai-postman-api-testing/).

### 8. Error Lens

Tampilkan error dan warning langsung di baris kode, bukan hanya di Problems panel. Ini bikin kamu langsung tahu ada masalah tanpa harus scroll ke bawah atau buka panel.

### 9. indent-rainbow

Warnai indentasi dengan warna berbeda. Ini sangat membantu di file JSX/TSX yang nesting-nya dalam. Kamu langsung bisa identifikasi level indentasi tanpa hitung manual.

### 10. Material Icon Theme

File icons yang bikin navigasi di explorer jadi lebih cepat. Kamu langsung bisa bedakan file `.tsx`, `.ts`, `.css`, `.json` dari icon-nya. Tanpa ini, semua file kelihatan sama.

### Bonus Extensions

Beberapa extension tambahan yang useful:

- **Bracket Pair Colorizer** — Sudah built-in di VS Code terbaru, aktifkan dengan `"editor.bracketPairColorization.enabled": true`
- **Console Ninja** — Tampilkan `console.log` output langsung di editor
- **GitHub Copilot** — AI code completion. Baca [perbandingan Cursor vs Copilot vs Codeium](/tech-review/cursor-vs-copilot-vs-codeium-2025/) untuk opsi AI coding assistant.
- **Todo Tree** — Highlight dan kumpulkan semua `TODO` comment di project
- **Markdown All in One** — Preview markdown langsung di VS Code

## Theme Recommendation

Pilihan theme itu personal, tapi ini rekomendasiku berdasarkan pengalaman:

### Dark Theme

**One Dark Pro** — Theme paling populer untuk VS Code. Warna yang balanced antara kontras dan readability. Tidak bikin mata cepat lelah waktu coding malam.

```json
{
  "workbench.colorTheme": "One Dark Pro"
}
```

Alternatif:
- **Tokyo Night** — Warna biru-ungu yang calming
- **Catppuccin Mocha** — Pastel dark theme yang aesthetic
- **GitHub Dark** — Familiar kalau sering pakai GitHub

### Light Theme

**GitHub Light Default** — Terang, bersih, dan enak dibaca di siang hari. Cocok untuk yang prefer light mode.

```json
{
  "workbench.colorTheme": "GitHub Light Default"
}
```

### Font

Pakai font yang punya ligatures untuk coding. Rekomendasi:

```json
{
  "editor.fontFamily": "'JetBrains Mono', 'Fira Code', Menlo, monospace",
  "editor.fontLigatures": true,
  "editor.fontSize": 14,
  "editor.lineHeight": 1.6
}
```

Download [JetBrains Mono](https://www.jetbrains.com/lp/mono/) (gratis) — font yang didesain khusus untuk developer. Punya ligatures yang bikin operator seperti `=>`, `!==`, `>=` lebih mudah dibaca.

## settings.json Lengkap

Ini settings.json yang aku pakai. Copy-paste ke VS Code kamu (`Ctrl+Shift+P` → "Preferences: Open User Settings (JSON)"):

```json
{
  // Editor
  "editor.fontSize": 14,
  "editor.lineHeight": 1.6,
  "editor.fontFamily": "'JetBrains Mono', Menlo, monospace",
  "editor.fontLigatures": true,
  "editor.cursorBlinking": "smooth",
  "editor.cursorSmoothCaretAnimation": "on",
  "editor.smoothScrolling": true,
  "editor.minimap.enabled": false,
  "editor.bracketPairColorization.enabled": true,
  "editor.guides.bracketPairs": "active",
  "editor.wordWrap": "on",
  "editor.tabSize": 2,
  "editor.suggestSelection": "first",
  "editor.linkedEditing": true,
  "editor.stickyScroll.enabled": true,

  // Files
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 1000,
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,

  // Terminal
  "terminal.integrated.fontSize": 13,
  "terminal.integrated.defaultProfile.linux": "zsh",

  // Workbench
  "workbench.colorTheme": "One Dark Pro",
  "workbench.iconTheme": "material-icon-theme",
  "workbench.startupEditor": "none",

  // Emmet
  "emmet.includeLanguages": {
    "javascript": "javascriptreact",
    "typescript": "typescriptreact"
  },

  // TypeScript
  "typescript.updateImportsOnFileMove.enabled": "always",
  "typescript.preferences.importModuleSpecifier": "relative",

  // Prettier
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true,
  "prettier.singleQuote": true,
  "prettier.trailingComma": "es5",

  // ESLint
  "eslint.validate": ["javascript", "typescript", "typescriptreact"],
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"
  },

  // Git
  "git.autofetch": true,
  "git.confirmSync": false,
  "git.enableSmartCommit": true,

  // Search exclude
  "search.exclude": [
    "**/node_modules",
    "**/dist",
    "**/.next",
    "**/build",
    "**/.git"
  ]
}
```

## Keyboard Shortcuts

Keyboard shortcuts adalah investasi produktivitas terbesar. Pakai ini secara konsisten dan kamu bisa hemat 30-60 menit per hari.

### Navigation (Wajib Hafal)

| Shortcut | Fungsi |
|----------|--------|
| `Ctrl+P` | Quick open file — ketik nama file langsung buka |
| `Ctrl+Shift+P` | Command palette — akses semua command |
| `Ctrl+G` | Go to line number |
| `Ctrl+Tab` | Switch antar tab yang terbuka |
| `Ctrl+\` | Split editor (side by side) |

### Editing (Paling Sering Dipakai)

| Shortcut | Fungsi |
|----------|--------|
| `Ctrl+D` | Select next occurrence — sangat powerful untuk rename |
| `Ctrl+Shift+L` | Select ALL occurrences |
| `Alt+Up/Down` | Pindahkan baris ke atas/bawah |
| `Shift+Alt+Up/Down` | Duplicate baris |
| `Ctrl+Shift+K` | Hapus baris |
| `Ctrl+/` | Toggle comment |
| `Ctrl+Shift+F` | Search di semua file |
| `Ctrl+H` | Find and replace |

### Advanced (Power User)

| Shortcut | Fungsi |
|----------|--------|
| `Ctrl+Shift+[` | Fold/collapse code block |
| `Ctrl+Shift+]` | Unfold code block |
| `Ctrl+K Ctrl+C` | Add line comment |
| `Ctrl+K Ctrl+U` | Remove line comment |
| `F2` | Rename symbol (refactor) |
| `F12` | Go to definition |
| `Shift+F12` | Find all references |
| `Alt+Click` | Multiple cursor di posisi click |

### Tips Menghafal Shortcut

Jangan hafalkan semua sekaligus. Pakai teknik ini:

1. **Minggu 1**: Fokus di `Ctrl+P` dan `Ctrl+Shift+P`. Dua ini saja sudah bikin perbedaan besar.
2. **Minggu 2**: Tambah `Ctrl+D`, `Alt+Up/Down`, dan `Ctrl+Shift+K`.
3. **Minggu 3**: Tambah editing shortcuts lain.
4. **Minggu 4**: Mulai pakai advanced shortcuts.

Cara terbaik: setiap kali kamu lakukan action yang pakai mouse, tanyakan "ada shortcut-nya gak?" Lalu pakai shortcut-nya.

## Snippets Custom

Selain extensions, kamu bisa bikin custom snippets. Buka `Ctrl+Shift+P` → "Configure User Snippets", lalu pilih bahasa.

Contoh custom snippet untuk Next.js:

```json
{
  "Next.js Page Component": {
    "prefix": "npage",
    "body": [
      "export default function ${1:PageName}() {",
      "  return (",
      "    <main className=\"${2:container}\">",
      "      <h1>${3:Title}</h1>",
      "    </main>",
      "  );",
      "}"
    ],
    "description": "Next.js page component"
  },
  "API Route": {
    "prefix": "napi",
    "body": [
      "import { NextResponse } from 'next/server';",
      "",
      "export async function ${1:GET}(request: Request) {",
      "  try {",
      "    $2",
      "    return NextResponse.json({ data: $3 });",
      "  } catch (error) {",
      "    return NextResponse.json(",
      "      { error: 'Internal Server Error' },",
      "      { status: 500 }",
      "    );",
      "  }",
      "}"
    ],
    "description": "Next.js API route handler"
  }
}
```

## Terminal Integration

VS Code punya built-in terminal yang powerful. Beberapa tips:

### Multi Terminal

```bash
# Buka terminal baru
Ctrl+`

# Split terminal (side by side)
Ctrl+Shift+`

# Switch antar terminal
Ctrl+PageUp / Ctrl+PageDown
```

### Useful Terminal Settings

```json
{
  "terminal.integrated.defaultProfile.linux": "zsh",
  "terminal.integrated.fontSize": 13,
  "terminal.integrated.cursorStyle": "line",
  "terminal.integrated.scrollback": 5000
}
```

### Task Automation

Buat `.vscode/tasks.json` untuk automate command yang sering dipakai:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Dev Server",
      "type": "npm",
      "script": "dev",
      "problemMatcher": [],
      "isBackground": true
    },
    {
      "label": "Build",
      "type": "npm",
      "script": "build",
      "problemMatcher": ["$tsc"]
    },
    {
      "label": "Lint Fix",
      "type": "npm",
      "script": "lint",
      "args": ["--fix"]
    }
  ]
}
```

Jalankan via `Ctrl+Shift+P` → "Tasks: Run Task".

## VS Code + Git Workflow

Kalau kamu belum pakai Git, sekarang waktu yang tepat untuk mulai. Baca [tutorial belajar Git untuk pemula](/tutorial/belajar-git-30-menit-pemula/) untuk dasar-dasarnya.

Di VS Code, Git terintegrasi langsung:

1. **Source Control panel** (`Ctrl+Shift+G`): Lihat perubahan, stage, commit
2. **Git diff**: Klik file yang berubah untuk lihat perbandingan inline
3. **Branch**: Klik branch name di bottom-left untuk switch/create branch
4. **Merge conflicts**: Resolve langsung di editor dengan inline buttons

## Workflow Tips untuk Developer Indonesia

### Remote Development

Banyak developer Indonesia kerja remote untuk perusahaan luar. VS Code punya Remote Development extension pack:

- **Remote - SSH**: Code langsung di server remote
- **Remote - WSL**: Develop di Windows Subsystem for Linux
- **Dev Containers**: Develop di Docker container
- **Remote - Tunnels**: Akses VS Code dari browser

Ini sangat helpful kalau laptop kamu spec-nya terbatas — coding di server yang lebih powerful.

### Copilot & AI Assistant

GitHub Copilot sekarang tersedia untuk semua developer. Di Indonesia, ada alternatif gratis yang tidak kalah bagus:

- **Codeium** — 100% gratis untuk individual
- **Continue** — Open source, bisa pakai model lokal

Baca [review Cursor vs Copilot vs Codeium](/tech-review/cursor-vs-copilot-vs-codeium-2025/) untuk perbandingan lengkap.

### Backup Settings

Setelah setup yang rapi, backup settings supaya tidak hilang saat ganti device:

1. **Settings Sync** (built-in): Login dengan GitHub, sync settings, extensions, keybindings ke cloud
2. **Manual export**: `Ctrl+Shift+P` → "Preferences: Open User Settings (JSON)", copy file `settings.json`

## Troubleshooting Umum

### VS Code Lemmot/Lag

```json
{
  "files.watcherExclude": {
    "**/node_modules/**": true,
    "**/.git/objects/**": true,
    "**/.git/subtree-cache/**": true,
    "**/dist/**": true
  },
  "search.followSymlinks": false,
  "editor.minimap.enabled": false
}
```

### TypeScript Error Tapi Seharusnya Benar

Restart TypeScript server: `Ctrl+Shift+P` → "TypeScript: Restart TS Server"

### Extensions Tidak Jalan

Reload VS Code: `Ctrl+Shift+P` → "Developer: Reload Window"

## FAQ

### VS Code atau Cursor?
VS Code lebih stabil dan punya ekosistem extension yang lebih besar. Cursor lebih powerful untuk AI-assisted coding tapi masih baru. Untuk web development general, VS Code tetap pilihan yang aman. Baca perbandingan lengkapnya di [Cursor vs Copilot vs Codeium](/tech-review/cursor-vs-copilot-vs-codeium-2025/).

### Berapa banyak extension yang ideal?
Tidak ada batasan pasti, tapi terlalu banyak extension bisa bikin VS Code lambat. Idealnya 10-15 extensions. Kalau merasa lemot, cek "Show Running Extensions" untuk lihat mana yang makan resource.

### Apakah settings bisa di-share ke team?
Bisa. Commit `.vscode/settings.json` dan `.vscode/extensions.json` ke repository. Rekan team yang buka project akan dapat rekomendasi settings dan extensions.

### WSL atau native Windows untuk web development?
WSL2 jauh lebih baik. Tools seperti Docker, Git, dan Node.js jalan lebih lancar di Linux environment. VS Code punya Remote WSL extension yang bikin experience-nya seamless.

### Kenapa formatOnSave tidak jalan?
Pastikan Prettier di-set sebagai default formatter. Kalau ada formatter lain (misalnya formatter bawaan VS Code), bisa conflict. Cek di settings: `"editor.defaultFormatter": "esbenp.prettier-vscode"`.

---

Setup VS Code yang tepat bisa menghemat waktu 30-60 menit per hari. Itu artinya dalam setahun kamu bisa hemat lebih dari 200 jam — waktu yang bisa dipakai untuk belajar teknologi baru atau bikin side project.

**Ada tips lain?** Share di komentar!
