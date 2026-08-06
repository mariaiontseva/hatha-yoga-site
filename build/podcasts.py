"""Podcast appearances by the project team — build-time data.

Gathered 6 Aug 2026 in answer to the PI's question ("do you think Claude will
be able to scrape them up?"). Every URL was fetched and confirmed to resolve
at that date. Audio podcasts only: lectures and conference recordings that
happen to sit on YouTube belong in build/films.py, not here.

Grouped by person, newest first — the same shape as the publications page.
The list runs past the end of the grant (2015–2020) on purpose: the books
came out years later, and most of these episodes are about that work.

Deliberately excluded:
- two paragliding interviews with Jim (Cloudbase Mayhem 2023, The 831 2021):
  not about the project (PI's call, Aug 2026)
- Mark Singleton on Lonely Guru Yoga Dialogues (2013): the host's site is
  gone, the episode survives only in the Wayback Machine
- Gupta: no podcast appearances found

Entry = (year, date, show, title, url, note). `note` carries a language tag
where the episode is not in English, otherwise "".
"""

PEOPLE = [
    ("Professor James Mallinson", [
        ("2025", "30 October 2025", "The Ancients",
         "Origins of Yoga",
         "https://shows.acast.com/the-ancients/episodes/origins-of-yoga", ""),
        ("2024", "27 November 2024", "New Books Network",
         "The Dattātreyayogaśāstra",
         "https://newbooksnetwork.com/the-dattatreyayogasastra", ""),
        ("2023", "20 December 2023", "Somatic Primer",
         "Living with the Sadhus",
         "https://www.buzzsprout.com/1927632/episodes/14179831-james-mallinson-living-with-the-sadhus", ""),
        ("2022", "11 December 2022", "Yogic Studies",
         "Dattātreya’s Discourse on Yoga",
         "https://podcast.yogicstudies.com/1046752/episodes/11790405-37-james-mallinson-dattatreya-s-discourse-on-yoga", ""),
        ("2022", "16 November 2022", "New Books Network",
         "The Amṛtasiddhi and Amṛtasiddhimūla (with Péter-Dániel Szántó)",
         "https://podcasts.apple.com/gb/podcast/james-mallinson-and-p%C3%A9ter-d%C3%A1niel-sz%C3%A1nt%C3%B3-the/id426502373?i=1000586401391", ""),
        ("2022", "20 September 2022", "Keen on Yoga",
         "The Origins of Hatha Yoga",
         "https://www.keenonyoga.com/podcast/james-mallinson-2/", ""),
        ("2022", "28 January 2022", "Keen on Yoga",
         "Medieval Hatha Yoga",
         "https://www.keenonyoga.com/podcast/james-mallinson/", ""),
        ("2022", "26 January 2022", "SOAS Radio",
         "Understanding Yoga Studies, 1: Indology",
         "https://soundcloud.com/soasradio/centre-for-yoga-studies-episode-1-interview-with-james-mallinson", ""),
        ("2021", "14 October 2021", "Yogic Studies",
         "The Source Texts of Haṭha Yoga",
         "https://podcast.yogicstudies.com/1046752/episodes/9369341-27-james-mallinson-the-source-texts-of-ha-ha-yoga", ""),
        ("2021", "23 June 2021", "Age Less / Live More",
         "Exploring the Haṭhapradīpikā",
         "https://yogatalkshow.libsyn.com/469-exploring-the-hathapradipika-with-dr-jim-mallinson", ""),
        ("2020", "14 June 2020", "Yogic Studies",
         "The History and Practice of Haṭha Yoga",
         "https://podcast.yogicstudies.com/1046752/episodes/4152494-5-james-mallinson-the-history-and-practice-of-ha-ha-yoga", ""),
        ("2020", "2 May 2020", "Jaipur Literature Festival",
         "Yoga in a Time of Crisis",
         "https://podcasts.apple.com/gb/podcast/yoga-in-a-time-of-crisis-james-mallinson/id1511301485?i=1000473600542", ""),
        ("2019", "6 May 2019", "J. Brown Yoga Talks",
         "Uncovering Yoga’s Ancestral Past",
         "https://www.jbrownyoga.com/yoga-talks-podcast/2019/5/james-mallinson", ""),
        ("2017", "18 August 2017", "Embodied Philosophy",
         "Hatha Yoga History, Philology and the Khecarīvidyā",
         "https://podcasts.apple.com/gb/podcast/james-mallinson-on-hatha-yoga-history-philology-and/id1046733414?i=1000398547509", ""),
        ("2014", "10 February 2014", "BBC Radio 4, Beyond Belief",
         "Yoga",
         "https://podcasts.apple.com/gb/podcast/yoga/id261779770?i=1000253293141", ""),
    ]),
    ("Dr Jason Birch", [
        ("2025", "26 January 2025", "Keen on Yoga",
         "Āsanas of the Yogacintāmaṇi",
         "https://www.keenonyoga.com/podcast/jason-birch-2/", ""),
        ("2024", "9 June 2024", "Embodied Philosophy",
         "The Lineage of Immortals",
         "https://www.embodiedphilosophy.com/the-lineage-of-immortals-with-jason-birch-172/", ""),
        ("2024", "8 May 2024", "Ancient Futures",
         "Becoming Immortal",
         "https://ancientfutures.substack.com/p/jason-birch", ""),
        ("2023", "6 November 2023", "Somatic Primer",
         "Light on Hatha Yoga",
         "https://www.buzzsprout.com/1927632/episodes/13918165-jason-birch-light-on-hatha-yoga", ""),
        ("2022", "29 June 2022", "Keen on Yoga",
         "The Haṭhapradīpikā",
         "https://www.keenonyoga.com/podcast/jason-birch/", ""),
        ("2022", "3 March 2022", "SOAS Radio",
         "Understanding Yoga Studies, 2",
         "https://soundcloud.com/soasradio/understanding-yoga-studies-episode-2-jason-birch", ""),
        ("2020", "26 July 2020", "Yogic Studies",
         "Manuscript Hunting and the History of Medieval Yogas",
         "https://podcast.yogicstudies.com/1046752/episodes/4691279-9-jason-birch-manuscript-hunting-and-the-history-of-medieval-yogas", ""),
        ("2018", "25 May 2018", "Hacking the Self",
         "Revisiting Yoga Philosophy",
         "https://www.sahajasoma.com/hacking-the-self-podcast/jason-birch", ""),
    ]),
    ("Dr Mark Singleton", [
        ("2026", "13 July 2026", "Yogic Studies",
         "Yoga Machine: Technology, Transhumanism and Transcendence",
         "https://podcast.yogicstudies.com/1046752/episodes/19459842-56-mark-singleton-yoga-machine-technology-transhumanism-and-transcendence", ""),
        ("2024", "9 July 2024", "Spirit Almanac",
         "El cuerpo de Yoga",
         "https://podcasts.apple.com/us/podcast/el-cuerpo-de-yoga-con-el-dr-mark-singleton/id1657379393?i=1000661621146",
         "in Spanish"),
        ("2020", "11 December 2020", "Yogic Studies",
         "Yoga Body, Ten Years Later",
         "https://podcast.yogicstudies.com/1046752/episodes/6792961-15-mark-singleton-yoga-body-10-years-later", ""),
        ("2018", "2 February 2018", "Embodied Philosophy",
         "Mark Singleton on Yoga Body",
         "https://www.embodiedphilosophy.com/mark-singleton-on-yoga-body-66/", ""),
    ]),
    ("Dr Daniela Bevilacqua", [
        ("2024", "29 December 2024", "Keen on Yoga",
         "Sādhus’ Understanding of Embodied Practices",
         "https://www.keenonyoga.com/podcast/daniela-bevilacqua-2/", ""),
        ("2024", "20 November 2024", "Yogic Studies",
         "From Tapas to Modern Yoga",
         "https://podcast.yogicstudies.com/1046752/episodes/16061197-49-daniela-bevilacqua-from-tapas-to-modern-yoga", ""),
        ("2024", "24 October 2024", "New Books Network",
         "From Tapas to Modern Yoga",
         "https://newbooksnetwork.com/from-tapas-to-modern-yoga", ""),
        ("2024", "2 June 2024", "Keen on Yoga",
         "Hatha Yoga, Tapas and Sādhus",
         "https://www.keenonyoga.com/podcast/daniela-bevilacqua/", ""),
        ("2023", "27 April 2023", "Ricercati",
         "Gli hindu e la comunità LGBT",
         "https://podcasts.apple.com/it/podcast/gli-hindu-e-la-comunit%C3%A0-lgbt/id1611577382?i=1000610832061",
         "in Italian"),
        ("2022", "19 October 2022", "Wise Studies",
         "Hindu Asceticism",
         "https://podcasts.apple.com/us/podcast/hindu-asceticism-with-daniela-bevilacqua/id1516104205?i=1000583200311", ""),
        ("2022", "28 April 2022", "SOAS Radio",
         "Understanding Yoga Studies, 4",
         "https://soundcloud.com/soasradio/cys4-daniela", ""),
        ("2020", "17 May 2020", "Yogic Studies",
         "Hindu Asceticism and Haṭha Yoga",
         "https://podcast.yogicstudies.com/1046752/episodes/3757892", ""),
    ]),
]


def panel_html():
    """The podcasts tab of the Films page."""
    total = sum(len(items) for _, items in PEOPLE)
    out = [f'<p class="tab-lead">{total} conversations with members of the '
           "project, from 2014 to the present. Each links out to the "
           "episode.</p>"]
    for name, items in PEOPLE:
        rows = []
        for year, date, show, title, url, note in items:
            tail = f' <span class="pod-note">({note})</span>' if note else ""
            rows.append(
                f'<tr><td>{year}</td><td><a href="{url}">{title}</a>'
                f'<span class="pod-show">{show} · {date}</span>{tail}</td></tr>')
        out.append('<table class="pub-list pod-list">'
                   f'<tr><th class="pub-head" colspan="2">{name}</th></tr>'
                   + "".join(rows) + "</table>")
    return "".join(out)
