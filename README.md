# Light on Haṭha Yoga — unified static site

One clean static site that brings two research resources under a shared
landing page and a single typographic system:

- **The Haṭha Yoga Project** (HYP) — `hyp/` — rebuilt from the SOAS site
- **Haṭhapradīpikā Online** (HP) — `hp/` — rebuilt from hathapradipika.online,
  including the interactive digital reader at `hp/reader/` (kept verbatim)

The landing page (`index.html`) is two tiles, one per resource.

## Why this exists

Both originals were WordPress sites with different themes (Avada/Fusion and
Enfold). This project extracts just their **content** and re-skins it with one
clean type system (self-hosted **Source Serif 4** + **Source Sans 3**, full
IAST diacritic coverage), producing plain static folders that any host can
serve — and that can be handed to Oxford IT as-is (no database, no CMS, no
server-side code, nothing to patch or maintain).

## Layout

```
index.html              landing (two tiles)
assets/site.css         shared stylesheet
assets/fonts/           self-hosted Source Serif 4 + Source Sans 3 (woff2)
assets/img/             landing tile images
hyp/<slug>/index.html   Haṭha Yoga Project pages (35)
hp/<slug>/index.html    Haṭhapradīpikā Online pages
hp/reader/              the digital reader, verbatim (~5 MB)
build/                  build scripts + data (NOT part of the deployed site)
docs/superpowers/       spec + implementation plan
```

## Serve it locally

```bash
python3 -m http.server 8899        # then open http://localhost:8899/
```

## Rebuild from the mirrors

The build reads two read-only WordPress mirrors that live **outside** this repo:

- `~/hyp-site/hyp.soas.ac.uk/`
- `~/hathapradipika-site/hatha.hosting144023.a2e88.netcup.net/`

```bash
python3 build/build_hp.py     # -> hp/<slug>/index.html + hp/assets/img/
python3 build/build_hyp.py    # -> hyp/<slug>/index.html + hyp/assets/img/
```

What the build does (`build/extract.py`, `build/template.py`):

- pulls the content region (`div.post-content` for HYP, `div.entry-content-wrapper`
  for HP), strips theme wrappers, scripts, sliders, share bars and inline styles;
- rewrites internal links: WordPress `?p=NN` permalinks → clean slugs
  (`build/pmap_*.json`), absolute old-host URLs → local, missing images dropped;
- copies every referenced image / PDF / audio file into `<site>/assets/img/`;
- wraps the result in the shared template with per-site navigation.

Verified: **0 broken images, 0 broken internal links, 0 links to the old hosts.**

## Handing it to Oxford IT

Oxford recommends its central Mosaic CMS but permits alternatives with a short
business case; static folders are the lowest-maintenance option to host. Before
hand-off, confirm **WCAG 2.1 AA** accessibility and University branding rules
(see https://www.ox.ac.uk/rules-for-websites).
