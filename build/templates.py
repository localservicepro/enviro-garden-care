# -*- coding: utf-8 -*-
"""Shared layout, structured data and reusable components."""

import json
import re

from data import (SITE, BIZ, MAP_EMBED, TRACKING_ID, IMG, SERVICES, ALL_SUBURBS,
                  AREA_GROUPS, FORM_FIELDS, CITABLE, STATS)


def plain(html):
    """Strip tags/entities so marked-up copy can be reused in meta and JSON-LD."""
    txt = re.sub(r"<[^>]+>", "", html)
    for a, b in (("&amp;", "&"), ("&nbsp;", " "), ("&mdash;", "—"), ("&#39;", "'")):
        txt = txt.replace(a, b)
    return re.sub(r"\s+", " ", txt).strip()


def page_url(path=""):
    """Root-relative URL for a page.

    Pages are written as directory indexes (about/index.html) so every URL is
    extensionless on any static host, with no rewrite rules:
        page_url("")                      -> "/"
        page_url("about")                 -> "/about/"
        page_url("services/lawn-mowing")  -> "/services/lawn-mowing/"
    """
    path = path.strip("/")
    return "/" + (path + "/" if path else "")


def svc_url(slug):
    return page_url("services/" + slug)


# --------------------------------------------------------------------------
# Icons (inline SVG, stroked with currentColor)
# --------------------------------------------------------------------------
ICONS = {
    "mower": '<path d="M3 17h7l2-4h6"/><circle cx="6" cy="19" r="2.4"/><circle cx="18" cy="19" r="2.4"/><path d="M12 13V5h6"/>',
    "shears": '<circle cx="6" cy="18" r="2.4"/><circle cx="18" cy="18" r="2.4"/><path d="M7.7 16.3 18 4M16.3 16.3 6 4"/>',
    "truck": '<path d="M2 7h11v9H2zM13 10h4.5l3 3.2V16H13z"/><circle cx="6.5" cy="18" r="1.8"/><circle cx="17" cy="18" r="1.8"/>',
    "palm": '<path d="M12 21V11"/><path d="M12 11c-3-3-7-3-9-1 3-2.6 7-2 9 1z"/><path d="M12 11c3-3 7-3 9-1-3-2.6-7-2-9 1z"/><path d="M12 11c0-4 2-7 5-8-3.8.4-6 3.4-5 8z"/><path d="M12 11c0-4-2-7-5-8 3.8.4 6 3.4 5 8z"/>',
    "leaf": '<path d="M4 20c0-8 6-14 16-15 0 11-6 16-13 16H4z"/><path d="M6 18c3-5 7-8 11-9"/>',
    "shield": '<path d="M12 3l7 3v5.5c0 4.4-3 8-7 9.5-4-1.5-7-5.1-7-9.5V6z"/><path d="m9 12 2 2 4-4"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.2 2"/>',
    "pin": '<path d="M12 21s7-5.6 7-11a7 7 0 1 0-14 0c0 5.4 7 11 7 11z"/><circle cx="12" cy="10" r="2.6"/>',
    "phone": '<path d="M6 3h3l2 5-2.4 1.4a12 12 0 0 0 6 6L16 13l5 2v3a2 2 0 0 1-2.2 2A17 17 0 0 1 4 5.2 2 2 0 0 1 6 3z"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 7 8.5 6 8.5-6"/>',
    "star": '<path d="m12 3.5 2.6 5.6 6 .8-4.4 4.2 1.1 6-5.3-2.9-5.3 2.9 1.1-6L3.4 9.9l6-.8z"/>',
    "check": '<path d="m4 12.5 5 5L20 6.5"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "chat": '<path d="M21 12a8 8 0 0 1-8 8H7l-4 2 1.3-4.2A8 8 0 1 1 21 12z"/>',
}


def icon(name, cls="icon"):
    return ('<svg class="%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" '
            'aria-hidden="true">%s</svg>' % (cls, ICONS[name]))


# --------------------------------------------------------------------------
# Structured data
# --------------------------------------------------------------------------
def _opening_hours():
    return [{
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": days,
        "opens": opens,
        "closes": closes,
    } for days, opens, closes, _ in BIZ["hours"]]


def local_business_schema():
    """LocalBusiness with full NAP, geo, hours and areaServed.

    Research, critical issue 04: none of this exists on the current site, which
    is why Google struggles to place the business anywhere.
    """
    return {
        "@type": ["LocalBusiness", "HomeAndConstructionBusiness"],
        "@id": SITE + "/#business",
        "name": BIZ["name"],
        "alternateName": BIZ["short"],
        "description": plain(CITABLE),
        "slogan": "NDIS registered lawn and garden care, Brisbane south side",
        "url": SITE + "/",
        "telephone": BIZ["phone_e164"],
        "email": BIZ["email"],
        "founder": {"@type": "Person", "name": BIZ["owner"]},
        "image": IMG["hero"],
        "logo": IMG["logo"],
        "priceRange": "$$",
        "currenciesAccepted": "AUD",
        "paymentAccepted": "Cash, Bank transfer, Card, NDIS plan managed invoice",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": BIZ["street"],
            "addressLocality": BIZ["suburb"],
            "addressRegion": BIZ["region"],
            "postalCode": BIZ["postcode"],
            "addressCountry": BIZ["country"],
        },
        "geo": {"@type": "GeoCoordinates",
                "latitude": BIZ["lat"], "longitude": BIZ["lng"]},
        "hasMap": plain(BIZ["gbp"]),
        "openingHoursSpecification": _opening_hours(),
        "sameAs": [BIZ["facebook"]],
        "areaServed": [{"@type": "City", "name": s, "addressRegion": "QLD",
                        "addressCountry": "AU"} for s in ALL_SUBURBS],
        "knowsAbout": ["Lawn mowing", "NDIS yard maintenance", "NDIS lawn mowing",
                       "Garden maintenance", "Hedge trimming", "Palm tree removal",
                       "Tree removal", "Green waste removal", "Lawn coring",
                       "Lawn top dressing", "Weed control", "Acreage mowing",
                       "Commercial lawn mowing"],
        "hasCredential": {
            "@type": "EducationalOccupationalCredential",
            "credentialCategory": "NDIS registered provider",
            "recognizedBy": {"@type": "GovernmentOrganization",
                             "name": "NDIS Quality and Safeguards Commission"},
        },
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Lawn and garden services — Brisbane south, Bayside, Logan and Redlands",
            "itemListElement": [{
                "@type": "Offer",
                "itemOffered": {
                    "@type": "Service",
                    "name": plain(s["name"]),
                    "url": SITE + svc_url(s["slug"]),
                },
            } for s in SERVICES],
        },
    }


def website_schema():
    return {
        "@type": "WebSite",
        "@id": SITE + "/#website",
        "url": SITE + "/",
        "name": BIZ["name"],
        "publisher": {"@id": SITE + "/#business"},
        "inLanguage": "en-AU",
    }


def breadcrumbs(trail):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [{
            "@type": "ListItem", "position": i + 1, "name": plain(name),
            "item": SITE + url,
        } for i, (name, url) in enumerate(trail)],
    }


def faq_schema(faqs):
    return {
        "@type": "FAQPage",
        "mainEntity": [{
            "@type": "Question",
            "name": plain(q),
            "acceptedAnswer": {"@type": "Answer", "text": plain(a)},
        } for q, a in faqs],
    }


def service_schema(svc):
    return {
        "@type": "Service",
        "@id": SITE + svc_url(svc["slug"]) + "#service",
        "serviceType": plain(svc["name"]),
        "name": plain(svc["h1"]),
        "description": plain(svc["desc"]),
        "url": SITE + svc_url(svc["slug"]),
        "provider": {"@id": SITE + "/#business"},
        "areaServed": [{"@type": "City", "name": s, "addressRegion": "QLD",
                        "addressCountry": "AU"} for s in svc["suburbs"]],
        "audience": {"@type": "Audience", "audienceType": plain(svc["audience"])},
        "offers": {"@type": "Offer", "priceCurrency": "AUD",
                   "availability": "https://schema.org/InStock",
                   "url": SITE + svc_url(svc["slug"])},
    }


def speakable():
    """Voice-assistant hook for the answer-engine work in research section 10."""
    return {"@type": "SpeakableSpecification",
            "cssSelector": [".speakable", ".faq__a"]}


# --------------------------------------------------------------------------
# Layout
# --------------------------------------------------------------------------
NAV = [
    ("Home", "/"),
    ("Services", "/services/"),
    ("Service Areas", "/#areas"),
    ("About", "/about/"),
    ("Contact", "/contact/"),
]


def head(page):
    """page: dict with title, desc, canonical, og_image, schema (list), body_class."""
    schema = {"@context": "https://schema.org", "@graph": page["schema"]}
    robots = page.get("robots", "index, follow, max-image-preview:large, max-snippet:-1")
    return """<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#0f2f1c">
<meta name="author" content="{biz}">
<meta name="geo.region" content="AU-QLD">
<meta name="geo.placename" content="Mount Gravatt, Brisbane">
<meta name="geo.position" content="{lat};{lng}">
<meta name="ICBM" content="{lat}, {lng}">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="en_AU">
<meta property="og:site_name" content="{biz}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og_image}">
<link rel="preconnect" href="https://lh3.googleusercontent.com" crossorigin>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/img/favicon.svg">
<link rel="stylesheet" href="/assets/css/style.css">
<script type="application/ld+json">{schema}</script>
</head>
<body class="{body_class}">
<a class="skip" href="#main">Skip to content</a>
<div class="scrollbar" id="scrollbar" aria-hidden="true"></div>
""".format(title=page["title"], desc=page["desc"], canonical=page["canonical"],
           og_image=page.get("og_image", IMG["hero"]),
           og_type=page.get("og_type", "website"),
           robots=robots, biz=BIZ["name"], lat=BIZ["lat"], lng=BIZ["lng"],
           body_class=page.get("body_class", ""),
           schema=json.dumps(schema, ensure_ascii=False, separators=(",", ":")))


def header(active=""):
    """active: the NAV href of the current page, e.g. "/about/"."""
    # Nested service links. The megamenu panel covers desktop; this list is what
    # shows inside the off-canvas drawer on mobile, where there is no hover.
    sub = "".join('<li><a href="%s">%s%s</a></li>'
                  % (svc_url(s["slug"]), icon(s["icon"], "icon icon--sm"), s["nav"])
                  for s in SERVICES)

    links = []
    for label, href in NAV:
        cls = ' class="is-active" aria-current="page"' if href == active else ""
        if href == "/services/":
            # data-nav is the hook main.js binds the dropdown to — deliberately
            # not a URL, so changing the nav href cannot silently kill it.
            links.append('<li data-nav="services"><a href="%s"%s>%s</a>'
                         '<ul class="nav__sub">%s</ul></li>' % (href, cls, label, sub))
        else:
            links.append('<li><a href="%s"%s>%s</a></li>' % (href, cls, label))

    svc_items = "".join(
        '<li><a href="%s">%s<strong>%s</strong><span>%s</span></a></li>' % (
            svc_url(s["slug"]), icon(s["icon"], "icon icon--sm"), s["nav"], s["tagline"])
        for s in SERVICES)

    return """<div class="topbar">
  <div class="wrap topbar__inner">
    <p>{pin}<span>1593 Logan Rd, Mount Gravatt QLD 4122</span></p>
    <p class="topbar__ndis">{shield}<span>NDIS registered provider</span></p>
    <p><a href="mailto:{email}">{mail}<span>{email}</span></a></p>
  </div>
</div>
<header class="site-header" id="site-header">
  <div class="wrap site-header__inner">
    <a class="brand" href="/" aria-label="{biz} — home">
      <img src="{logo}" alt="{biz} logo" width="52" height="52" loading="eager" decoding="async" fetchpriority="high">
      <span class="brand__txt"><strong>A1 Lawn Care</strong><em>Mount Gravatt · Brisbane</em></span>
    </a>
    <nav class="nav" id="nav" aria-label="Main">
      <ul class="nav__list">
        {links}
      </ul>
      <div class="nav__cta">
        <a class="btn btn--ghost" href="tel:{tel}">{ph_icon}{phone}</a>
        <a class="btn btn--primary" href="/contact/">Get a free quote</a>
      </div>
    </nav>
    <a class="header-call" href="tel:{tel}" aria-label="Call {phone}">{ph_icon}</a>
    <button class="burger" id="burger" aria-expanded="false" aria-controls="nav" aria-label="Open menu">
      <span></span><span></span><span></span>
    </button>
  </div>
  <div class="megamenu" id="megamenu" hidden>
    <div class="wrap megamenu__inner">
      <div class="megamenu__lead">
        <span class="eyebrow">Our services</span>
        <p>Six specialist services across more than 150 suburbs of Brisbane south, Bayside,
           Logan and the Redlands — all from one local crew at Mount Gravatt.</p>
        <a class="link-arrow" href="/services/">See all services {ar}</a>
      </div>
      <ul class="megamenu__grid">{svc}</ul>
    </div>
  </div>
</header>
""".format(biz=BIZ["name"], logo=IMG["logo"], links="\n        ".join(links),
           tel=BIZ["phone_e164"], phone=BIZ["phone_display"], svc=svc_items,
           email=BIZ["email"], ph_icon=icon("phone", "icon icon--sm"),
           pin=icon("pin", "icon icon--xs"), shield=icon("shield", "icon icon--xs"),
           mail=icon("mail", "icon icon--xs"), ar=icon("arrow", "icon icon--sm"))


def footer():
    svc_links = "".join('<li><a href="%s">%s</a></li>' % (svc_url(s["slug"]), s["name"])
                        for s in SERVICES)
    areas = "".join('<li>%s</li>' % s for s in ALL_SUBURBS)
    hours = "".join('<div class="hours__row"><span>%s</span><span>%s – %s</span></div>'
                    % (label, o.lstrip("0"), c.lstrip("0"))
                    for _, o, c, label in BIZ["hours"])
    return """<footer class="site-footer">
  <div class="wrap">
    <div class="site-footer__top">
      <div class="site-footer__brand">
        <a class="brand brand--footer" href="/">
          <img src="{logo}" alt="{biz} logo" width="56" height="56" loading="lazy" decoding="async">
          <span class="brand__txt"><strong>A1 Lawn Care</strong><em>Pty Ltd · Mount Gravatt</em></span>
        </a>
        <p class="site-footer__blurb speakable">{citable}</p>
        <img class="site-footer__ndis" src="{ndis}" width="150" height="60" loading="lazy" decoding="async"
             alt="NDIS registered provider — A1 Lawn Care, Brisbane lawn mowing and yard maintenance">
        <div class="site-footer__social">
          <a href="{fb}" rel="noopener" target="_blank">Facebook</a>
          <a href="{gbp}" rel="noopener" target="_blank">Find us on Google Maps</a>
        </div>
      </div>
      <div class="site-footer__col">
        <h2>Services</h2>
        <ul>{svc}</ul>
      </div>
      <div class="site-footer__col">
        <h2>Company</h2>
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/about/">About A1 Lawn Care</a></li>
          <li><a href="/services/">All services</a></li>
          <li><a href="/#areas">Service areas</a></li>
          <li><a href="/#faq">Questions answered</a></li>
          <li><a href="/contact/">Contact &amp; free quote</a></li>
        </ul>
      </div>
      <div class="site-footer__col site-footer__contact">
        <h2>Get in touch</h2>
        <address class="speakable">
          <a class="site-footer__phone" href="tel:{tel}">{phone}</a>
          <a href="mailto:{email}">{email}</a>
          <span><strong>{biz}</strong><br>{street}<br>{sub} {reg} {pc}</span>
        </address>
        <div class="hours">{hours}</div>
        <p class="hours__note">{hnote}</p>
      </div>
    </div>
    <div class="site-footer__areas">
      <h2>Suburbs we service</h2>
      <ul>{areas}</ul>
    </div>
    <div class="site-footer__base">
      <p>&copy; <span id="year">2026</span> {biz}. {abn}</p>
      <p>Lawn mowing services Brisbane · NDIS mowing · Garden maintenance Brisbane ·
         Palm tree removal Brisbane · Green waste removal Brisbane · Hedge trimming Brisbane southside</p>
    </div>
  </div>
</footer>
<a class="callbar" href="tel:{tel}">
  {ph_icon}<span>Call {phone}</span><em>Free quote · NDIS registered</em>
</a>
<button class="totop" id="totop" type="button" aria-label="Back to top">{up}</button>
<script src="/assets/js/main.js" defer></script>
<script src="https://link.msgsndr.com/js/external-tracking.js" data-tracking-id="{track}"></script>
</body>
</html>
""".format(biz=BIZ["name"], logo=IMG["logo"], svc=svc_links, areas=areas,
           tel=BIZ["phone_e164"], phone=BIZ["phone_display"], email=BIZ["email"],
           street=BIZ["street"], sub=BIZ["suburb"], reg=BIZ["region"], pc=BIZ["postcode"],
           hours=hours, hnote=BIZ["hours_note"], fb=BIZ["facebook"], gbp=BIZ["gbp"],
           citable=CITABLE, ndis=IMG["ndis"], abn=BIZ["abn_note"], track=TRACKING_ID,
           ph_icon=icon("phone", "icon icon--sm"),
           up='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
              'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
              '<path d="M12 19V5M5 12l7-7 7 7"/></svg>')


# --------------------------------------------------------------------------
# Components
# --------------------------------------------------------------------------
def section_head(eyebrow, title, intro, centred=True, level=2):
    return """<div class="section__head{cls} reveal">
      <span class="eyebrow">{eyebrow}</span>
      <h{lv}>{title}</h{lv}>
      <p>{intro}</p>
    </div>""".format(cls=" section__head--center" if centred else "", eyebrow=eyebrow,
                     title=title, intro=intro, lv=level)


def quote_form(form_id="quote-form", preselect=None, heading=None, compact=False):
    rows = []
    for name, label, merge, kind, required, placeholder, options in FORM_FIELDS:
        req = ' required' if required else ''
        star = ' <span class="req" aria-hidden="true">*</span>' if required else ''
        wide = ' field--wide' if kind == "textarea" else ''
        if kind == "select":
            opts = ['<option value="">Please select…</option>']
            for o in options:
                sel = ' selected' if preselect and plain(o) == plain(preselect) else ''
                opts.append('<option value="%s"%s>%s</option>' % (plain(o), sel, o))
            control = ('<select id="%s-%s" name="%s" data-ghl="%s"%s>%s</select>'
                       % (form_id, name, name, merge, req, "".join(opts)))
        elif kind == "textarea":
            control = ('<textarea id="%s-%s" name="%s" data-ghl="%s" rows="4" '
                       'placeholder="%s"%s></textarea>'
                       % (form_id, name, name, merge, placeholder, req))
        else:
            auto = {"full_name": "name", "email": "email", "phone": "tel",
                    "property_address": "street-address"}.get(name, "on")
            control = ('<input type="%s" id="%s-%s" name="%s" data-ghl="%s" '
                       'autocomplete="%s" placeholder="%s"%s>'
                       % (kind, form_id, name, name, merge, auto, placeholder, req))
        rows.append('<div class="field%s"><label for="%s-%s">%s%s</label>%s</div>'
                    % (wide, form_id, name, label, star, control))

    head_html = ""
    if heading:
        head_html = ('<div class="quote__head"><h2>%s</h2>'
                     '<p>Tell us about the property and we will come back with a price — '
                     'usually the same day. NDIS plan managed invoicing available.</p></div>'
                     % heading)

    return """<div class="quote{cls}">
  {head}
  <!-- method="get" is the no-JS fallback only: a native POST to a static page is
       a 405 on most static hosts. With JS the submit is intercepted, so no field
       value ever reaches the URL. Lead capture is handled by the GoHighLevel
       tracking script — see assets/js/main.js. -->
  <form class="quote__form" id="{fid}" method="get" action="/thank-you/" novalidate>
    <div class="quote__grid">
      {rows}
    </div>
    <div class="quote__consent">
      <p>By sending this you agree we can contact you about your quote. No spam, no shared data.</p>
    </div>
    <button type="submit" class="btn btn--primary btn--block">
      <span class="btn__label">Get my free quote</span>
      <span class="btn__spin" aria-hidden="true"></span>
    </button>
    <p class="quote__alt">Prefer to talk? Call <a href="tel:{tel}">{phone}</a> — you will get
      {owner}, not a call centre.</p>
    <p class="quote__error" role="alert" hidden></p>
  </form>
</div>""".format(cls=" quote--compact" if compact else "", head=head_html, fid=form_id,
                 rows="\n      ".join(rows), tel=BIZ["phone_e164"],
                 phone=BIZ["phone_display"], owner=BIZ["owner"].split()[0])


def map_embed(title="A1 Lawn Care, 1593 Logan Rd Mount Gravatt, on Google Maps"):
    return """<div class="mapwrap reveal">
  <iframe src="{src}" title="{title}" width="600" height="450"
          style="border:0" allowfullscreen loading="lazy"
          referrerpolicy="strict-origin-when-cross-origin"></iframe>
</div>""".format(src=MAP_EMBED, title=title)


def faq_block(faqs, title="Frequently asked questions",
              intro="The questions we get asked most, answered straight — no hedging.",
              eyebrow="Answers"):
    items = []
    for i, (q, a) in enumerate(faqs):
        items.append("""<details class="faq"{open}>
      <summary class="faq__q"><span>{q}</span>{chev}</summary>
      <div class="faq__a"><p>{a}</p></div>
    </details>""".format(q=q, a=a, open=" open" if i == 0 else "",
                         chev='<svg class="faq__chev" viewBox="0 0 24 24" fill="none" '
                              'stroke="currentColor" stroke-width="2" stroke-linecap="round" '
                              'aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>'))
    return """<section class="section section--faq" id="faq">
  <div class="wrap wrap--narrow">
    {head}
    <div class="faqs reveal">
      {items}
    </div>
  </div>
</section>""".format(head=section_head(eyebrow, title, intro), items="\n      ".join(items))


def areas_section(heading="Where we mow across Brisbane",
                  intro=None, eyebrow=None):
    intro = intro or ("More than 150 suburbs across four regions, all run out of Mount Gravatt. "
                      "These are the ones we are in most weeks — if you are nearby and not "
                      "listed, ring and ask.")
    cards = []
    for i, (name, blurb, subs) in enumerate(AREA_GROUPS):
        chips = "".join('<li>%s</li>' % s for s in subs)
        cards.append("""<article class="area reveal" style="--d:%dms">
        <h3>%s <span class="area__count">%d suburbs</span></h3>
        <p>%s</p>
        <ul class="chips">%s</ul>
      </article>""" % (i * 70, name, len(subs), blurb, chips))
    return """<section class="section section--areas" id="areas">
  <div class="wrap">
    {head}
    <div class="areas">
      <div class="areas__list">
        {cards}
      </div>
      <div class="areas__map">
        {map}
        <div class="areas__card reveal">
          <p class="areas__addr"><strong>{biz}</strong><br>{street}<br>{sub} {reg} {pc}</p>
          <p class="areas__note">Every job is run from the Logan Rd depot — no travel
             surcharge inside the suburbs listed here.</p>
          <a class="btn btn--ghost btn--sm" href="{gbp}" target="_blank" rel="noopener">Open in Google Maps</a>
        </div>
      </div>
    </div>
  </div>
</section>""".format(head=section_head(eyebrow or (icon("pin", "icon icon--sm") + " Service areas"),
                                       heading, intro),
                     cards="\n        ".join(cards), map=map_embed(), biz=BIZ["name"],
                     street=BIZ["street"], sub=BIZ["suburb"], reg=BIZ["region"],
                     pc=BIZ["postcode"], gbp=BIZ["gbp"])


def marquee(items=None):
    """Single-row suburb ticker. The list is duplicated so the loop is seamless."""
    items = items or ALL_SUBURBS
    run = "".join('<li>%s</li>' % s for s in items)
    return """<div class="marquee" aria-hidden="true">
  <ul class="marquee__run">{run}</ul>
  <ul class="marquee__run">{run}</ul>
</div>""".format(run=run)


def cta_band(title=None, text=None, img=None):
    title = title or "Get your lawn back on a schedule"
    text = text or ("A free quote, an honest answer about when we can actually get there, and "
                    "no obligation to book. NDIS plan managed invoicing available.")
    return """<section class="cta" style="--cta-img:url('{img}')">
  <div class="wrap cta__inner reveal">
    <div class="cta__copy">
      <h2>{title}</h2>
      <p>{text}</p>
    </div>
    <div class="cta__actions">
      <a class="btn btn--primary btn--lg" href="/contact/">Get a free quote</a>
      <a class="btn btn--outline btn--lg" href="tel:{tel}">{ph}{phone}</a>
    </div>
  </div>
</section>""".format(img=img or IMG["cta"], title=title, text=text,
                     tel=BIZ["phone_e164"], phone=BIZ["phone_display"],
                     ph=icon("phone", "icon icon--sm"))


def gallery_section(items, title="Our recent work",
                    intro=("Real lawns, real clean-ups, real blocks across Brisbane&#39;s south "
                           "side, Bayside, Logan and the Redlands."),
                    feature=True):
    """feature=True makes the first tile a 2x2 hero.

    The grid is 4 columns, so a featured tile consumes 4 cells: pass a count that
    fills whole rows (8 items featured, or 4/8 unfeatured) or the last row is
    left with a hole.
    """
    cells = []
    for i, (src, alt) in enumerate(items):
        cells.append('<figure class="shot%s reveal" style="--d:%dms">'
                     '<img src="%s" alt="%s" loading="lazy" decoding="async" '
                     'width="900" height="675"></figure>'
                     % (" shot--feature" if (feature and i == 0) else "", i * 60, src, alt))
    return """<section class="section section--work" id="work">
  <div class="wrap">
    {head}
    <div class="shots">
      {cells}
    </div>
  </div>
</section>""".format(head=section_head("Our recent work", title, intro),
                     cells="\n      ".join(cells))


def stats_strip():
    cells = []
    for i, (num, suffix, label, note) in enumerate(STATS):
        cells.append("""<div class="stat reveal" style="--d:%dms">
        <strong><span class="count" data-count="%s">%s</span>%s</strong>
        <span class="stat__label">%s</span>
        <span class="stat__note">%s</span>
      </div>""" % (i * 80, num, num, suffix, label, note))
    return """<section class="stats">
  <div class="wrap stats__inner">
      {cells}
  </div>
</section>""".format(cells="\n      ".join(cells))


def ndis_band():
    """Research: 'Add an NDIS trust strip above the fold.'"""
    return """<section class="ndis-band">
  <div class="wrap ndis-band__inner reveal">
    <img src="{ndis}" width="132" height="54" loading="eager" decoding="async"
         alt="NDIS registered provider logo — A1 Lawn Care Brisbane">
    <div class="ndis-band__copy">
      <h2>An NDIS registered provider for lawn mowing and yard maintenance</h2>
      <p class="speakable">A1 Lawn Care Pty Ltd is an NDIS registered provider. We work with
         plan managed, self managed and NDIA managed participants across Brisbane&#39;s south
         side, Bayside, Logan and the Redlands, and we invoice plan managers directly.</p>
    </div>
    <a class="btn btn--outline" href="/services/ndis-yard-garden-maintenance/">NDIS services {ar}</a>
  </div>
</section>""".format(ndis=IMG["ndis_white"], ar=icon("arrow", "icon icon--sm"))


def service_cards(services=None, limit=None):
    services = services or SERVICES
    if limit:
        services = services[:limit]
    cards = []
    for i, s in enumerate(services):
        cards.append("""<article class="card reveal" style="--d:{d}ms">
        <a class="card__link" href="{url}">
          <span class="card__media">
            <img src="{img}" alt="{alt}" loading="lazy" decoding="async" width="800" height="600">
          </span>
          <span class="card__body">
            <span class="card__icon">{icon}</span>
            <h3>{name}</h3>
            <p>{tag}</p>
            <span class="card__kw">{kw}</span>
            <span class="link-arrow">Read more {ar}</span>
          </span>
        </a>
      </article>""".format(d=i * 70, url=svc_url(s["slug"]), img=IMG[s["img"]],
                           alt="%s in Brisbane by A1 Lawn Care — %s"
                               % (plain(s["name"]), plain(s["suburbs"][0])),
                           icon=icon(s["icon"]), name=s["name"], tag=s["tagline"],
                           kw=plain(s["keyword"]).title(),
                           ar=icon("arrow", "icon icon--sm")))
    return "\n      ".join(cards)


def crumbs(trail):
    parts = []
    for i, (name, url) in enumerate(trail):
        if i == len(trail) - 1:
            parts.append('<li aria-current="page">%s</li>' % name)
        else:
            parts.append('<li><a href="%s">%s</a></li>' % (url, name))
    return ('<nav class="crumbs" aria-label="Breadcrumb"><div class="wrap"><ol>%s</ol></div></nav>'
            % "".join(parts))
