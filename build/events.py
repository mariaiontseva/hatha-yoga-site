"""HYP events — everything is now past, so the 'Upcoming Events' / 'Past
Events' section headings are removed (events kept as one list). The stray
'Latest site update …' banner line is dropped too.

The 2019 entries were written before the events happened; PI asked (Aug 2026)
for past tense throughout. TENSE maps the exact phrases used on the page —
longest first, so specific fixes (incl. the 'is presentation' typo) win over
the generic ones.
"""
from bs4 import BeautifulSoup

DROP_HEAD = {"upcoming events", "past events"}

TENSE = [
    ("is presentation the paper", "presented the paper"),   # also fixes the typo
    ("have a lecture series", "held a lecture series"),
    ("will be holding", "held"),
    ("will be at", "were at"),
    ("is presenting", "presented"),
    ("are holding", "held"),
    ("is holding", "held"),
    ("are hosting", "hosted"),
    ("is hosting", "hosted"),
]


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
    out = "".join(str(c) for c in root.contents).strip()
    for old, new in TENSE:
        out = out.replace(old, new)
    return out
