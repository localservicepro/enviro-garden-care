# -*- coding: utf-8 -*-
"""Post-build validation: JSON-LD, internal links, meta lengths, SEO targets."""

import glob
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}

errors, warnings = [], []


def err(f, m):
    errors.append("%s: %s" % (f, m))


def warn(f, m):
    warnings.append("%s: %s" % (f, m))


class Balance(HTMLParser):
    def __init__(self, fname):
        super().__init__(convert_charrefs=True)
        self.fname, self.stack = fname, []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            err(self.fname, "stray </%s>" % tag)
            return
        if self.stack[-1][0] == tag:
            self.stack.pop()
        else:
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i][0] == tag:
                    err(self.fname, "</%s> closed while <%s> (line %d) still open"
                        % (tag, self.stack[-1][0], self.stack[-1][1]))
                    del self.stack[i:]
                    return
            err(self.fname, "stray </%s>" % tag)


pages = sorted(glob.glob(os.path.join(ROOT, "*.html")) +
               glob.glob(os.path.join(ROOT, "*", "index.html")) +
               glob.glob(os.path.join(ROOT, "services", "*", "index.html")))


def resolve(href):
    """Map a site URL onto the file that serves it.

    Everything is root-relative now, and pages are directory indexes, so
    "/about/" is served by about/index.html and "/" by index.html.
    """
    path = href.split("#")[0].split("?")[0]
    if not path:
        return None
    if not path.startswith("/"):
        return False          # relative link — no longer expected anywhere
    path = path.lstrip("/")
    if path == "" or path.endswith("/"):
        path += "index.html"
    return os.path.join(ROOT, path)


def url_of(rel):
    """Inverse of resolve(): the URL a generated file is served at."""
    rel = rel.replace(os.sep, "/")
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[:-len("index.html")]
    return "/" + rel

print("Checking %d pages\n" % len(pages))
seen_titles, seen_descs, seen_canon = {}, {}, {}

for path in pages:
    rel = os.path.relpath(path, ROOT)
    src = open(path, encoding="utf-8").read()

    # --- tag balance -----------------------------------------------------
    parser = Balance(rel)
    parser.feed(src)
    for tag, line in parser.stack:
        if tag not in ("html", "body"):
            err(rel, "unclosed <%s> opened line %d" % (tag, line))

    # --- JSON-LD ---------------------------------------------------------
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', src, re.S)
    if not blocks:
        err(rel, "no JSON-LD block")
    for block in blocks:
        try:
            data = json.loads(html.unescape(block))
        except ValueError as exc:
            err(rel, "invalid JSON-LD — %s" % exc)
            continue
        types = [n.get("@type") for n in data.get("@graph", [])]
        flat = []
        for t in types:
            flat.extend(t if isinstance(t, list) else [t])
        if "LocalBusiness" not in flat:
            err(rel, "JSON-LD missing LocalBusiness")
        if rel not in ("thank-you/index.html", "404.html") and "BreadcrumbList" not in flat \
                and rel != "index.html":
            warn(rel, "no BreadcrumbList")

    # --- head essentials -------------------------------------------------
    title = re.search(r"<title>(.*?)</title>", src, re.S)
    desc = re.search(r'<meta name="description" content="(.*?)">', src, re.S)
    canon = re.search(r'<link rel="canonical" href="(.*?)">', src)
    if not title:
        err(rel, "no <title>")
    if not desc:
        err(rel, "no meta description")
    if not canon:
        err(rel, "no canonical")

    if title:
        t = html.unescape(title.group(1))
        if len(t) > 65:
            warn(rel, "title %d chars (>65): %s" % (len(t), t))
        seen_titles.setdefault(t, []).append(rel)
    if desc:
        d = html.unescape(desc.group(1))
        if not 110 <= len(d) <= 165:
            warn(rel, "meta description %d chars (target 110-165)" % len(d))
        seen_descs.setdefault(d, []).append(rel)
    if canon:
        seen_canon.setdefault(canon.group(1), []).append(rel)

    # --- headings --------------------------------------------------------
    h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", src, re.S)
    if len(h1s) != 1:
        err(rel, "%d <h1> tags (expected 1)" % len(h1s))
    if not re.search(r"<h2", src):
        warn(rel, "no <h2>")

    # --- images ----------------------------------------------------------
    for tag in re.findall(r"<img\b[^>]*>", src):
        if 'alt="' not in tag:
            err(rel, "img without alt: %s" % tag[:90])
        elif re.search(r'alt=""', tag):
            warn(rel, "empty alt: %s" % tag[:90])
        if "loading=" not in tag:
            warn(rel, "img without loading attr: %s" % tag[:70])

    # --- tracking + analytics -------------------------------------------
    if "link.msgsndr.com/js/external-tracking.js" not in src:
        err(rel, "missing GHL tracking script")
    if src.count("link.msgsndr.com/js/external-tracking.js") != 1:
        err(rel, "tracking script present %d times (expected 1)"
            % src.count("link.msgsndr.com/js/external-tracking.js"))

    # --- map embed -------------------------------------------------------
    if rel in ("index.html", "about/index.html", "contact/index.html"):
        if "google.com/maps/embed" not in src:
            err(rel, "missing Google Map embed")

    # --- forms -----------------------------------------------------------
    for form in re.findall(r"<form\b[^>]*>", src):
        action = re.search(r'action="([^"]+)"', form)
        if not action:
            err(rel, "form without action")
        elif action.group(1) != "/thank-you/":
            err(rel, "form action is not /thank-you/: %s" % action.group(1))

    # --- internal links --------------------------------------------------
    for attr in ("href", "src", "action"):
        for ref in re.findall(r'%s="([^"]+)"' % attr, src):
            if ref.startswith(("http", "mailto:", "tel:", "#", "data:")):
                continue
            resolved = resolve(ref)
            if resolved is None:
                continue
            if resolved is False:
                err(rel, "relative %s (expected root-relative) -> %s" % (attr, ref))
                continue
            if not os.path.exists(resolved):
                err(rel, "broken %s -> %s" % (attr, ref))
            elif ref.split("#")[0].endswith(".html") and ref != "/404.html":
                err(rel, "%s still exposes .html -> %s" % (attr, ref))

# --- duplicates ----------------------------------------------------------
for t, files in seen_titles.items():
    if len(files) > 1:
        err("global", "duplicate <title> across %s" % ", ".join(files))
for d, files in seen_descs.items():
    if len(files) > 1:
        err("global", "duplicate meta description across %s" % ", ".join(files))
for c, files in seen_canon.items():
    if len(files) > 1:
        err("global", "duplicate canonical %s across %s" % (c, ", ".join(files)))

# --- sitemap -------------------------------------------------------------
sitemap = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
for path in pages:
    rel = os.path.relpath(path, ROOT)
    needle = url_of(rel)
    if rel in ("thank-you/index.html", "404.html"):
        if needle + "<" in sitemap:
            err("sitemap.xml", "%s should not be listed" % needle)
        continue
    if needle + "<" not in sitemap:
        err("sitemap.xml", "missing %s" % needle)
if ".html<" in sitemap:
    err("sitemap.xml", "sitemap still contains a .html URL")

# --- keyword targets from the research doc -------------------------------
TARGETS = {
    "index.html": "lawn mowing gold coast",
    "services/lawn-mowing/index.html": "lawn mowing coomera",
    "services/acreage-mowing/index.html": "acreage mowing gold coast",
    "services/garden-maintenance/index.html": "garden maintenance gold coast",
    "services/green-waste-removal/index.html": "green waste removal gold coast",
    "services/commercial-property-maintenance/index.html":
        "commercial property maintenance gold coast",
}
print("Primary keyword placement (title / H1 / first 100 words):")
for rel, kw in TARGETS.items():
    src = open(os.path.join(ROOT, rel), encoding="utf-8").read()
    title = html.unescape(re.search(r"<title>(.*?)</title>", src, re.S).group(1)).lower()
    h1 = html.unescape(re.sub(r"<[^>]+>", " ", re.search(r"<h1[^>]*>(.*?)</h1>", src, re.S).group(1))).lower()
    h1 = re.sub(r"\s+", " ", h1)
    body = re.sub(r"<(script|style)\b.*?</\1>", " ", src, flags=re.S)
    body = re.sub(r"<[^>]+>", " ", body.split("<main")[-1])
    body = re.sub(r"\s+", " ", html.unescape(body)).lower()
    first100 = " ".join(body.split()[:100])
    marks = [("title", kw in title), ("h1", kw in h1), ("first100", kw in first100)]
    ok = all(m[1] for m in marks)
    print("  %-52s %s  %s" % (rel, "PASS" if ok else "CHECK",
                              " ".join("%s:%s" % (n, "y" if v else "n") for n, v in marks)))
    if not ok:
        warn(rel, "keyword '%s' missing from: %s"
             % (kw, ", ".join(n for n, v in marks if not v)))
    density = body.count(kw) / max(len(body.split()), 1) * 100 * len(kw.split())
    print("       density %.2f%% (%d exact matches, %d words)"
          % (density, body.count(kw), len(body.split())))

print("\n%d error(s), %d warning(s)" % (len(errors), len(warnings)))
for e in errors:
    print("  ERROR   %s" % e)
for w in warnings:
    print("  warning %s" % w)
sys.exit(1 if errors else 0)
