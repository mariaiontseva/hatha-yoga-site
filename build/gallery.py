"""Group runs of image-only links into a responsive thumbnail grid.

WordPress galleries flatten to a long vertical stack of `<a><img></a>` links.
This wraps each run of >=2 consecutive image-only anchors in
`<div class="gallery">` so CSS can render a clean thumbnail grid.
Single linked images are left as-is.
"""
from bs4 import BeautifulSoup, NavigableString, Tag


def _is_img_link(node):
    if not isinstance(node, Tag) or node.name != "a":
        return False
    kids = [c for c in node.children if isinstance(c, Tag)]
    return len(kids) == 1 and kids[0].name == "img" and node.get_text(strip=True) == ""


def wrap(content_html):
    soup = BeautifulSoup(content_html, "lxml")
    root = soup.body or soup
    nodes = [c for c in root.contents
             if isinstance(c, Tag) or (isinstance(c, NavigableString) and c.strip())]
    out, i, n = [], 0, len(nodes)
    while i < n:
        if _is_img_link(nodes[i]):
            run = []
            while i < n and _is_img_link(nodes[i]):
                run.append(nodes[i]); i += 1
            if len(run) >= 2:
                g = soup.new_tag("div", **{"class": "gallery"})
                for a in run:
                    g.append(a)
                out.append(g)
            else:
                out.extend(run)
        else:
            out.append(nodes[i]); i += 1
    for c in list(root.contents):
        c.extract()
    for node in out:
        root.append(node)
    return "".join(str(c) for c in root.contents).strip()


def index(content_html):
    """Gallery landing: pair each image-link with its following heading into a
    card grid (image + label, the whole card links to that field site)."""
    soup = BeautifulSoup(content_html, "lxml")
    root = soup.body or soup
    nodes = [c for c in root.children if isinstance(c, Tag)]
    out, cards, i, n = [], [], 0, len(nodes)

    def flush():
        if cards:
            g = soup.new_tag("div", **{"class": "galindex"})
            for c in cards:
                g.append(c)
            out.append(g)
            cards.clear()

    while i < n:
        el = nodes[i]
        if _is_img_link(el):
            href = el.get("href", "")
            img = el.find("img")
            label = ""
            if i + 1 < n and nodes[i + 1].name in ("h1", "h2", "h3"):
                label = nodes[i + 1].get_text(" ", strip=True); i += 1
            card = soup.new_tag("a", **{"class": "galcard", "href": href})
            wrap = soup.new_tag("span", **{"class": "galcard-img"})
            wrap.append(img); card.append(wrap)
            lab = soup.new_tag("span", **{"class": "galcard-label"})
            lab.string = label; card.append(lab)
            cards.append(card); i += 1
        else:
            flush(); out.append(el); i += 1
    flush()
    for c in list(root.contents):
        c.extract()
    for node in out:
        root.append(node)
    return "".join(str(c) for c in root.contents).strip()


def book(content_html):
    """Book page (roots of yoga): float the portrait cover, give the stacked
    top headings a real hierarchy (title / byline / lead), style ORDER as a
    button."""
    soup = BeautifulSoup(content_html, "lxml")
    root = soup.body or soup
    img = root.find("img")
    if img:
        img["class"] = img.get("class", []) + ["book-cover"]
    # give the stacked top headings a real hierarchy: title / byline / lead
    hcount = 0
    lead_el = None
    for el in [c for c in root.children if isinstance(c, Tag)]:
        if el.name == "p":
            break                                   # reached the body copy
        if el.name in ("h1", "h2", "h3"):
            if hcount == 0:
                inner = el.find_all(["h1", "h2", "h3"])   # the nested title + byline
                title = inner[0].get_text(" ", strip=True) if inner else el.get_text(" ", strip=True)
                byline = inner[1].get_text(" ", strip=True) if len(inner) > 1 else ""
                nt = soup.new_tag("h1", **{"class": "book-title"}); nt.string = title
                el.replace_with(nt)
                if byline:
                    p = soup.new_tag("p", **{"class": "book-byline"}); p.string = byline
                    nt.insert_after(p)
            else:
                el.name = "p"; el["class"] = ["book-lead"]
                st = el.find("strong")
                if st:
                    st.unwrap()
                lead_el = el
            hcount += 1
    order = None
    for a in root.find_all("a"):
        if a.get_text(strip=True).upper() in ("ORDER", "ORDER NOW", "BUY"):
            a["class"] = a.get("class", []) + ["btn"]
            order = a
    # float just the cover top-left; put the ORDER button under the lead line
    if img is not None:
        aside = soup.new_tag("div", **{"class": "book-aside"})
        img.insert_before(aside)
        aside.append(img)
    if order is not None and lead_el is not None:
        lead_el.insert_after(order)
    return "".join(str(c) for c in root.contents).strip()
