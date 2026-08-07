# Changelog — Light on Haṭha Yoga site

## 2026-08-07

- **The intake workflow no longer loses a change when two land at once.**
  Deleting two photographs in a row made the second run push onto a
  remote that had already moved; git refused and the run failed. It now
  starts again from the current remote and redoes the work, up to five
  times. Everything it does is derived from build/uploads.json and the
  pending batches, so redoing it is safe.

- **An uploaded place now gets its own page**, like Hampi or Shringeri:
  breadcrumb back to the Gallery, the place as a heading, how many
  photographs and who sent them, and the same thumbnail grid and
  lightbox. The card under “Photographs by site” opens it, and the map's
  “All N photographs” link works again. Written by the intake workflow
  from build/uploads.json, because the site's own pages come from a
  WordPress mirror that a workflow cannot reach; when the last
  photograph of a place goes, its page goes with it.

- **Uploaded places now appear under “Photographs by site” too**, not
  only on the map. They have no page of their own, so the card opens the
  place on the map instead; the strip's “All N photographs” link, which
  used to point at a page that does not exist, is hidden for them.
- The intake workflow rewrites the cards as well as the map data, and the
  result is byte-identical to a full local rebuild.

## 2026-08-06 (later)

- **Podcasts tab: the standfirst removed.** The line counting the
  episodes and their span went; the list speaks for itself.

- **Podcasts, as a second tab on the Films page** (PI asked whether we could
  gather the team's podcast appearances — we can). 35 audio episodes,
  2014–2026, grouped by person with Jim first, laid out like the
  publications page: year on the left, episode linked, show and date beneath.
  Films stays the default tab; `/hyp/films/#podcasts` links straight to the
  other one. Keyboard-operable, and without JS both panels simply show.
  - Excluded: two paragliding interviews with Jim (not about the project),
    one Singleton episode whose host site is gone (Wayback only), and Gupta,
    who has no podcast appearances.
  - Two episodes are not in English and say so in the line (Spanish, Italian).
  - Every URL was fetched and confirmed; the six keenonyoga.com links answer
    403 to scripts but load fine in a browser.

## 2026-08-06

- **Films: "Final" dropped from the symposium video's title** (PI: it was
  filmed near the start of the project, not at its end).
- **HP printed edition: text replaced with the PI's wording** — the book has
  been accepted by the EFEO in Pondicherry and is due by the end of 2026
  (the old paragraph promised a 2026 Paris launch that has been superseded).
- Podcasts: the PI asks whether we can gather the team's podcast
  appearances — parked for a separate conversation with MI.

Kept by Maria (with Claude) from 4 Aug 2026 onwards; one entry per shipped
change, newest first. Earlier work (July 2026: Project Publications heading,
gallery lightbox, Film section, Jason's and Mark's publication lists, Jason's
bio/photo) predates this log — see `git log` for that history.

## 2026-08-05

- **Fieldwork map on the Gallery page** (PI request). An interactive map of
  India above the site cards, under a "Fieldwork map" heading, with
  "Photographs by site" heading the folders below it: every photograph is a
  point, points cluster as they overlap, and a pin opens a card with a
  thumbnail, the site, the region, the date of the shoot and a link into that
  site's folder. The map *complements* the folders, it does not replace them.
  - **Draws on load**, with retina (@2x) tiles so the basemap stays crisp.
    Note this means the tile server sees a visitor's IP as soon as the gallery
    opens — worth a line in the site's privacy notice before handover.
  - **Self-hosted** Leaflet + MarkerCluster in `assets/vendor/` (204 KB), our
    own markers, no CDN — the site stays a set of plain static folders.
    Leaflet is only linked on the page that actually has a map.
  - **Tiles**: CARTO Positron over OpenStreetMap data, attributed as required.
  - **Dates come from the photographs' own EXIF** (Kadri 6–8 March 2016,
    Hampi 11–14 March, Panhale Kaji 17 March). No photograph carries GPS — the
    Sony A7 used for the fieldwork has no GPS module — so each one currently
    sits on its site's point. `build/places.py` already reads per-photo GPS
    and honours a manual `PHOTO_COORDS` override, so genuine per-photograph
    clusters appear as soon as located photographs arrive.

- **Films now play in a large lightbox, not inside the small card.** Clicking
  a card opens a full-width 16:9 player (up to 1100px) over a dimmed page,
  with the title and source on two lines beneath it and an n/m counter.
  Arrows step through the videos of that section, Esc closes and stops
  playback, focus is trapped and returns to the card. Same behaviour as the
  photo gallery, so the site works one way throughout.
- **The Haṭhābhyāsapaddhati film is live on the Films page.** All six parts
  uploaded to the project's own YouTube channel
  ([@lightonhathayoga](https://www.youtube.com/@lightonhathayoga), a Brand
  Account so ownership can be handed on) as **unlisted**: they play from the
  site but are not listed on YouTube. The "Coming soon" placeholders are gone;
  every card is click-to-play through youtube-nocookie like the rest.
  Original numbering kept (1–5, 7) — part 6 is still missing.

## 2026-08-04

- **Roots of Yoga: out of the nav menu, into the bibliographies** (PI
  request). The menu item is gone from all HYP pages; the book itself is now
  a 2017 entry in both Jim's and Mark's book lists (chronological order),
  each linking to the book's page, which still exists at its old address —
  nothing breaks, incl. the "Publication of Roots of Yoga" link on Events.
- **Films page: the PI's curated YouTube list is live** (PI email "YouTube
  videos", 4 Aug 2026). 41 videos in 8 sections — the HYP Final Symposium
  first ("top billing" per the PI), then The Haṭhābhyāsapaddhati Film
  (6 "Coming soon" cards awaiting MI's YouTube uploads of the Drive files),
  Roots of Yoga, one section per team member, Further Viewing, and a link to
  the SOAS Centre of Yoga Studies channel. Every id verified alive; display
  titles editorially normalised from the real YouTube titles. Cards are
  click-to-play via youtube-nocookie (assets/films.js) — no YouTube cookies
  before the visitor presses play; without JS they are plain YouTube links.
  Known gaps for the PI: 5 links in his email arrived corrupted, 1 video is
  dead/private (r9rl5gM9S8o), 2 playlist links kept as single videos.
- **Gallery: film placeholder removed** (PI request). The "Coming soon" film
  card and the section headings are gone — the gallery is photos-only again;
  the film now lives solely under Films. A gallery redesign is planned.
- **Nav: Gallery moved after Publications; new FILMS section** (PI request).
  Menu order is now Home, Team, Publications, Gallery, Films, Events,
  Resources, Libraries, Blog. New page `hyp/films/` says "Coming soon." —
  wired to list the films from `build/films.py` once the embeds exist.
- **Publications: Daniela's section moved above Gupta's** (PI request).
  Order is now Birch, Mallinson, Singleton, Bevilacqua, Gupta.
- **Events: all verbs to past tense** (PI request). The 2019 entries were
  written before the events happened ("is presenting", "will be holding", …);
  all 12 phrases now read as past ("presented", "held", "were at", "hosted").
  Also fixes the original site's typo "is presentation the paper".
  Done in `build/events.py` so it survives rebuilds.
- Changelog started.
