"""Tag bibliography-style tables on the publications page.

A table whose first column is mostly years (or blank) is a citation list, not
tabular data — mark it `.pub-list` so CSS can render it as a clean bibliography
(year label + flowing citation) instead of a boxed grid.
"""
import re
from bs4 import BeautifulSoup
import jimpubs

YEAR = re.compile(r"^\d{3,4}\b")


def restructure(content_html):
    soup = BeautifulSoup(content_html, "lxml")
    # inject Jim's HYP publications (with links) above the 'previous publications'
    # lists — nothing existing is removed
    anchor = next((h for h in soup.find_all(["h1", "h2", "h3"])
                   if "PREVIOUS PUBLICATIONS" in h.get_text(" ", strip=True).upper()), None)
    jim = BeautifulSoup(jimpubs.block(), "lxml")
    jim_nodes = list((jim.body or jim).contents)
    if anchor:
        for node in jim_nodes:
            anchor.insert_before(node)
    else:
        root0 = soup.body or soup
        for node in reversed(jim_nodes):
            root0.insert(0, node)
    for t in soup.find_all("table"):
        rows = t.find_all("tr")
        yearish = total = 0
        for r in rows:
            cells = r.find_all(["td", "th"])
            if not cells:
                continue
            total += 1
            c0 = cells[0].get_text(strip=True)
            if c0 == "" or YEAR.match(c0):
                yearish += 1
        if total and yearish / total >= 0.5:
            t["class"] = t.get("class", []) + ["pub-list"]
            # header rows (empty first <th> + a name/section <th>) -> span to the
            # left edge like the year column, instead of sitting in column 2
            for r in rows:
                cells = r.find_all(["td", "th"])
                if (len(cells) >= 2 and cells[0].name == "th"
                        and cells[0].get_text(strip=True) == ""
                        and cells[-1].name == "th" and cells[-1].get_text(strip=True)):
                    for extra in cells[:-1]:
                        extra.decompose()
                    cells[-1]["colspan"] = str(len(cells))
                    cells[-1]["class"] = cells[-1].get("class", []) + ["pub-head"]
    root = soup.body or soup
    return "".join(str(c) for c in root.contents).strip()
