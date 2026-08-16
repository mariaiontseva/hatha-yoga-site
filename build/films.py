"""The Films page — YouTube videos curated by the PI (email 'YouTube videos',
4 Aug 2026).

The project's own Haṭhābhyāsapaddhati film was here too, uploaded 5 Aug 2026
to youtube.com/@lightonhathayoga (a Brand Account, so ownership can be handed
on later), but it came off the site on 14 Aug at the PI's request — see
WITHHELD below.

Display titles were editorially normalised from the real YouTube titles
(fetched via oEmbed 4 Aug 2026); every id was verified alive that day.
Cards are click-to-play: films.js swaps the thumbnail for a youtube-nocookie
embed on click, so no YouTube cookies land before the visitor chooses to
play. Without JS the card is a plain link to youtube.com.

Item = (youtube_id_or_None, title, source). id=None -> 'Coming soon' card.

Known gaps, reported to MI 4 Aug 2026: five links in the PI's email arrived
corrupted (encoding ate characters after '?v') and one id (r9rl5gM9S8o) is
dead/private — the PI may want to resend those; 'Part 2' of Keen on Yoga's
Haṭhapradīpikā interview is here, Part 1 is likely among the corrupted ones.
"""

CHANNEL = ("SOAS Centre of Yoga Studies",
           "https://www.youtube.com/@soascentreofyogastudies6694")

# Off the site since 14 Aug 2026, at the PI's request ("Please take the
# Haṭhābhyāsapaddhati films off the website. It may only be temporary."), after
# Jason Birch reported that the files are unedited footage. Kept here rather
# than deleted: to put the film back, move this entry into SECTIONS, where it
# belongs after "The Haṭha Yoga Project".
#
# Uploaded to the project's own channel (youtube.com/@lightonhathayoga) on
# 5 Aug 2026, unlisted. Part 6 is missing, hence the jump from 5 to 7 — the
# original numbering is kept.
WITHHELD = ("The Haṭhābhyāsapaddhati Film", [
    ("DnEp-4FRaqo", "1. Introduction", "The Haṭha Yoga Project"),
    ("kfTLG3SZiRI", "2. Supine Poses", "The Haṭha Yoga Project"),
    ("MCRBO7T4YvU", "3. Prone Poses", "The Haṭha Yoga Project"),
    ("0y4WAkw51Cs", "4. Stationary Poses", "The Haṭha Yoga Project"),
    ("_tBcQv-4etQ", "5. Standing Poses", "The Haṭha Yoga Project"),
    ("Zh4iZrTlCew", "7. Piercing Poses", "The Haṭha Yoga Project"),
])

SECTIONS = [
    ("The Haṭha Yoga Project", [
        # "final" dropped — it was filmed near the start of the project,
        # but it is still the symposium (PI, 6 Aug 2026)
        ("6PWk-ZywGis",
         "The Haṭha Yoga Project: Symposium",
         "SOAS University of London"),
        ("GenKUMqRfqc",
         "The Haṭha Yoga Project at the British Museum",
         "Dr Jason Birch"),
    ]),
    ("Roots of Yoga", [
        ("_3hPjoPXA6Y",
         "James Mallinson and Mark Singleton in Conversation",
         "The New York Society Library"),
        ("_3jYJWmHwr8",
         "Roots of Yoga at the Jaipur Literature Festival (excerpts)",
         "Jaipur Literature Festival"),
        ("oJTrTNoyLHM", "Roots of Yoga", "lecture"),
        ("1W-uZUAQqOk", "The Reading of Roots of Haṭha Yoga", "ERCcOMICS"),
    ]),
    ("James Mallinson", [
        ("wl_ZXBMpKXU",
         "From Tapas to Hard Yoga: The History of the Āsanas of Haṭha Yoga",
         "Smithsonian Museum"),
        ("oz3napMhU0c", "Tantra’s Influence on Yoga", "The British Museum"),
        ("hFWj-geACgU", "Haṭha Yoga: An Illustrated History",
         "Loyola Marymount University"),
        ("eUD2ni2U890", "Tantric Traditions and Haṭhayoga", "Brown University"),
        ("w46keD8nS44", "A Very Brief History of Yoga",
         "Balliol College, Oxford"),
        ("9JEQtwPgj1g", "Haṭhayoga’s Tantric Buddhist Roots", "ELTE, Budapest"),
        ("wJo6YY-VdLk", "The Ascetic Roots of Yoga", "advaya"),
        ("mBb1u5S_vFE", "The History and Practices of Haṭha Yoga",
         "Wise Studies"),
        ("woAjrHT-Hx0", "Alchemy Reader: Untangling Traditions", "AyurYog"),
        ("wWGhnU579Ps", "The Origins of Yoga", "The Know Show"),
        ("APfR0UTDTbs", "Haṭha Yoga Traditions", "Somatic Primer Podcast"),
        ("1VJNrxL7pfM", "Haṭha Yoga Project Interview", "YogaLite"),
    ]),
    ("Jason Birch", [
        ("3nDUnvYA6Kw", "The Amaraugha: The Genesis of Haṭha and Rājayoga",
         "SOAS Centre of Yoga Studies"),
        ("hO2t0rFmhHA",
         "Āsanas of the Yogacintāmaṇi &amp; The Dattātreyayogaśāstra "
         "(with James Mallinson)",
         "SOAS Centre of Yoga Studies"),
        ("6lR2jJF-D2I", "The Dawn of Physical Yoga (with Giacomella Orofino)",
         "SOAS Centre of Yoga Studies"),
        ("8JH4nC-cGj4", "Yoga on the Eve of Colonialism", "Embodied Philosophy"),
        ("azyX_d2VfaE", "The Lineage of Immortals", "Embodied Philosophy"),
        ("h8yV7SFQISQ", "The Amaraughaprabodha: Haṭha and Rāja Yoga",
         "Buddhist Yoga"),
        ("jgzpD4nqgsk",
         "How Does the Practice of Physical Yoga Result in Liberation?",
         "university lecture"),
        ("QfRf8vMPgm8", "The Complex Āsanas of Mohanadās", "Yoga Vidya"),
        ("wfItonGTgw0", "The Haṭhapradīpikā, Part 2", "Keen on Yoga"),
        ("lr53OBNbX8o", "Manuscript Hunting and the History of Medieval Yogas",
         "Yogic Studies Podcast"),
    ]),
    ("Mark Singleton", [
        ("xyO2chklfdM",
         "Yoga As We Know It: The Development of the Physical Practices of Yoga",
         "advaya"),
        ("gAXiDm-okLY", "Yoga Body, 10 Years Later", "Yogic Studies Podcast"),
        ("UiRfEQ_MkEk", "On Yoga Body", "Embodied Philosophy"),
        ("WW83KlIFtRw", "Lecture at Brown University", "Brown University"),
        ("bImz0pP1D3s",
         "Vivekananda, Ling, Reich: Confluences of Modern Posture Practice",
         "Wise Studies"),
    ]),
    ("Daniela Bevilacqua", [
        ("mDdTkGx4gkE", "Yoga and Tapasyā in the Ascetic World",
         "SOAS Centre of Yoga Studies"),
        ("xmU4JW597ms", "Hindu Asceticism and Haṭha Yoga",
         "Yogic Studies Podcast"),
        ("UIifWTzC0RE", "Sādhus and Siddhis", "Keen on Yoga"),
        ("HmRK6_XE670", "Haṭha Yoga Project Interview", "Keen on Yoga"),
        ("CuYqBnyXNEI", "Haṭha Yoga Project Interview", "YogaLite"),
    ]),
    ("Further Viewing", [
        ("ct9bvUkOx9I", "A History of Yoga: Latest Research and Scholarship",
         "Yogacampus"),
        ("i_KDbsRuNO0",
         "Yoga and the Traditional Physical Practices of South Asia (workshop)",
         "SOAS"),
        ("6-PNG0u3ku8", "Elements and Chakras", "Heather Elton"),
    ]),
]

_PLAY = ('<svg viewBox="0 0 24 24" aria-hidden="true">'
         '<path d="M8 5v14l11-7z" fill="currentColor"/></svg>')


def _card(vid, title, source):
    src = f'<span class="ytcard-src">{source}</span>' if source else ""
    if vid:
        return (f'<a class="ytcard" href="https://www.youtube.com/watch?v={vid}"'
                f' data-yt="{vid}" target="_blank" rel="noopener">'
                f'<span class="ytcard-img">'
                f'<img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt=""'
                f' loading="lazy"><span class="ytcard-play">{_PLAY}</span></span>'
                f'<span class="ytcard-title">{title}</span>{src}</a>')
    return (f'<div class="ytcard ytcard-soon">'
            f'<span class="ytcard-img ytcard-blank">{_PLAY}'
            f'<span class="soon-badge">Coming soon</span></span>'
            f'<span class="ytcard-title">{title}</span>{src}</div>')


def page_html(podcasts_html=""):
    """Films, with podcasts on a second tab of the same page."""
    films = ['<p class="tab-lead">Talks, lectures and interviews by the '
             'project team, and the project’s own films.</p>']
    for heading, items in SECTIONS:
        cards = "".join(_card(*it) for it in items)
        films.append(f'<h2 class="galsec">{heading}</h2>'
                     f'<div class="ytgrid">{cards}</div>')
    films.append(f'<p>More recordings on the <a href="{CHANNEL[1]}">{CHANNEL[0]}'
                 f' YouTube channel</a>.</p>')

    if not podcasts_html:
        return "<h1>Films</h1>" + "".join(films)

    return (
        '<h1>Films &amp; Podcasts</h1>'
        '<div class="tabs" role="tablist" aria-label="Films and podcasts">'
        '  <button type="button" class="tab is-on" role="tab" id="tab-films"'
        '   aria-controls="panel-films" aria-selected="true">Films</button>'
        '  <button type="button" class="tab" role="tab" id="tab-podcasts"'
        '   aria-controls="panel-podcasts" aria-selected="false">Podcasts</button>'
        '</div>'
        '<section class="tabpanel is-on" id="panel-films" role="tabpanel"'
        ' aria-labelledby="tab-films">' + "".join(films) + '</section>'
        '<section class="tabpanel" id="panel-podcasts" role="tabpanel"'
        ' aria-labelledby="tab-podcasts" hidden>' + podcasts_html + '</section>')
