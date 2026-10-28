#!/usr/bin/env python3
"""Search public image sources for a subject and return verified, usable URLs.

Sources, used in this order when available:
  unsplash   official API, needs UNSPLASH_ACCESS_KEY in the environment
  pexels     official API, needs PEXELS_API_KEY in the environment
  openverse  keyless (aggregates Flickr, Wikimedia and others; licenses vary)
  commons    keyless Wikimedia Commons search (licenses vary)

Every returned URL has been requested and confirmed to load as an image.
Unreachable or rate-limited sources are skipped with a note on stderr.

Usage:
  python3 find_images.py "baker shaping sourdough" [--count 8]
                         [--orientation landscape|portrait|square]
                         [--source auto|unsplash|pexels|openverse|commons]
                         [--width 1600]

Prints a JSON list of {url, width, height, description, source, license,
credit, page}. Standard library only.
"""

import argparse
import concurrent.futures
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

UA = "jawdrop-skill/1.0 (website image search; verifies public image URLs)"
TIMEOUT = 20


def get_json(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.load(resp)


def loads_as_image(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "image/*,*/*;q=0.8"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            resp.read(1024)
            return 200 <= resp.status < 300 and resp.headers.get("Content-Type", "").startswith("image/")
    except Exception:
        return False


def strip_tags(text):
    return re.sub(r"<[^>]+>", "", text or "").strip()


def matches_orientation(width, height, orientation):
    if not orientation or not width or not height:
        return True
    ratio = width / height
    return {"landscape": ratio > 1.15, "portrait": ratio < 0.87, "square": 0.87 <= ratio <= 1.15}[orientation]


def search_unsplash(query, count, orientation, width):
    key = os.environ.get("UNSPLASH_ACCESS_KEY")
    if not key:
        return None
    params = {"query": query, "per_page": min(count * 2, 30)}
    if orientation:
        params["orientation"] = "squarish" if orientation == "square" else orientation
    data = get_json("https://api.unsplash.com/search/photos?" + urllib.parse.urlencode(params),
                    {"Authorization": f"Client-ID {key}", "Accept-Version": "v1"})
    out = []
    for p in data.get("results", []):
        out.append({
            "url": f"{p['urls']['raw']}&auto=format&fit=crop&w={width}&q=80",
            "width": p.get("width"), "height": p.get("height"),
            "description": p.get("alt_description") or p.get("description") or "",
            "source": "unsplash", "license": "Unsplash License (free, attribution appreciated)",
            "credit": f"Photo by {p['user']['name']} on Unsplash",
            "page": p["links"]["html"],
        })
    return out


def search_pexels(query, count, orientation, width):
    key = os.environ.get("PEXELS_API_KEY")
    if not key:
        return None
    params = {"query": query, "per_page": min(count * 2, 40)}
    if orientation:
        params["orientation"] = orientation
    data = get_json("https://api.pexels.com/v1/search?" + urllib.parse.urlencode(params),
                    {"Authorization": key})
    out = []
    for p in data.get("photos", []):
        pid = p["id"]
        out.append({
            "url": f"https://images.pexels.com/photos/{pid}/pexels-photo-{pid}.jpeg?auto=compress&cs=tinysrgb&w={width}",
            "width": p.get("width"), "height": p.get("height"),
            "description": p.get("alt") or "",
            "source": "pexels", "license": "Pexels License (free, attribution not required)",
            "credit": f"Photo by {p.get('photographer', 'unknown')} on Pexels",
            "page": p.get("url"),
        })
    return out


def search_openverse(query, count, orientation, width):
    params = {"q": query, "page_size": min(count * 3, 20), "license_type": "commercial"}
    if orientation:
        params["aspect_ratio"] = {"landscape": "wide", "portrait": "tall", "square": "square"}[orientation]
    data = get_json("https://api.openverse.org/v1/images/?" + urllib.parse.urlencode(params))
    out = []
    for p in data.get("results", []):
        license_name = f"CC {p.get('license', '').upper()} {p.get('license_version') or ''}".strip()
        if p.get("license") in ("cc0", "pdm"):
            license_name = "Public domain (" + p["license"].upper() + ")"
        out.append({
            "url": p.get("url"),
            "width": p.get("width"), "height": p.get("height"),
            "description": p.get("title") or "",
            "source": f"openverse/{p.get('source')}", "license": license_name,
            "credit": p.get("attribution") or p.get("creator") or "",
            "page": p.get("foreign_landing_url"),
        })
    return out


def search_commons(query, count, orientation, width):
    params = {
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": f"{query} filetype:bitmap", "gsrnamespace": 6, "gsrlimit": min(count * 3, 30),
        "prop": "imageinfo", "iiprop": "url|size|mime|extmetadata", "iiurlwidth": width,
        "iiextmetadatafilter": "LicenseShortName|Artist|ImageDescription",
    }
    data = get_json("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params))
    out = []
    for page in (data.get("query") or {}).get("pages", {}).values():
        info = (page.get("imageinfo") or [{}])[0]
        meta = info.get("extmetadata") or {}
        if not info.get("mime", "").startswith("image/"):
            continue
        out.append({
            "url": info.get("thumburl") or info.get("url"),
            "width": info.get("width"), "height": info.get("height"),
            "description": strip_tags(meta.get("ImageDescription", {}).get("value"))[:200]
                           or page.get("title", "").replace("File:", ""),
            "source": "wikimedia-commons",
            "license": meta.get("LicenseShortName", {}).get("value", "see page"),
            "credit": strip_tags(meta.get("Artist", {}).get("value")),
            "page": info.get("descriptionurl"),
        })
    return out


SOURCES = {
    "unsplash": search_unsplash,
    "pexels": search_pexels,
    "openverse": search_openverse,
    "commons": search_commons,
}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("query")
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--orientation", choices=["landscape", "portrait", "square"])
    parser.add_argument("--source", default="auto", choices=["auto", *SOURCES])
    parser.add_argument("--width", type=int, default=1600, help="requested image width where the CDN supports it")
    args = parser.parse_args()

    names = list(SOURCES) if args.source == "auto" else [args.source]
    candidates = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(names)) as pool:
        futures = {pool.submit(SOURCES[n], args.query, args.count, args.orientation, args.width): n for n in names}
        for future in concurrent.futures.as_completed(futures):
            name = futures[future]
            try:
                found = future.result()
            except Exception as exc:
                print(f"note: {name} unavailable ({type(exc).__name__}: {exc})", file=sys.stderr)
                continue
            if found is None:
                print(f"note: {name} skipped (no API key in the environment)", file=sys.stderr)
                continue
            candidates.extend(c for c in found if c.get("url"))

    # Keep the source priority order, filter by shape, then verify.
    order = {n: i for i, n in enumerate(SOURCES)}
    candidates.sort(key=lambda c: order.get(c["source"].split("/")[0], 99))
    candidates = [c for c in candidates if matches_orientation(c.get("width"), c.get("height"), args.orientation)]

    verified = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        checks = list(pool.map(lambda c: (c, loads_as_image(c["url"])), candidates))
    for candidate, ok in checks:
        if ok:
            verified.append(candidate)
        if len(verified) >= args.count:
            break

    if not verified:
        print("note: no verified results. Try more specific or different wording, or find Pexels photo IDs "
              "with a web search as described in references/imagery.md.", file=sys.stderr)
    print(json.dumps(verified, indent=2, ensure_ascii=False))
    return 0 if verified else 1


if __name__ == "__main__":
    sys.exit(main())
