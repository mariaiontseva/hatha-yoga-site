"""Build the HP sub-site (hp/<slug>/index.html) from the Enfold mirror."""
import os, json, shutil, sys
from urllib.parse import unquote
sys.path.insert(0, os.path.dirname(__file__))
import extract, template, teams, gallery

PMAP = json.load(open(os.path.join(os.path.dirname(__file__), "pmap_hp.json")))

MIRROR = "/Users/mariaiontseva/hathapradipika-site/hatha.hosting144023.a2e88.netcup.net"
OUT = "/Users/mariaiontseva/hatha-yoga-local/hp"
IMG = os.path.join(OUT, "assets", "img")

# source slug -> output slug ("" = hp/index.html home).  active = nav key.
PAGES = [
    ("index",             "",                 "hp/"),
    ("team",              "team",             "hp/team/"),
    ("events",            "events",           "hp/events/"),
    ("printed-edition",   "printed-edition",  "hp/printed-edition/"),
    ("imprint",           "imprint",          ""),
    ("privacy-policy-2",  "privacy-policy-2", ""),
    ("disclaimer",        "disclaimer",       ""),
    ("cookie-policy-uk",  "cookie-policy-uk", ""),
]


def build():
    os.makedirs(IMG, exist_ok=True)
    all_used = set()
    for src_slug, out_slug, active in PAGES:
        src = (os.path.join(MIRROR, "index.html") if src_slug == "index"
               else os.path.join(MIRROR, src_slug, "index.html"))
        if not os.path.isfile(src):
            print("  MISSING", src); continue
        title, html, used = extract.extract_content(src, "enfold", site="hp", pmap=PMAP)
        if out_slug == "team":
            html = teams.restructure(html, "hp")
        else:
            html = gallery.wrap(html)
        all_used |= used
        root = "../" if out_slug == "" else "../../"
        page = template.render_page(title, html, site="hp", active=active, root=root)
        dest_dir = OUT if out_slug == "" else os.path.join(OUT, out_slug)
        os.makedirs(dest_dir, exist_ok=True)
        open(os.path.join(dest_dir, "index.html"), "w", encoding="utf-8").write(page)
        print(f"  hp/{out_slug or '(home)'}  <- {src_slug}  ({len(html)} chars, {len(used)} imgs)")
    # copy referenced images
    for p in all_used:
        clean = unquote(os.path.basename(p)).split("?")[0]
        try:
            shutil.copy2(p, os.path.join(IMG, clean))
        except Exception as e:
            print("  img fail", clean, e)
    print(f"copied {len(all_used)} images -> hp/assets/img/")


if __name__ == "__main__":
    build()
