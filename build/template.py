"""Shared page template for the unified Hatha Yoga site.

render_page(title, content_html, site, active, root) -> full HTML document
using the shell classes defined in assets/site.css.

All content pages live at depth 2 (e.g. hyp/team/index.html), so `root`
defaults to "../../". Nav hrefs are built relative to `root` so the site
works both when served from / and from a project subpath.
"""

# label -> slug path relative to site root (no leading slash)
NAVS = {
    "hyp": [
        ("Home",          "hyp/"),
        ("Team",          "hyp/team/"),
        ("Publications",  "hyp/publications/"),
        ("Roots of Yoga", "hyp/roots-of-yoga/"),
        ("Resources",     "hyp/resources/"),
        ("Libraries",     "hyp/libraries/"),
        ("Events",        "hyp/events/"),
        ("Blog",          "hyp/blog/"),
        ("Gallery",       "hyp/gallery/"),
    ],
    "hp": [
        ("Home",            "hp/"),
        ("Team",            "hp/team/"),
        ("Events",          "hp/events/"),
        ("Digital Edition", "hp/reader/"),
        ("Printed Edition", "hp/printed-edition/"),
    ],
}

TITLES = {"hyp": "The Haṭha Yoga Project", "hp": "Haṭhapradīpikā Online"}

FOOTERS = {
    "hyp": ('<span>The Haṭha Yoga Project · SOAS University of London</span>'
            '<span><a href="{root}hp/">Haṭhapradīpikā Online →</a></span>'),
    "hp":  ('<span>Haṭhapradīpikā Online · a critical edition &amp; translation</span>'
            '<span><a href="{root}hyp/">The Haṭha Yoga Project →</a> · '
            '<a href="{root}hp/imprint/">Imprint</a> · '
            '<a href="{root}hp/privacy-policy-2/">Privacy</a></span>'),
}


def _nav(site, active, root):
    out = []
    for label, slug in NAVS[site]:
        cur = ' aria-current="page"' if slug == active else ''
        out.append(f'<a href="{root}{slug}"{cur}>{label}</a>')
    return "\n      ".join(out)


def render_page(title, content_html, site, active="", root="../../"):
    site_title = TITLES[site]
    nav = _nav(site, active, root)
    footer = FOOTERS[site].format(root=root)
    # substitute content placeholders per page depth
    content_html = (content_html
                    .replace("{{IMG}}", f"{root}{site}/assets/img")
                    .replace("{{ROOT}}", root))
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — {site_title}</title>
<link rel="stylesheet" href="{root}assets/site.css">
<link rel="stylesheet" href="{root}assets/{site}.css">
</head>
<body class="site-{site}">
<header class="site-header"><div class="site-header-inner">
  <a class="site-title" href="{root}{site}/">{site_title}</a>
  <nav class="site-nav">
      {nav}
  </nav>
</div></header>

<main class="site-main narrow">
{content_html}
</main>

<footer class="site-footer"><div class="site-footer-inner">
  {footer}
</div></footer>
</body>
</html>
"""
