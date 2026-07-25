"""Editorial bio overrides for the HYP team page (supplied by the PI).
Keyed by an uppercase name substring; teams.restructure applies them.
"""

ROUTLEDGE = ("https://www.routledge.com/The-Khecarividya-of-Adinatha-A-Critical-"
             "Edition-and-Annotated-Translation/Mallinson/p/book/9780415391153")
CLAY = "http://www.claysanskritlibrary.org"
YOGAVIDYA = "http://yogavidya.com"
BBC = "http://www.bbc.co.uk/programmes/b06b4qmq"
SI = "http://www.si.edu/exhibitions/details/yoga-the-art-of-transformation-4911"
ACADEMIA = "https://oxford.academia.edu/JamesMallinson"

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

# Jason Birch's bio, supplied by him 25 Jul 2026 ('Jason Birch Biography
# July 2026.pages'); the photo (jason-birch-2026.jpg) arrived with the same
# email and lives in BOTH <site>/assets/img dirs so the override works on
# the HYP and HP team pages alike.
BIRCH_BIO = """
<p>Jason Birch (DPhil, Oxon) is an historian of South Asian traditions of yoga
and medicine. He is a Senior Research Associate at the University of Alberta, a
Research Associate at SOAS University of London, and an Honorary Associate of
the University of Sydney. Through extensive fieldwork in India and the
reconstruction of Sanskrit primary sources, Birch has revealed the early history
of Rājayoga, the supreme yoga of meditation, as well as its physical
counterpart, Haṭhayoga (the yoga of force). His research has also identified a
corpus of Sanskrit and vernacular texts that emerged during Haṭhayoga’s
<i>floruit</i>, the period in which physical yoga flourished on the eve of
colonialism.</p>
<p>His published work on the history of medicine includes the 2018 publication
<i>Premodern Yoga Traditions and Ayurveda: Preliminary Remarks on Shared
Terminology, Theory and Praxis</i>
(DOI: <a href="https://doi.org/10.18732/hssa.v6i0.25">10.18732/hssa.v6i0.25</a>),
and his co-authorship of the 2023 project book <i>On the Plastic Surgery of the
Ears and Nose: The Nepalese Version of the Suśrutasaṃhitā</i>
(DOI: <a href="https://doi.org/10.11588/hasp.1203">10.11588/hasp.1203</a>). In
addition to other publications arising from the Suśruta Project, he wrote the
chapter “Yoga and Ayurvedic Medicine” for the Comparative Guts project
(book DOI: <a href="https://doi.org/10.38071/2024-00345-3">10.38071/2024-00345-3</a>,
and website). He is a major contributor to the continuing work of editing and
translating the Nepalese version of the <i>Suśrutasaṃhitā</i>, and is preparing
a monograph on the concept of wellbeing (<i>svāsthya</i>) in early Ayurveda.</p>
<p>Among Birch’s major book publications on the history of yoga are <i>A Manual
on the Practice of Haṭhayoga: An Edition and Translation of the Pune Manuscript
of the Haṭhābhyāsapaddhati</i> (with Mark Singleton and James Mallinson),
<i>Āsanas of the Yogacintāmaṇi: The Largest Premodern Compilation on Postural
Practice</i>, and <i>The Amaraugha and Amaraughaprabodha of Gorakṣanātha: The
Genesis of Haṭha and Rājayoga</i>. He is also a co-author of the
<a href="{{ROOT}}hp/reader/">digital critical edition of the Haṭhapradīpikā</a>,
one of the main outputs of the Light on Haṭha Project.</p>
<p>Jason Birch received his bachelor’s degree in Sanskrit and Hindi from the
University of Sydney. He was awarded a Clarendon Scholarship to pursue doctoral
studies at Balliol College, Oxford, under Alexis Sanderson. He completed his
DPhil in 2013. In 2014, he was a Research Fellow at the Oxford Centre for Hindu
Studies, and in 2015 he joined AyurYog, an ERC-funded Project at the University
of Vienna. Later that year he joined the five-year Haṭha Yoga Project at SOAS
University of London, where he translated and edited Sanskrit texts on Haṭha
and Rājayoga. He is a founding member of SOAS’s Centre for Yoga Studies and of
the diamond open-access Journal of Yoga Studies.</p>
"""

OVERRIDES = {
    "JAMES MALLINSON": {
        "name": "PROFESSOR JAMES MALLINSON",
        "role": "Principal Investigator",
        "bio_html": MALLINSON_BIO,
    },
    "JASON BIRCH": {
        "name": "DR JASON BIRCH",
        "role": "Post-Doctoral Researcher",
        "bio_html": BIRCH_BIO,
        "photo": "jason-birch-2026.jpg",
    },
}
