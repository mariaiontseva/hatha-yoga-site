# Unified Hatha Yoga Site — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn two mirrored WordPress sites (HYP, HP) into one clean static site with a shared landing page and a single typographic system, each sub-site keeping its current structure.

**Architecture:** A small Python extractor pulls the content region out of each mirrored WordPress page (Fusion/Avada for HYP, Enfold for HP), drops it into one shared semantic HTML template, and links one shared stylesheet. Landing page = two tiles. The HP reader is copied verbatim, never re-templated.

**Tech Stack:** Static HTML/CSS, self-hosted Source Serif 4 + Source Sans 3 (woff2), Python 3 + BeautifulSoup4 + lxml (build-time only, not shipped), a local static server for verification.

## Global Constraints

- **Typography:** Source Serif 4 (headings + body) + Source Sans 3 (nav/labels/UI), self-hosted in `assets/fonts/`. No external font CDN.
- **IAST is non-negotiable:** every page must render ā ī ū ṛ ṝ ḷ ṃ ḥ ṅ ñ ṭ ḍ ṇ ś ṣ correctly.
- **Structure preserved:** do NOT merge or rewrite content between sites. Re-skin only.
- **Reader exempt:** `hp/reader/` (index.html + default.css + settings.js + images) is copied as-is; no template, no CSS override.
- **Repo:** work in `~/hatha-yoga-local/` (standalone repo, remote `origin` = mariaiontseva/hatha-yoga-site). Never commit from `~`.
- **Fully static:** no server-side code, no DB, deployable as plain folders.

## Source layout (inputs, read-only)

- HYP mirror: `~/hyp-site/hyp.soas.ac.uk/` — Fusion/Avada, content in `div.post-content`.
- HP mirror: `~/hathapradipika-site/hatha.hosting144023.a2e88.netcup.net/` — Enfold/Avia.
- Reader (already extracted): currently `~/hatha-yoga-local/hp/` → must move to `hp/reader/`.

## Target layout (outputs)

```
index.html                 landing (2 tiles)
assets/site.css            shared stylesheet
assets/fonts/*.woff2       self-hosted Source Serif 4 + Source Sans 3
assets/img/                landing tile images
hyp/<page>/index.html      re-skinned HYP pages
hp/<page>/index.html       re-skinned HP pages
hp/reader/                 HP reader, verbatim
build/                     extractor + template (NOT deployed)
```

---

### Task 1: Type foundation — fonts + shared stylesheet

**Files:**
- Create: `assets/fonts/` (woff2 files), `assets/site.css`, `build/_typetest.html`

**Interfaces:**
- Produces: `assets/site.css` exposing CSS custom props `--font-serif`, `--font-sans`, base type scale, `.site-header`, `.site-nav`, `.site-main`, `.site-footer` classes consumed by all later tasks.

- [ ] **Step 1:** Download the two families as woff2 into `assets/fonts/` (Source Serif 4: 400, 400i, 600; Source Sans 3: 400, 600). Source: Google Fonts / gwFH github. Verify: `ls assets/fonts/*.woff2 | wc -l` ≥ 5.
- [ ] **Step 2:** Write `assets/site.css`: `@font-face` blocks (font-display:swap), `:root` tokens (`--font-serif:"Source Serif 4",serif; --font-sans:"Source Sans 3",sans-serif;` + color/space scale), base element styles (body serif, h1–h3, links, `figure img{max-width:100%}`), and the shell classes `.site-header/.site-nav/.site-main/.site-footer`. Light + readable; museum-clean.
- [ ] **Step 3:** Write `build/_typetest.html` linking `../assets/site.css` with an IAST paragraph (Haṭhapradīpikā, prāṇāyāma, kuṇḍalinī, Haṭhasaṅketacandrikā) and one verse.
- [ ] **Step 4 (verify):** Serve locally (`python3 -m http.server 8899 -d ~/hatha-yoga-local`), open `/build/_typetest.html`, screenshot. Confirm the served fonts load (not a system fallback) and every diacritic renders. Fix any missing glyph/weight before proceeding.
- [ ] **Step 5:** Commit `assets/` + `build/_typetest.html`.

---

### Task 2: Extractor + shared template

**Files:**
- Create: `build/template.py`, `build/extract.py`

**Interfaces:**
- Produces: `render_page(title, content_html, site, active) -> str` in `build/template.py` (full HTML doc using the Task 1 shell classes + a nav built from `site`'s page list).
- Produces: `extract_content(src_html_path, theme) -> (title, content_html)` in `build/extract.py`, where `theme in {"fusion","enfold"}`. `fusion` → inner of `div.post-content` with `div.fusion-*` wrapper divs unwrapped; `enfold` → inner of the Enfold main content region; both strip `script`, `style`, empty divs, and inline `style=`/theme classes, keeping headings, paragraphs, lists, tables, `figure/img`, links.

- [ ] **Step 1:** Write `build/template.py::render_page`. Nav = a small hardcoded dict per site (label → relative href) so menus are clean and identical in shape. Include header (site title + nav), `<main class="site-main">`, footer with legal links (HP) / contact (HYP).
- [ ] **Step 2:** Write `build/extract.py::extract_content` using BeautifulSoup(lxml). Implement both theme branches + a shared `clean(node)` that removes `script,style,noscript`, unwraps `div`s that only carry theme classes, drops `class`/`style`/`id` attrs except on `a[href]`/`img[src]`, and rewrites asset `src`/`href` from the mirror path to the new local path.
- [ ] **Step 3 (verify):** Run `extract_content` on ONE HYP page and ONE HP page, print the cleaned HTML length and first 500 chars. Confirm real content (headings/paragraphs), no `fusion-`/`avia-` wrappers, no `<script>`.
- [ ] **Step 4:** Commit `build/template.py` + `build/extract.py`.

---

### Task 3: Build the HP sub-site (`hp/`)

**Files:**
- Create: `hp/<page>/index.html` for each HP page; `build/build_hp.py`
- Move: `hp/{index.html,default.css,settings.js,images}` → `hp/reader/`

**Interfaces:**
- Consumes: `render_page`, `extract_content` (Task 2).

- [ ] **Step 1:** Move the current reader files into `hp/reader/` (`git mv`). Confirm `hp/reader/index.html` loads and its relative asset links still resolve.
- [ ] **Step 2:** Write `build/build_hp.py`: iterate the real HP pages (home, printed-edition, team, events, imprint, privacy, disclaimer, cookie — skip `?p=` alias files), call `extract_content(...,"enfold")` → `render_page(...,site="hp")`, write to `hp/<slug>/index.html`. Copy referenced `wp-content/uploads` images into `hp/assets/img/` and rewrite paths.
- [ ] **Step 3 (verify):** Run it. Serve, open `/hp/` and 3 inner pages + `/hp/reader/`. Screenshot. Confirm: unified type, working nav, images present, reader intact, no theme leftovers.
- [ ] **Step 4:** Commit `hp/` + `build/build_hp.py`.

---

### Task 4: Build the HYP sub-site (`hyp/`)

**Files:**
- Create: `hyp/<page>/index.html` for each HYP page; `build/build_hyp.py`

**Interfaces:**
- Consumes: `render_page`, `extract_content` (Task 2).

- [ ] **Step 1:** Write `build/build_hyp.py`: iterate the real HYP pages (home, team, publications, roots-of-yoga, chapters, resources, libraries, events, blog, gallery, contact, workshop, field sites Dabhoi/Hampi/Kadri/Panhale-Kaji/Shringeri, the special studies, and the 15 all-souls-2017 talk pages — skip `?p=` aliases + `nggallery` helper files), `extract_content(...,"fusion")` → `render_page(...,site="hyp")`. Copy referenced `wp-content/uploads` + gallery images into `hyp/assets/img/` and rewrite paths.
- [ ] **Step 2 (verify):** Run it. Serve, open `/hyp/` + 5 varied inner pages (a talk page, a field site, gallery, publications, team). Screenshot. Confirm type/nav/images and no Fusion wrappers.
- [ ] **Step 3:** Commit `hyp/` + `build/build_hyp.py`.

---

### Task 5: Landing page (two tiles)

**Files:**
- Modify: `index.html` (replace the old palm-leaf scaffold)
- Create: `assets/img/tile-hyp.jpg`, `assets/img/tile-hp.jpg`

**Interfaces:**
- Consumes: `assets/site.css` (Task 1).

- [ ] **Step 1:** Pick one representative image per tile from the mirrors' galleries (e.g. a field-site photo for HYP, a manuscript/print image for HP); place in `assets/img/`.
- [ ] **Step 2:** Rewrite `index.html`: minimal centered layout, short intro line, two large tiles (image + type overlay/beside), tile 1 → `hyp/` ("Hatha Yoga Project"), tile 2 → `hp/` ("Haṭhapradīpikā Online — critical edition"). Uses `assets/site.css` fonts; accessible alt text; responsive (stack on narrow).
- [ ] **Step 3 (verify):** Serve, screenshot desktop + narrow (`preview_resize`). Confirm both tiles link correctly and type matches the sub-sites.
- [ ] **Step 4:** Commit `index.html` + `assets/img/`.

---

### Task 6: Cross-site polish, link check, deploy prep

**Files:**
- Modify: any pages with broken links/assets; Create: `README.md`

- [ ] **Step 1:** Run a link/asset check across the built site (e.g. a short Python script or `wget --spider -r` against the local server) → list broken hrefs/img srcs. Fix path-rewrite misses in the build scripts and rebuild.
- [ ] **Step 2 (verify):** Re-run the checker → zero broken internal links; spot-check dark-mode/contrast and mobile on 3 pages.
- [ ] **Step 3:** Write `README.md` (what this is, how to rebuild: run `build/build_hp.py` + `build/build_hyp.py`, how to serve, how to hand to Oxford IT as static folders). Remove `README.txt` scaffold + `build/_typetest.html`.
- [ ] **Step 4:** Commit. Optional: enable GitHub Pages (root) for a live preview at mariaiontseva.github.io/hatha-yoga-site — confirm with Maria first (repo is private; Pages would expose it).

---

## Notes for the implementer

- The two mirrors are **read-only sources** outside the repo — never edit them; only read.
- `?p=NN.html` files are permalink duplicates — always skip them; use the pretty-slug page.
- When the extractor mangles a specific page (WordPress markup is inconsistent), prefer fixing the `clean()` heuristic over hand-editing output, so a rebuild stays reproducible — but a handful of manual fixes on stubborn pages is acceptable and should be noted in the commit.
- Verification is visual (served + screenshot) rather than unit tests: the deliverable is rendered pages, so "does it render correctly with IAST + nav + images" is the pass condition each task.
