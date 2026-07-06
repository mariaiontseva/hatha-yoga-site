"""HYP home intro — replaced with the PI's (James Mallinson) 2026 copy:
past-tense project description, workshop paragraph removed. Keeps the
'Read the project proposal' link.
"""
from bs4 import BeautifulSoup

P1 = ("The Haṭha Yoga Project was a research project funded by the European "
      "Research Council which was hosted by SOAS University of London and ran "
      "from 2015 to 2020. Its primary aim was to chart the history of physical "
      "yoga practice by means of philology, i.e. the study of texts on yoga, "
      "and ethnography, i.e. fieldwork among practitioners of yoga. The project "
      "team consisted of four researchers based at SOAS and two at the École "
      "française d’Extrême Orient, Pondicherry.")
P2 = ("The project’s primary outputs are critical editions and annotated "
      "translations of ten Sanskrit texts on haṭha yoga and a range of "
      "monographs, journal articles, book chapters and encyclopedia entries.")

DROP = ("is a five-year", "primary outputs will be", "Latest site update")


def restructure(html):
    soup = BeautifulSoup(html, "lxml")
    root = soup.body or soup
    for p in root.find_all("p"):
        t = p.get_text(" ", strip=True)
        if any(d in t for d in DROP):
            p.decompose()
    h = root.find(["h1", "h2"])
    p1 = soup.new_tag("p"); p1.string = P1
    p2 = soup.new_tag("p"); p2.string = P2
    if h:
        h.insert_after(p1)
        p1.insert_after(p2)
    else:
        root.insert(0, p2); root.insert(0, p1)
    return "".join(str(c) for c in root.contents).strip()
