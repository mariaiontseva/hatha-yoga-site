"""Contact page: the WordPress contact form can't work on a static site (it is
stripped as a <form>). Replace the dangling 'form below' promise with a clean
contact block — a link to the project team + affiliations.
"""
import re

TEAM_LINK = ('<p class="contact-lead">'
             '<a href="{{ROOT}}hyp/team/">Contact the project team →</a></p>')
AFFIL = ('<p class="contact-affil">SOAS, University of London'
         ' · University of Oxford · Universität Marburg</p>')


def restructure(html):
    # drop the reference to the (now absent) form
    html = re.sub(r"\s*please contact us using the form below\.?",
                  " please get in touch.", html, flags=re.I)
    return html.rstrip() + TEAM_LINK + AFFIL
