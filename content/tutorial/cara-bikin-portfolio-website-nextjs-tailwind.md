---
title: "Cara Bikin Portfolio Website dalam 1 Hari (Next.js + Tailwind)"
date: 2026-03-16
draft: false
slug: "cara-bikin-portfolio-website-nextjs-tailwind"
description: "Tutorial bikin portfolio website profesional dalam 1 hari menggunakan Next.js dan Tailwind CSS."
categories: ['Tutorial']
tags: ['portfolio', 'nextjs', 'tailwind', 'web-development']
ShowShareButtons: true
ShowReadingTime: true
ShowToc: true
---

Portfolio website itu kartu nama digital kamu sebagai developer. Di era remote work dan hiring global, recruiter hampir selalu ngecek portfolio sebelum lanjut ke interview. Yang bikin kaget, banyak developer Indonesia dengan skill bagus tapi gak punya portfolio online.

Di tutorial ini, aku bakal jelasin langkah-langkah bikin portfolio website profesional dalam 1 hari menggunakan Next.js dan Tailwind CSS. Kenapa dua stack ini? Karena Next.js memberikan performa dan SEO yang solid, sementara Tailwind bikin proses styling jadi sangat cepat tanpa perlu bikin CSS dari nol.

## Kenapa Next.js + Tailwind?

Sebelum mulai coding, penting untuk paham kenapa kombinasi ini ideal untuk portfolio:

**Next.js:**
- Server-side rendering (SSR) dan static site generation (SSG) untuk SEO optimal
- File-based routing yang intuitif
- Image optimization built-in dengan `next/image`
- Fast refresh untuk development yang cepat
- Deploy gampang ke Vercel (gratis)

**Tailwind CSS:**
- Utility-first, jadi kamu styling langsung di markup
- Responsive design tinggal tambah prefix `md:`, `lg:`
- Dark mode support dengan satu class
- File CSS production sangat kecil karena tree-shaking
- Konsisten tanpa perlu bikin design system dari nol

## Prasyarat

Pastikan kamu sudah punya:
- **Node.js 18+** terinstall (cek dengan `node --version`)
- **npm atau yarn** (npm sudah include dengan Node.js)
- **Text editor** — rekomendasiku VS Code, baca [setup VS Code untuk web development](/tutorial/setup-vs-code-web-development-2025/)
- **Git** terinstall untuk version control dan deploy
- **GitHub account** untuk push kode dan deploy ke Vercel

## Step 1: Setup Project

Buka terminal dan jalankan command berikut:

```bash
npx create-next-app@latest my-portfolio
```

Pilih opsi berikut saat setup wizard muncul:
```
Would you like to use TypeScript? → Yes
Would you like to use ESLint? → Yes
Would you like to use Tailwind CSS? → Yes
Would you like to use `src/` directory? → Yes
Would you like to use App Router? → Yes
Would you like to customize the default import alias? → No
```

Masuk ke folder project:

```bash
cd my-portfolio
npm run dev
```

Buka `http://localhost:3000` di browser. Kalau muncul halaman default Next.js, setup berhasil.

### Struktur Folder

Buat struktur folder yang rapi untuk project portfolio:

```bash
mkdir -p src/components src/data src/app/projects
```

Hasilnya:
```
my-portfolio/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   ├── components/
│   └── data/
├── public/
│   └── images/
├── tailwind.config.ts
└── package.json
```

## Step 2: Data Portfolio

Biar mudah di-maintain, pisahkan data portfolio ke file terpisah. Buat `src/data/portfolio.ts`:

```typescript
export const profile = {
  name: "Dovi Developer",
  role: "Full Stack Developer",
  location: "Jakarta, Indonesia",
  email: "hello@dovi.my.id",
  github: "https://github.com/dovi",
  linkedin: "https://linkedin.com/in/dovi",
  bio: "Full Stack Developer yang fokus di Next.js, React, dan Node.js. Suka bikin tools yang solve masalah nyata.",
};

export const skills = [
  { name: "Next.js", level: 90 },
  { name: "React", level: 85 },
  { name: "TypeScript", level: 80 },
  { name: "Node.js", level: 75 },
  { name: "Tailwind CSS", level: 90 },
  { name: "PostgreSQL", level: 70 },
  { name: "Docker", level: 65 },
  { name: "AWS", level: 60 },
];

export const projects = [
  {
    title: "E-Commerce Platform",
    description:
      "Platform e-commerce full-stack dengan fitur payment gateway Midtrans, admin dashboard, dan real-time inventory tracking.",
    tech: ["Next.js", "Prisma", "PostgreSQL", "Midtrans"],
    image: "/images/ecommerce.jpg",
    github: "https://github.com/dovi/ecommerce",
    live: "https://ecommerce-demo.dovi.my.id",
  },
  {
    title: "Task Management App",
    description:
      "Aplikasi manajemen tugas dengan drag-and-drop, real-time collaboration, dan notifikasi via email.",
    tech: ["React", "Node.js", "Socket.io", "MongoDB"],
    image: "/images/taskmanager.jpg",
    github: "https://github.com/dovi/taskmanager",
    live: "https://taskmanager.dovi.my.id",
  },
  {
    title: "AI Chatbot Assistant",
    description:
      "Chatbot berbasis LLM untuk customer service UMKM. Support Bahasa Indonesia dan integrasi WhatsApp.",
    tech: ["Python", "FastAPI", "OpenAI", "Tailwind"],
    image: "/images/chatbot.jpg",
    github: "https://github.com/dovi/chatbot",
    live: "https://chatbot.dovi.my.id",
  },
];

export const experience = [
  {
    company: "Tech Startup ID",
    role: "Frontend Developer",
    period: "2024 - Sekarang",
    highlights: [
      "Bangun dashboard analytics yang dipakai 5000+ user",
      "Redesign UI yang naikin conversion rate 35%",
      "Implement CI/CD pipeline dengan GitHub Actions",
    ],
  },
  {
    company: "Digital Agency Jakarta",
    role: "Junior Developer",
    period: "2023 - 2024",
    highlights: [
      "Develop 15+ website klien menggunakan WordPress dan Next.js",
      "Setup development workflow yang reduce delivery time 40%",
    ],
  },
];
```

## Step 3: Build Komponen

### Navbar

Buat `src/components/Navbar.tsx`:

```tsx
"use client";
import { useState } from "react";
import Link from "next/link";

const navLinks = [
  { href: "#about", label: "Tentang" },
  { href: "#skills", label: "Skill" },
  { href: "#projects", label: "Project" },
  { href: "#experience", label: "Pengalaman" },
  { href: "#contact", label: "Kontak" },
];

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="fixed top-0 w-full bg-white/80 dark:bg-gray-950/80 backdrop-blur-md z-50 border-b border-gray-200 dark:border-gray-800">
      <div className="max-w-5xl mx-auto px-4 py-4 flex justify-between items-center">
        <Link href="/" className="text-xl font-bold text-gray-900 dark:text-white">
          {"<dovi />"}
        </Link>

        {/* Desktop Navigation */}
        <div className="hidden md:flex gap-6">
          {navLinks.map((link) => (
            <a
              key={link.href}
              href={link.href}
              className="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors text-sm font-medium"
            >
              {link.label}
            </a>
          ))}
        </div>

        {/* Mobile Menu Button */}
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="md:hidden text-gray-600 dark:text-gray-300"
          aria-label="Toggle menu"
        >
          {isOpen ? "✕" : "☰"}
        </button>
      </div>

      {/* Mobile Navigation */}
      {isOpen && (
        <div className="md:hidden px-4 pb-4 space-y-2">
          {navLinks.map((link) => (
            <a
              key={link.href}
              href={link.href}
              onClick={() => setIsOpen(false)}
              className="block py-2 text-gray-600 dark:text-gray-300 hover:text-blue-600"
            >
              {link.label}
            </a>
          ))}
        </div>
      )}
    </nav>
  );
}
```

### Hero Section

Buat `src/components/Hero.tsx`:

```tsx
import { profile } from "@/data/portfolio";

export default function Hero() {
  return (
    <section className="min-h-screen flex items-center justify-center px-4">
      <div className="max-w-3xl text-center">
        <p className="text-blue-600 dark:text-blue-400 font-medium mb-4">
          Halo, saya
        </p>
        <h1 className="text-4xl md:text-6xl font-bold text-gray-900 dark:text-white mb-4">
          {profile.name}
        </h1>
        <h2 className="text-2xl md:text-3xl text-gray-600 dark:text-gray-300 mb-6">
          {profile.role}
        </h2>
        <p className="text-lg text-gray-500 dark:text-gray-400 mb-8 max-w-xl mx-auto">
          {profile.bio}
        </p>
        <div className="flex gap-4 justify-center">
          <a
            href="#projects"
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
          >
            Lihat Project
          </a>
          <a
            href="#contact"
            className="px-6 py-3 border border-gray-300 dark:border-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:border-blue-600 hover:text-blue-600 transition-colors font-medium"
          >
            Hubungi Saya
          </a>
        </div>
      </div>
    </section>
  );
}
```

### Project Card

Buat `src/components/ProjectCard.tsx`:

```tsx
import Image from "next/image";

interface ProjectProps {
  title: string;
  description: string;
  tech: string[];
  image: string;
  github: string;
  live: string;
}

export default function ProjectCard({
  title,
  description,
  tech,
  image,
  github,
  live,
}: ProjectProps) {
  return (
    <div className="group border border-gray-200 dark:border-gray-800 rounded-xl overflow-hidden hover:shadow-lg transition-all duration-300">
      <div className="relative h-48 bg-gray-100 dark:bg-gray-800">
        <Image
          src={image}
          alt={title}
          fill
          className="object-cover group-hover:scale-105 transition-transform duration-300"
        />
      </div>
      <div className="p-5">
        <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2">
          {title}
        </h3>
        <p className="text-gray-600 dark:text-gray-400 text-sm mb-4 line-clamp-3">
          {description}
        </p>
        <div className="flex flex-wrap gap-2 mb-4">
          {tech.map((t) => (
            <span
              key={t}
              className="px-2 py-1 text-xs bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded-md font-medium"
            >
              {t}
            </span>
          ))}
        </div>
        <div className="flex gap-3">
          <a
            href={github}
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-gray-600 dark:text-gray-400 hover:text-blue-600 transition-colors"
          >
            GitHub →
          </a>
          <a
            href={live}
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-gray-600 dark:text-gray-400 hover:text-blue-600 transition-colors"
          >
            Live Demo →
          </a>
        </div>
      </div>
    </div>
  );
}
```

### Contact Section

Buat `src/components/Contact.tsx`:

```tsx
import { profile } from "@/data/portfolio";

export default function Contact() {
  return (
    <section id="contact" className="py-20 px-4">
      <div className="max-w-2xl mx-auto text-center">
        <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
          Hubungi Saya
        </h2>
        <p className="text-gray-600 dark:text-gray-400 mb-8">
          Tertarik bekerja sama? Kirim email atau connect di sosial media.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <a
            href={`mailto:${profile.email}`}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
          >
            Kirim Email
          </a>
          <a
            href={profile.github}
            target="_blank"
            rel="noopener noreferrer"
            className="px-6 py-3 border border-gray-300 dark:border-gray-700 rounded-lg hover:border-blue-600 transition-colors font-medium"
          >
            GitHub
          </a>
          <a
            href={profile.linkedin}
            target="_blank"
            rel="noopener noreferrer"
            className="px-6 py-3 border border-gray-300 dark:border-gray-700 rounded-lg hover:border-blue-600 transition-colors font-medium"
          >
            LinkedIn
          </a>
        </div>
      </div>
    </section>
  );
}
```

## Step 4: Halaman Utama

Edit `src/app/page.tsx` untuk menggabungkan semua komponen:

```tsx
import Navbar from "@/components/Navbar";
import Hero from "@/components/Hero";
import ProjectCard from "@/components/ProjectCard";
import Contact from "@/components/Contact";
import { projects, skills, experience, profile } from "@/data/portfolio";

export default function Home() {
  return (
    <>
      <Navbar />
      <main className="bg-white dark:bg-gray-950">
        <Hero />

        {/* About */}
        <section id="about" className="py-20 px-4 bg-gray-50 dark:bg-gray-900">
          <div className="max-w-3xl mx-auto">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-8 text-center">
              Tentang Saya
            </h2>
            <div className="prose dark:prose-invert max-w-none">
              <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                {profile.bio} Berdomisili di {profile.location} dengan pengalaman
                membangun web application yang scalable dan user-friendly. Fokus
                pada tech stack modern seperti Next.js, React, dan Node.js.
              </p>
            </div>
          </div>
        </section>

        {/* Skills */}
        <section id="skills" className="py-20 px-4">
          <div className="max-w-3xl mx-auto">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-8 text-center">
              Skill & Teknologi
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {skills.map((skill) => (
                <div key={skill.name} className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="font-medium text-gray-700 dark:text-gray-300">
                      {skill.name}
                    </span>
                    <span className="text-gray-500">{skill.level}%</span>
                  </div>
                  <div className="h-2 bg-gray-200 dark:bg-gray-800 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-blue-600 rounded-full transition-all duration-1000"
                      style={{ width: `${skill.level}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Projects */}
        <section id="projects" className="py-20 px-4 bg-gray-50 dark:bg-gray-900">
          <div className="max-w-5xl mx-auto">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-8 text-center">
              Project
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {projects.map((project) => (
                <ProjectCard key={project.title} {...project} />
              ))}
            </div>
          </div>
        </section>

        {/* Experience */}
        <section id="experience" className="py-20 px-4">
          <div className="max-w-3xl mx-auto">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-8 text-center">
              Pengalaman
            </h2>
            <div className="space-y-8">
              {experience.map((exp) => (
                <div
                  key={exp.company}
                  className="border-l-2 border-blue-600 pl-6"
                >
                  <h3 className="text-lg font-bold text-gray-900 dark:text-white">
                    {exp.role}
                  </h3>
                  <p className="text-blue-600 dark:text-blue-400 font-medium mb-2">
                    {exp.company} · {exp.period}
                  </p>
                  <ul className="space-y-1">
                    {exp.highlights.map((h, i) => (
                      <li
                        key={i}
                        className="text-gray-600 dark:text-gray-400 text-sm"
                      >
                        • {h}
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>
        </section>

        <Contact />
      </main>
    </>
  );
}
```

## Step 5: SEO & Metadata

Edit `src/app/layout.tsx` untuk menambahkan metadata SEO:

```tsx
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Dovi Developer — Full Stack Developer Jakarta",
  description:
    "Portfolio Dovi Developer, Full Stack Developer di Jakarta. Spesialisasi Next.js, React, dan Node.js.",
  keywords: ["developer", "portfolio", "nextjs", "react", "jakarta", "indonesia"],
  openGraph: {
    title: "Dovi Developer — Full Stack Developer",
    description: "Portfolio & project showcase",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="id" className="scroll-smooth">
      <body className={`${inter.className} antialiased`}>{children}</body>
    </html>
  );
}
```

## Step 6: Responsive Check

Sebelum deploy, pastikan website responsive. Tailwind bikin ini gampang dengan breakpoint prefix:

```html
<!-- Mobile: 1 kolom, Tablet: 2 kolom, Desktop: 3 kolom -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
```

Test di berbagai ukuran:
- **Mobile**: 375px (iPhone SE)
- **Tablet**: 768px (iPad)
- **Desktop**: 1280px (laptop)

Gunakan DevTools di browser (`Ctrl+Shift+M` di Firefox/Chrome) untuk responsive testing.

## Step 7: Deploy ke Vercel

Portfolio sudah selesai, sekarang saatnya deploy biar bisa diakses publik.

### Push ke GitHub

```bash
git init
git add .
git commit -m "feat: initial portfolio website"
git remote add origin https://github.com/username/my-portfolio.git
git push -u origin main
```

Kalau belum familiar dengan Git, baca [tutorial belajar Git dalam 30 menit](/tutorial/belajar-git-30-menit-pemula/).

### Import ke Vercel

1. Buka [vercel.com](https://vercel.com) dan login dengan GitHub
2. Klik **"Add New → Project"**
3. Pilih repository `my-portfolio`
4. Vercel auto-detect Next.js, klik **"Deploy"**
5. Tunggu 1-2 menit, portfolio kamu live!

### Custom Domain

Kalau sudah punya domain sendiri:
1. Masuk ke project settings di Vercel
2. Klik **"Domains"**
3. Tambahkan domain kamu
4. Update DNS records sesuai instruksi Vercel

Domain `.com` biasanya sekitar Rp 130.000-160.000/tahun. Bisa beli di Namecheap, Cloudflare Registrar, atau Niagahoster.

## Tips Portfolio yang Menarik untuk Recruiter

Setelah bantu beberapa teman bikin portfolio dan dapat feedback dari recruiter, ini pola yang bikin portfolio dilirik:

**1. Highlight Impact, Bukan Hanya Fitur**
Jangan tulis "Buat website e-commerce". Lebih baik: "Bangun e-commerce yang handle 500+ transaksi/bulan dengan Midtrans payment gateway."

**2. Show Your Code**
Link ke GitHub repo yang clean. Recruiter tech kadang langsung cek kode kamu. Pastikan ada README yang informatif.

**3. Live Demo Wajib Ada**
Portfolio tanpa live demo seperti CV tanpa pengalaman. Deploy semua project yang layak ditunjukkan.

**4. Keep It Simple**
Portfolio bukan tempat show off animasi ribet. Prioritas: cepat load, mudah navigasi, informasi jelas.

**5. Update Berkala**
Portfolio yang terakhir update 2 tahun lalu memberi kesan developer yang tidak aktif. Minimal update setiap 3-6 bulan.

## Performa Website

Karena pakai Next.js dan Tailwind, performa portfolio kamu seharusnya sudah excellent out of the box. Untuk memastikan:

- **Lighthouse score**: Target 90+ untuk semua kategori
- **First Contentful Paint**: < 1.5 detik
- **Largest Contentful Paint**: < 2.5 detik
- **Total bundle size**: < 200KB (tanpa gambar)

Tips tambahan untuk optimasi:
- Kompres gambar sebelum upload (pakai [Squoosh](https://squoosh.app/) atau TinyPNG)
- Gunakan `next/image` untuk lazy loading otomatis
- Hindari import library besar yang tidak perlu

## FAQ

### Apakah Next.js terlalu berat untuk portfolio sederhana?
Tidak juga. Next.js support static export, jadi hasilnya bisa jadi file HTML/CSS/JS biasa yang sangat ringan. Static generation di Next.js menghasilkan website yang cepat dan SEO-friendly.

### Berapa biaya total untuk portfolio ini?
Gratis. Vercel free tier sudah cukup untuk portfolio personal. Kamu hanya perlu bayar domain kalau mau custom domain (sekitar Rp 130.000/tahun). Kalau belum mau beli domain, Vercel kasih subdomain gratis.

### Apakah perlu database untuk portfolio?
Tidak. Portfolio statis dengan data hardcoded di file TypeScript sudah cukup. Kalau nanti butuh CMS, bisa tambahkan Contentlayer atau MDX untuk blog, atau pakai Sanity/Strapi untuk content management.

### Bagaimana cara bikin animasi yang bagus?
Gunakan Framer Motion untuk animasi React yang smooth. Install dengan `npm install framer-motion` dan tambahkan entry animation di setiap section. Tapi jangan berlebihan — animasi yang terlalu banyak bikin website terasa lambat.

### Bisa pakai template daripada bikin dari nol?
Bisa. Beberapa template gratis yang bagus: [Tailwind UI](https://tailwindui.com/), [HyperUI](https://hyperui.dev/), atau cari "Next.js portfolio template" di GitHub. Tapi kalau mau belajar, bikin dari nol lebih bermanfaat.

### Bagaimana cara menambahkan blog ke portfolio?
Tambahkan folder `/blog` di app router dan pakai MDX untuk menulis konten markdown yang bisa di-render sebagai React component. Next.js support ini dengan package `@next/mdx`.

---

Portfolio yang bagus itu investasi waktu yang sangat worth it. Dalam 1 hari, kamu bisa punya website profesional yang bisa dipakai bertahun-tahun. Mulai dari yang sederhana, iterasi seiring waktu.

**Butuh bantuan?** Email aku di [kontak@dovi.my.id](mailto:kontak@dovi.my.id)!
