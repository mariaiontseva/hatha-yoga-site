"""Structure the libraries page: <b> headers + newline/<br>-separated
institution names -> clean <h3> subheadings + bulleted <ul> lists.
"""
import re
from html import escape
from bs4 import BeautifulSoup, NavigableString, Tag


def restructure(html):
    soup = BeautifulSoup(html, "lxml")
    root = soup.body or soup
    sections = []          # (header, [items])
    cur = None

    def add(text):
        if cur is None:
            return
        for ln in re.split(r"[\r\n]+", text):
            ln = ln.strip()
            if ln:
                cur[1].append(ln)

    for c in list(root.children):
        if isinstance(c, Tag) and c.name in ("b", "strong"):
            cur = (c.get_text(strip=True), [])
            sections.append(cur)
        elif isinstance(c, Tag) and c.name == "br":
            continue
        elif isinstance(c, NavigableString):
            add(str(c))
        elif isinstance(c, Tag):
            add(c.get_text("\n"))

    if not sections:
        return html
    out = []
    for header, items in sections:
        out.append(f"<h3>{escape(header)}</h3>")
        if items:
            lis = "".join(f"<li>{escape(i)}</li>" for i in items)
            out.append(f'<ul class="inst-list">{lis}</ul>')
    return "".join(out)
