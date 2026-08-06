#!/usr/bin/env python3
"""Turn pending upload batches into photographs on the site.

Run by .github/workflows/intake.yml whenever the upload page drops a file into
uploads/pending/. For each batch it:

  * fetches every photograph from its Blob URL,
  * shrinks it to a sane width and writes it into hyp/assets/img/,
  * geocodes the place the sender typed — once per place, cached in
    build/geocache.json so a rebuild never calls out again,
  * appends the entries to build/uploads.json, which the map reads,
  * moves the batch file to uploads/done/ so it is not processed twice.

Deliberately forgiving: a photograph that fails to fetch is reported and
skipped rather than failing the whole batch, and a place that cannot be
geocoded still gets its photographs in — they simply wait for coordinates
instead of being dropped.
"""
import io
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PENDING = os.path.join(ROOT, "uploads", "pending")
DONE = os.path.join(ROOT, "uploads", "done")
IMG = os.path.join(ROOT, "hyp", "assets", "img")
UPLOADS = os.path.join(ROOT, "build", "uploads.json")
GEOCACHE = os.path.join(ROOT, "build", "geocache.json")
MAX_WIDTH = 2000
UA = "light-on-hatha-yoga-site/1.0 (maria.iontseva@wolfson.ox.ac.uk)"


def load(path, fallback):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, ValueError):
        return fallback


def save(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
        f.write("\n")


def geocode(place, cache):
    """(lat, lon) or (None, None). Cached, so each place is looked up once."""
    key = place.strip().lower()
    if not key:
        return None, None
    if key in cache:
        hit = cache[key]
        return (hit.get("lat"), hit.get("lon")) if hit else (None, None)

    url = ("https://nominatim.openstreetmap.org/search?"
           + urllib.parse.urlencode({"q": place, "format": "json", "limit": 1}))
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=25) as r:
            hits = json.load(r)
        time.sleep(1.2)                      # Nominatim asks for 1 req/sec
    except Exception as e:
        print(f"    geocoder failed for {place!r}: {e}")
        return None, None

    if not hits:
        print(f"    no coordinates found for {place!r} — photographs will wait")
        cache[key] = None
        save(GEOCACHE, cache)
        return None, None

    lat, lon = float(hits[0]["lat"]), float(hits[0]["lon"])
    cache[key] = {"lat": lat, "lon": lon, "matched": hits[0].get("display_name", "")}
    save(GEOCACHE, cache)
    print(f"    {place!r} → {lat:.4f}, {lon:.4f}")
    return lat, lon


def safe_name(name, taken):
    base, ext = os.path.splitext(name)
    base = re.sub(r"[^\w\-]+", "-", base, flags=re.UNICODE).strip("-") or "photo"
    ext = ext.lower() if ext.lower() in (".jpg", ".jpeg", ".png") else ".jpg"
    if ext == ".jpeg":
        ext = ".jpg"
    candidate = base + ext
    n = 2
    while candidate in taken or os.path.exists(os.path.join(IMG, candidate)):
        candidate = f"{base}-{n}{ext}"
        n += 1
    return candidate


def main():
    from PIL import Image

    batches = sorted(f for f in os.listdir(PENDING) if f.endswith(".json")) \
        if os.path.isdir(PENDING) else []
    if not batches:
        print("No pending batches.")
        return

    uploads = load(UPLOADS, [])
    cache = load(GEOCACHE, {})
    taken = {r["file"] for r in uploads}
    os.makedirs(IMG, exist_ok=True)
    os.makedirs(DONE, exist_ok=True)

    for name in batches:
        path = os.path.join(PENDING, name)
        rec = load(path, None)
        if not rec:
            print(f"  {name}: unreadable, left in place")
            continue

        print(f"\n  batch {rec.get('batch')} — {len(rec.get('photos', []))} photographs"
              f" — {rec.get('location') or 'no location'}"
              f" — {rec.get('photographer') or 'photographer not given'}")

        for p in rec.get("photos", []):
            place = p.get("location") or rec.get("location", "")
            lat, lon = geocode(place, cache)
            try:
                req = urllib.request.Request(p["url"], headers={"User-Agent": UA})
                with urllib.request.urlopen(req, timeout=120) as r:
                    data = r.read()
                im = Image.open(io.BytesIO(data)).convert("RGB")
            except Exception as e:
                print(f"    could not fetch {p.get('file')}: {e} — skipped")
                continue

            if im.width > MAX_WIDTH:
                im = im.resize(
                    (MAX_WIDTH, round(im.height * MAX_WIDTH / im.width)),
                    Image.LANCZOS)
            out_name = safe_name(p.get("file", "photo.jpg"), taken)
            im.save(os.path.join(IMG, out_name), quality=88, optimize=True)
            taken.add(out_name)

            uploads.append({
                "file": out_name,
                "caption": p.get("caption", ""),
                "location": place,
                "lat": lat, "lon": lon,
                "photographer": rec.get("photographer", ""),
                "added": rec.get("submitted", "")[:10],
                "batch": rec.get("batch", ""),
            })
            print(f"    {out_name}  {im.width}×{im.height}")

        os.replace(path, os.path.join(DONE, name))

    save(UPLOADS, uploads)
    print(f"\n{len(uploads)} uploaded photographs on the site in total.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:                     # never leave the repo half-done
        print(f"intake failed: {e}")
        sys.exit(1)
