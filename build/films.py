"""Films shown in the Gallery — build-time data, same pattern as *pubs.py.

Each film: dict(slug, title, blurb, embed).

embed=None  -> the gallery shows a non-clickable 'Coming soon' card.
embed="..." -> set it to the hosted player URL (Oxford media / Vimeo /
youtube-nocookie — NOT a plain YouTube embed, which sets cookies on a
University domain) and rerun the build: hyp/film/<slug>/ appears with the
player and the card becomes a link to it.

The video file itself can never live in this repository: GitHub Pages caps
files at 100 MB and the repo at 1 GB. Hosting is external, always.
"""

FILMS = [
    dict(
        slug="hatha-yoga-project-film",
        title="The Haṭha Yoga Project Film",
        blurb="Filmed during the project’s fieldwork in India.",
        embed=None,
    ),
]

_PLAY = ('<svg viewBox="0 0 24 24" aria-hidden="true">'
         '<path d="M8 5v14l11-7z" fill="currentColor"/></svg>')


def section_html():
    """The 'Film' section appended to the gallery index."""
    cards = []
    for f in FILMS:
        if f["embed"]:
            cards.append(
                f'<a class="galcard" href="{{{{ROOT}}}}hyp/film/{f["slug"]}/">'
                f'<span class="galcard-img galcard-play">{_PLAY}</span>'
                f'<span class="galcard-label">{f["title"]}</span></a>')
        else:
            cards.append(
                f'<div class="galcard galcard-soon">'
                f'<span class="galcard-img galcard-play">{_PLAY}'
                f'<span class="soon-badge">Coming soon</span></span>'
                f'<span class="galcard-label">{f["title"]}</span></div>')
    return ('<h2 class="galsec">Film</h2>'
            '<div class="galindex">' + "".join(cards) + '</div>')


def pages():
    """(slug, title, html) for each released film — empty while embed=None."""
    out = []
    for f in FILMS:
        if not f["embed"]:
            continue
        out.append((f["slug"], f["title"],
            '<p class="crumb"><a href="{{ROOT}}hyp/gallery/">&#8592; Gallery</a></p>'
            f'<h1>{f["title"]}</h1>'
            f'<div class="filmwrap"><iframe src="{f["embed"]}" title="{f["title"]}" '
            'allowfullscreen loading="lazy"></iframe></div>'
            f'<p>{f["blurb"]}</p>'))
    return out
