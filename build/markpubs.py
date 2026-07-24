"""Mark Singleton's publications 2016 -> now (PI request, July 2026 — same
treatment as Jason's: project-era only, earlier work covered by the
academia.edu note).

He is, as the PI put it, 'a lot more cagey online': his academia.edu profile
(soas.academia.edu/MarkSingleton) lists only 9 papers and his SOAS profile
blocks automated fetching, so this list is shorter than Jason's by nature,
not by oversight.  Compiled 24 Jul 2026 from Wikipedia, publisher pages and
the old site's own 2016 row.  Roots of Yoga links to the site's own page.

Each item = (year, url_or_None, title_html, rest_html).
"""

A = "https://www.academia.edu/"

BOOKS = [
    ("2025",
     A + "169067390/The_Ha%E1%B9%ADh%C4%81bhy%C4%81sapaddhati_edition_and_translation",
     "<i>A Manual on the Practice of Haṭhayoga: An Edition and Translation of "
     "the Pune Manuscript of the Haṭhābhyāsapaddhati</i>",
     " (co-authored with Jason Birch and James Mallinson). Pondicherry: IFP/EFEO."),
    ("2017",
     "{{ROOT}}hyp/roots-of-yoga/",
     "<i>Roots of Yoga</i>",
     " (co-authored with James Mallinson). London: Penguin Classics."),
]

ARTICLES = [
    ("2020",
     None,
     "“Early Haṭha Yoga”",
     ", in <i>Routledge Handbook of Yoga and Meditation Studies</i>, eds. Suzanne "
     "Newcombe &amp; Karen O’Brien-Kop. Abingdon: Routledge."),
    ("2020",
     None,
     "“The Scholar-Practitioner of Yoga in the Western Academy”",
     " (with Borayin Larios), in <i>Routledge Handbook of Yoga and Meditation "
     "Studies</i>, eds. Suzanne Newcombe &amp; Karen O’Brien-Kop. Abingdon: Routledge."),
    ("2019",
     "https://doi.org/10.34000/JoYS.2019.V2.002",
     "“The Yoga of the Haṭhābhyāsapaddhati: Haṭhayoga on the Cusp of Modernity”",
     " (with Jason Birch), pp.3–70 in <i>Journal of Yoga Studies</i> 2."),
    ("2017",
     None,
     "“The Spiritual Body in Twentieth-Century Yoga”",
     ", in proceedings of the international workshop, Kyoto University."),
    ("2017",
     None,
     "“David Frawley and Vedic Yoga”",
     ", in <i>In the Name of the Veda</i>. Abingdon: Routledge."),
    ("2016",
     None,
     "“Yoga and Physical Culture: Transnational History and Blurred Discursive "
     "Contexts”",
     ", pp.172–184 in <i>Routledge Handbook of Contemporary India</i>, ed. Knut A. "
     "Jacobsen. Abingdon: Routledge."),
]


def _rows(items):
    out = []
    for year, url, title, rest in items:
        t = f'<a href="{url}">{title}</a>' if url else title
        out.append(f"<tr><td>{year}</td><td>{t}{rest}</td></tr>")
    return "".join(out)


def section_html():
    return ("<table>"
            "<tr><th></th><th>DR MARK SINGLETON</th></tr>"
            "<tr><td></td><td>BOOKS</td></tr>" + _rows(BOOKS) +
            "<tr><td></td><td>ARTICLES</td></tr>" + _rows(ARTICLES) +
            "</table>")
