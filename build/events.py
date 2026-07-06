"""HYP events — everything is now past, so the 'Upcoming Events' / 'Past
Events' section headings are removed (events kept as one list). The stray
'Latest site update …' banner line is dropped too.
"""
from bs4 import BeautifulSoup

DROP_HEAD = {"upcoming events", "past events"}


def restructure(html):
    soup = BeautifulSoup(html, "lxml")
    root = soup.body or soup
    for el in root.find_all(["h1", "h2", "h3", "p"]):
        t = el.get_text(" ", strip=True)
        if t.lower() in DROP_HEAD:
            el.decompose()
        elif el.name in ("h1", "h2", "h3") and t == "":
            el.decompose()
        elif "Latest site update" in t:
            el.decompose()
    return "".join(str(c) for c in root.contents).strip()
