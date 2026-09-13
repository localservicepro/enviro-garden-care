# -*- coding: utf-8 -*-
"""Build the A1 Lawn Care site: writes every HTML page, sitemap.xml and robots.txt.

    python3 build/build.py     # write the site
    python3 build/check.py     # validate it (must exit 0)

Nothing in the repository root is hand-edited — it is all generated from
build/data.py, build/pages.py and build/templates.py.
"""

import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pages                                                    # noqa: E402
from data import SITE, BIZ, IMG, SERVICES, HOME_FAQS            # noqa: E402
from templates import (breadcrumbs, faq_schema, footer, head, header,   # noqa: E402
                       local_business_schema, page_url, service_schema,
                       speakable, svc_url, website_schema)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = datetime.date.today().isoformat()

BASE_GRAPH = [local_business_schema(), website_schema()]


def write(rel_url, html):
    """Write a page at a URL: "/" -> index.html, "/about/" -> about/index.html."""
    rel = "index.html" if rel_url == "/" else rel_url.strip("/") + "/index.html"
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("  wrote %-46s %6d bytes" % (rel, len(html.encode("utf-8"))))
    return rel


def page(url, title, desc, body, schema_extra=(), og_image=None, active="",
         robots=None, body_class=""):
    meta = {
        "title": title,
        "desc": desc,
        "canonical": SITE + url,
        "og_image": og_image or IMG["hero"],
        "schema": BASE_GRAPH + list(schema_extra),
        "body_class": body_class,
    }
    if robots:
        meta["robots"] = robots
    return head(meta) + header(active) + body + footer()


# --------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------
def build_pages():
    written = []

    # Home — research Phase 1: these strings are deployed exactly as specified.
    written.append(write("/", page(
        "/",
        "Lawn Mowing Services Brisbane | A1 Lawn Care Mt Gravatt",
        "Lawn mowing services in Brisbane by A1 Lawn Care - an NDIS registered provider "
        "covering Mount Gravatt, Sunnybank, Bayside &amp; Logan. Get a free quote today.",
        pages.home(),
        schema_extra=[faq_schema(HOME_FAQS), speakable()],
        active="/")))

    # Services hub
    written.append(write("/services/", page(
        "/services/",
        "Lawn &amp; Garden Services Brisbane | A1 Lawn Care",
        "Lawn mowing, NDIS yard maintenance, garden care, palm removal, green waste and "
        "hedging across Brisbane&#39;s south side, Bayside, Logan and the Redlands.",
        pages.services_hub(),
        schema_extra=[breadcrumbs([("Home", "/"), ("Services", "/services/")])],
        active="/services/")))

    # Six service pages
    for svc in SERVICES:
        url = svc_url(svc["slug"])
        written.append(write(url, page(
            url, svc["title"], svc["desc"], pages.service_page(svc),
            schema_extra=[
                service_schema(svc),
                faq_schema(svc["faqs"]),
                breadcrumbs([("Home", "/"), ("Services", "/services/"),
                             (svc["name"], url)]),
                speakable(),
            ],
            og_image=IMG[svc["img"]],
            active="/services/")))

    # About
    written.append(write("/about/", page(
        "/about/",
        "About A1 Lawn Care | NDIS Lawn &amp; Garden Care Mt Gravatt",
        "A1 Lawn Care Pty Ltd is an NDIS registered lawn and garden business at 1593 Logan Rd, "
        "Mount Gravatt, servicing Brisbane south, Bayside, Logan and the Redlands.",
        pages.about(),
        schema_extra=[breadcrumbs([("Home", "/"), ("About", "/about/")]), speakable()],
        og_image=IMG["about"],
        active="/about/")))

    # Contact
    written.append(write("/contact/", page(
        "/contact/",
        "Contact A1 Lawn Care | Free Quotes Brisbane Southside",
        "Contact A1 Lawn Care for a free quote on lawn mowing, garden and yard maintenance "
        "across Brisbane. Call 0456 198 080 — Mount Gravatt based, NDIS registered.",
        pages.contact(),
        schema_extra=[
            breadcrumbs([("Home", "/"), ("Contact", "/contact/")]),
            faq_schema(HOME_FAQS[:4]),
            speakable(),
        ],
        active="/contact/")))

    # Thank you — the redirect target for every form submit. Never indexed.
    written.append(write("/thank-you/", page(
        "/thank-you/",
        "Thank You | A1 Lawn Care Brisbane",
        "Thanks for your quote request — A1 Lawn Care will come back to you the same day, "
        "usually within a few hours. Call 0456 198 080 if you need it sooner.",
        pages.thank_you(),
        robots="noindex, follow",
        body_class="page-thanks")))

    return written


def build_404():
    html = page(
        "/404.html",
        "Page Not Found | A1 Lawn Care Brisbane",
        "That page could not be found. Browse A1 Lawn Care&#39;s lawn mowing, garden "
        "maintenance and yard services across Brisbane, or call 0456 198 080.",
        pages.not_found(),
        robots="noindex, follow",
        body_class="page-thanks")
    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8") as fh:
        fh.write(html)
    print("  wrote %-46s %6d bytes" % ("404.html", len(html.encode("utf-8"))))


# --------------------------------------------------------------------------
# sitemap.xml / robots.txt
# --------------------------------------------------------------------------
def build_sitemap():
    urls = [(page_url(""), "1.0", "weekly")]
    urls.append((page_url("services"), "0.9", "monthly"))
    urls += [(svc_url(s["slug"]), "0.9", "monthly") for s in SERVICES]
    urls.append((page_url("about"), "0.6", "yearly"))
    urls.append((page_url("contact"), "0.7", "yearly"))

    body = "\n".join(
        "  <url>\n"
        "    <loc>%s%s</loc>\n"
        "    <lastmod>%s</lastmod>\n"
        "    <changefreq>%s</changefreq>\n"
        "    <priority>%s</priority>\n"
        "  </url>" % (SITE, url, TODAY, freq, pri)
        for url, pri, freq in urls)

    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           '%s\n</urlset>\n' % body)
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write(xml)
    print("  wrote %-46s %6d bytes  (%d urls)"
          % ("sitemap.xml", len(xml.encode("utf-8")), len(urls)))


def build_robots():
    txt = """User-agent: *
Allow: /
Disallow: /thank-you/

# Answer engines and AI assistants are welcome — the site is written to be read
# by them (see the SEO research, section 10: GEO & AEO).
User-agent: GPTBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

Sitemap: %s/sitemap.xml
""" % SITE
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write(txt)
    print("  wrote %-46s %6d bytes" % ("robots.txt", len(txt.encode("utf-8"))))


if __name__ == "__main__":
    print("Building %s — %s\n" % (BIZ["name"], SITE))
    written = build_pages()
    build_404()
    build_sitemap()
    build_robots()
    print("\n%d pages + 404 + sitemap + robots written." % len(written))
