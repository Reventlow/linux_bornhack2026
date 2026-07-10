# Handoff: Linux for the Curious — BornHack 2026 workshop deck

## Overview
A 28-slide presentation deck for a 2-hour, hands-on "Intro to Linux" workshop at BornHack 2026, aimed at complete newcomers. Part 1 (~50 min) covers theory: what Linux is, history, the kernel, distros, commercial vs community, release models, package managers, desktop environments, choosing a first distro. Part 2 (~60 min) is hands-on: 9 numbered TASK slides walking attendees through `pwd/ls/cd`, `mkdir/touch`, `nano`, `cat/less`, `cp/mv`, `rm`, `man/tldr`, and `btop`, plus a cheat-sheet slide and closing.

It is the sibling deck to "Docker for the Curious" (github.com/Reventlow/docker_bornhack2026) and intentionally reuses that deck's exact visual system ("matcha" palette). The most natural deployment is the same as that repo: serve the deck as a static site (e.g. nginx in Docker), optionally bundling it into a single self-contained `index.html`.

## About the Design Files
The files in this bundle are **design references created in HTML** — a working prototype showing the intended look and behavior, not production code to copy blindly. The task is to recreate/host this deck in the target repo's existing environment and patterns (for the sibling repo: `source/` + built `deck/index.html` served by nginx). The deck itself is plain HTML/CSS with two supporting scripts and runs in any modern browser with no build step.

## Fidelity
**High-fidelity.** Colors, typography, spacing, and copy are final. Recreate pixel-perfectly; all values are specified below and present in the source file.

## Files
- `Linux for the Curious.dc.html` — the full deck. All 28 slides are inline-styled `<section>` elements inside an `<x-import>` mount of `deck-stage`. Everything visual lives in this one file.
- `deck-stage.js` — vanilla web component that provides the 1920×1080 stage: letterboxed scaling, keyboard/tap navigation, slide-count overlay, thumbnail rail (drag to reorder), print-to-PDF (one page per slide). Reuse as-is.
- `support.js` — runtime for the `.dc.html` container format (template parsing, `<x-import>` mounting). Reuse as-is, or port the `<section>` markup into any plain HTML page that loads `deck-stage.js` directly (`<deck-stage width="1920" height="1080">…sections…</deck-stage>`).

## Deck architecture
- Canvas: **1920×1080** (16:9). The stage scales to fit the window; author sizes are absolute px.
- Each slide is one `<section data-label="…" data-screen-label="…">`. The stage positions/sizes slides; sections must not set their own position/inset.
- All styling is **inline** on each element (no stylesheet classes). Shared values come from CSS custom properties declared once in a `:root` block (see Design Tokens).
- One `@keyframes blink` animation (cursor blocks on Title and Prompt slides): `0%,49% {opacity:1} 50%,100% {opacity:0}`, applied as `animation: blink 1.1s steps(1) infinite`.

## Design Tokens (matcha — identical to the Docker deck)
Colors:
- `--bg: #f4f1e8` page/slide background (warm cream)
- `--panel: #faf8f0` card background
- `--panel2: #eae6d9` terminal title bars / recessed fills
- `--line: #c5c2b0` all borders
- `--ink: #3a4433` primary text (dark moss)
- `--soft: #46503f` body text
- `--dim: #818678` secondary/mono comments
- `--faint: #979b8e` footers
- `--green: #6b8054` accent: headings-in-cards, `$` prompts, eyebrows
- `--amber: #DE6A41` accent: TASK badges, warnings, links
- Terminal window dots: `#b9baae` (all three, muted — not traffic-light colors)
- Terminal output text: `#7a9461`; terminal inline comments: `#818678`
- Green-tinted highlight fills: `rgba(107,128,84,0.12)` / `0.16` with `--green` border
- Divider slides: solid `--green` background, text `#f4f1e8` (muted: `rgba(244,241,232,0.75)`)

Background texture (every non-divider slide):
`background-image: linear-gradient(rgba(122,148,97,0.14) 1px, transparent 1px), linear-gradient(90deg, rgba(122,148,97,0.14) 1px, transparent 1px); background-size: 96px 96px;` over `--bg`.

Typography:
- `--mono: 'JetBrains Mono'` (weights 400/500/700/800) — titles, eyebrows, badges, terminal text, footers, `#` comment lines
- `--sans: 'IBM Plex Sans'` (weights 400/500/600) — body prose
- Both loaded from Google Fonts.

Type scale:
- Hero titles (Title/Exit/dividers): 800 110–120px/1.04–1.08 mono, letter-spacing -0.02em
- Slide titles (h1): `800 64px/1.12` mono, letter-spacing -0.01em
- Lead paragraphs: 400 34–36px/1.5 sans
- Body: 400 27–30px/1.4–1.55 sans
- Terminal/pre: 500 26px/1.85 mono (24px in 3-up cards)
- Eyebrows: 500 24px mono, letter-spacing 0.1em, color `--green`, format `## section-name`
- `#` comment lines: 500 25–26px/1.7 mono, `--dim`
- Footers: 500 24px mono, `--faint`
- Minimum anywhere: 24px.

Spacing / geometry:
- Slide padding: `90px 110px 44px` (TASK slides: `80px 110px 44px`)
- Title → content gap: 44–64px; card grids gap 24–32px
- Cards: radius 14px (12px for terminal windows/rows), border `1px solid --line`, background `--panel`, padding ~30–44px
- Footer on every slide, pinned with `margin-top: auto`: left `$ linux for the curious`, right `bornhack 2026`

## Recurring components
1. **Eyebrow + title**: green `## concepts`-style eyebrow, then h1.
2. **Terminal window**: `--panel` card, radius 12, `--panel2` header bar with three 13px `#b9baae` dots + mono label (`type along`, `you@bornhack:~`), body is a `<pre>` (26px/1.85 mono). `$` in `--green`, commands in `--ink`, output `#7a9461`, comments `#818678`. Note: line breaks inside the pre are authored *inside* the trailing span of each line (the `.dc` template parser strips whitespace-only text nodes between spans); if porting to plain HTML, normal newlines in the `<pre>` are fine.
3. **TASK badge row** (9 hands-on slides): `TASK n` chip — 700 26px mono, `#3a4433` on `--amber`, padding 8px 18px, radius 6, letter-spacing 0.06em — followed by amber mono note (`hands-on`, `hands-on — everyone`, `hands-on — careful now`, `hands-on — your first install`).
4. **TASK slide layout**: grid `1.15fr 0.85fr`, gap 44px — terminal "type along" left, explanation grid right (`auto 1fr` rows: green mono keyword, sans description), ending with a `#` comment line.
5. **Callout**: `--panel` card with `--green` border (checkpoints) or `--amber` border (warnings, e.g. the `rm` "no trash can" card), `→` or `⚠` lead-in.
6. **Divider slides** (Part 1 / Part 2): solid green, fake prompt `you@bornhack:~$ cd part-1/`, 120px "Part 1", 56px subtitle.

## Slide inventory (data-labels, in order)
1. Title · 2. Format · 3. Part 1 (divider) · 4. What Is Linux · 5. History · 6. Kernel (layer diagram: you → apps & shell → distro → kernel → hardware; kernel box green-highlighted) · 7. Distro (equation: kernel + package manager + software + desktop = a distro) · 8. Distro Tour (8 cards) · 9. Commercial vs Community · 10. Release Models (fixed/rolling/LTS) · 11. Package Managers (apt/dnf/pacman cards + snap/flatpak) · 12. Desktops (GNOME, KDE Plasma, COSMIC, Hyprland) · 13. Choosing (4 "if → then" rows) · 14. Part 2 (divider) · 15. Why Terminal · 16. Task 0 Terminal (Linux/macOS/Windows-WSL + checkpoint) · 17. Prompt (annotated `alice@campbox:~$`) · 18. Task 1 Navigate · 19. Task 2 Make · 20. Task 3 Nano (includes mock nano UI with ^O/^X/^K chips) · 21. Task 4 Read · 22. Task 5 Move · 23. Task 6 Delete (amber warning card) · 24. Task 7 Help (man/tldr, first `sudo apt install`) · 25. Task 8 Btop (mock meter bars: cpu green 38%, mem amber 61%, net gray 2.1M) · 26. Cheat Sheet (6 cards: navigate/create/read/move & delete/help/install) · 27. Where Next (3 cards) · 28. Exit.

## Interactions & Behavior
Provided entirely by `deck-stage.js`:
- ←/→ arrows, space, tap zones: prev/next; slide position persists in the URL
- Thumbnail rail: click to jump, drag to reorder
- Print → one page per slide (PDF export)
- No per-slide animation beyond the two blinking cursors; slide transition is the stage default.

## State Management
None. The deck is fully static; no data fetching, no forms.

## Assets
No external images or icons. Everything is typography, CSS borders/fills, and the two blinking-cursor blocks. Fonts via Google Fonts (JetBrains Mono, IBM Plex Sans) — self-host them if the venue's network is unreliable.

## Deployment suggestion (matching the sibling repo)
Mirror `Reventlow/docker_bornhack2026`: keep these sources in `source/`, produce a single self-contained `deck/index.html`, serve with a tiny nginx Docker image, publish via the existing GitHub Actions workflow. A second variant of this deck in a dark green-on-black terminal theme exists in the design project ("Linux for the Curious (dark).dc.html") if a dark version is ever wanted.
