# Changelog — Light on Haṭha Yoga site

Kept by Maria (with Claude) from 4 Aug 2026 onwards; one entry per shipped
change, newest first. Earlier work (July 2026: Project Publications heading,
gallery lightbox, Film section, Jason's and Mark's publication lists, Jason's
bio/photo) predates this log — see `git log` for that history.

## 2026-08-04

- **Roots of Yoga: out of the nav menu, into the bibliographies** (PI
  request). The menu item is gone from all HYP pages; the book itself is now
  a 2017 entry in both Jim's and Mark's book lists (chronological order),
  each linking to the book's page, which still exists at its old address —
  nothing breaks, incl. the "Publication of Roots of Yoga" link on Events.
- **Events: all verbs to past tense** (PI request). The 2019 entries were
  written before the events happened ("is presenting", "will be holding", …);
  all 12 phrases now read as past ("presented", "held", "were at", "hosted").
  Also fixes the original site's typo "is presentation the paper".
  Done in `build/events.py` so it survives rebuilds.
- Changelog started.
