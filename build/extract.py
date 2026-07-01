"""Content extractor for the two mirrored WordPress sites.

extract_content(src_html_path, theme) -> (title, content_html)
  theme "fusion"  -> HYP (Avada/Fusion): content in div.post-content
  theme "enfold"  -> HP  (Enfold/Avia):  content across div.entry-content-wrapper

The returned content_html is cleaned semantic markup: headings, paragraphs,
lists, tables, figure/img, links. Theme wrappers, scripts, styles and inline
attributes are stripped. Image/href srcs are rewritten via `rewrite_asset`,
which also records every referenced local image in `assets_used`.
"""
import os, re
from bs4 import BeautifulSoup, NavigableString, Tag, Comment

KEEP_TAGS = {"h1","h2","h3","h4","h5","h6","p","ul","ol","li","strong","em","b","i",
             "a","img","figure","figcaption","blockquote","table","thead","tbody",
             "tr","th","td","br","hr","sup","sub","span","div"}
DROP_TAGS = {"script","style","noscript","iframe","form","button","input","svg",
             "link","meta"}
# theme/junk classes whose divs should be unwrapped (contents kept, tag removed)
UNWRAP_HINT = re.compile(r"fusion|avia|av-|av_|entry-content|post-content|wrapper|"
                         r"container|column|col-|row|clearfix|widget|sc_", re.I)


def _clean_attrs(tag, base_dir, assets_used):
    if tag.name == "a":
        href = tag.get("href", "")
        tag.attrs = {}
        if href:
            tag["href"] = rewrite_link(href, base_dir, assets_used)
    elif tag.name == "img":
        src = tag.get("src") or tag.get("data-src") or ""
        alt = tag.get("alt", "")
        tag.attrs = {}
        if src:
            tag["src"] = rewrite_asset(src, base_dir, assets_used)
        tag["alt"] = alt
        tag["loading"] = "lazy"
    else:
        tag.attrs = {}


def rewrite_asset(src, base_dir, assets_used):
    """Map a mirror image path to hp/hyp assets/img/<file> and record the source."""
    if src.startswith("data:"):
        return src
    src = src.split("?")[0].split("#")[0]
    fname = os.path.basename(src)
    if not fname:
        return src
    # locate the real file inside the mirror (relative or absolute-ish)
    cand = _resolve_local(src, base_dir)
    if cand:
        assets_used.add(cand)
    return f"../assets/img/{fname}"


def rewrite_link(href, base_dir, assets_used):
    """Rewrite internal permalink-style links to clean local paths; leave
    external and anchor links alone. Best-effort — polish pass fixes misses."""
    if href.startswith(("http://","https://","mailto:","tel:","#")):
        # external absolute back to same host -> make relative later in polish
        return href
    # image/file link
    if re.search(r"\.(jpg|jpeg|png|gif|webp|svg|pdf)$", href, re.I):
        return rewrite_asset(href, base_dir, assets_used)
    return href


def _resolve_local(src, base_dir):
    """Return an existing file path inside the mirror for this src, or None."""
    src = src.split("?")[0]
    # strip protocol+host if absolute
    src = re.sub(r"^https?://[^/]+/", "", src)
    for cand in (os.path.join(base_dir, src),
                 os.path.join(base_dir, src.lstrip("/"))):
        if os.path.isfile(cand):
            return cand
    # fall back: search by basename under the mirror (wp-content/uploads)
    fname = os.path.basename(src)
    up = os.path.join(base_dir, "wp-content", "uploads")
    if os.path.isdir(up):
        for root, _, files in os.walk(up):
            if fname in files:
                return os.path.join(root, fname)
    return None


# widget containers to remove wholesale (slider, search, social, share bars)
REMOVE_SELECTORS = ("div.rev_slider_wrapper, div.rev_slider, div.tp-banner-container, "
                    "ul.rev-slidebg, div.forcefullwidth_wrapper_tp_banner, "
                    "div.fusion-sharing-box, div.fusion-social-links, "
                    "div.avia_textblock ~ div.hr, div.fusion-breadcrumbs")


def _prune(node, base_dir, assets_used):
    # strip HTML comments (e.g. "START REVOLUTION SLIDER ...")
    for c in node.find_all(string=lambda s: isinstance(s, Comment)):
        c.extract()
    # remove known widget containers wholesale
    for w in node.select(REMOVE_SELECTORS):
        w.decompose()
    for el in list(node.descendants):
        if isinstance(el, Tag) and el.name in DROP_TAGS:
            el.decompose()
    # unwrap junk container divs/spans, clean attrs on the rest
    for el in list(node.find_all(True)):
        if el.name not in KEEP_TAGS:
            el.unwrap()
            continue
        if el.name in ("div","span"):
            cls = " ".join(el.get("class", []))
            if not cls or UNWRAP_HINT.search(cls) or el.name == "div":
                el.unwrap()
                continue
        _clean_attrs(el, base_dir, assets_used)
    return node


def _collapse(html):
    # drop empty paragraphs / stray whitespace-only nodes
    s = BeautifulSoup(html, "lxml")
    for p in s.find_all(["p","li","span"]):
        if not p.get_text(strip=True) and not p.find("img"):
            p.decompose()
    # drop now-empty lists
    for lst in s.find_all(["ul","ol"]):
        if not lst.find("li"):
            lst.decompose()
    body = s.body or s
    return "".join(str(c) for c in body.contents).strip()


def _title(soup, fallback):
    t = soup.find("title")
    if t:
        txt = t.get_text(strip=True)
        txt = re.split(r"\s*[|–-]\s*", txt)[0].strip()
        if txt:
            return txt
    h = soup.find(["h1","h2"])
    return h.get_text(" ", strip=True) if h else fallback


def extract_content(src_html_path, theme, assets_used=None):
    if assets_used is None:
        assets_used = set()
    base_dir = _mirror_root(src_html_path)
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
        _prune(b, base_dir, assets_used)
        parts.append("".join(str(c) for c in b.contents))
    content = _collapse("\n".join(parts))
    return title, content, assets_used


def _mirror_root(path):
    """Walk up to the mirror host root (dir containing wp-content or index.html)."""
    d = os.path.dirname(path)
    while d and d != "/":
        if os.path.isdir(os.path.join(d, "wp-content")):
            return d
        d = os.path.dirname(d)
    return os.path.dirname(path)
