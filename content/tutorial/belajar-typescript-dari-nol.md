---
title: "Belajar TypeScript dari Nol (2026)"
date: 2026-04-16
draft: false
slug: "belajar-typescript-dari-nol"
description: "Tutorial TypeScript untuk JavaScript developer. Dari basic types sampai generics, lengkap dengan contoh kode."
categories: [Tutorial]
tags: ['typescript', 'javascript', 'tutorial', 'pemula', 'web-development']
ShowShareLinks: true
ShowReadingTime: true
ShowToc: true
---

Ceritanya begini: dulu aku skeptis banget sama TypeScript. "Buat apa nambahin types? JavaScript udah cukup kok."

Lalu aku join project yang pakai JavaScript murni, 200+ files, gak ada type checking. Ada bug yang bikin production down: user ID yang seharusnya number, ternyata string. Dan gak ketauan sampai user complaint.

Sejak itu aku gak pernah balik ke JavaScript tanpa TypeScript. Trust me, TypeScript itu investasi waktu yang ROI-nya gede banget.

## TypeScript Itu Apa?

TypeScript = JavaScript + Type System

Semua yang valid di JavaScript, valid di TypeScript. TypeScript cuma nambahin static types yang bikin compiler bisa nge-catch error sebelum runtime.

```javascript
// JavaScript — error baru ketauan pas jalan
function greet(name) {
  return "Hello " + name.toUpperCase();
}
greet(42); // 💥 Runtime error!
```

```typescript
// TypeScript — error langsung ketauan di editor
function greet(name: string): string {
  return "Hello " + name.toUpperCase();
}
greet(42); // ❌ Compile error: Argument of type 'number' not assignable
```

## Setup

Install TypeScript:

```bash
npm install -g typescript
# atau
npx tsc --init
```

Init project:

```bash
mkdir belajar-ts && cd belajar-ts
npm init -y
npm install typescript --save-dev
npx tsc --init
```

tsconfig.json basic:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

Build dan run:

```bash
npx tsc           # Compile ke JavaScript
node dist/index.js
```

## Basic Types

```typescript
// Primitive types
let nama: string = "Dovi";
let umur: number = 25;
let aktif: boolean = true;
let kosong: null = null;
let belum: undefined = undefined;

// Array
let angka: number[] = [1, 2, 3, 4, 5];
let buah: Array<string> = ["apel", "jeruk", "mangga"];

// Tuple — array dengan urutan type yang tetap
let pasangan: [string, number] = ["umur", 25];

// Enum
enum Status {
  Pending = "PENDING",
  Active = "ACTIVE",
  Inactive = "INACTIVE"
}
let statusUser: Status = Status.Active;

// Any — HINDARI INI (cheat code)
let bebas: any = "boleh apa aja";
bebas = 42;     // OK
bebas = true;   // OK
// Tapi... gak ada type checking. Defeats the purpose.

// Unknown — lebih aman dari any
let gakTau: unknown = "something";
// gakTau.toUpperCase(); // ❌ Error!
if (typeof gakTau === "string") {
  gakTau.toUpperCase(); // ✅ OK karena udah di-check
}

// Void & Never
function logMessage(msg: string): void {
  console.log(msg);
  // void = gak return apa-apa
}

function throwError(msg: string): never {
  throw new Error(msg);
  // never = gak pernah selesai (throw/loop infinite)
}
```

## Functions

```typescript
// Function dengan type annotations
function tambah(a: number, b: number): number {
  return a + b;
}

// Optional parameter (pakai ?)
function sapa(nama: string, greeting?: string): string {
  return `${greeting || "Halo"}, ${nama}!`;
}
sapa("Dovi");           // "Halo, Dovi!"
sapa("Dovi", "Hey");    // "Hey, Dovi!"

// Default parameter
function buatUser(
  name: string,
  role: "admin" | "user" = "user",
  active: boolean = true
) {
  return { name, role, active };
}

// Rest parameters
function sum(...numbers: number[]): number {
  return numbers.reduce((acc, n) => acc + n, 0);
}
sum(1, 2, 3, 4, 5); // 15

// Function type
type MathOperation = (a: number, b: number) => number;

const kali: MathOperation = (a, b) => a * b;
const bagi: MathOperation = (a, b) => a / b;
```

## Objects & Interfaces

```typescript
// Interface — kontrak untuk object shape
interface User {
  id: number;
  name: string;
  email: string;
  age?: number;              // Optional
  readonly createdAt: Date;  // Gak bisa diubah setelah init
}

const user: User = {
  id: 1,
  name: "Dovi",
  email: "dovi@example.com",
  createdAt: new Date()
};

// user.createdAt = new Date(); // ❌ Error: readonly

// Extending interfaces
interface AdminUser extends User {
  permissions: string[];
  level: number;
}

const admin: AdminUser = {
  id: 2,
  name: "Admin",
  email: "admin@example.com",
  createdAt: new Date(),
  permissions: ["read", "write", "delete"],
  level: 1
};

// Type alias — mirip interface tapi lebih fleksibel
type ApiResponse<T> = {
  success: boolean;
  data: T;
  message?: string;
  timestamp: number;
};

type ProductListResponse = ApiResponse<Product[]>;
type UserResponse = ApiResponse<User>;
```

## Union & Literal Types

```typescript
// Union type — bisa salah satu dari beberapa type
type StringOrNumber = string | number;

function formatId(id: StringOrNumber): string {
  if (typeof id === "string") {
    return id.toUpperCase();
  }
  return `#${id.toString().padStart(6, "0")}`;
}

// Literal type — value yang tepat
type Theme = "light" | "dark" | "system";
type HttpMethod = "GET" | "POST" | "PUT" | "DELETE";
type Status = "idle" | "loading" | "success" | "error";

// Discriminated unions — powerful pattern
type Result<T> =
  | { status: "success"; data: T }
  | { status: "error"; error: string }
  | { status: "loading" };

function handleResult(result: Result<User>) {
  switch (result.status) {
    case "loading":
      console.log("Loading...");
      break;
    case "success":
      console.log(`User: ${result.data.name}`);  // TS knows data exists
      break;
    case "error":
      console.log(`Error: ${result.error}`);      // TS knows error exists
      break;
  }
}
```

## Generics

Generics itu template types. Bikin komponen yang reusable untuk berbagai type.

```typescript
// Tanpa generics — harus buat function per type
function getFirstString(arr: string[]): string | undefined {
  return arr[0];
}
function getFirstNumber(arr: number[]): number | undefined {
  return arr[0];
}

// Pakai generics — satu function untuk semua
function getFirst<T>(arr: T[]): T | undefined {
  return arr[0];
}

getFirst<string>(["a", "b", "c"]);  // string | undefined
getFirst<number>([1, 2, 3]);         // number | undefined
getFirst(["a", "b"]);                // TS infer otomatis: string | undefined

// Generic interface
interface Repository<T> {
  findById(id: number): Promise<T | null>;
  findAll(): Promise<T[]>;
  create(item: Omit<T, "id">): Promise<T>;
  update(id: number, item: Partial<T>): Promise<T>;
  delete(id: number): Promise<boolean>;
}

// Implementasi
class UserRepository implements Repository<User> {
  private users: User[] = [];

  async findById(id: number): Promise<User | null> {
    return this.users.find(u => u.id === id) || null;
  }

  async findAll(): Promise<User[]> {
    return this.users;
  }

  async create(item: Omit<User, "id">): Promise<User> {
    const newUser: User = {
      id: this.users.length + 1,
      ...item,
      createdAt: new Date()
    };
    this.users.push(newUser);
    return newUser;
  }

  async update(id: number, item: Partial<User>): Promise<User> {
    const index = this.users.findIndex(u => u.id === id);
    if (index === -1) throw new Error("User not found");
    this.users[index] = { ...this.users[index], ...item };
    return this.users[index];
  }

  async delete(id: number): Promise<boolean> {
    const index = this.users.findIndex(u => u.id === id);
    if (index === -1) return false;
    this.users.splice(index, 1);
    return true;
  }
}
```

## Utility Types

TypeScript punya built-in utility types yang super useful:

```typescript
interface User {
  id: number;
  name: string;
  email: string;
  password: string;
}

// Partial — semua fields jadi optional
type UpdateUser = Partial<User>;
// { id?: number; name?: string; email?: string; password?: string }

// Required — semua fields jadi required
type CompleteUser = Required<User>;

// Pick — pilih beberapa fields saja
type UserPreview = Pick<User, "id" | "name">;
// { id: number; name: string }

// Omit — hapus beberapa fields
type PublicUser = Omit<User, "password">;
// { id: number; name: string; email: string }

// Record — bikin type dengan key-value yang konsisten
type UserRoles = Record<string, "admin" | "user" | "moderator">;
const roles: UserRoles = {
  dovi: "admin",
  budi: "user"
};

// Exclude & Extract
type AllColors = "red" | "blue" | "green" | "yellow";
type WarmColors = Extract<AllColors, "red" | "yellow">;
type CoolColors = Exclude<AllColors, "red" | "yellow">;

// ReturnType — extract return type dari function
function createUser() {
  return { id: 1, name: "test", email: "test@test.com" };
}
type NewUser = ReturnType<typeof createUser>;
```

## Real-World Example: Express API

```typescript
import express, { Request, Response, NextFunction } from "express";

// Type definitions
interface Todo {
  id: number;
  title: string;
  completed: boolean;
  createdAt: Date;
}

interface CreateTodoBody {
  title: string;
}

interface UpdateTodoBody {
  title?: string;
  completed?: boolean;
}

// Typed request handlers
const app = express();
app.use(express.json());

let todos: Todo[] = [];
let nextId = 1;

// GET /todos
app.get("/todos", (req: Request, res: Response<Todo[]>) => {
  res.json(todos);
});

// POST /todos
app.post(
  "/todos",
  (req: Request<{}, {}, CreateTodoBody>, res: Response<Todo | { error: string }>) => {
    const { title } = req.body;

    if (!title || title.trim() === "") {
      return res.status(400).json({ error: "Title is required" });
    }

    const todo: Todo = {
      id: nextId++,
      title: title.trim(),
      completed: false,
      createdAt: new Date()
    };

    todos.push(todo);
    res.status(201).json(todo);
  }
);

// PATCH /todos/:id
app.patch(
  "/todos/:id",
  (req: Request<{ id: string }, {}, UpdateTodoBody>, res: Response) => {
    const id = parseInt(req.params.id);
    const todo = todos.find(t => t.id === id);

    if (!todo) {
      return res.status(404).json({ error: "Todo not found" });
    }

    if (req.body.title !== undefined) todo.title = req.body.title;
    if (req.body.completed !== undefined) todo.completed = req.body.completed;

    res.json(todo);
  }
);

app.listen(3000, () => console.log("Server running on port 3000"));
```

## Tips Buat Pemula TypeScript

**1. Mulai dari `strict: true`**
Jangan pernah disable strict mode. Memang sakit di awal, tapi bikin kamu belajar lebih cepet dan code jauh lebih aman.

**2. Jangan overuse `any`**
Kalau kamu nulis `any`, artinya kamu nyerah. Lebih baik pakai `unknown` dan type check secara manual.

```typescript
// ❌ Nope
function process(data: any) { ... }

// ✅ Better
function process(data: unknown) {
  if (typeof data === "object" && data !== null) {
    // Now you can work with it
  }
}
```

**3. Pakai `as const` untuk literal values**
```typescript
// Biasa — type-nya string
const API_URL = "https://api.example.com"; // type: string

// as const — type-nya literal "https://api.example.com"
const API_URL = "https://api.example.com" as const;
// type: "https://api.example.com"
```

**4. Type inference itu temanmu**
Gak semua variabel perlu diberi type manual. TypeScript bisa infer dari value:

```typescript
// Gak perlu:
const name: string = "Dovi";
const age: number = 25;

// Biarkan TypeScript infer:
const name = "Dovi";  // string
const age = 25;        // number
```

Tapi untuk function parameters dan return types, SELALU tulis type-nya.

**5. Pakai VS Code dengan TypeScript**
Autocomplete, error highlighting, dan refactoring tools-nya juara. Setting VS Code:

```json
{
  "typescript.tsdk": "node_modules/typescript/lib",
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode"
}
```

## Pitfalls Umum

**1. Array methods di forEach gak bisa return**
```typescript
// ❌ Gak bisa
const filtered = [1, 2, 3].forEach(n => {
  if (n > 1) return n;
});

// ✅ Pakai filter/map/reduce
const filtered = [1, 2, 3].filter(n => n > 1);
```

**2. Object.keys return string[], bukan keyof**
```typescript
interface Config {
  host: string;
  port: number;
}

const config: Config = { host: "localhost", port: 3000 };

// Object.keys selalu return string[]
const keys = Object.keys(config); // string[], bukan (keyof Config)[]

// Kalau butuh typed keys:
function typedKeys<T>(obj: T): (keyof T)[] {
  return Object.keys(obj) as (keyof T)[];
}
```

**3. Module resolution bikin bingung**
Kalau import error padahal file ada, cek `moduleResolution` di tsconfig:
- `node` — lama, tapi compatible
- `NodeNext` — recommended untuk Node.js terbaru
- `bundler` — untuk Vite/Webpack

## Conclusion

TypeScript itu skill wajib buat JavaScript developer di 2025. Learning curve-nya ada, tapi setelah terbiasa, kamu gak akan mau balik ke JavaScript murni.

Mulai dari project kecil: convert satu file JavaScript ke TypeScript, terus expand. Jangan langsung convert semua sekaligus — nanti overwhelmed.

Semangat belajar! Kalau ada pertanyaan, chat aku di [Telegram](https://t.me/dovi). Aku sering share tips TypeScript di sana.
