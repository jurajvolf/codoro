# Codoro Design System (DESIGN.md)

## 1. Visual World & Philosophy
Codoro is a next-generation Python learning environment and classroom management OS.
Its aesthetic sits at the intersection of **Linear**, **Raycast**, and **Cursor** — precision developer tooling built for deep focus, tactile delight, and effortless comprehension.

### Core Tenets
1. **Developer Tool Precision:** 1px hairline borders, dark obsidian surfaces, subtle inset highlights, zero sloppy gradients.
2. **Tactile Micro-interactions:** Every button and interactive tab reacts with `scale(0.96)` on press (`make-interfaces-feel-better`).
3. **Information Density & Clean Hierarchy:** Progressive disclosure through crisp segmented navigation and accordions instead of vertical content walls.
4. **Tabular Numerals Everywhere:** All XP, Doros, streak days, time limits, and counters use `font-variant-numeric: tabular-nums` in `JetBrains Mono`.
5. **Strict Craft Floor:** Zero raw unicode emojis as icons, zero `transition: all`, zero kicker/eyebrow text, themed browser surfaces (`::selection`, `caret-color`, custom scrollbars).

---

## 2. Color Palette & Tokens

### Dark Mode (Primary Scene: Deep Obsidian `#080C14`)
```css
--bg-canvas: #080C14;
--bg-surface: #0E1420;
--bg-subtle: #141C2E;
--bg-elevated: #1A2438;
--border-hairline: rgba(255, 255, 255, 0.08);
--border-strong: rgba(255, 255, 255, 0.16);
--border-glow: rgba(99, 102, 241, 0.4);

--text-primary: #F8FAFC;
--text-secondary: #CBD5E1;
--text-muted: #8492A6;

--ro-indigo: #6366F1;
--ro-indigo-hover: #4F46E5;
--ro-indigo-soft: rgba(99, 102, 241, 0.14);
--ro-indigo-border: rgba(99, 102, 241, 0.35);

--visor-cyan: #38BDF8;
--visor-cyan-bg: rgba(56, 189, 248, 0.12);

--gold-text: #FBBF24;
--gold-bg: rgba(245, 158, 11, 0.14);
--gold-border: rgba(245, 158, 11, 0.32);

--flame-text: #FB7185;
--flame-bg: rgba(244, 63, 94, 0.14);
--flame-border: rgba(244, 63, 94, 0.32);

--emerald-text: #34D399;
--emerald-bg: rgba(16, 185, 129, 0.14);
--emerald-border: rgba(16, 185, 129, 0.32);
```

### Light Mode (Apple / Stripe Slate `#F8FAFC`)
```css
--bg-canvas: #F8FAFC;
--bg-surface: #FFFFFF;
--bg-subtle: #F1F5F9;
--bg-elevated: #E2E8F0;
--border-hairline: #E2E8F0;
--border-strong: #CBD5E1;
--border-glow: rgba(70, 54, 245, 0.25);

--text-primary: #0F172A;
--text-secondary: #334155;
--text-muted: #64748B;

--ro-indigo: #4636F5;
--ro-indigo-hover: #3728E0;
--ro-indigo-soft: #EEF0FF;
--ro-indigo-border: #C7CEFF;

--visor-cyan: #0891B2;
--visor-cyan-bg: #ECFEFF;

--gold-text: #B45309;
--gold-bg: #FEF3C7;
--gold-border: #FDE68A;

--flame-text: #BE123C;
--flame-bg: #FFE4E6;
--flame-border: #FECDD3;

--emerald-text: #047857;
--emerald-bg: #D1FAE5;
--emerald-border: #A7F3D0;
```

---

## 3. Typography Stack
- **Display Headings (`h1`, `h2`, `h3`):** `'Plus Jakarta Sans', sans-serif`, font weights `700, 800`, letter spacing `-0.025em`, `text-wrap: balance`.
- **UI & Body:** `'Inter', sans-serif`, font weights `400, 500, 600`, line height `1.6`, `text-wrap: pretty`.
- **Code & Numeric Data:** `'JetBrains Mono', monospace`, `font-variant-numeric: tabular-nums`.

---

## 4. Concentric Radii & Elevation
- Outer container: `var(--radius-lg)` = `16px`
- Inner card / form: `var(--radius-md)` = `12px`
- Interactive buttons / inputs: `var(--radius-sm)` = `8px`
- Sub-controls / tags: `var(--radius-xs)` = `6px`
- Pill badges: `9999px`

---

## 5. Motion Tokens (transitions.dev & make-interfaces-feel-better)
- `--duration-micro: 80ms;` (instant feedback on click)
- `--duration-quick: 150ms;` (hover states, dropdowns)
- `--duration-fast: 250ms;` (tab switches, panel expands)
- `--ease-smooth-out: cubic-bezier(0.22, 1, 0.36, 1);`
- Strict ban on `transition: all`.
