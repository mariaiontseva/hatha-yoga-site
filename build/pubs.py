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

ACADEMIA = {
    "James Mallinson": "https://oxford.academia.edu/JamesMallinson",
    "Daniela Bevilacqua": "https://iscte-iul.academia.edu/DanielaBevilacqua",
}


def _academia_note(name):
    url = ACADEMIA[name]
    return (f'<p class="pub-academia">Other publications by {name} are available on '
            f'<a href="{url}">academia.edu</a>.</p>')


def _remove_proposed_outputs(soup):
    """Per the PI: drop the 'Proposed Project Outputs' block (kept only to
    fill the page early on) — everything from that heading up to the team
    publications heading."""
    root = soup.body or soup
    kids = [c for c in root.children if getattr(c, "name", None)]
    start = end = None
    for i, el in enumerate(kids):
        t = el.get_text(" ", strip=True).upper()
        if el.name in ("h1", "h2", "h3"):
            if start is None and "PROPOSED PROJECT OUTPUTS" in t:
                start = i
            elif start is not None and "PREVIOUS PUBLICATIONS" in t:
                end = i
                break
    if start is not None:
        for el in kids[start:(end if end is not None else len(kids))]:
            el.decompose()


def _rename_heading(soup):
    """Per the PI (July 2026): the page heading is 'Project Publications'.
    MUST run AFTER _remove_proposed_outputs — that function finds the end of
    the block it deletes by matching the old text 'PREVIOUS PUBLICATIONS';
    renaming first would silently break the deletion."""
    for el in soup.find_all(["h1", "h2", "h3"]):
        if "PREVIOUS PUBLICATIONS" in el.get_text(" ", strip=True).upper():
            el.clear()
            el.string = "Project Publications"
            break


def restructure(content_html):
    soup = BeautifulSoup(content_html, "lxml")

    _remove_proposed_outputs(soup)
    _rename_heading(soup)

    # Jim: keep ONLY his HYP publications — replace the old bibliography table
    # with a fresh HYP-only section + an academia.edu note.
    mtable = next((t for t in soup.find_all("table")
                   if "DR JAMES MALLINSON" in t.get_text(" ", strip=True).upper()), None)
    if mtable:
        jim = BeautifulSoup(jimpubs.section_html(), "lxml").find("table")
        note = BeautifulSoup(_academia_note("James Mallinson"), "lxml").find("p")
        mtable.replace_with(jim)
        jim.insert_after(note)

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
            dnote = BeautifulSoup(_academia_note("Daniela Bevilacqua"), "lxml").find("p")
            gtable.insert_after(new_table)
            new_table.insert_after(dnote)

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
