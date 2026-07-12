"""Daniela Bevilacqua's HYP-related publications (supplied by her, 2026).
She has no existing personal bibliography table on Publications, so this adds
a NEW section (matching the Birch/Mallinson/Singleton/Gupta format) — not a
merge. Linked titles follow the Jason Birch style (link on the title itself).
"""

ARTICLES = [
    ("Forthcoming",
     None,
     "“Sadhus' yoga: Soteriological and Pragmati Approaches among Indian Ascetics”",
     ". In <i>Handbook of Contemporary Yoga</i>, edited by Måns Broo. Brill."),
    ("Forthcoming",
     None,
     "“Living through mantras. The Use of Mantras Among Contemporary Hindu Ascetics”",
     ". <i>Kervan</i>."),
    ("2026",
     "https://cswr.hds.harvard.edu/news/2026/03/27/sadhus",
     "“Sadhus.”",
     " <i>Archive of Mystical Experiences</i>. Center for the Study of World "
     "Religions, Harvard Divinity School."),
    ("2025",
     "https://doi.org/10.1080/00856401.2025.2524248",
     "“Embodying sacred pain: Practice of austerities among Hindu ascetics”",
     ". <i>South Asia: Journal of South Asian Studies</i>, 48(4), 804–823."),
    ("2025",
     None,
     "“Tapobhūmi: When Spiritual Power Saturates the Landscape”",
     ". <i>Religions of South Asia</i> 19.2 (2025) 203–225."),
    ("2022",
     None,
     "“Towards a Nath Re-appropriation of Hatha-Yoga”",
     ". In <i>The Power of the Nath Yogis: Yogic Charisma, Political Influence and "
     "Social Authority</i>, edited by D. Bevilacqua, E. Stuparich, 281–306. "
     "Amsterdam, Netherlands: Amsterdam University Press."),
    ("2020",
     None,
     "“Globalization and Asceticism: Foreign Ascetics on the Threshold of Hindu "
     "Religious Orders”",
     ". In <i>Routledge International Handbook of Religion in Global Society</i>, "
     "edited by J.S. Cornelio &amp; F. Gautier, 199–211. Routledge."),
    ("2020",
     None,
     "“Observing Yoga: The Use of Ethnographic Methodologies to Develop Yoga "
     "Studies”",
     ". In <i>Routledge Handbook of Yoga and Meditation Studies</i>, edited by "
     "Karen O’Brien Cop &amp; Suzanne Newcombe, 393–408. United Kingdom: Routledge."),
    ("2018",
     None,
     "“Old Tool for New Times: The Discovery of an Ancient Holy Site in "
     "Contemporary India.”",
     " <i>Journal of the British Association for the Study of Religions</i>, "
     "v. 20: 45–66."),
    ("2017",
     "https://doi.org/10.1558/rosa.37023",
     "“Let the Sādhus Talk. Ascetic understanding of Haṭha Yoga and yogāsanas”",
     ", <i>Religions of South Asia</i> 11 (2-3): 182–206."),
    ("2017",
     "https://doi.org/10.13135/1825-263X/2269",
     "“Are women entitled to become ascetics? An historical and ethnographic "
     "glimpse on female asceticism in Hindu religions”",
     ". <i>Kervan International Journal of Afro-Asiatic Studies</i>, 21: 51–79."),
]

BOOK = [
    ("2024", None,
     "<i>From Tapas to Modern Yoga. Sādhus’ Understanding of Embodied Practices</i>",
     ". Equinox Publisher."),
]

VOLUME = [
    ("2023", None,
     "“Yoga and the Traditional Physical Practices of South Asia, Influence, "
     "Entanglement and Confrontation.”",
     " <i>Journal of Yoga Studies</i>, vol. 4 (Special Issue). Edited with "
     "Mark Singleton."),
    ("2022", None,
     "<i>The Power of the Nath Yogis: Yogic Charisma, Political Influence and "
     "Social Authority</i>",
     ". Amsterdam, Netherlands: Amsterdam University Press. Edited with "
     "Eloisa Stuparich."),
]

ENCYCLOPEDIC = [
    ("2021", None,
     "“Lignées de yogis: la construction des identités (xvi-xviii siècle)”, "
     "352–365; “Vivre en sadhu dans l’Inde contemporaine”, 589–607",
     ". In <i>Yoga. L’encyclopedie</i>, edited by Ysé Tardan-Macquelier. Paris: "
     "Les Editions Albin Michel."),
]


def _rows(items):
    out = []
    for year, url, title, rest in items:
        cite = f'<a href="{url}">{title}</a>{rest}' if url else f"{title}{rest}"
        out.append(f"<tr><td>{year}</td><td>{cite}</td></tr>")
    return "".join(out)


def _subhead(label):
    # match the other tables' convention: bold label in the citation column
    return f"<tr><td></td><td><strong>{label}</strong></td></tr>"


def section_html():
    parts = ['<table><tr><th></th><th>DR DANIELA BEVILACQUA</th></tr>']
    parts.append(_subhead("ARTICLES &amp; BOOK CHAPTERS"))
    parts.append(_rows(ARTICLES))
    parts.append(_subhead("BOOK"))
    parts.append(_rows(BOOK))
    parts.append(_subhead("EDITED VOLUMES"))
    parts.append(_rows(VOLUME))
    parts.append(_subhead("ENCYCLOPEDIC ENTRY"))
    parts.append(_rows(ENCYCLOPEDIC))
    parts.append('</table>')
    return "".join(parts)
