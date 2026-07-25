"""Jason Birch's publications — as confirmed by Jason himself (email to Jim
and Maria, 25 Jul 2026), which supersedes the list compiled from open sources
on 24 Jul 2026.  Exactly his HYP books + 'peer-review articles during the
Project', nothing else (MI, 25 Jul 2026).

Choices fixed by that email + MI's direction:
- book links go to hal.science (his preference; resolved via the HAL API,
  since the links in his email arrived as bot-wall stubs);
- the Amaraugha is dated 2023 per Jason — note that IFP/EFEO/HAL catalogue
  it as 2024; his word was chosen deliberately;
- article titles keep the published wording (his email paraphrases from
  memory); the 2020 OUP chapter links to the DOI he supplied.

Each item = (year, url_or_None, title_html, rest_html).
"""

BOOKS = [
    ("2025",
     "https://hal.science/hal-05432677",
     "<i>A Manual on the Practice of Haṭhayoga: An Edition and Translation of "
     "the Pune Manuscript of the Haṭhābhyāsapaddhati</i>",
     " (co-authored with Mark Singleton and James Mallinson). Collection "
     "Indologie, Hatha Yoga Series. Pondicherry: Institut Français de Pondichéry."),
    ("2024",
     "https://hal.science/hal-05306877",
     "<i>Āsanas of the Yogacintāmaṇi: The Largest Premodern Compilation on "
     "Postural Practice</i>",
     ". Collection Indologie 161, Hatha Yoga Series 4. Pondicherry: Institut "
     "Français de Pondichéry."),
    ("2023",
     "https://hal.science/hal-05306873",
     "<i>The Amaraugha and Amaraughaprabodha of Gorakṣanātha: The Genesis of "
     "Haṭha and Rājayoga</i>",
     ". Collection Indologie 157, Hatha Yoga Series 3. Pondicherry: Institut "
     "Français de Pondichéry."),
]

ARTICLES = [
    ("2020",
     "https://doi.org/10.1093/oso/9780198733508.003.0009",
     "“The Quest for Liberation-in-Life: A Survey of Early Works on Haṭha- and "
     "Rājayoga”",
     ", pp.200–242 in <i>The [Oxford] History of Hinduism: Hindu Practice</i>, "
     "ed. Gavin Flood. Oxford: OUP."),
    ("2020",
     "https://doi.org/10.1163/9789004432802_021",
     "“Haṭhayoga’s Floruit on the Eve of Colonialism”",
     ", pp.451–479 in <i>Śaivism and the Tantric Traditions: Essays in Honour "
     "of Alexis G.J.S. Sanderson</i>. Leiden: Brill."),
    ("2019",
     "https://doi.org/10.34000/JoYS.2019.V2.002",
     "“The Yoga of the Haṭhābhyāsapaddhati: Haṭhayoga on the Cusp of Modernity”",
     " (with Mark Singleton), pp.3–70 in <i>Journal of Yoga Studies</i> 2."),
    ("2019",
     "https://doi.org/10.1007/s10781-019-09401-5",
     "“The Amaraughaprabodha: New Evidence on the Manuscript Transmission of an "
     "Early Work on Haṭha- and Rājayoga”",
     ", pp.947–977 in <i>Journal of Indian Philosophy</i> 47."),
    ("2018",
     "https://doi.org/10.18732/hssa.v6i0.25",
     "“Premodern Yoga Traditions and Ayurveda: Preliminary Remarks on Shared "
     "Terminology, Theory and Praxis”",
     ", pp.1–83 in <i>History of Science in South Asia</i> 6."),
    ("2018",
     "https://www.vandenhoeck-ruprecht-verlage.com/media/pdf/9f/78/68/OA_978-3-7370-0862-4.pdf",
     "“The Proliferation of Āsanas in Late Mediaeval Yoga Texts”",
     ", pp.101–180 in <i>Yoga in Transformation: Historical and Contemporary "
     "Perspectives</i>, eds. Karl Baier, Philipp Maas &amp; Karin Preisendanz. "
     "Vienna: V&amp;R unipress."),
]


def _rows(items):
    out = []
    for year, url, title, rest in items:
        t = f'<a href="{url}">{title}</a>' if url else title
        out.append(f"<tr><td>{year}</td><td>{t}{rest}</td></tr>")
    return "".join(out)


def section_html():
    """Jason's section: exactly the list he confirmed, books then articles."""
    return ("<table>"
            "<tr><th></th><th>DR JASON BIRCH</th></tr>"
            "<tr><td></td><td>BOOKS</td></tr>" + _rows(BOOKS) +
            "<tr><td></td><td>ARTICLES</td></tr>" + _rows(ARTICLES) +
            "</table>")
