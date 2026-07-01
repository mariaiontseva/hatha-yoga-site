"""Build the HYP sub-site (hyp/<slug>/index.html) from the Fusion/Avada mirror.

Auto-discovers pages: MIRROR/index.html (home) + every MIRROR/<slug>/index.html,
skipping permalink aliases (?p=) and nggallery slideshow helpers.
"""
import os, glob, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
import extract, template

MIRROR = "/Users/mariaiontseva/hyp-site/hyp.soas.ac.uk"
OUT = "/Users/mariaiontseva/hatha-yoga-local/hyp"
IMG = os.path.join(OUT, "assets", "img")

# nav keys that should be highlighted when their page is the active one
NAV_ACTIVE = {"team","publications","roots-of-yoga","resources","libraries",
              "events","blog","gallery"}
SKIP = {"index"}  # home handled separately; "roots-of-yoga.html" dup ignored via dirs only


TOP_LEVEL = ["dabhoi", "hampi", "kadri", "panhale-kaji"]  # field sites as <slug>.html


def discover():
    pages = [("index", os.path.join(MIRROR, "index.html"), "")]  # home
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


def build():
    os.makedirs(IMG, exist_ok=True)
    all_used = set()
    n = 0
    for slug, src, active in discover():
        if not os.path.isfile(src):
            print("  MISSING", src); continue
        title, html, used = extract.extract_content(src, "fusion")
        if len(html) < 20:          # genuinely empty page — skip
            print("  skip (empty)", slug); continue
        all_used |= used
        page = template.render_page(title, html, site="hyp", active=active, root="../../")
        dest = OUT if slug == "index" else os.path.join(OUT, slug)
        os.makedirs(dest, exist_ok=True)
        open(os.path.join(dest, "index.html"), "w", encoding="utf-8").write(page)
        n += 1
        print(f"  hyp/{'(home)' if slug=='index' else slug}  ({len(html)} chars, {len(used)} imgs)")
    for p in all_used:
        try:
            shutil.copy2(p, os.path.join(IMG, os.path.basename(p)))
        except Exception as e:
            print("  img fail", os.path.basename(p), e)
    print(f"built {n} pages, copied {len(all_used)} images -> hyp/assets/img/")


if __name__ == "__main__":
    build()
