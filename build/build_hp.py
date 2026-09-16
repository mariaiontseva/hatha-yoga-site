"""Build the HP sub-site (hp/<slug>/index.html) from the Enfold mirror."""
import os, re, json, shutil, sys
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
        if out_slug == "imprint":
            # PI, 16 Sep 2026: Nils Liersch asked for his details to come off
            # the site. The mirror's page is a German Impressum made out to him
            # personally, with his home address, tax number and mobile number.
            # Replaced wholesale, per the PI: him as the contact, no telephone,
            # Maria named as operator. The § 55 RStV citation goes too: it was
            # superseded by § 18 MStV in 2020, and a German imprint is not
            # required of a site run from Oxford in any case.
            html = (
                "<p><strong>Website operator:</strong></p>"
                "<p>Maria Iontseva<br/>\n"
                '<a href="mailto:maria.iontseva@wolfson.ox.ac.uk">'
                "maria.iontseva@wolfson.ox.ac.uk</a></p>"
                "<p><strong>Responsible for the content:</strong></p>"
                "<p>Professor James Mallinson<br/>\n"
                "Faculty of Asian and Middle Eastern Studies<br/>\n"
                "University of Oxford</p>"
                "<p><strong>Contact:</strong></p>"
                '<p><a href="mailto:jim.mallinson@ames.ox.ac.uk">'
                "jim.mallinson@ames.ox.ac.uk</a></p>"
                "<p>Light on Haṭha Yoga is a joint project of the University "
                "of Oxford and Philipps-Universität Marburg, funded by the "
                "AHRC and the DFG.</p>")
        if out_slug == "privacy-policy-2":
            # same request: the data controller block named him personally,
            # with the same home address and a student e-mail address
            html = re.sub(
                r"<p><strong>Data controller</strong></p><p>.*?</p>",
                "<p><strong>Data controller</strong></p><p>"
                "Professor James Mallinson<br/>\n"
                "Faculty of Asian and Middle Eastern Studies, "
                "University of Oxford<br/>\n"
                'E-mail address: <a href="mailto:jim.mallinson@ames.ox.ac.uk">'
                "jim.mallinson@ames.ox.ac.uk</a><br/>\n"
                'Link to the imprint: <a href="{{ROOT}}hp/imprint/">'
                "https://yoga.ames.ox.ac.uk/hp/imprint/</a></p>",
                html, count=1, flags=re.S)
        if out_slug == "printed-edition":
            # PI, 6 Aug 2026: launch plan superseded — replace the paragraph
            html = re.sub(
                r"We plan to launch the printed edition.*?later this year\.",
                "A book version of the edition of the text, together with "
                "four extensive introductory chapters, has been accepted for "
                "publication by the EFEO in Pondicherry and should be "
                "available by the end of 2026.",
                html, flags=re.S)
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
