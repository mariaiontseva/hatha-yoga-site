"""James Mallinson's Haṭha Yoga Project publications (supplied by the PI, 2026).
Each entry's TITLE is the hyperlink (matching the Jason Birch format) — no
trailing 'read the full text' link. Merged into his existing section by pubs.py.
Each item = (year, url, title_html, rest_html).
"""

A = "https://www.academia.edu/"

BOOKS = [
    ("2025",
     A + "169067390/The_Ha%E1%B9%ADh%C4%81bhy%C4%81sapaddhati_edition_and_translation",
     "<i>A Manual on the Practice of Yoga: A Critical Edition and Annotated "
     "Translation of the Haṭhābhyāsapaddhati</i>",
     " (co-authored with Jason Birch and Mark Singleton). Pondicherry: IFP/EFEO."),
    ("2024",
     A + "144142644/The_Datt%C4%81treyayoga%C5%9B%C4%81stra_in_full_open_access_",
     "<i>The Dattātreyayogaśāstra</i>",
     ". Pondicherry: IFP/EFEO."),
    ("2022",
     A + "100432728/The_Am%E1%B9%9Btasiddhi_and_Am%E1%B9%9Btasiddhim%C5%ABla_the_"
         "Earliest_Texts_of_the_Ha%E1%B9%ADhayoga_Tradition",
     "<i>The Amṛtasiddhi and Amṛtasiddhimūla: The Earliest Texts of the Haṭhayoga</i>",
     "."),
]

ARTICLES = [
    ("2025",
     A + "144515176/The_Am%E1%B9%9Btasiddhi_Ha%E1%B9%ADhayoga_s_Flash_in_the_Alchemical_Pan",
     "“The Amṛtasiddhi: Haṭhayoga’s Flash in the Alchemical Pan”",
     ", pp.255–270 in <i>Indian Alchemy: Sources and Contexts</i>, ed. Dagmar Wujastyk. OUP."),
    ("2023",
     A + "121815947/Nath_Yogis_and_their_Amazing_Apparel_in_Early_Material_and_Textual_Sources",
     "“Nath Yogis and their ‘Amazing Apparel’ in Early Material and Textual Sources”",
     ", pp.65–95 in <i>Objects, Images, Stories: Simon Digby’s historical method</i>, "
     "ed. F. Orsini. OUP."),
    ("2022",
     A + "73383217/Mallinson_2022_Yogabhaskara_Jaipur_Palace",
     "“Manuscript of the Yogabhāskara or Radiance of Yoga”",
     ", pp.76–77 in <i>Masterpieces at the Jaipur Court</i>, ed. Mrinalini "
     "Venkateswaran &amp; Giles Tillotson. Delhi: Niyogi."),
    ("2021",
     A + "82535776/Yoga_Ha%E1%B9%ADha",
     "“Yoga: Haṭha”",
     " in <i>The Encyclopedia of Philosophy of Religion</i>, ed. Stewart Goetz and "
     "Charles Taliaferro. Wiley-Blackwell."),
    ("2020",
     A + "43937946/The_Am%E1%B9%9Btasiddhi_Ha%E1%B9%ADhayoga_s_Tantric_Buddhist_Source_Text",
     "“The Amṛtasiddhi: Haṭhayoga’s Tantric Buddhist Source Text”",
     ", pp.409–425 in <i>Śaivism and the Tantric Traditions: A Festschrift for Alexis "
     "Sanderson</i>, eds. Dominic Goodall, Shaman Hatley &amp; Harunaga Isaacson. Leiden: Brill."),
    ("2020",
     A + "44326659/Ha%E1%B9%ADhayogas_Early_History_From_Vajray%C4%81na_Sexual_Restraint_"
         "to_Universal_Somatic_Soteriology",
     "“Haṭhayoga’s early history: from sexual restraint in Vajrayāna to universal "
     "somatic soteriology”",
     ", pp.177–199 in <i>A History of Hindu Practice</i>, ed. Gavin Flood. Oxford: OUP."),
    ("2019",
     A + "38828589/K%C4%81lava%C3%B1cana_in_the_Konkan_How_a_Vajray%C4%81na_Ha%E1%B9%ADha"
         "yoga_Tradition_Cheated_Buddhisms_Death_in_India",
     "“Kālavañcana in the Konkan: How a Vajrayāna Haṭhayoga Tradition Cheated "
     "Buddhism’s Death in India”",
     ", pp.1–33 in <i>Religions</i> 10, 273."),
    ("2018",
     A + "37387077/Mallinson_2018_Yoga_and_Sex_What_is_the_Purpose_of_Vajrol%C4%ABmudr%C4%81_pdf",
     "“Yoga and Sex: What is the Purpose of Vajrolīmudrā?”",
     ", pp.181–222 in <i>Yoga in Transformation</i>, ed. Philipp Maas &amp; Karin "
     "Preisendanz. Vienna: V&amp;R unipress."),
]


def _rows(items):
    return "".join(
        f'<tr><td>{year}</td><td><a href="{url}">{title}</a>{rest}</td></tr>'
        for year, url, title, rest in items
    )


def book_rows():
    return _rows(BOOKS)


def article_rows():
    return _rows(ARTICLES)


def section_html():
    """Jim's HYP publications only, as a standalone pub-list section
    (matching the other team members' tables)."""
    return ("<table>"
            "<tr><th></th><th>PROFESSOR JAMES MALLINSON</th></tr>"
            "<tr><td></td><td>BOOKS</td></tr>" + _rows(BOOKS) +
            "<tr><td></td><td>ARTICLES</td></tr>" + _rows(ARTICLES) +
            "</table>")
