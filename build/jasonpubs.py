"""Jason Birch's publications 2016 -> now (requested by the PI, July 2026:
'scrape his publications from 2016 to now … and put them on the site then ask
him to check').

academia.edu blocks automated fetching (HTTP 403), so this list was compiled
24 Jul 2026 from open sources instead: theluminescent.org/p/publications.html
(his own site), his SOAS staff profile, EFEO/IFP catalogues and journal DOIs.
Titles link to academia.edu where the URL is known (house style), otherwise to
the DOI / publisher page.  LEGACY holds his pre-2016 rows carried over from
the old site (with the mangled Rājayoga link repaired).

Each item = (year, url_or_None, title_html, rest_html).
"""

A = "https://www.academia.edu/"

BOOKS = [
    ("2025",
     A + "169067390/The_Ha%E1%B9%ADh%C4%81bhy%C4%81sapaddhati_edition_and_translation",
     "<i>A Manual on the Practice of Haṭhayoga: An Edition and Translation of "
     "the Pune Manuscript of the Haṭhābhyāsapaddhati</i>",
     " (co-authored with James Mallinson and Mark Singleton). Pondicherry: IFP/EFEO."),
    ("2024",
     "https://publications.efeo.fr/en/livres/1019_sanas-of-the-yogacint-ma-i",
     "<i>Āsanas of the Yogacintāmaṇi: The Largest Premodern Compilation on "
     "Postural Practice</i>",
     ". Pondicherry: IFP/EFEO."),
    ("2024",
     "https://publications.efeo.fr/en/livres/1013_the-amaraugha-and-amaraughaprabodha-of-gorak-an-tha",
     "<i>The Amaraugha and Amaraughaprabodha of Gorakṣanātha: The Genesis of "
     "Haṭha and Rājayoga</i>",
     ". Pondicherry: IFP/EFEO."),
    ("2023",
     "https://doi.org/10.11588/hasp.1203",
     "<i>On the Plastic Surgery of the Ears and Nose: The Nepalese Version of "
     "the Suśrutasaṃhitā</i>",
     " (co-authored with Dominik Wujastyk et al.). Heidelberg: Heidelberg Asian "
     "Studies Publishing."),
]

ARTICLES = [
    ("2023",
     "https://doi.org/10.34000/JoYS.2023.V4.01",
     "“Premodern Yogāsanas and Modern Postural Practice: Distinct Regional "
     "Collections of Āsanas on the Eve of Colonialism”",
     " (with Jacqueline Hargreaves), pp.31–82 in <i>Journal of Yoga Studies</i> 4."),
    ("2022",
     A + "78953966/The_Ocean_of_Yoga_An_Unpublished_Compendium_Called_the_Yog%C4%81r%E1%B9%87ava",
     "“The Ocean of Yoga: An Unpublished Compendium Called the Yogārṇava”",
     " (with S V B K V Gupta), pp.345–385 in <i>Journal of Indian Philosophy</i> 50, 3."),
    ("2021",
     None,
     "“Cleaning the Body like a Conch: The Haṭhasaṅketacandrikā and "
     "Śaṅkhaprakṣālana”",
     ", <i>Academia Letters</i>, Article 144."),
    ("2020",
     A + "44672605",
     "“The Quest for Liberation-in-Life: A Survey of Early Works on Haṭha- and "
     "Rājayoga”",
     ", pp.200–242 in <i>Hindu Practice</i>, ed. Gavin Flood. Oxford: OUP."),
    ("2020",
     "https://doi.org/10.1163/9789004432802_021",
     "“Haṭhayoga’s Floruit on the Eve of Colonialism”",
     ", pp.451–479 in <i>Śaivism and the Tantric Traditions: A Festschrift for "
     "Alexis Sanderson</i>, eds. Dominic Goodall, Shaman Hatley &amp; Harunaga "
     "Isaacson. Leiden: Brill."),
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
    ("2016",
     None,
     "“The Yamas and Niyamas: Patanjali’s View”",
     " (with Jacqueline Hargreaves), <i>Yoga Scotland Magazine</i>, Issue 29 (January)."),
    ("2016",
     None,
     "“The Yamas and Niyamas: Medieval and Modern Views”",
     " (with Jacqueline Hargreaves), <i>Yoga Scotland Magazine</i>, Issue 50 (May)."),
]

# pre-2016 rows carried over from the old site (Rājayoga link was mangled
# WordPress output — de-linked; everything else kept verbatim)
LEGACY = [
    ("2015",
     A + "12099338/The_Yogat%C4%81r%C4%81val%C4%AB_and_the_Hidden_History_of_Yoga",
     "“The <i>Yogataravali</i> and the Hidden History of Yoga”",
     ", <i>Namarupa Magazine</i>, Issue 20 (Spring 2015)"),
    ("2013",
     None,
     "‘The <i>Amanaska</i>: King of All Yogas: A Critical Edition and Annotated "
     "Translation with a Monographic Introduction.’",
     " DPhil Thesis, Oxford."),
    ("2013",
     None,
     "‘Rājayoga: The Reincarnations of the King of All Yogas’",
     ", <i>The International Journal of Hindu Studies</i>, 17, 3: 401–444"),
    ("2011",
     A + "1539699/Meaning_of_ha%E1%B9%ADha_in_Early_Ha%E1%B9%ADhayoga",
     "‘The Meaning of <i>haṭha</i> in Early <i>Haṭhayoga</i>’",
     ", <i>The Journal of the American Oriental Society</i>, 131.4."),
    ("2011",
     None,
     "“Universalist and Missionary Jainism: Jain Yoga of the Terāpanthī Tradition”",
     " in <i>Yoga in Practice</i>, Ed David White, University of Chicago Press"),
]


def _rows(items):
    out = []
    for year, url, title, rest in items:
        t = f'<a href="{url}">{title}</a>' if url else title
        out.append(f"<tr><td>{year}</td><td>{t}{rest}</td></tr>")
    return "".join(out)


def section_html():
    """Jason's full section: new books + new-and-legacy articles."""
    return ("<table>"
            "<tr><th></th><th>DR JASON BIRCH</th></tr>"
            "<tr><td></td><td>BOOKS</td></tr>" + _rows(BOOKS) +
            "<tr><td></td><td>ARTICLES</td></tr>" + _rows(ARTICLES + LEGACY) +
            "</table>")
