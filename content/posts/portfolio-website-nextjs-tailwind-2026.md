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

Portfolio website itu kartu nama digital kamu. Kalau kamu seorang developer, desainer, atau freelancer, punya website portfolio sendiri itu **wajib** di tahun 2026. Klien dan recruiter sekarang cari kandidat lewat Google — kalau nama kamu nggak muncul, ya kalah saing.

Di tutorial ini aku bakal jelasin step-by-step cara bikin portfolio website profesional pakai **Next.js 15** dan **Tailwind CSS v4**. Nggak perlu pengalaman frontend mahir — cukup paham HTML/CSS dasar dan sedikit React. Targetnya: dalam 1 hari website kamu sudah live di internet.

## Kenapa Next.js + Tailwind CSS?

Sebelum mulai coding, penting buat paham kenapa stack ini jadi favorit developer Indonesia (dan dunia) di 2026:

- **Next.js** — React framework yang support SSR, SSG, dan App Router. Performa luar biasa, SEO-friendly, dan ecosystem besar.
- **Tailwind CSS** — Utility-first CSS framework. Nggak perlu nulis CSS dari nol, cukup pakai class langsung di JSX.
- **Vercel** — Hosting gratis yang terintegrasi sempurna dengan Next.js. Deploy cuma sekali klik dari GitHub.

Kombinasi ini mempercepat development secara signifikan. Portfolio yang biasanya butuh seminggu, bisa selesai dalam hitungan jam.

## Step 1: Setup Project Next.js

Buka terminal dan jalankan command berikut untuk membuat project baru:

```bash
npx create-next-app@latest my-portfolio
```

Saat installer berjalan, pilih opsi berikut:

- **TypeScript?** → Yes
- **ESLint?** → Yes
- **Tailwind CSS?** → Yes
- **src/ directory?** → Yes
- **App Router?** → Yes
- **Turbopack?** → Yes

Masuk ke folder project dan jalankan development server:

```bash
cd my-portfolio
npm run dev
```

Buka `http://localhost:3000` di browser. Kalau muncul halaman default Next.js, berarti setup berhasil!

## Step 2: Struktur Folder & Komponen

Buat folder `components` di dalam `src/app/` dan siapkan komponen-komponen ini:

```
src/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   └── globals.css
├── components/
│   ├── Navbar.tsx
│   ├── Hero.tsx
│   ├── About.tsx
│   ├── Projects.tsx
│   ├── Contact.tsx
│   └── Footer.tsx
```

Kita akan build satu per satu komponen ini. Setiap komponen menggunakan Tailwind class supaya styling cepat dan konsisten.

## Step 3: Buat Navbar Responsive

Navbar yang clean dan responsive itu penting banget. Berikut contoh komponen Navbar dengan hamburger menu untuk mobile:

```tsx
"use client";
import { useState } from "react";
import Link from "next/link";

const navLinks = [
  { href: "#about", label: "Tentang" },
  { href: "#projects", label: "Proyek" },
  { href: "#contact", label: "Kontak" },
];

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="fixed top-0 w-full bg-white/80 backdrop-blur-md z-50 border-b">
      <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
        <Link href="/" className="text-xl font-bold text-indigo-600">
          Dovi.dev
        </Link>
        {/* Desktop */}
        <div className="hidden md:flex gap-6">
          {navLinks.map((link) => (
            <a key={link.href} href={link.href} className="hover:text-indigo-600 transition">
              {link.label}
            </a>
          ))}
        </div>
        {/* Mobile toggle */}
        <button className="md:hidden" onClick={() => setIsOpen(!isOpen)}>
          ☰
        </button>
      </div>
      {/* Mobile menu */}
      {isOpen && (
        <div className="md:hidden px-4 pb-4 flex flex-col gap-3">
          {navLinks.map((link) => (
            <a key={link.href} href={link.href} onClick={() => setIsOpen(false)}>
              {link.label}
            </a>
          ))}
        </div>
      )}
    </nav>
  );
}
```

Perhatikan penggunaan `backdrop-blur-md` dan `bg-white/80` — ini teknik glassmorphism yang bikin navbar terlihat modern dan elegan.

## Step 4: Hero Section yang Menarik

Hero section adalah hal pertama yang dilihat visitor. Buat yang impactful tapi tetap simpel:

```tsx
export default function Hero() {
  return (
    <section className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-50 to-white">
      <div className="text-center px-4">
        <h1 className="text-4xl md:text-6xl font-bold mb-4">
          Hi, aku <span className="text-indigo-600">Dovi</span>
        </h1>
        <p className="text-lg md:text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Full-stack developer yang passionate bikin aplikasi web yang cepat,
          indah, dan mudah diakses semua orang.
        </p>
        <div className="flex gap-4 justify-center">
          <a href="#projects" className="bg-indigo-600 text-white px-6 py-3 rounded-lg hover:bg-indigo-700 transition">
            Lihat Proyek
          </a>
          <a href="#contact" className="border border-indigo-600 text-indigo-600 px-6 py-3 rounded-lg hover:bg-indigo-50 transition">
            Hubungi Aku
          </a>
        </div>
      </div>
    </section>
  );
}
```

Gunakan `bg-gradient-to-br` untuk gradient halus di background. Dua tombol CTA (Call-to-Action) yang jelas sangat penting untuk engagement.

## Step 5: Projects Section dengan Cards

Bagian proyek adalah showcase utama portfolio kamu. Buat dalam format card grid. Yang paling penting: setiap project card harus jelas menceritakan **masalah apa yang diselesaikan** dan **apa dampaknya** — bukan cuma daftar teknologi.

```tsx
const projects = [
  {
    title: "E-Commerce App",
    description: "Platform toko online dengan fitur keranjang, checkout, dan payment gateway.",
    tech: ["Next.js", "Prisma", "PostgreSQL"],
    link: "#",
  },
  {
    title: "Task Manager",
    description: "Aplikasi manajemen tugas dengan drag-and-drop dan real-time sync.",
    tech: ["React", "Firebase", "Tailwind"],
    link: "#",
  },
  {
    title: "Weather Dashboard",
    description: "Dashboard cuaca interaktif dengan data visualisasi dan notifikasi.",
    tech: ["Vue.js", "Chart.js", "OpenWeather API"],
    link: "#",
  },
];

export default function Projects() {
  return (
    <section id="projects" className="py-20 px-4 max-w-6xl mx-auto">
      <h2 className="text-3xl font-bold mb-10 text-center">Proyek Saya</h2>
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {projects.map((project) => (
          <div key={project.title} className="border rounded-xl p-6 hover:shadow-lg transition">
            <h3 className="text-xl font-semibold mb-2">{project.title}</h3>
            <p className="text-gray-600 mb-4">{project.description}</p>
            <div className="flex flex-wrap gap-2 mb-4">
              {project.tech.map((t) => (
                <span key={t} className="bg-indigo-100 text-indigo-700 text-sm px-2 py-1 rounded">
                  {t}
                </span>
              ))}
            </div>
            <a href={project.link} className="text-indigo-600 hover:underline">
              Lihat Detail →
            </a>
          </div>
        ))}
      </div>
    </section>
  );
}
```

Grid responsif dari Tailwind (`grid md:grid-cols-2 lg:grid-cols-3`) bikin layout otomatis menyesuaikan layar — mobile 1 kolom, tablet 2 kolom, desktop 3 kolom.

## Step 6: About Section

About section adalah tempat kamu bercerita tentang diri sendiri—latar belakang, keahlian, dan apa yang bikin kamu berbeda. Jangan terlalu formal; tulis dengan gaya yang natural dan relatable.

```tsx
export default function About() {
  const skills = ["Next.js", "TypeScript", "Tailwind CSS", "Node.js", "PostgreSQL", "Docker"];

  return (
    <section id="about" className="py-20 px-4 max-w-4xl mx-auto">
      <h2 className="text-3xl font-bold mb-6 text-center">Tentang Saya</h2>
      <p className="text-gray-600 leading-relaxed mb-8 text-center">
        Saya seorang full-stack developer dengan pengalaman 3+ tahun membangun
        aplikasi web dari nol hingga production. Passionate tentang performa,
        aksesibilitas, dan clean code.
      </p>
      <div className="flex flex-wrap justify-center gap-3">
        {skills.map((skill) => (
          <span key={skill} className="bg-indigo-50 text-indigo-600 px-4 py-2 rounded-full text-sm font-medium">
            {skill}
          </span>
        ))}
      </div>
    </section>
  );
}
```

Tips: gunakan bahasa pertama ("Saya") karena lebih personal. Tunjukkan angka spesifik kalau bisa ("3+ tahun", "10+ project selesai")—ini meningkatkan kepercayaan visitor.

## Step 7: Contact Form dengan Formspree

Untuk contact form tanpa backend, kamu bisa pakai layanan seperti **Formspree** (50 submissions/bulan gratis). Cukup buat form dengan action ke endpoint Formspree:

```tsx
export default function Contact() {
  return (
    <section id="contact" className="py-20 px-4 max-w-2xl mx-auto">
      <h2 className="text-3xl font-bold mb-6 text-center">Hubungi Saya</h2>
      <form action="https://formspree.io/f/your-form-id" method="POST" className="flex flex-col gap-4">
        <input type="text" name="name" placeholder="Nama" required className="border rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        <input type="email" name="email" placeholder="Email" required className="border rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        <textarea name="message" placeholder="Pesan" rows={5} required className="border rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        <button type="submit" className="bg-indigo-600 text-white px-6 py-3 rounded-lg hover:bg-indigo-700 transition font-medium">
          Kirim Pesan
        </button>
      </form>
    </section>
  );
}
```

## Step 8: Footer yang Clean

Footer cukup sederhana—tampilkan social links dan copyright. Kamu bisa tambahkan ikon dari library seperti Lucide React:

```tsx
export default function Footer() {
  return (
    <footer className="border-t py-8 px-4 text-center text-gray-500 text-sm">
      <p>© 2026 Dovi.dev. Dibuat dengan Next.js & Tailwind CSS.</p>
      <div className="flex justify-center gap-4 mt-3">
        <a href="https://github.com/username" className="hover:text-indigo-600 transition">GitHub</a>
        <a href="https://linkedin.com/in/username" className="hover:text-indigo-600 transition">LinkedIn</a>
        <a href="https://twitter.com/username" className="hover:text-indigo-600 transition">Twitter</a>
      </div>
    </footer>
  );
}
```

## SEO Optimization untuk Portfolio

Portfolio yang nggak ter-index di Google itu sia-sia. Berikut optimasi SEO yang wajib kamu lakukan:

### Metadata di App Router

Buka `layout.tsx` dan tambahkan metadata default:

```tsx
export const metadata = {
  title: "Dovi — Full-Stack Developer",
  description: "Portfolio Dovi, full-stack developer yang membangun aplikasi web cepat dan indah.",
  openGraph: {
    title: "Dovi — Full-Stack Developer",
    description: "Portfolio profesional Dovi",
    images: ["/og-image.png"],
  },
};
```

### Per-Page Metadata

Di setiap page, kamu bisa override metadata default. Ini penting supaya setiap halaman punya deskripsi yang unik dan relevan.

### Core Web Vitals

Next.js sudah sangat baik dalam Core Web Vitals out of the box. Tapi pastikan kamu juga:

- Gunakan `next/image` untuk semua gambar (otomatis lazy load dan optimasi)
- Minimalkan bundle size dengan dynamic imports
- Hindari layout shift (CLS) dengan memberi dimensi eksplisit ke elemen

## Susun Semua di page.tsx

Gabungkan semua komponen di halaman utama:

```tsx
import Navbar from "@/components/Navbar";
import Hero from "@/components/Hero";
import About from "@/components/About";
import Projects from "@/components/Projects";
import Contact from "@/components/Contact";
import Footer from "@/components/Footer";

export default function Home() {
  return (
    <main>
      <Navbar />
      <Hero />
      <About />
      <Projects />
      <Contact />
      <Footer />
    </main>
  );
}
```

## Opsi Deploy

Portfolio sudah jadi, sekarang saatnya deploy. Berikut beberapa opsi terbaik:

- **Vercel** (Rekomendasi #1) — Integrasi native dengan Next.js. Push ke GitHub, import project, deploy otomatis. Pakai subdomain `vercel.app` gratis, atau hubungkan custom domain `.my.id` seharga Rp15-30rb/tahun.
- **Netlify** — Alternatif solid dengan fitur mirip. Support Next.js via adapter. Free tier generous.
- **Cloudflare Pages** — Performa edge network global yang cepat banget. Support Next.js sejak 2024.
- **Railway / Fly.io** — Kalau butuh backend/database juga, platform PaaS ini cocok.

Untuk deploy di Vercel, caranya simpel banget:

```bash
npm i -g vercel
vercel login
vercel --prod
```

Atau cukup push ke GitHub dan connect repository di dashboard Vercel. Setiap push ke `main` akan auto-deploy.

## Tips Portfolio yang Efektif

Setelah bikin ratusan portfolio untuk klien, berikut tips yang paling bikin beda:

1. **Kurangi animasi berlebihan** — Portfolio yang lambat bikin visitor kabur. Target loading time di bawah 2 detik.
2. **Tulis deskripsi proyek yang jelas** — Jelaskan masalah yang diselesaikan, bukan cuma teknologi yang dipakai.
3. **Sertakan link live demo** — Recruiter dan klien mau langsung coba, bukan cuma baca.
4. **Optimasi untuk SEO** — Tambahkan meta tags, Open Graph image, dan structured data. Pakai `next/head` atau metadata di App Router.
5. **Mobile-first design** — Mayoritas traffic Indonesia dari smartphone. Pastikan semua elemen tampil bagus di layar kecil.
6. **Tambahkan testimonial** — Kalau sudah punya klien, minta review singkat. Social proof sangat powerful.
7. **Update rutin** — Portfolio yang terakhir diupdate 2 tahun lalu kesannya nggak aktif. Tambahkan proyek baru minimal setiap 3 bulan.

## FAQ

**Berapa biaya bikin portfolio sendiri?**
Gratis! Next.js, Tailwind, dan Vercel semuanya free. Kalau mau custom domain, biaya mulai dari Rp15rb/tahun untuk domain `.my.id`.

**Apakah perlu bisa backend untuk bikin portfolio?**
Tidak. Portfolio statis sudah cukup untuk 90% kasus. Kalau butuh contact form, pakai layanan gratis seperti Formspree atau Resend.

**Berapa lama bikin portfolio dari nol?**
Dengan tutorial ini, pemula bisa selesai dalam 4-8 jam. Developer berpengalaman bisa 2-3 jam saja.

**Next.js atau WordPress untuk portfolio?**
Kalau kamu developer, Next.js lebih fleksibel dan performanya jauh lebih baik. Kalau nggak mau coding, WordPress atau Framer bisa jadi alternatif.

**Bagaimana cara bikin portfolio tampil di Google?**
Submit sitemap ke Google Search Console, tambahkan meta description di setiap halaman, dan pastikan website kamu fast-loading. Google sangat menghargai Core Web Vitals yang baik.

## Kesimpulan

Bikin portfolio website itu nggak harus ribet atau mahal. Dengan Next.js dan Tailwind CSS, kamu bisa buat website yang profesional, cepat, dan responsive dalam hitungan jam. Yang paling penting itu **mulai** — jangan perfeksionis di awal. Portfolio yang live dan bisa diakses itu 10x lebih baik daripada yang masih ada di localhost.

Setelah website live, fokus di konten: tambahkan proyek-proyek terbaikmu, tulis deskripsi yang compelling, dan update secara rutin. Portfolio kamu adalah investasi jangka panjang untuk karir di tech.

Kalau ada pertanyaan atau butuh bantuan, jangan ragu buat DM di Telegram. Happy coding! 🚀
