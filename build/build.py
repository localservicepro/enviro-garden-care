# -*- coding: utf-8 -*-
"""Generate the static site.

    python3 build/build.py

Pages are written as directory indexes (about/index.html) so every URL is
extensionless — /about/, /services/lawn-mowing/ — on any static host, with no
rewrite rules or host-specific "pretty URL" setting required.

404.html stays a flat file at the root because that is where hosts look for it.
"""

import os
import sys
import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from data import SITE, SERVICES  # noqa: E402
from templates import page_url, svc_url  # noqa: E402
import pages  # noqa: E402

TODAY = datetime.date.today().isoformat()


def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path) or ROOT, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    print("  %-46s %7.1f KB" % (rel, len(content.encode("utf-8")) / 1024.0))


def sitemap(urls):
    rows = "".join(
        "\n  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>"
        "\n    <changefreq>%s</changefreq>\n    <priority>%s</priority>\n  </url>"
        % (loc, TODAY, freq, pri) for loc, freq, pri in urls)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s\n</urlset>\n' % rows)


def robots():
    return """User-agent: *
Allow: /
Disallow: /thank-you/

# AI and answer engines are explicitly welcome to read and cite this site.
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Google-Extended
Allow: /

Sitemap: %s/sitemap.xml
""" % SITE


def main():
    print("Building %s" % SITE)

    write("index.html", pages.home())
    write("about/index.html", pages.about())
    write("services/index.html", pages.services_hub())
    write("contact/index.html", pages.contact())
    write("thank-you/index.html", pages.thank_you())
    write("404.html", pages.not_found())

    for svc in SERVICES:
        write("services/%s/index.html" % svc["slug"], pages.service_page(svc))

    urls = [(SITE + page_url(), "weekly", "1.0"),
            (SITE + page_url("services"), "monthly", "0.9")]
    urls += [(SITE + svc_url(s["slug"]), "monthly", "0.9") for s in SERVICES]
    urls += [(SITE + page_url("about"), "monthly", "0.7"),
             (SITE + page_url("contact"), "monthly", "0.8")]
    write("sitemap.xml", sitemap(urls))
    write("robots.txt", robots())

    print("Done — %d pages." % (6 + len(SERVICES)))


if __name__ == "__main__":
    main()
