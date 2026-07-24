# Jim's July 2026 feedback — design

**Source:** email from James Mallinson (PI) to Maria Iontseva, 24 July 2026.

**Goal:** carry out the PI's requests on the publications and gallery sections,
and prepare the ground for the HYP film.

**Governing decision (PI, confirmed 24 July 2026):** do exactly what Jim asks.
No editorial hedging, no "pending confirmation" notes, no substituting our own
judgement for his. Where his literal instruction cannot be executed (see
academia.edu below), achieve the same end by another route and say so — do not
silently narrow the scope.

## Architectural constraint that shapes every item

Every HYP page is regenerated from the read-only WordPress mirror by
`build/build_hyp.py`. Anything not present in the mirror — new publications,
new photographs, the film — is erased by the next rebuild if written straight
into the generated HTML.

The repo already has the pattern for this: `build/jimpubs.py` and
`build/danielapubs.py` hold new content as Python data, and `build/pubs.py`
grafts it into the extracted page at build time. **All new content in this spec
follows that pattern.** Nothing is hand-edited into `hyp/*/index.html`.

Second standing constraint: the site is handed to Oxford IT as plain static
folders — no database, no server-side code, no third-party runtime
dependencies. New interactive behaviour must be self-contained vanilla JS.

---

## 1. Publications — heading

`PREVIOUS PUBLICATIONS BY THE PROJECT TEAM` → `Project Publications`.

Implementation note: `build/pubs.py` `_remove_proposed_outputs()` locates the end
of the block it deletes by matching the text `PREVIOUS PUBLICATIONS`. The rename
must happen **after** that deletion runs, or the deletion silently stops working
and the "Proposed Project Outputs" block returns to the page. The ordering is
load-bearing and gets a comment saying so.

## 2. Publications — Jason Birch, 2016 to now

Jim: *"For Jason you could scrape his publications from 2016 to now from
academia.edu and put them on the site then ask him to check. That might be
better for provoking him into action."*

**academia.edu returns HTTP 403 to automated requests** — verified 24 July 2026
against `oxford.academia.edu/JasonBirch`. His profile is in fact at
`soas.academia.edu/JasonBirch`. The list is therefore compiled from open
sources and published exactly as Jim intends:

- `theluminescent.org/p/publications.html` — his own site; covers 2016–2024 with
  DOIs, but is incomplete (no 2017, 2021–2022, 2025 entries)
- SOAS staff profile
- *Journal of Yoga Studies*, EFEO/IFP catalogues, publisher DOI landing pages

Where an academia.edu URL for a given work is known, it is the link target —
that matches the house style already used for Jim's and Jason's entries.

Output: `build/jasonpubs.py`, shaped like `build/jimpubs.py` (`BOOKS`,
`ARTICLES`, `section_html()`), merged into his existing section by `pubs.py`,
followed by the standard academia.edu note pointing at `soas.academia.edu/JasonBirch`.

Published without caveats. Jim then asks Jason to check it — that provocation is
the point of the exercise.

## 3. Publications — Mark Singleton

Jim: *"Not sure about Mark, he's a lot more cagey online. But ChatGPT found a few
things to get started with."*

His section on the site currently stops at 2016. Same treatment as Jason: search
open sources for everything published since 2016, compile `build/marksingleton.py`
in the same shape, merge, publish. Expected to be a shorter and thinner list than
Jason's — that is the known and accepted state, not a reason to skip him.

## 4. Gallery — photographs, "a bit more user friendly"

Jim did not specify what "user friendly" means. Current state: five field-site
cards (Dabhoi, Hampi, Kadri, Panhale Kaji, Shringeri); each page holds 3–11
photographs in a 116px grid; clicking one navigates away to the bare JPEG. No
captions, no way back except the browser button, no way to move to the next
photograph, no photographer credit.

Scope:

- **Lightbox** — self-contained vanilla JS, no library. Keyboard operable: Esc
  closes, arrow keys move, focus is trapped while open, trigger regains focus on
  close. Required for the WCAG 2.1 AA confirmation the README already flags as a
  precondition for Oxford IT handover.
- **Captions** — the `alt` attributes are already meaningful ("Siddha on Stick",
  "Matsyendra", "Āsana 1"); surface them under each photograph in the lightbox.
- **Thumbnails** — grid minimum from 116px to ~170px.
- **Photographer credit** — one line per field site. Names are not yet known;
  the line is only added once the team supplies them (see §6).

## 5. Gallery — the film

Jim: *"It would be good also to put up the film, or at least start thinking about
it. I guess that would go in the gallery section."* Not yet buildable, and this
spec deliberately stops at the constraints:

- **Footage is incomplete.** The remainder is with Jason.
- **Possible embargo** until Jason's Mysore book is out.
- **Possible dispute.** Jim's position: the recut made to accompany his new book
  is not an HYP output, and the filming was paid for with HYP ERC money.
- **The video cannot live in this repository.** GitHub Pages caps files at 100 MB
  and repositories at 1 GB. Hosting must be external, embedded on the site.
  Oxford's own media services fit the ox.ac.uk domain and Jim's "this is an HYP
  output" argument best; Vimeo is the fallback; YouTube only via
  `youtube-nocookie` or a click-to-load facade, because a plain embed sets
  cookies on a University domain.

When unblocked: an `hyp/film/` page plus a card for it on the gallery index.

## 6. Gallery — more photographs

Blocked. Jim and Daniela both have unsorted fieldwork photographs. Design work
waits until the volume is known, then follows the same pattern as everything
else: `build/photos.py` plus `assets/img/fieldwork/`, so additions survive a
rebuild.

## 7. Correspondence (deferred by MI, 24 July 2026 — not part of this build)

- Jason — the film, and a request to check his publications list
- The team — fieldwork photographs, and the film
- Jim — receipt for the paid invoice; 4 August in Oxford; the LLM conference

## Order of work

1. Heading rename + gallery lightbox/captions/thumbnails (nothing blocks these)
2. Jason's publications, then Mark's
3. The film — revisit once Jason has answered

Each is a separate commit, verified against a local server before it is pushed.
