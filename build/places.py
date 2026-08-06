"""Field sites on the map (Gallery) — coordinates + per-photo metadata.

Coordinates were geocoded via OpenStreetMap Nominatim, 5 Aug 2026; Panhalakaji
came from its Wikipedia entry (Nominatim has no record of the caves).

Per-photo data is read from the images themselves at build time: the EXIF of
the field photographs carries the camera and the exact date of the shoot
(Sony ILCE-7 for most of them, one Olympus E-M10), which is what dates the
expedition on the map. Their EXIF carries NO GPS — the A7 has no GPS module —
so a photograph inherits its site's coordinates unless it has its own.

To add a site: one entry below plus the photo folder. To place a photograph on
its own point (real clustering rather than one pin per site), give it a
`lat`/`lon` in PHOTO_COORDS, or upload photographs whose EXIF has GPS — the
build reads that automatically.
"""
import json
import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

SITES = [
    dict(slug="hampi", name="Hampi",
         region="Vijayanagara, Karnataka", lat=15.33580, lon=76.46102),
    dict(slug="dabhoi", name="Dabhoi",
         region="Vadodara, Gujarat", lat=22.13362, lon=73.42010),
    dict(slug="kadri", name="Kadri",
         region="Mangaluru, Karnataka", lat=12.88589, lon=74.85560),
    dict(slug="panhale-kaji", name="Panhale Kaji",
         region="Ratnagiri, Maharashtra", lat=17.64568, lon=73.24507),
    dict(slug="shringeri", name="Shringeri",
         region="Chikkamagaluru, Karnataka", lat=13.42617, lon=75.25537),
]

# photographs with their own coordinates, keyed by file name — empty for now;
# fill in as fieldwork photographs with known locations arrive
PHOTO_COORDS = {}

# Photographs sent through the upload page live here rather than in a mirror
# page. The file is written by the intake workflow, and the upload page reads
# it back so the team can see what they have sent, retitle it or remove it.
UPLOADS = os.path.join(os.path.dirname(__file__), "uploads.json")


def uploaded():
    """[{file, caption, location, photographer, added, batch}, …]"""
    try:
        with open(UPLOADS, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except (ValueError, OSError) as e:
        print(f"  !! build/uploads.json unreadable ({e}) — treated as empty")
        return []


def _exif(path):
    """(date, camera, lat, lon) from a photograph; any of them may be None."""
    try:
        ex = Image.open(path)._getexif()
    except Exception:
        return None, None, None, None
    if not ex:
        return None, None, None, None
    d = {TAGS.get(k, k): v for k, v in ex.items()}
    date = (d.get("DateTimeOriginal") or d.get("DateTime") or "")[:10].replace(":", "-") or None
    camera = " ".join(x.strip() for x in (d.get("Make", ""), d.get("Model", "")) if x).strip() or None
    lat = lon = None
    gps = d.get("GPSInfo")
    if gps:
        g = {GPSTAGS.get(k, k): v for k, v in gps.items()}
        try:
            def dec(v, ref):
                out = float(v[0]) + float(v[1]) / 60 + float(v[2]) / 3600
                return -out if ref in ("S", "W") else out
            if g.get("GPSLatitude") and g.get("GPSLongitude"):
                lat = dec(g["GPSLatitude"], g.get("GPSLatitudeRef", "N"))
                lon = dec(g["GPSLongitude"], g.get("GPSLongitudeRef", "E"))
        except Exception:
            pass
    return date, camera, lat, lon


def collect(out_root, photos_by_site):
    """Build the map's data: one entry per site, carrying its photographs.

    photos_by_site: {slug: [(file name, alt text), ...]} from the site's page.

    One marker per site is what the map draws — a photograph that carries its
    own coordinates keeps them here, ready for the day the map splits a site
    into several points.
    """
    img_dir = os.path.join(out_root, "assets", "img")
    out = []
    for site in SITES:
        files = photos_by_site.get(site["slug"], [])
        photos, dates = [], []
        for fn, alt in files:
            path = os.path.join(img_dir, fn)
            date, camera, lat, lon = _exif(path) if os.path.isfile(path) else (None,) * 4
            own = PHOTO_COORDS.get(fn)
            if own:
                lat, lon = own["lat"], own["lon"]
            if date:
                dates.append(date)
            photos.append(dict(file=fn, alt=alt, date=date, camera=camera,
                               lat=lat if lat is not None else site["lat"],
                               lon=lon if lon is not None else site["lon"],
                               located=lat is not None))
        out.append(dict(site, photos=photos, count=len(photos),
                        dates=sorted(set(dates)),
                        thumb=files[0][0] if files else None))

    out.extend(_uploaded_places(img_dir))
    return out


def _uploaded_places(img_dir):
    """Photographs sent through the upload page, grouped into map points by
    the place the sender typed. The intake workflow geocodes each place once
    and stores lat/lon here, so the build never calls out to a geocoder."""
    groups = {}
    for rec in uploaded():
        if rec.get("lat") is None or rec.get("lon") is None:
            continue                      # not placed yet — skip, don't guess
        key = rec.get("location", "").strip()
        groups.setdefault(key, []).append(rec)

    places = []
    for name, recs in sorted(groups.items()):
        photos, dates = [], []
        for r in recs:
            path = os.path.join(img_dir, r["file"])
            date = r.get("date") or (_exif(path)[0] if os.path.isfile(path) else None)
            if date:
                dates.append(date)
            photos.append(dict(file=r["file"], alt=r.get("caption", ""),
                               date=date, camera=r.get("photographer"),
                               lat=r["lat"], lon=r["lon"], located=True))
        head = recs[0]
        places.append(dict(
            slug="", name=name.split(",")[0].strip() or name,
            region=name, lat=head["lat"], lon=head["lon"],
            photos=photos, count=len(photos), dates=sorted(set(dates)),
            thumb=photos[0]["file"] if photos else None))
    return places
