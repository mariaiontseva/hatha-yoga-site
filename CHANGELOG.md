# Changelog — Light on Haṭha Yoga site

Kept by Maria (with Claude) from 4 Aug 2026 onwards; one entry per shipped
change, newest first. Earlier work (July 2026: Project Publications heading,
gallery lightbox, Film section, Jason's and Mark's publication lists, Jason's
bio/photo) predates this log — see `git log` for that history.

## 2026-08-05

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
