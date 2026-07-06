"""Editorial bio overrides for the HYP team page (supplied by the PI).
Keyed by an uppercase name substring; teams.restructure applies them.
"""

ROUTLEDGE = ("https://www.routledge.com/The-Khecarividya-of-Adinatha-A-Critical-"
             "Edition-and-Annotated-Translation/Mallinson/p/book/9780415391153")
CLAY = "http://www.claysanskritlibrary.org"
YOGAVIDYA = "http://yogavidya.com"
BBC = "http://www.bbc.co.uk/programmes/b06b4qmq"
SI = "http://www.si.edu/exhibitions/details/yoga-the-art-of-transformation-4911"
ACADEMIA = "https://soas.academia.edu/JamesMallinson"

MALLINSON_BIO = f"""
<p>James (Jim) Mallinson is the Boden Professor of Sanskrit at the University of
Oxford. From 2013–2023 he worked at SOAS University of London where from
2015–2020 he was the Principal Investigator of the Hatha Yoga Project. Professor
Mallinson has a BA in Sanskrit and Old Iranian from the University of Oxford
(1991), an MA in South Asian Area Studies (with ethnography as its primary
subject) from SOAS (1993) and a DPhil. from the University of Oxford (2001). His
doctoral thesis was a critical edition of the Khecarīvidyā, an early text on
haṭha yoga, and was supervised by Professor Alexis Sanderson. A
<a href="{ROUTLEDGE}">revised version of the thesis</a> was published by Routledge
in 2007.</p>
<p>After completing his doctoral studies Professor Mallinson worked as a
principal translator for the <a href="{CLAY}">Clay Sanskrit Library</a>, for
which he produced five volumes of translations of Sanskrit poetry. He has also
published translations of two haṭha yoga texts, the Gheraṇḍa Saṃhitā (2004) and
Śivasaṃhitā (2007) for <a href="{YOGAVIDYA}">YogaVidya.com</a>. In addition to
these books Dr Mallinson has published numerous articles, book chapters and
encyclopedia articles. Roots of Yoga, a reader of translations of texts on yoga
introduced and edited by Professor Mallinson and Dr Mark Singleton was published
in the Penguin Classics series in January 2017.</p>
<p>Professor Mallinson’s primary research method is philology, in particular the
study of manuscripts of Sanskrit texts on yoga, which he complements with
ethnographic data drawn from extensive fieldwork with Indian ascetics and the
study of art historical sources. In recognition of his long association with the
Rāmānandī Indian ascetic saṃpradāya, in 2013 the order honoured him with the
title of mahant, an event recorded in the Smithsonian Channel’s television
documentary <a href="{BBC}">West Meets East</a>. His work on art historical
depictions of yogis led to his being invited to be a consultant and catalogue
author for the 2013 exhibition ‘<a href="{SI}">Yoga: The Art of Transformation</a>’
at the Smithsonian Institute in Washington D.C.</p>
<p>Many of Professor Mallinson’s publications may be downloaded from
<a href="{ACADEMIA}">here</a>.</p>
"""

OVERRIDES = {
    "JAMES MALLINSON": {
        "name": "Professor James Mallinson",
        "role": "Principal Investigator",
        "bio_html": MALLINSON_BIO,
    },
}
