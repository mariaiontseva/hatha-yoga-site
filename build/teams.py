"""Restructure a team page's flat content into uniform member cards.

restructure(content_html, site) -> html

Each member becomes:
  <article class="member">
    <img class="member-photo" ...>            (optional)
    <div class="member-body">
      <h3 class="member-name">Name</h3>
      <p class="member-role">Role</p>          (optional)
      ...bio nodes...
    </div>
  </article>

Section headings (PROJECT MEMBERS, ADVISORY PANEL, ...) and non-member content
pass through untouched. HYP order is img→name→bio; HP order is name→role→img→bio.
"""
import re
from bs4 import BeautifulSoup, NavigableString, Tag

HEADINGS = {"h1", "h2", "h3", "h4"}


def _split_name_role(text):
    text = re.sub(r"\s+", " ", text).strip()
    m = re.match(r"^(.*?)\s*\(([^)]*)\)\s*$", text)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return text, ""


def _els(node):
    """Top-level nodes, keeping tags and non-blank strings."""
    out = []
    for c in node.contents:
        if isinstance(c, Tag):
            out.append(c)
        elif isinstance(c, NavigableString) and c.strip():
            out.append(c)
    return out


def _card(soup, photo, name, role, bio):
    art = soup.new_tag("article", **{"class": "member"})
    if photo is not None:
        photo["class"] = "member-photo"
        art.append(photo)
    body = soup.new_tag("div", **{"class": "member-body"})
    if name:
        h = soup.new_tag("h3", **{"class": "member-name"})
        h.string = name
        body.append(h)
    if role:
        r = soup.new_tag("p", **{"class": "member-role"})
        r.string = role
        body.append(r)
    for b in bio:
        body.append(b)
    art.append(body)
    return art


def _build_hyp(soup, nodes):
    out = []
    i, n = 0, len(nodes)
    while i < n:
        el = nodes[i]
        if isinstance(el, Tag) and el.name == "img":
            photo = el; i += 1
            name = role = ""
            # name heading (may be empty -> name comes from first bio paragraph)
            if i < n and isinstance(nodes[i], Tag) and nodes[i].name in HEADINGS:
                txt = nodes[i].get_text(" ", strip=True)
                if txt:
                    name, role = _split_name_role(txt)
                i += 1
            bio = []
            while i < n:
                nn = nodes[i]
                if isinstance(nn, Tag) and (nn.name == "img" or nn.name in HEADINGS):
                    break
                if not name and isinstance(nn, Tag) and nn.name == "p":
                    name, role = _split_name_role(nn.get_text(" ", strip=True))
                    i += 1; continue
                bio.append(nn); i += 1
            out.append(_card(soup, photo, name, role, bio))
        else:
            out.append(el); i += 1
    return out


def _build_hp(soup, nodes):
    out = []
    i, n = 0, len(nodes)
    while i < n:
        el = nodes[i]
        # a member starts at a heading that is followed (soon) by an image
        if isinstance(el, Tag) and el.name in HEADINGS:
            name = el.get_text(" ", strip=True)
            j = i + 1
            role = ""
            if j < n and isinstance(nodes[j], Tag) and nodes[j].name == "p":
                ptxt = nodes[j].get_text(" ", strip=True)
                if len(ptxt) < 60:                      # short line = the role
                    role = ptxt.rstrip("."); j += 1
            photo = None
            if j < n and isinstance(nodes[j], Tag) and nodes[j].name == "img":
                photo = nodes[j]; j += 1
            if photo is None:                            # not a member card — pass through
                out.append(el); i += 1; continue
            bio = []
            while j < n and not (isinstance(nodes[j], Tag) and nodes[j].name in HEADINGS):
                bio.append(nodes[j]); j += 1
            out.append(_card(soup, photo, _split_name_role(name)[0],
                             role or _split_name_role(name)[1], bio))
            i = j
        else:
            out.append(el); i += 1
    return out


def restructure(content_html, site):
    soup = BeautifulSoup(content_html, "lxml")
    root = soup.body or soup
    nodes = _els(root)
    rebuilt = _build_hyp(soup, nodes) if site == "hyp" else _build_hp(soup, nodes)
    for c in list(root.contents):
        c.extract()
    for node in rebuilt:
        root.append(node)
    return "".join(str(c) for c in root.contents).strip()
