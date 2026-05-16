---
version: alpha
name: Mandate — Imperial Ghibli
description: >
  Dark imperial Chinese theme infused with Studio Ghibli warmth —
  deep ink backgrounds, luminous gold accents, firefly glow halos,
  and hand-painted watercolor atmosphere. Film-grade cinematic UI.

colors:
  # Semantic key — agents use this as the default accent
  primary: "{colors.gold}"

  # Background palette — deep ink, never pure black
  bg: "#09090b"
  bg2: "#0f0f13"
  bg3: "#18181b"

  # Card surfaces — warm-toned dark grays
  card: "#1c1c21"
  card2: "#222228"
  card3: "#2a2a32"

  # Borders
  border: "#27272a"
  border2: "#3f3f46"

  # Text hierarchy
  text: "#fafafa"
  text2: "#a1a1aa"
  text3: "#71717a"

  # Imperial gold — the primary accent
  gold: "#e2b64f"
  gold2: "#f5d98a"
  gold-dim: "#b8860b"

  # Vermilion red — secondary accent, urgency/CTAs
  red: "#c43a31"
  red2: "#e85d50"
  red-dark: "#8b0000"

  # Utility
  green: "#22c55e"
  blue: "#3b82f6"
  purple: "#a78bfa"

  # Firefly glow (Ghibli-inspired warm light halos)
  firefly: "#f0c060"
  firefly-soft: "#f5e6b8"

typography:
  h1:
    fontFamily: Noto Serif SC
    fontSize: 3.8rem
    fontWeight: 900
    lineHeight: 1.15
    letterSpacing: "-0.02em"
  h2:
    fontFamily: Noto Serif SC
    fontSize: 2.2rem
    fontWeight: 700
    lineHeight: 1.25
    letterSpacing: "-0.01em"
  h3:
    fontFamily: Noto Serif SC
    fontSize: 1.2rem
    fontWeight: 600
    lineHeight: 1.4
  body-lg:
    fontFamily: Inter
    fontSize: 1.125rem
    fontWeight: 400
    lineHeight: 1.8
  body:
    fontFamily: Inter
    fontSize: 1rem
    fontWeight: 400
    lineHeight: 1.7
  body-sm:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: Inter
    fontSize: 0.75rem
    fontWeight: 600
    letterSpacing: 0.12em
  nav-link:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: 500
    lineHeight: 1.4

rounded:
  sm: 10px
  md: 16px
  lg: 24px
  pill: 100px

spacing:
  xs: 8px
  sm: 16px
  md: 24px
  lg: 32px
  xl: 48px
  section: 100px
  section-sm: 60px

shadows:
  card-hover: "0 12px 40px rgba(226, 182, 79, 0.08)"
  card-hover-red: "0 16px 48px rgba(196, 58, 49, 0.15)"
  btn-primary: "0 8px 30px rgba(226, 182, 79, 0.3)"
  btn-red: "0 8px 30px rgba(196, 58, 49, 0.3)"
  imperial-card: "0 16px 48px rgba(184, 134, 11, 0.15), 0 0 80px rgba(226, 182, 79, 0.06)"
  firefly-glow: "0 0 20px rgba(240, 192, 96, 0.4), 0 0 60px rgba(240, 192, 96, 0.15)"

components:
  button-primary:
    backgroundColor: "{colors.gold}"
    textColor: "#000000"
    rounded: "{rounded.sm}"
    padding: "14px 28px"
    typography: body
  button-primary-hover:
    backgroundColor: "{colors.gold2}"
  button-secondary:
    backgroundColor: transparent
    textColor: "{colors.text}"
    rounded: "{rounded.sm}"
    padding: "14px 28px"
  button-secondary-hover:
    textColor: "{colors.gold}"
  button-red:
    backgroundColor: "{colors.red}"
    textColor: "#ffffff"
    rounded: 6px
    padding: "6px 14px"
  button-red-hover:
    backgroundColor: "{colors.red2}"

  nav:
    backgroundColor: "rgba(9, 9, 11, 0.85)"
  nav-link-active:
    textColor: "{colors.gold}"

  card:
    backgroundColor: "{colors.card}"
    rounded: "{rounded.md}"
  card-hover:
    backgroundColor: "{colors.card}"

  imperial-card:
    backgroundColor: "linear-gradient(180deg, {colors.card}, #1a1410)"
    rounded: "{rounded.md}"
  imperial-card-hover:
    backgroundColor: "linear-gradient(180deg, {colors.card}, #1a1410)"

  hero-badge:
    backgroundColor: "rgba(226, 182, 79, 0.1)"
    textColor: "{colors.gold}"
    rounded: "{rounded.pill}"
    padding: "6px 16px"

  course-card-hover:
    backgroundColor: "{colors.card}"

  glow-dot:
    backgroundColor: "{colors.red}"
    size: 8px
---

## Overview

**Mandate** is a Chinese imperial history platform — 94 courses spanning 24
dynasties and 200+ emperors. The visual identity fuses two seemingly opposite
worlds:

- **Imperial China**: deep ink-black backgrounds, vermilion seals, luminous
  gold accents, and the weight of four millennia.
- **Studio Ghibli**: warm firefly light halos, atmospheric radial gradients,
  subtle hover animations that breathe, and a hand-painted watercolor soul.

The result is *dark academia meets Hayao Miyazaki* — scholarly without being
cold, warm without being casual. Every interaction should feel like turning
the page of an illuminated manuscript under firefly light.

**Core principles:**
1. **Gold is the voice.** Every interactive element, active state, and
   emphasis flows through the gold palette. Red is reserved for urgency
   and vermilion-seal moments.
2. **Never pure black.** `#09090b` is the darkest surface — deep ink, not
   void. All backgrounds have warmth.
3. **Atmosphere over chrome.** Radial gradients, backdrop blurs, and
   subtle shadows build depth without heavy borders.
4. **Animation is meaning.** Hover lifts, glow pulses, and float keyframes
   aren't decoration — they signal interactivity and hierarchy.
5. **Firefly light.** Warm amber halos (`{colors.firefly}`, `{colors.firefly-soft}`)
   should pool around key content areas like lantern light in a Ghibli night scene.

## Colors

The palette is built on a **dark imperial foundation** with **gold as the
primary accent** and **red as the secondary (seal/urgency) accent**.

### Backgrounds
- **`bg` (`#09090b`):** Deepest surface — the "ink" of the page. Used for
  `body` background and the deepest sections.
- **`bg2` (`#0f0f13`):** Slightly lifted. Section backgrounds that need
  differentiation from the body.
- **`bg3` (`#18181b`):** Elevated surface. Use for inset panels or code
  blocks that need subtle separation.

### Surfaces (Cards)
- **`card` (`#1c1c21`):** Default card background. Warm-toned dark gray —
  not cold, not flat.
- **`card2` (`#222228`):** Secondary card — nested cards, footers, sidebars.
- **`card3` (`#2a2a32`):** Highest surface — hover states, active cards,
  modal backgrounds.

### Text
- **`text` (`#fafafa`):** Primary body and heading text. Near-white with
  warmth — pure `#ffffff` is too harsh against the ink background.
- **`text2` (`#a1a1aa`):** Secondary text — descriptions, metadata, dates.
  Muted but readable on dark surfaces.
- **`text3` (`#71717a`):** Tertiary — placeholders, disabled states, fine
  print. Lowest contrast that still passes WCAG AA on `{colors.bg}`.

### Gold (Primary Accent)
- **`gold` (`#e2b64f`):** The imperial gold. Used for primary CTAs, active
  nav links, section labels, and key emphasis. Bright enough to glow but
  warm enough to feel ancient.
- **`gold2` (`#f5d98a`):** Hover/intensified gold. Lighter, brighter — used
  on button hover and highlight states.
- **`gold-dim` (`#b8860b`):** Muted gold — decorative lines, scrollbar
  thumbs, subtle gradients. The "aged" gold.

### Red (Secondary / Seal Accent)
- **`red` (`#c43a31`):** Vermilion — the color of Chinese imperial seals.
  Used for "hot" CTAs (live indicators, unread badges, destructive actions),
  and key stat highlights.
- **`red2` (`#e85d50`):** Button hover red. Brighter, more urgent.
- **`red-dark` (`#8b0000`):** Deep red — atmospheric gradients, subtle
  background washes. Never used for text or interactive elements.

### Firefly Glow (Ghibli Atmosphere)
- **`firefly` (`#f0c060`):** The core firefly color — warm amber-yellow.
  Used in `box-shadow` halos (`{shadows.firefly-glow}`) and radial gradient
  highlights. Think: the soft floating lights in *Spirited Away*.
- **`firefly-soft` (`#f5e6b8`):** Diffused firefly — larger, fainter glow
  pools for section backgrounds and hero atmosphere.

### Utility
- `green`, `blue`, `purple` are tertiary — success indicators, links
  (when gold isn't appropriate), and decorative accents respectively.

### WCAG Notes
- `{colors.text}` on `{colors.bg}`: contrast ratio ~17.5:1 (AAA)
- `{colors.text2}` on `{colors.bg}`: ~8.6:1 (AAA)
- `{colors.text3}` on `{colors.bg}`: ~4.6:1 (AA — borderline, avoid for
  body text; use only for placeholders and disabled states)
- `{colors.gold}` on `{colors.bg}`: ~8.2:1 (AAA)
- `#000000` on `{colors.gold}` (button text): ~10.5:1 (AAA)

## Typography

Two typefaces, one voice:

- **Noto Serif SC** (serif): All headings, imperial numbers, course titles,
  and any text that carries the weight of history. The serifs evoke carved
  stone and brush calligraphy.
- **Inter** (sans-serif): Body text, navigation, labels, UI controls. Clean
  and modern — the scholar's notebook, not the emperor's edict.

### Hierarchy
- **h1** — Massive, tight, authoritative. Hero titles and section anchors.
  Letter-spacing tightened for cinematic impact.
- **h2** — Section headers. Bold but approachable. Slightly tighter tracking.
- **h3** — Subsection headers. Semi-bold, no tracking adjustment.
- **body-lg** — Lead paragraphs, course descriptions, featured content.
  Generous line-height (1.8) for readability on dark backgrounds.
- **body** — Default prose. Inter at 1rem with comfortable leading.
- **body-sm** — Metadata, dates, footnotes. Muted with `{colors.text3}`.
- **label** — Uppercase category tags. Wide tracking (0.12em) in gold.
  Always paired with gold color.

### Rules
1. Headings always use `var(--serif)` (Noto Serif SC). Never sans-serif.
2. Body always uses `var(--sans)` (Inter). Never serif.
3. Gold gradient text (`linear-gradient(135deg, gold, red)`) is reserved
   for hero stat numbers only — never use on body text.
4. Chinese text in body uses the inherited Inter fallback — Noto Serif SC
   is too ornate for 3000+ character course content.

## Layout & Spacing

### Grid System
- **Container**: `max-width: 1200px`, centered, `padding: 0 24px`
- **Container (narrow)**: `max-width: 800px` — for long-form reading
- **2-column**: `grid-template-columns: repeat(2, 1fr)`, gap 32px
- **3-column**: `grid-template-columns: repeat(3, 1fr)`, gap 24px
- **4-column**: `grid-template-columns: repeat(4, 1fr)`, gap 20px
- **Responsive**: All grids collapse to single column at 768px.
  4-column grids collapse to 2-column at 900px first.

### Section Rhythm
- Default section: `padding: 100px 0` (desktop) → `60px 0` (mobile)
- Compact section: `padding: 60px 0`
- Content sections alternate between `{colors.bg}` (default) and subtle
  radial gradient overlays for visual variety.

### Navigation
- Fixed top bar, 64px height, `backdrop-filter: blur(20px)` with
  semi-transparent `{colors.bg}` background.
- Progress bar (3px) below nav — gold-to-red gradient, fills on scroll.

### Breathing Room
- Between hero and first section: generous whitespace (100px+)
- Card grids: 24-32px gaps. Never cramp imperial content.
- Text blocks: `max-width: 620px` for hero subtitles, `800px` for reading
  length. Line-length discipline improves dark-theme readability.

## Elevation & Depth

The design avoids heavy borders and hard shadows. Instead, depth comes from:

### Atmosphere (Background Depth)
- **Hero**: Three overlapping `radial-gradient` ellipses in gold (8%), red
  (5%), and blue (3%) — creates a soft, non-repeating atmospheric glow.
  Each ellipse is positioned at different corners with different sizes,
  producing an organic, Ghibli-sky effect.
- **Sections**: Single or double radial gradients at section edges,
  always subtle (3-8% opacity). Never dominates the content.
- **Imperial cards**: `linear-gradient(180deg, card → #1a1410)` —
  cards darken toward the bottom, suggesting depth.

### Card Elevation
- Resting: flat against background, border only.
- Hover: `translateY(-4px)` lift + gold-tinted `box-shadow`
  (`{shadows.card-hover}`). The gold shadow is the key — it's
  the firefly glow effect.
- Imperial cards hover: stronger gold shadow
  (`{shadows.imperial-card}`) with an 80px-radius outer glow.

### Glass & Blur
- Navigation bar: `backdrop-filter: blur(20px)` on semi-transparent bg.
- Course detail overlay: blurred backdrop behind modal content.
- Never use glass effects on content cards — it reduces readability.

### The Firefly Rule
Any element that "floats" above the page (cards on hover, modals, tooltips)
should carry a subtle gold or firefly-colored glow. This is the Ghibli
signature — light that feels warm and alive, not sterile.

## Shapes

### Border Radius
- **Cards, sections, modals**: `{rounded.md}` (16px) — soft but not
  cartoonish.
- **Buttons, inputs, tags**: `{rounded.sm}` (10px) — slightly rounded,
  approachable.
- **Pills/badges**: `{rounded.pill}` (100px) — fully rounded. Used for
  hero badges, status indicators.
- **Small CTAs** (like the red "latest" badge): 6px — intentionally
  sharper for contrast with the otherwise soft shapes.

### Borders
- Default: `1px solid {colors.border}` — subtle, barely visible on dark
  backgrounds.
- Hover: `1px solid {colors.gold}` — the border "lights up."
- Never use borders thicker than 1px. The design's weight comes from
  shadows and atmosphere, not outlines.

## Components

### Buttons
Three variants, each with clear purpose:

1. **`button-primary`** — Gold background, black text. The primary action
   on any page. Only ONE per viewport section. Hover lifts + glows gold.
2. **`button-secondary`** — Transparent with border. Secondary/tertiary
   actions. Hover glows the border gold (`{colors.gold}`).
3. **`button-red`** — Red background, white text. Small (6px radius,
   6px padding). Used for "hot" indicators like live badges and status
   dots. Animated glow pulse.

### Navigation
- Fixed, 64px, blurred glass background.
- Logo: Noto Serif SC, gold, with red icon.
- Links: Inter 0.875rem, `{colors.text2}` → `{colors.gold}` on hover.
- CTA button: standard `button-primary` sizing in nav context.
- Mobile: hamburger menu at ≤768px. Full nav links hidden.

### Cards

**Imperial Cards** (emperor gallery scroll):
- Horizontal scroll container. 180px wide cards.
- Bottom-darkened gradient background.
- Gold horizontal divider line (decorative).
- Gold gradient overlay that appears on hover.
- Hover: lift + gold glow shadow. Emperor name in gold.
- Float animation on robe emoji (3 staggered keyframe timings).

**Course Cards** (homepage grid):
- 3-column responsive grid. Links to `courses.html?course=N`.
- Hover: lift + gold border + subtle shadow.
- Course number badge: gold gradient background, black number text.
- Title in serif, description in sans body-sm.

**Feature Cards** (generic content):
- Default card background. Hover lifts to gold border.
- Icon + heading + description layout.

### Hero
- Full viewport height, centered content.
- Three overlapping radial gradients for atmosphere.
- Gold dot pulse animation in badge.
- Gradient text (gold→red) on stat numbers only.
- Two CTAs: primary (gold) + secondary (outline).
- Stats row: three columns of gradient numbers + muted labels.

### Firefly Atmosphere
Not a component, but a treatment: any section can receive firefly glow by
adding:
- A `radial-gradient` ellipse in `{colors.firefly}` at 4-8% opacity
- Positioned to one side or corner (never center)
- Combined with deeper background gradients for depth
- The effect should feel like soft lantern light, not a spotlight

## Do's and Don'ts

✅ **DO:**
- Use gold (`{colors.gold}`) as the sole interactive accent color.
  Red is secondary — seals, urgency, live indicators.
- Keep backgrounds warm. Never use `#000000` — always `{colors.bg}` or darker
  warm variants.
- Add firefly glow (`{shadows.firefly-glow}`) to any elevated element.
- Use radial gradients for atmosphere, not linear — organic, not mechanical.
- Animate hovers (lift + glow). Static cards feel dead on this theme.
- Use Noto Serif SC for all headings. The serif carries the historical weight.
- Keep card content concise. Course details belong in the overlay, not the grid.

❌ **DON'T:**
- Don't use blue for primary actions. Blue is a utility link color only.
- Don't use pure white (`#ffffff`) for text — too harsh on the ink background.
  Always `{colors.text}` (`#fafafa`).
- Don't add borders thicker than 1px. Let shadows and atmosphere define shape.
- Don't center radial gradients. Always offset to edges/corners for natural feel.
- Don't use box-shadow without a gold or firefly tint. Gray/black shadows feel
  cold and generic.
- Don't animate everything. Only cards, buttons, badges, and glow dots get
  motion. Content text should stay still.
- Don't use more than one `button-primary` per section. Gold should be scarce
  to feel precious.
- Don't put 3000+ character course content on cards. Cards are gateways;
  detail overlays are reading spaces.
