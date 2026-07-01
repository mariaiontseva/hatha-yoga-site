"""Build the HYP sub-site (hyp/<slug>/index.html) from the Fusion/Avada mirror.

Auto-discovers pages: MIRROR/index.html (home) + every MIRROR/<slug>/index.html,
skipping permalink aliases (?p=) and nggallery slideshow helpers.
"""
import os, re, glob, json, shutil, sys
from urllib.parse import unquote
sys.path.insert(0, os.path.dirname(__file__))
import extract, template, teams, pubs, gallery, libraries, blog

PMAP = json.load(open(os.path.join(os.path.dirname(__file__), "pmap_hyp.json")))

MIRROR = "/Users/mariaiontseva/hyp-site/hyp.soas.ac.uk"
OUT = "/Users/mariaiontseva/hatha-yoga-local/hyp"
IMG = os.path.join(OUT, "assets", "img")

# nav keys that should be highlighted when their page is the active one
NAV_ACTIVE = {"team","publications","roots-of-yoga","resources","libraries",
              "events","blog","gallery"}
SKIP = {"index"}  # home handled separately; "roots-of-yoga.html" dup ignored via dirs only


TOP_LEVEL = ["dabhoi", "hampi", "kadri", "panhale-kaji"]  # field sites as <slug>.html


def discover():
    pages = [("index", os.path.join(MIRROR, "index.html"), "hyp/")]  # home
    for d in sorted(glob.glob(os.path.join(MIRROR, "*", "index.html"))):
        slug = os.path.basename(os.path.dirname(d))
        if "?p=" in d or "nggallery" in slug or slug in SKIP:
            continue
        active = f"hyp/{slug}/" if slug in NAV_ACTIVE else ""
        pages.append((slug, d, active))
    for slug in TOP_LEVEL:
        f = os.path.join(MIRROR, f"{slug}.html")
        if os.path.isfile(f):
            pages.append((slug, f, ""))
    return pages


def _hero(src, all_used):
    """Rebuild the home Revolution Slider as a clean CSS crossfade hero."""
    from bs4 import BeautifulSoup
    s = BeautifulSoup(open(src, encoding="utf-8", errors="replace").read(), "lxml")
    sl = s.select_one("div.rev_slider_wrapper, .rev_slider")
    if not sl:
        return ""
    base = extract._mirror_root(src)
    imgs = []
    for img in sl.find_all("img"):
        for attr in ("src", "data-lazyload", "data-lazy", "data-src"):
            v = img.get(attr)
            if v and re.search(r"\.(jpg|jpeg|png)", v, re.I):
                loc = extract._resolve_local(v, base)
                if loc:
                    all_used.add(loc)
                    imgs.append(unquote(os.path.basename(v.split("?")[0])))
                break
    if not imgs:
        return ""
    tags = "".join(f'<img src="{{{{IMG}}}}/{fn}" alt="" loading="lazy">' for fn in imgs)
    return f'<div class="hero" data-count="{len(imgs)}">{tags}</div>'


def _emit(slug, src, active, root, all_used):
    title, html, used = extract.extract_content(src, "fusion", site="hyp", pmap=PMAP)
    if len(html) < 20:
        print("  skip (empty)", slug); return False
    if slug == "team":
        html = teams.restructure(html, "hyp")
    if slug == "publications":
        html = pubs.restructure(html)
    if slug == "libraries":
        html = libraries.restructure(html)
    if slug == "blog":
        html = blog.build(src, "hyp", PMAP, used)
    if slug == "gallery":
        html = gallery.index(html)
    elif slug == "roots-of-yoga":
        html = gallery.book(html)
    elif slug not in ("team", "blog"):
        html = gallery.wrap(html)
    if slug == "index":
        html = _hero(src, used) + html
    all_used |= used
    page = template.render_page(title, html, site="hyp", active=active, root=root)
    dest = OUT if slug == "index" else os.path.join(OUT, slug)
    os.makedirs(dest, exist_ok=True)
    open(os.path.join(dest, "index.html"), "w", encoding="utf-8").write(page)
    print(f"  hyp/{'(home)' if slug=='index' else slug}  ({len(html)} chars, {len(used)} imgs)")
    return True


def build():
    os.makedirs(IMG, exist_ok=True)
    all_used = set()
    built = set()
    n = 0
    for slug, src, active in discover():
        if not os.path.isfile(src):
            print("  MISSING", src); continue
        root = "../" if slug == "index" else "../../"
        if _emit(slug, src, active, root, all_used):
            n += 1; built.add(slug)
    # fill pages that exist ONLY as ?p=NN alias files (pretty permalink not mirrored)
    for nn, slug in PMAP.items():
        if not slug or slug in built:
            continue
        alias = os.path.join(MIRROR, f"index.html?p={nn}.html")
        if os.path.isfile(alias) and _emit(slug, alias, "", "../../", all_used):
            n += 1; built.add(slug)
            print(f"    (from alias p={nn})")
    for p in all_used:
        clean = unquote(os.path.basename(p)).split("?")[0]
        try:
            shutil.copy2(p, os.path.join(IMG, clean))
        except Exception as e:
            print("  img fail", clean, e)
    print(f"built {n} pages, copied {len(all_used)} images -> hyp/assets/img/")


if __name__ == "__main__":
    build()
