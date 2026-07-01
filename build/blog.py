"""Blog listing builder.

The blog page is a list of <article> blocks (thumbnail + title + meta +
excerpt), NOT a single post-content region — so it needs its own extraction.
Produces clean post cards; records featured images in assets_used.
"""
import re
from html import escape
from bs4 import BeautifulSoup
import extract

DATE = re.compile(r"([A-Z][a-z]+ \d{1,2}(?:st|nd|rd|th)?,? \d{4})")


def build(src_path, site, pmap, assets_used):
    ctx = {"base_dir": extract._mirror_root(src_path), "assets_used": assets_used,
           "pmap": pmap or {}, "site": site}
    soup = BeautifulSoup(open(src_path, encoding="utf-8", errors="replace").read(), "lxml")
    out = []
    for art in soup.find_all("article"):
        h = art.find(["h1", "h2", "h3"])
        if not h:
            continue
        a = h.find("a")
        title = h.get_text(" ", strip=True)
        href = extract.rewrite_link(a.get("href", ""), ctx) if a and a.get("href") else ""

        img = art.find("img")
        thumb = ""
        if img:
            newsrc = extract.rewrite_asset(img.get("src") or img.get("data-src") or "", ctx)
            if newsrc:
                thumb = (f'<a class="post-thumb" href="{href}">'
                         f'<img src="{newsrc}" alt="" loading="lazy"></a>')

        author = date = ""
        meta = art.select_one(".fusion-meta-info, .fusion-single-line-meta, .post-meta, .fusion-meta-info-wrapper")
        if meta:
            mt = meta.get_text(" ", strip=True)
            m = re.search(r"By\s+([^|]+?)\s*(?:\||$)", mt)
            author = m.group(1).strip() if m else ""
            d = DATE.search(mt)
            date = d.group(1) if d else ""

        pc = art.select_one("div.post-content, div.fusion-post-content")
        excerpt = ""
        if pc:
            excerpt = re.sub(r"\s+", " ", pc.get_text(" ")).strip()
            while title and excerpt.startswith(title):      # drop repeated leading title
                excerpt = excerpt[len(title):].lstrip(" :–-")

        meta_line = " · ".join(x for x in (f"By {author}" if author else "", date) if x)
        parts = [thumb, '<div class="post-body">',
                 f'<h3 class="post-title"><a href="{href}">{escape(title)}</a></h3>']
        if meta_line:
            parts.append(f'<p class="post-meta">{escape(meta_line)}</p>')
        if excerpt:
            parts.append(f"<p>{escape(excerpt)}</p>")
        if href:
            parts.append(f'<a class="post-more" href="{href}">Read the full post →</a>')
        parts.append("</div>")
        out.append(f'<article class="post">{"".join(parts)}</article>')
    return "".join(out)
