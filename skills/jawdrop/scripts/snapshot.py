#!/usr/bin/env python3
"""Screenshot a page at desktop and mobile sizes with headless Chrome, and
report console errors, so you can look at what you built.

Usage:
  python3 snapshot.py <index.html | http://localhost:3000> [--out DIR]
                      [--sizes 1440x900,390x844] [--wait 7000]

  --sizes  Comma-separated WIDTHxHEIGHT list. Use a tall size such as
           1440x3200 to see more of the page in one image.
  --wait   Milliseconds of page time to let load animations play before the
           screenshot (Chrome fast-forwards this virtual time).

Finds Chrome, Chromium, Edge or Brave automatically; set CHROME_PATH to
override. Prints the screenshot paths and any console errors or warnings.
Exit code is 1 if the browser can't be found or reports a JavaScript error.
Standard library only.
"""

import argparse
import glob
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse

CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]
PATH_NAMES = ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
              "microsoft-edge", "brave-browser", "chrome"]
PLAYWRIGHT_GLOBS = [
    "~/Library/Caches/ms-playwright/chromium-*/chrome-mac*/Chromium.app/Contents/MacOS/Chromium",
    "~/Library/Caches/ms-playwright/chromium-*/chrome-mac*/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing",
    "~/.cache/ms-playwright/chromium-*/chrome-linux*/chrome",
]

# Chrome logs console output as CONSOLE(12)] in older versions and CONSOLE:12] in newer ones.
CONSOLE_RE = re.compile(r'CONSOLE[:(]\d+\)?\]\s*"(?P<msg>.*)",\s*source:\s*(?P<src>.*)$')
ERROR_HINTS = ("Uncaught", "Error", "Failed to load resource", "is not defined", "Cannot read")


def find_browser():
    env = os.environ.get("CHROME_PATH")
    if env and os.path.exists(env):
        return env
    for path in CANDIDATES:
        if os.path.exists(path):
            return path
    for name in PATH_NAMES:
        found = shutil.which(name)
        if found:
            return found
    for pattern in PLAYWRIGHT_GLOBS:
        matches = sorted(glob.glob(os.path.expanduser(pattern)))
        if matches:
            return matches[-1]
    return None


def to_url(target):
    if re.match(r"^[a-z]+://", target):
        return target
    path = pathlib.Path(target).expanduser().resolve()
    if path.is_dir():
        path = path / "index.html"
    if not path.exists():
        sys.exit(f"error: {path} does not exist")
    return path.as_uri()


def shoot(browser, url, width, height, wait, out_path):
    with tempfile.TemporaryDirectory() as profile:
        cmd = [
            browser, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
            "--no-default-browser-check", "--mute-audio", f"--user-data-dir={profile}",
            f"--window-size={width},{height}", f"--virtual-time-budget={wait}",
            "--enable-logging=stderr", "--v=0", f"--screenshot={out_path}", url,
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    messages = []
    for line in proc.stderr.splitlines():
        match = CONSOLE_RE.search(line)
        if match:
            messages.append(f"{match.group('msg')}  ({match.group('src').strip()})")
    return os.path.exists(out_path), messages, proc.stderr


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("target")
    parser.add_argument("--out", default=".")
    parser.add_argument("--sizes", default="1440x900,390x844")
    parser.add_argument("--wait", type=int, default=7000)
    args = parser.parse_args()

    browser = find_browser()
    if not browser:
        print("error: no Chrome, Chromium, Edge or Brave found. Set CHROME_PATH, or review the site with "
              "browser tools instead.", file=sys.stderr)
        return 1

    url = to_url(args.target)
    os.makedirs(args.out, exist_ok=True)
    page_path = urllib.parse.unquote(urllib.parse.urlparse(url).path)
    stem = re.sub(r"[^a-zA-Z0-9]+", "-", pathlib.Path(page_path).stem).strip("-") or "page"

    all_messages = set()
    for size in args.sizes.split(","):
        width, height = (int(v) for v in size.lower().split("x"))
        out_path = os.path.abspath(os.path.join(args.out, f"{stem}-{width}x{height}.png"))
        ok, messages, stderr = shoot(browser, url, width, height, args.wait, out_path)
        if ok:
            print(f"screenshot: {out_path}")
        else:
            print(f"error: no screenshot for {size}\n{stderr[-1500:]}", file=sys.stderr)
        all_messages.update(messages)

    errors = sorted(m for m in all_messages if any(h in m for h in ERROR_HINTS))
    others = sorted(all_messages - set(errors))
    if errors:
        print("\nconsole errors:")
        for m in errors:
            print(f"  {m}")
    if others:
        print("\nconsole messages:")
        for m in others:
            print(f"  {m}")
    if not all_messages:
        print("\nconsole: clean")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
