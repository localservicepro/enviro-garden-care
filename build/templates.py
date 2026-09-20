# -*- coding: utf-8 -*-
"""Shared layout, schema and component templates."""

import json
import re
from data import (SITE, BIZ, MAP_EMBED, TRACKING_ID, IMG, SERVICES, ALL_SUBURBS,
                  AREA_GROUPS, FORM_FIELDS, CITABLE, PRICE, RANGE, RANGE_TAIL)


def plain(html):
    """Strip tags/entities so marked-up copy can be reused in meta and JSON-LD."""
    txt = re.sub(r"<[^>]+>", "", html)
    for a, b in (("&amp;", "&"), ("&nbsp;", " "), ("&mdash;", "—"), ("&#39;", "'")):
        txt = txt.replace(a, b)
    return re.sub(r"\s+", " ", txt).strip()


def page_url(path=""):
    """Root-relative URL for a page.

    Pages are written as directory indexes (about/index.html) so the site has
    extensionless URLs on any static host with no rewrite rules:
        page_url("")                      -> "/"
        page_url("about")                 -> "/about/"
        page_url("services/lawn-mowing")  -> "/services/lawn-mowing/"
    """
    path = path.strip("/")
    return "/" + (path + "/" if path else "")


def svc_url(slug):
    return page_url("services/" + slug)


# --------------------------------------------------------------------------
# Icons (inline SVG, currentColor)
# --------------------------------------------------------------------------
ICONS = {
    "mower": '<path d="M3 17h7l2-4h6"/><circle cx="6" cy="19" r="2.4"/><circle cx="18" cy="19" r="2.4"/><path d="M12 13V5h6"/>',
    "tractor": '<path d="M4 17h5m4 0h7"/><circle cx="7" cy="17" r="3.2"/><circle cx="18" cy="17" r="2.6"/><path d="M4 13V7h6l3 6"/>',
    "shears": '<circle cx="6" cy="18" r="2.4"/><circle cx="18" cy="18" r="2.4"/><path d="M7.7 16.3 18 4M16.3 16.3 6 4"/>',
    "truck": '<path d="M2 7h11v9H2zM13 10h4.5l3 3.2V16H13z"/><circle cx="6.5" cy="18" r="1.8"/><circle cx="17" cy="18" r="1.8"/>',
    "building": '<path d="M4 20V5a1 1 0 0 1 1-1h9a1 1 0 0 1 1 1v15M15 10h4a1 1 0 0 1 1 1v9M2 20h20"/><path d="M8 8h3M8 12h3M8 16h3"/>',
    "tools": '<path d="M14.5 6.5a3.5 3.5 0 0 0 4.6 4.6l-8.2 8.2a2.3 2.3 0 0 1-3.2-3.2z"/><path d="M6 3l3 3-2 2-3-3z"/>',
    "leaf": '<path d="M4 20c0-8 6-14 16-15 0 11-6 16-13 16H4z"/><path d="M6 18c3-5 7-8 11-9"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.2 2"/>',
    "shield": '<path d="M12 3l7 3v5.5c0 4.4-3 8-7 9.5-4-1.5-7-5.1-7-9.5V6z"/><path d="m9 12 2 2 4-4"/>',
    "pin": '<path d="M12 21s7-5.6 7-11a7 7 0 1 0-14 0c0 5.4 7 11 7 11z"/><circle cx="12" cy="10" r="2.6"/>',
    "phone": '<path d="M6 3h3l2 5-2.4 1.4a12 12 0 0 0 6 6L16 13l5 2v3a2 2 0 0 1-2.2 2A17 17 0 0 1 4 5.2 2 2 0 0 1 6 3z"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 7 8.5 6 8.5-6"/>',
    "star": '<path d="m12 3.5 2.6 5.6 6 .8-4.4 4.2 1.1 6-5.3-2.9-5.3 2.9 1.1-6L3.4 9.9l6-.8z"/>',
    "check": '<path d="m4 12.5 5 5L20 6.5"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "home": '<path d="M3 11.5 12 4l9 7.5"/><path d="M5.5 10v9.5h13V10"/><path d="M10 19.5v-5h4v5"/>',
    "camera": '<path d="M4 8h3l1.5-2h7L17 8h3v11H4z"/><circle cx="12" cy="13" r="3.2"/>',
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
    return {
        "@type": ["LocalBusiness", "HomeAndConstructionBusiness"],
        "@id": SITE + "/#business",
        "name": BIZ["name"],
        "alternateName": "Enviro Garden Care",
        "description": plain(CITABLE),
        "url": SITE + "/",
        "telephone": BIZ["phone_e164"],
        "email": BIZ["email"],
        "image": IMG["hero"],
        "logo": IMG["logo"],
        "priceRange": "$$",
        "currenciesAccepted": "AUD",
        # CD r94 (awaiting client): street kept in hidden schema only so the NAP
        # matches the Google Business Profile. Toggle in data.py.
        "address": dict(
            [("@type", "PostalAddress")]
            + ([("streetAddress", BIZ["street"])] if BIZ["show_street_in_schema"] else [])
            + [("addressLocality", BIZ["suburb"]),
               ("addressRegion", BIZ["region"]),
               ("postalCode", BIZ["postcode"]),
               ("addressCountry", BIZ["country"])]),
        "geo": {"@type": "GeoCoordinates",
                "latitude": BIZ["lat"], "longitude": BIZ["lng"]},
        "hasMap": BIZ["gbp"],
        "openingHoursSpecification": _opening_hours(),
        "sameAs": [BIZ["facebook"], BIZ["gbp"]],
        "areaServed": [{"@type": "City", "name": s, "addressRegion": "QLD",
                        "addressCountry": "AU"} for s in ALL_SUBURBS],
        "knowsAbout": ["Lawn mowing", "Acreage mowing", "Ride-on mowing",
                       "Garden maintenance", "Hedge trimming", "Weed control",
                       "Green waste removal", "Commercial grounds maintenance",
                       "Odd jobs and minor handyman repairs"],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Lawn and garden services — Northern Gold Coast",
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
    """page: dict with title, desc, canonical, og_image, schema(list), body_class"""
    schema = {"@context": "https://schema.org", "@graph": page["schema"]}
    return """<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="theme-color" content="#143d2a">
<meta name="geo.region" content="AU-QLD">
<meta name="geo.placename" content="Pimpama, Gold Coast">
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
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://lh3.googleusercontent.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700;9..144,800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/img/favicon.svg">
<link rel="stylesheet" href="/assets/css/style.css">
<script type="application/ld+json">{schema}</script>
</head>
<body class="{body_class}">
<a class="skip" href="#main">Skip to content</a>
""".format(title=page["title"], desc=page["desc"], canonical=page["canonical"],
           og_image=page.get("og_image", IMG["hero"]),
           og_type=page.get("og_type", "website"),
           biz=BIZ["name"], lat=BIZ["lat"], lng=BIZ["lng"],
           body_class=page.get("body_class", ""),
           schema=json.dumps(schema, ensure_ascii=False, separators=(",", ":")))


def header(active=""):
    """active: the NAV href of the current page, e.g. "/about/"."""
    # Nested service links. Hidden on desktop (the megamenu panel covers that);
    # shown inside the off-canvas drawer on mobile, where there is no hover.
    sub = "".join('<li><a href="%s">%s%s</a></li>'
                  % (svc_url(s["slug"]), icon(s["icon"], "icon icon--sm"), s["nav"])
                  for s in SERVICES)

    links = []
    for label, href in NAV:
        is_active = (href == active)
        cls = ' class="is-active" aria-current="page"' if is_active else ""
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

    return """<header class="site-header" id="site-header">
  <div class="wrap site-header__inner">
    <a class="brand" href="/" aria-label="{biz} — home">
      <img src="{logo}" alt="{biz} logo" width="44" height="44" loading="eager" decoding="async">
      <span class="brand__txt"><strong>Enviro Garden Care</strong><em>&amp; Odd Jobs · Pimpama</em></span>
    </a>
    <nav class="nav" id="nav" aria-label="Main">
      <ul class="nav__list">
        {links}
      </ul>
      <div class="nav__cta">
        <a class="btn btn--ghost" href="tel:{tel}">{ph_icon}{phone}</a>
        <a class="btn btn--primary" href="/contact/">Get a free estimate</a>
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
        <p>Lawn, garden and grounds care from Parkwood to Windaroo and all suburbs in between — plus the odd jobs we fit in through the quieter months.</p>
        <a class="link-arrow" href="/services/">See all services {ar}</a>
      </div>
      <ul class="megamenu__grid">{svc}</ul>
    </div>
  </div>
</header>
""".format(biz=BIZ["name"], logo=IMG["logo"], links="\n        ".join(links),
           tel=BIZ["phone_e164"], phone=BIZ["phone_display"], svc=svc_items,
           ph_icon=icon("phone", "icon icon--sm"), ar=icon("arrow", "icon icon--sm"))


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
          <img src="{logo}" alt="{biz} logo" width="48" height="48" loading="lazy" decoding="async">
          <span class="brand__txt"><strong>Enviro Garden Care</strong><em>&amp; Odd Jobs</em></span>
        </a>
        <p class="site-footer__blurb">{citable}</p>
        <div class="site-footer__social">
          <a href="{fb}" rel="noopener" target="_blank">Facebook</a>
          <a href="{gbp}" rel="noopener" target="_blank">Google Business Profile</a>
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
          <li><a href="/about/">About us</a></li>
          <li><a href="/services/">All services</a></li>
          <li><a href="/#areas">Service areas</a></li>
          <li><a href="/contact/">Contact &amp; quotes</a></li>
        </ul>
      </div>
      <div class="site-footer__col site-footer__contact">
        <h2>Get in touch</h2>
        <address>
          <a class="site-footer__phone" href="tel:{tel}">{phone}</a>
          <a href="mailto:{email}">{email}</a>
          <span>{sub} {reg} {pc}</span>
        </address>
        <div class="hours">{hours}</div>{hnote}
      </div>
    </div>
    <div class="site-footer__areas">
      <h2>Areas we service</h2>
      <ul>{areas}</ul>
      <p class="site-footer__areas-note">Parkwood to Windaroo and all suburbs in between.</p>
    </div>
    <div class="site-footer__base">
      <p>&copy; <span id="year">2026</span> {biz}. All rights reserved. ABN available on request.</p>
      <p>Lawn mowing Gold Coast · Acreage mowing · Garden maintenance · Northern Gold Coast</p>
    </div>
  </div>
</footer>
<a class="callbar" href="tel:{tel}">
  {ph_icon}<span>Call {phone}</span><em>Free estimate · Mon–Sat</em>
</a>
<script src="/assets/js/main.js" defer></script>
<script src="https://link.msgsndr.com/js/external-tracking.js" data-tracking-id="{track}"></script>
</body>
</html>
""".format(biz=BIZ["name"], logo=IMG["logo"], svc=svc_links, areas=areas,
           tel=BIZ["phone_e164"], phone=BIZ["phone_display"], email=BIZ["email"],
           street=BIZ["street"], sub=BIZ["suburb"], reg=BIZ["region"], pc=BIZ["postcode"],
           hours=hours,
           hnote=('\n        <p class="hours__note">%s</p>' % BIZ["hours_note"]) if BIZ["hours_note"] else "",
           fb=BIZ["facebook"], gbp=BIZ["gbp"],
           citable=("A Pimpama-based, family-owned lawn mowing and garden maintenance business "
                    "servicing the Northern Gold Coast from Parkwood to Windaroo and all "
                    "suburbs in between."),
           track=TRACKING_ID, ph_icon=icon("phone", "icon icon--sm"))


# --------------------------------------------------------------------------
# Components
# --------------------------------------------------------------------------
def quote_form(form_id="quote-form", compact=False, preselect=None, heading=None):
    rows = []
    for name, label, merge, kind, required, placeholder, options in FORM_FIELDS:
        req = ' required' if required else ''
        star = ' <span class="req" aria-hidden="true">*</span>' if required else ''
        wide = ' field--wide' if kind == "textarea" or name == "property_address" else ''
        if kind == "select":
            opts = ['<option value="">Please select…</option>']
            for o in options:
                sel = ' selected' if preselect and plain(o) == plain(preselect) else ''
                opts.append('<option value="%s"%s>%s</option>' % (plain(o), sel, o))
            control = ('<select id="%s-%s" name="%s" data-ghl="%s"%s>%s</select>'
                       % (form_id, name, name, merge, req, "".join(opts)))
        elif kind == "file":
            # CD r20. Rendered hidden until main.js confirms an upload endpoint is
            # configured; otherwise a "text or email your photos" line shows instead,
            # because the tracking script cannot carry files.
            control = ('<input type="file" id="%s-%s" name="%s" data-ghl="%s" '
                       'accept="image/*" multiple data-max-files="6" data-max-mb="8">'
                       '<span class="field__hint">%s</span>'
                       '<div class="field__thumbs" aria-live="polite"></div>'
                       % (form_id, name, name, merge, placeholder))
            rows.append('<div class="field field--wide field--file" hidden>'
                        '<label for="%s-%s">%s</label>%s</div>'
                        % (form_id, name, label, control))
            rows.append('<div class="field field--wide field--photos-alt">'
                        '<p>%s <strong>Have photos of the property?</strong> Text them to '
                        '<a href="sms:%s">%s</a> or email <a href="mailto:%s">%s</a> after you '
                        'send this — it helps us get the price right.</p></div>'
                        % (icon("camera", "icon icon--sm"), BIZ["phone_e164"],
                           BIZ["phone_display"], BIZ["email"], BIZ["email"]))
            continue
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
                     '<p>Tell us about the property and we will come back with %s — '
                     'usually the same day.</p></div>' % (heading, PRICE))

    return """<div class="quote{cls}">
  {head}
  <!-- method="get" is the no-JS fallback only: a native POST to a static page
       is a 405 on most static hosts. With JS the submit is intercepted, so no
       field values ever reach the URL. Capture is handled by the GHL tracking
       script — see assets/js/main.js. -->
  <form class="quote__form" id="{fid}" method="get" action="/thank-you/" novalidate>
    <div class="quote__grid">
      {rows}
    </div>
    <div class="quote__consent">
      <p>By sending this you agree we can contact you about your estimate. No spam, no shared data.</p>
    </div>
    <button type="submit" class="btn btn--primary btn--block">
      <span class="btn__label">Get my free estimate</span>
      <span class="btn__spin" aria-hidden="true"></span>
    </button>
    <p class="quote__alt">Prefer to talk? Call <a href="tel:{tel}">{phone}</a> — you will get {owner}, not a call centre.</p>
    <p class="quote__fine">Every price is approximate and confirmed on inspection.</p>
    <p class="quote__error" role="alert" hidden></p>
  </form>
</div>""".format(cls=" quote--compact" if compact else "", head=head_html, fid=form_id,
                 rows="\n      ".join(rows), tel=BIZ["phone_e164"],
                 phone=BIZ["phone_display"], owner=BIZ["owner"].split()[0])


def map_embed(title="Enviro Garden Care & Odd Jobs on Google Maps"):
    return """<div class="mapwrap reveal">
  <iframe src="{src}" title="{title}" width="600" height="450"
          style="border:0" allowfullscreen loading="lazy"
          referrerpolicy="strict-origin-when-cross-origin"></iframe>
</div>""".format(src=MAP_EMBED, title=title)


def faq_block(faqs, title="Frequently asked questions",
              intro="The questions we get asked most, answered straight."):
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
  <div class="wrap">
    <div class="section__head reveal">
      <span class="eyebrow">{eyebrow}</span>
      <h2>{title}</h2>
      <p>{intro}</p>
    </div>
    <div class="faqs reveal">
      {items}
    </div>
  </div>
</section>""".format(title=title, intro=intro, eyebrow="Answers", items="\n      ".join(items))


def areas_section(heading="Where we mow on the Northern Gold Coast", intro=None):
    intro = intro or ("Nineteen named suburbs, one truck, no travel surcharge. We work the "
                      "Northern Gold Coast from Windaroo down to Parkwood, and any suburb in "
                      "between — if you are on this list, you are covered.")
    cards = []
    for name, blurb, subs in AREA_GROUPS:
        chips = "".join('<li>%s</li>' % s for s in subs)
        cards.append("""<article class="area reveal">
        <h3>%s</h3>
        <p>%s</p>
        <ul class="chips">%s</ul>
      </article>""" % (name, blurb, chips))
    return """<section class="section section--areas" id="areas">
  <div class="wrap">
    <div class="section__head reveal">
      <span class="eyebrow">{pin} Service areas</span>
      <h2>{heading}</h2>
      <p>{intro}</p>
    </div>
    <div class="areas">
      <div class="areas__list">
        {cards}
        <p class="areas__tail reveal">…and any suburb in between Parkwood and Windaroo. Not sure? Ring — we probably drive past you.</p>
      </div>
      <div class="areas__map">
        {map}
        <div class="areas__card reveal">
          <p class="areas__addr"><strong>{biz}</strong><br>Based in {sub} {reg} {pc}</p>
          <a class="btn btn--ghost btn--sm" href="{gbp}" target="_blank" rel="noopener">Open in Google Maps</a>
        </div>
      </div>
    </div>
  </div>
</section>""".format(heading=heading, intro=intro, cards="\n        ".join(cards),
                     map=map_embed(), biz=BIZ["name"],
                     sub=BIZ["suburb"], reg=BIZ["region"], pc=BIZ["postcode"],
                     gbp=BIZ["gbp"], pin=icon("pin", "icon icon--sm"))


def cta_band(title=None, text=None):
    title = title or "Get your lawn back on a schedule"
    text = text or ("Free estimate, no obligation — an approximate price pending inspection, "
                    "and an honest answer about when we can actually get there.")
    return """<section class="cta" style="--cta-img:url('{img}')">
  <div class="wrap cta__inner reveal">
    <div>
      <h2>{title}</h2>
      <p>{text}</p>
    </div>
    <div class="cta__actions">
      <a class="btn btn--primary btn--lg" href="/contact/">Get a free estimate</a>
      <a class="btn btn--outline btn--lg" href="tel:{tel}">{ph}{phone}</a>
    </div>
  </div>
</section>""".format(img=IMG["cta"], title=title, text=text,
                     tel=BIZ["phone_e164"], phone=BIZ["phone_display"],
                     ph=icon("phone", "icon icon--sm"))


def gallery_section(items, title="Our recent work",
                    intro="Real lawns, real blocks, real clean-ups across the northern Gold Coast.",
                    feature=False):
    """feature=True makes the first tile a 2x2 hero.

    The grid is 4 columns, so a featured tile consumes 4 cells. Pass a count
    that fills whole rows (9 items featured, or 4/8 items unfeatured) or the
    last row will be left with a hole.
    """
    cells = []
    for i, (src, alt) in enumerate(items):
        cells.append('<figure class="shot%s reveal" style="--d:%dms">'
                     '<img src="%s" alt="%s" loading="lazy" decoding="async" '
                     'width="900" height="675"></figure>'
                     % (" shot--feature" if (feature and i == 0) else "", i * 60, src, alt))
    return """<section class="section section--work" id="work">
  <div class="wrap">
    <div class="section__head reveal">
      <span class="eyebrow">Our recent work</span>
      <h2>{title}</h2>
      <p>{intro}</p>
    </div>
    <div class="shots">
      {cells}
    </div>
  </div>
</section>""".format(title=title, intro=intro, cells="\n      ".join(cells))


def crumbs(trail):
    parts = []
    for i, (name, url) in enumerate(trail):
        if i == len(trail) - 1:
            parts.append('<li aria-current="page">%s</li>' % name)
        else:
            parts.append('<li><a href="%s">%s</a></li>' % (url, name))
    return ('<nav class="crumbs" aria-label="Breadcrumb"><div class="wrap"><ol>%s</ol></div></nav>'
            % "".join(parts))
