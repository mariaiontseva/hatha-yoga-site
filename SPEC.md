# Unified Hatha Yoga Site — Design Spec

**Date:** 2026-07-01
**Owner:** Maria Iontseva
**Status:** awaiting review → then implementation plan

## Goal

Combine two existing WordPress sites into **one static site** with a shared
landing page and a single, clean visual language. Each source site keeps its
**own current structure and content** — this is a re-skin + portal, not a content
merge.

## Structure

```
/                         Shared landing — two tiles
├─ /hyp/                  Hatha Yoga Project  (full hyp.soas.ac.uk)
└─ /hp/                   HP online           (full hathapradipika.online)
     └─ /hp/reader/       Haṭhapradīpikā Online reader — kept AS IS (interactive)
```

- **Landing:** two large tiles → HYP and HP online. Minimal, typographic.
- **Both sub-sites preserve their existing page tree and navigation.**
- Only the *presentation* is unified.

## Sources (already mirrored locally)

| Site | Meaning | Local mirror | Scope |
|------|---------|--------------|-------|
| HYP | Hatha Yoga Project (SOAS, AHRC) | `~/hyp-site/hyp.soas.ac.uk/` | full site, ~25 unique pages |
| HP  | Light on Haṭha / hathapradipika.online | `~/hathapradipika-site/…netcup.net/` | full site + reader |
| Reader | Haṭhapradīpikā Online | already in `~/hatha-yoga-local/hp/` | interactive, untouched |

## Approach — strip & reskin (not CSS-override)

Extract the **content** from each mirrored WordPress page and place it into one
clean, semantic HTML template with a single shared stylesheet. Do **not** keep the
Avada/Fusion theme CSS/JS and override it — that stays messy and fragile.

- Clean semantic HTML: header / nav / main / footer.
- One shared `assets/site.css` + fonts, used by landing, HYP, and HP.
- Preserve each page's real content, headings, images, links.
- Rewrite internal links to the new local paths.
- **Reader is exempt** — embedded as-is under `/hp/reader/`.

## Visual system

- **Typography:** Source Serif 4 (headings + body reading) + Source Sans 3 (nav,
  labels, UI). Both have full IAST / Latin Extended Additional coverage —
  non-negotiable requirement (ā ī ū ṛ ṝ ḷ ṃ ḥ ṅ ñ ṭ ḍ ṇ ś ṣ render correctly).
- **Style:** clean, contemporary, "museum-clean." Generous whitespace, restrained
  palette, thin rules, no heavy WordPress chrome.
- Self-host the two font families in `assets/fonts/` (no external CDN dependency,
  works offline and survives hand-off to IT).

## Destination

Research-project output (Hatha Yoga Project — AHRC). Fully static → can be handed
to Oxford IT as folders, or self-hosted (GitHub Pages) first. No DB, no CMS,
nothing to maintain. Meets the accepted exception to the Oxford Mosaic policy.

## Out of scope

- No content rewriting/merging between the two sites.
- No CMS, no build framework required (plain static; a light generator only if it
  reduces duplication).
- No changes to the reader app internals.

## Resolved decisions

1. **Landing tiles** — image **and** typography (a representative photo per tile,
   with the type treatment over/beside it).
2. **All Souls 2017** — keep the 15 talk pages as-is for now; optimise into an
   archive later.
3. **Fonts** — self-hosted in `assets/fonts/`, confirmed. No external CDN.
4. **Version control** — project lives in its own standalone git repo
   (`mariaiontseva/hatha-yoga-site`, private), independent of the home-dir repo,
   so nothing leaks to unrelated remotes.
