"""Tag bibliography-style tables on the publications page.

A table whose first column is mostly years (or blank) is a citation list, not
tabular data — mark it `.pub-list` so CSS can render it as a clean bibliography
(year label + flowing citation) instead of a boxed grid.
"""
import re
from bs4 import BeautifulSoup
import jimpubs
import danielapubs

YEAR = re.compile(r"^\d{3,4}\b")


def _insert_rows_after(head_row, rows_html):
    frag = BeautifulSoup("<table>" + rows_html + "</table>", "lxml")
    for r in reversed(frag.find_all("tr")):
        head_row.insert_after(r)


def restructure(content_html):
    soup = BeautifulSoup(content_html, "lxml")
    # MERGE Jim's new HYP publications INTO his existing 'DR JAMES MALLINSON'
    # table (newest first) — no separate/duplicate section, nothing removed
    mtable = next((t for t in soup.find_all("table")
                   if "DR JAMES MALLINSON" in t.get_text(" ", strip=True).upper()), None)
    if mtable:
        rows = mtable.find_all("tr")

        def subhead(keyword):
            for r in rows:
                cells = r.find_all(["td", "th"])
                if cells and cells[-1].get_text(strip=True).upper().startswith(keyword):
                    return r
            return None

        bh = subhead("BOOKS")
        ah = subhead("ARTICLES")
        if bh:
            _insert_rows_after(bh, jimpubs.book_rows())
        if ah:
            _insert_rows_after(ah, jimpubs.article_rows())

    # ADD Daniela Bevilacqua's publications as a NEW section — she has no
    # existing PERSONAL bibliography table (her surname appears only as an
    # author credit in the shared Monographs table, which must not count),
    # so this is an addition, not a merge — placed right after the last
    # personal table (Gupta's) in the team list.
    def _is_personal_header_table(t, name):
        first = t.find("tr")
        if not first:
            return False
        cells = first.find_all(["td", "th"])
        return (len(cells) >= 2 and cells[0].get_text(strip=True) == ""
                and name in cells[-1].get_text(strip=True).upper())

    if not any(_is_personal_header_table(t, "BEVILACQUA") for t in soup.find_all("table")):
        gtable = next((t for t in soup.find_all("table")
                      if _is_personal_header_table(t, "GUPTA")), None)
        if gtable:
            new_table = BeautifulSoup(danielapubs.section_html(), "lxml").find("table")
            gtable.insert_after(new_table)

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
            for r in rows:
                cells = r.find_all(["td", "th"])
                if len(cells) < 2:
                    continue
                c0 = cells[0].get_text(strip=True)
                c1 = cells[-1].get_text(" ", strip=True)
                # person header row (empty first <th> + a name <th>) -> span to
                # the left edge like the year column, instead of sitting in col 2
                if (cells[0].name == "th" and c0 == ""
                        and cells[-1].name == "th" and c1):
                    for extra in cells[:-1]:
                        extra.decompose()
                    cells[-1]["colspan"] = str(len(cells))
                    cells[-1]["class"] = cells[-1].get("class", []) + ["pub-head"]
                # section sub-heading (BOOK / ARTICLES / VOLUME …): empty year +
                # a short all-caps label -> ONE shared style via .pub-sub (no
                # reliance on inline <strong> scattered through the content)
                elif (c0 == "" and c1 and len(c1) <= 44
                        and c1 == c1.upper() and not YEAR.match(c1)):
                    cells[-1]["class"] = cells[-1].get("class", []) + ["pub-sub"]
                    st = cells[-1].find("strong")   # drop now-redundant inline bold
                    if st:
                        st.unwrap()
    root = soup.body or soup
    return "".join(str(c) for c in root.contents).strip()
