"""Content extractor for the two mirrored WordPress sites.

extract_content(src_html_path, theme, site, pmap) -> (title, content_html)
  theme "fusion"  -> HYP (Avada/Fusion): content in div.post-content
  theme "enfold"  -> HP  (Enfold/Avia):  content across div.entry-content-wrapper
  site  "hyp"|"hp": used to build internal link targets
  pmap  {"NN": "slug"}: WordPress ?p=NN permalink -> clean slug map

Returned content_html is cleaned semantic markup using two placeholders that
template.render_page substitutes per page depth:
  {{ROOT}}  -> path back to site root ("../" home, "../../" inner)
  {{IMG}}   -> path to this site's image dir ("{root}{site}/assets/img")
"""
import os, re
from urllib.parse import unquote
from bs4 import BeautifulSoup, NavigableString, Tag, Comment

KEEP_TAGS = {"h1","h2","h3","h4","h5","h6","p","ul","ol","li","strong","em","b","i",
             "a","img","figure","figcaption","blockquote","table","thead","tbody",
             "tr","th","td","br","hr","sup","sub","span","div"}
DROP_TAGS = {"script","style","noscript","iframe","form","button","input","svg",
             "link","meta"}
UNWRAP_HINT = re.compile(r"fusion|avia|av-|av_|entry-content|post-content|wrapper|"
                         r"container|column|col-|row|clearfix|widget|sc_", re.I)
REMOVE_SELECTORS = ("div.rev_slider_wrapper, div.rev_slider, div.tp-banner-container, "
                    "ul.rev-slidebg, div.forcefullwidth_wrapper_tp_banner, "
                    "div.fusion-sharing-box, div.fusion-social-links, "
                    "div.fusion-breadcrumbs")
IMG_EXT = re.compile(r"\.(jpg|jpeg|png|gif|webp|svg)$", re.I)
FILE_EXT = re.compile(r"\.(jpg|jpeg|png|gif|webp|svg|pdf|docx?|zip|mp3|m4a|wav|ogg)$", re.I)
SLUG_RE = re.compile(r"[A-Za-z0-9āīūṛṝḷḹṃḥṅñṭḍṇśṣ_-]+$")


def _clean_name(src):
    """Decode + strip query/fragment, return a clean basename."""
    src = unquote(src).split("#")[0].split("?")[0]
    return os.path.basename(src)


def rewrite_asset(src, ctx):
    """Return the new asset path, or None if the file is missing from the mirror."""
    if src.startswith("data:"):
        return src
    fname = _clean_name(src)
    if not fname:
        return None
    cand = _resolve_local(src, ctx["base_dir"])
    if not cand:
        return None
    ctx["assets_used"].add(cand)
    return "{{IMG}}/" + fname


def rewrite_link(href, ctx):
    site = ctx["site"]; pmap = ctx["pmap"]
    if href.startswith(("mailto:", "tel:", "#", "javascript")):
        return href
    # absolute URL pointing at the mirror's OWN host -> treat as internal
    host = os.path.basename(ctx["base_dir"])
    href = re.sub(rf"^https?://{re.escape(host)}/?", "/", href)
    dec = unquote(href)
    # WordPress permalink alias ?p=NN -> clean slug
    m = re.search(r"[?&]p=(\d+)", dec)
    if m and m.group(1) in pmap:
        slug = pmap[m.group(1)]
        return "{{ROOT}}" + site + "/" + (slug + "/" if slug else "")
    # the HP digital reader
    if re.search(r"/reader/?", dec) or "digital-edition" in dec:
        return "{{ROOT}}hp/reader/"
    # a file/asset link (image, pdf, audio) -> copy + link, or drop if missing
    if FILE_EXT.search(dec.split("?")[0]):
        return rewrite_asset(href, ctx)  # may be None -> link unwrapped
    # nggallery slideshow helpers -> the gallery page
    if "nggallery" in dec:
        return "{{ROOT}}" + site + "/gallery/"
    # external absolute to another host -> leave as-is
    if href.startswith(("http://", "https://")):
        return href
    # relative internal link to a sibling mirror page -> map by slug
    base = dec.split("#")[0].split("?")[0].strip("/")
    seg = base.split("/")[-1].replace("index.html", "")
    seg = re.sub(r"\.html$", "", seg)
    if seg and SLUG_RE.fullmatch(seg):
        return "{{ROOT}}" + site + "/" + seg + "/"
    return href


def _resolve_local(src, base_dir):
    src = unquote(src).split("#")[0].split("?")[0]
    src = re.sub(r"^https?://[^/]+/", "", src)
    for cand in (os.path.join(base_dir, src),
                 os.path.join(base_dir, src.lstrip("/"))):
        if os.path.isfile(cand):
            return cand
    fname = os.path.basename(src)
    up = os.path.join(base_dir, "wp-content")
    if os.path.isdir(up):
        for root, _, files in os.walk(up):
            for f in files:
                # disk names may carry a saved query suffix, e.g. "x.jpg?t=123"
                if f == fname or unquote(f).split("?")[0] == fname:
                    return os.path.join(root, f)
    return None


def _clean_attrs(tag, ctx):
    if tag.name == "a":
        href = tag.get("href", "")
        tag.attrs = {}
        new = rewrite_link(href, ctx) if href else ""
        if new:
            tag["href"] = new
        else:
            tag.unwrap()          # dead/missing target -> keep the text only
    elif tag.name == "img":
        src = tag.get("src") or tag.get("data-src") or ""
        alt = tag.get("alt", "")
        new = rewrite_asset(src, ctx) if src else None
        if not new:
            tag.decompose()       # image missing from mirror -> drop it
            return
        tag.attrs = {}
        tag["src"] = new
        tag["alt"] = alt
        tag["loading"] = "lazy"
    else:
        tag.attrs = {}


def _prune(node, ctx):
    for c in node.find_all(string=lambda s: isinstance(s, Comment)):
        c.extract()
    for w in node.select(REMOVE_SELECTORS):
        w.decompose()
    for el in list(node.descendants):
        if isinstance(el, Tag) and el.name in DROP_TAGS:
            el.decompose()
    for el in list(node.find_all(True)):
        if el.name not in KEEP_TAGS:
            el.unwrap(); continue
        if el.name in ("div", "span"):
            cls = " ".join(el.get("class", []))
            if el.name == "div" or not cls or UNWRAP_HINT.search(cls):
                el.unwrap(); continue
        _clean_attrs(el, ctx)
    return node


def _collapse(html):
    s = BeautifulSoup(html, "lxml")
    for p in s.find_all(["p", "li", "span"]):
        if not p.get_text(strip=True) and not p.find("img"):
            p.decompose()
    for lst in s.find_all(["ul", "ol"]):
        if not lst.find("li"):
            lst.decompose()
    body = s.body or s
    return "".join(str(c) for c in body.contents).strip()


def _title(soup, fallback):
    t = soup.find("title")
    if t:
        txt = re.split(r"\s*[|–]\s*", t.get_text(strip=True))[0].strip()
        if txt:
            return txt
    h = soup.find(["h1", "h2"])
    return h.get_text(" ", strip=True) if h else fallback


def extract_content(src_html_path, theme, site, pmap=None, assets_used=None):
    ctx = {"base_dir": _mirror_root(src_html_path),
           "assets_used": assets_used if assets_used is not None else set(),
           "pmap": pmap or {}, "site": site}
    html = open(src_html_path, encoding="utf-8", errors="replace").read()
    soup = BeautifulSoup(html, "lxml")
    title = _title(soup, os.path.basename(os.path.dirname(src_html_path)))

    if theme == "fusion":
        region = soup.select_one("div.post-content")
        blocks = [region] if region else []
    elif theme == "enfold":
        blocks = soup.select("div.entry-content-wrapper")
    else:
        raise ValueError(theme)

    parts = []
    for b in blocks:
        _prune(b, ctx)
        parts.append("".join(str(c) for c in b.contents))
    content = _collapse("\n".join(parts))
    return title, content, ctx["assets_used"]


def _mirror_root(path):
    d = os.path.dirname(path)
    while d and d != "/":
        if os.path.isdir(os.path.join(d, "wp-content")):
            return d
        d = os.path.dirname(d)
    return os.path.dirname(path)
