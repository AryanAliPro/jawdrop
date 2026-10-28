#!/usr/bin/env python3
"""Check that every external URL a website depends on actually loads.

Scans files and folders for http(s) URLs (images, scripts, stylesheets, fonts),
requests each one, and reports anything broken together with where it appears.
Optionally saves a small thumbnail of every image so you can look at them.

Usage:
  python3 check_urls.py <path-or-url> [...] [--thumbs DIR] [--all] [--timeout 20] [--json]

  <path-or-url>  Files, folders (scanned recursively) or URLs to check directly.
  --thumbs DIR   Save a thumbnail of every working image URL into DIR.
  --all          Also check ordinary links (social profiles, other sites). By
                 default only assets the page loads are checked.
  --json         Print results as JSON instead of a table.

Exit code is 1 if any asset is broken, 0 otherwise. Standard library only.
"""

import argparse
import concurrent.futures
import html
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

SCAN_EXTENSIONS = {
    ".html", ".htm", ".css", ".scss", ".sass", ".less", ".js", ".mjs", ".cjs",
    ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".astro", ".md", ".mdx", ".json",
}
SKIP_DIRS = {"node_modules", ".git", ".next", ".nuxt", ".svelte-kit", ".astro",
             "dist", "build", "out", ".vercel", ".output", "coverage", "__pycache__"}
SKIP_FILES = {"package-lock.json", "npm-shrinkwrap.json", "composer.lock"}

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".webp", ".avif", ".svg", ".ico")
ASSET_EXTENSIONS = IMAGE_EXTENSIONS + (
    ".js", ".mjs", ".css", ".woff", ".woff2", ".ttf", ".otf", ".mp4", ".webm",
    ".mp3", ".json", ".glb", ".gltf", ".hdr", ".lottie",
)
IMAGE_HOSTS = {
    "images.unsplash.com", "plus.unsplash.com", "images.pexels.com",
    "upload.wikimedia.org", "live.staticflickr.com", "cdn.pixabay.com",
    "images.ctfassets.net", "res.cloudinary.com",
}
ASSET_HOSTS = IMAGE_HOSTS | {
    "cdn.jsdelivr.net", "unpkg.com", "cdnjs.cloudflare.com", "esm.sh",
    "ga.jspm.io", "cdn.skypack.dev", "fonts.googleapis.com", "fonts.gstatic.com",
    "api.fontshare.com", "cdn.fontshare.com", "use.typekit.net",
    "assets.codepen.io", "lottie.host",
}
# Namespace and spec URLs that appear in markup but are never fetched.
IGNORE_PREFIXES = (
    "http://www.w3.org/", "https://www.w3.org/", "http://schema.org", "https://schema.org",
    "http://ogp.me/", "https://ogp.me/", "http://purl.org/", "http://ns.adobe.com/",
    "http://localhost", "https://localhost", "http://127.0.0.1", "https://127.0.0.1",
)

URL_RE = re.compile(r"""https?://[^\s"'`<>()\\{}|^\[\]]+""")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/130.0 Safari/537.36")


def clean(url):
    url = html.unescape(url)
    return url.rstrip(".,;:!?*'\"")


def is_image(url):
    parsed = urllib.parse.urlparse(url)
    return parsed.netloc in IMAGE_HOSTS or parsed.path.lower().endswith(IMAGE_EXTENSIONS)


def is_asset(url):
    parsed = urllib.parse.urlparse(url)
    return parsed.netloc in ASSET_HOSTS or parsed.path.lower().endswith(ASSET_EXTENSIONS)


def iter_files(path):
    if os.path.isfile(path):
        yield path
        return
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for name in files:
            if name in SKIP_FILES:
                continue
            if os.path.splitext(name)[1].lower() in SCAN_EXTENSIONS:
                yield os.path.join(root, name)


def collect(targets):
    """Return {url: [locations]} for every URL found in the targets."""
    found = {}
    for target in targets:
        if target.startswith(("http://", "https://")):
            found.setdefault(target, []).append("(argument)")
            continue
        if not os.path.exists(target):
            print(f"warning: {target} does not exist", file=sys.stderr)
            continue
        for path in iter_files(target):
            try:
                with open(path, encoding="utf-8", errors="ignore") as fh:
                    for lineno, line in enumerate(fh, 1):
                        for match in URL_RE.findall(line):
                            url = clean(match)
                            if url.startswith(IGNORE_PREFIXES) or "${" in url:
                                continue
                            found.setdefault(url, []).append(f"{path}:{lineno}")
            except OSError as exc:
                print(f"warning: cannot read {path}: {exc}", file=sys.stderr)
    return found


def thumb_url(url):
    """Ask image CDNs for a small rendition so thumbnails download fast."""
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc in {"images.unsplash.com", "plus.unsplash.com", "images.pexels.com"}:
        query = dict(urllib.parse.parse_qsl(parsed.query))
        query.update({"w": "400"})
        query.pop("h", None)
        return urllib.parse.urlunparse(parsed._replace(query=urllib.parse.urlencode(query)))
    return url


def fetch(url, timeout, want_body=False, max_bytes=8_000_000, accept="image/avif,image/webp,image/*,text/css,*/*;q=0.8"):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        status = resp.status
        ctype = resp.headers.get("Content-Type", "")
        body = resp.read(max_bytes) if want_body else resp.read(2048)
        return status, ctype, body


def check(url, timeout, thumbs_dir, index):
    result = {"url": url, "kind": "image" if is_image(url) else ("asset" if is_asset(url) else "link")}
    try:
        status, ctype, _ = fetch(url, timeout)
        result.update(status=status, content_type=ctype.split(";")[0])
        ok = 200 <= status < 300
        if ok and result["kind"] == "image" and not ctype.startswith("image/"):
            ok = False
            result["error"] = f"expected an image, got {ctype or 'no content type'}"
        result["ok"] = ok
    except urllib.error.HTTPError as exc:
        result.update(ok=False, status=exc.code, error=str(exc.reason))
    except Exception as exc:  # timeouts, DNS failures, TLS errors
        result.update(ok=False, status=None, error=f"{type(exc).__name__}: {exc}")

    if thumbs_dir and result.get("ok") and result["kind"] == "image":
        try:
            # Ask for JPEG or PNG so the thumbnail opens in any image viewer.
            _, ctype, body = fetch(thumb_url(url), timeout, want_body=True,
                                   accept="image/jpeg,image/png;q=0.9,image/*;q=0.5")
            ext = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp",
                   "image/avif": ".avif", "image/gif": ".gif", "image/svg+xml": ".svg"}.get(
                       ctype.split(";")[0], ".img")
            host = urllib.parse.urlparse(url).netloc.replace(".", "-")
            path = os.path.join(thumbs_dir, f"{index:03d}-{host}{ext}")
            with open(path, "wb") as fh:
                fh.write(body)
            result["thumbnail"] = path
        except Exception as exc:
            result["thumbnail_error"] = str(exc)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("targets", nargs="+")
    parser.add_argument("--thumbs", metavar="DIR")
    parser.add_argument("--all", action="store_true", help="also check ordinary links")
    parser.add_argument("--timeout", type=float, default=20)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    found = collect(args.targets)
    urls = [u for u in found if args.all or is_asset(u) or found[u] == ["(argument)"]]
    if not urls:
        print("No external asset URLs found.")
        return 0
    if args.thumbs:
        os.makedirs(args.thumbs, exist_ok=True)

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(check, url, args.timeout, args.thumbs, i): url
                   for i, url in enumerate(sorted(urls), 1)}
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
    results.sort(key=lambda r: (r["ok"], r["kind"], r["url"]))
    for r in results:
        r["found_in"] = found[r["url"]][:5]

    broken_assets = [r for r in results if not r["ok"] and r["kind"] != "link"]
    broken_links = [r for r in results if not r["ok"] and r["kind"] == "link"]

    if args.json:
        print(json.dumps({"checked": len(results), "broken_assets": len(broken_assets),
                          "broken_links": len(broken_links), "results": results}, indent=2))
    else:
        for r in results:
            mark = "OK    " if r["ok"] else "BROKEN"
            detail = r.get("content_type") or r.get("error", "")
            print(f"{mark} {str(r.get('status') or '---'):>3} {r['kind']:<5} {r['url']}  [{detail}]")
            if not r["ok"]:
                for loc in r["found_in"]:
                    print(f"         at {loc}")
            if r.get("thumbnail"):
                print(f"         thumbnail: {r['thumbnail']}")
        print(f"\nChecked {len(results)} URLs: {len(broken_assets)} broken assets, "
              f"{len(broken_links)} broken links.")
        if broken_assets:
            print("Replace or remove every broken asset before hand-over.")
    return 1 if broken_assets else 0


if __name__ == "__main__":
    sys.exit(main())
