# -*- coding: utf-8 -*-
"""Page bodies. Copy follows the SEO research spec in build/seo-research-source.html."""

from data import (SITE, BIZ, IMG, SERVICES, ALL_SUBURBS, HOME_FAQS, CITABLE, CITABLE_ABOUT, GOOGLE_RATING, REVIEWS,
                  GALLERY_HOME, GALLERY_ABOUT, GALLERY_BY_SERVICE, PRICE, FREQ)
from templates import (head, header, footer, icon, quote_form, map_embed, faq_block,
                       areas_section, cta_band, gallery_section, crumbs, plain,
                       local_business_schema, website_schema, breadcrumbs,
                       faq_schema, service_schema, speakable, page_url, svc_url)

TEL = BIZ["phone_e164"]
PHONE = BIZ["phone_display"]


def _trust_bar():
    items = [
        ("home", "Family owned &amp; run", "Shanon does the mowing, not a franchise crew"),
        ("pin", "Based in Pimpama", "Parkwood to Windaroo and all suburbs in between"),
        ("clock", "Fortnightly or one-off", "No lock-in contracts, three-weekly through winter"),
        ("shield", "Fully insured", "Public liability cover on every job"),
    ]
    cells = "".join(
        '<li class="trust__item reveal" style="--d:%dms">%s<div><strong>%s</strong>'
        '<span>%s</span></div></li>' % (i * 70, icon(k), t, d)
        for i, (k, t, d) in enumerate(items))
    return '<section class="trust"><div class="wrap"><ul class="trust__list">%s</ul></div></section>' % cells


def _service_cards(featured=None):
    cards = []
    for i, s in enumerate(SERVICES):
        if featured and s["slug"] == featured:
            continue
        cards.append("""<article class="svc reveal" style="--d:{d}ms">
        <a class="svc__link" href="{url}">
          <div class="svc__media">
            <img src="{img}" alt="{alt}" loading="lazy" decoding="async" width="1200" height="800">
          </div>
          <div class="svc__body">
            <span class="svc__icon">{ic}</span>
            <h3>{name}</h3>
            <p>{tag}</p>
            <span class="link-arrow">{kw} {ar}</span>
          </div>
        </a>
      </article>""".format(
            d=i * 70, url=svc_url(s["slug"]), img=IMG[s["img"]],
            alt="%s — %s by Enviro Garden Care &amp; Odd Jobs, Northern Gold Coast" % (
                plain(s["name"]), plain(s["keyword"])),
            ic=icon(s["icon"]), name=s["name"], tag=s["tagline"],
            kw=s["keyword"].title() if s["keyword"].islower() else s["keyword"],
            ar=icon("arrow", "icon icon--sm")))
    return "\n      ".join(cards)


# ==========================================================================
# HOME
# ==========================================================================
def home():
    page = {
        "title": "Lawn Mowing Gold Coast | Enviro Garden Care &amp; Odd Jobs",
        "desc": ("Reliable lawn mowing Gold Coast north, Parkwood to Windaroo and all suburbs in "
                 "between. Acreage mowing, hedges, garden care. Family owned, Pimpama based."),
        "canonical": SITE + "/",
        "og_image": IMG["hero"],
        "body_class": "page-home",
        "schema": [local_business_schema(), website_schema(),
                   faq_schema(HOME_FAQS),
                   {"@type": "WebPage", "@id": SITE + "/#webpage", "url": SITE + "/",
                    "name": "Lawn Mowing Gold Coast | Enviro Garden Care & Odd Jobs",
                    "isPartOf": {"@id": SITE + "/#website"},
                    "about": {"@id": SITE + "/#business"},
                    "speakable": speakable(), "inLanguage": "en-AU"}],
    }

    hero = """<section class="hero" style="--hero-img:url('{img}')">
  <div class="hero__bg" aria-hidden="true"></div>
  <div class="wrap hero__inner">
    <div class="hero__copy">
      <span class="tag tag--glow"><i></i>Now booking across 19 northern suburbs</span>
      <h1>Lawn Mowing Gold Coast — <span class="hl">Pimpama to Coomera</span> and the Northern Suburbs</h1>
      <p class="hero__range">Parkwood to Windaroo and all suburbs in between</p>
      <p class="hero__lead speakable">{citable} Based in Pimpama and mowing Coomera, Ormeau, Helensvale and Hope Island fortnightly.</p>
      <ul class="hero__ticks">
        <li>{ck} Mow, edge and blow down — clippings in your green bin</li>
        <li>{ck} Residential, acreage, strata and commercial</li>
        <li>{ck} Family owned and run — no franchise, no call centre</li>
      </ul>
      <div class="hero__actions">
        <a class="btn btn--primary btn--lg" href="#quote">Get a free estimate</a>
        <a class="btn btn--outline btn--lg" href="tel:{tel}">{ph}{phone}</a>
      </div>
      <div class="hero__proof">
        <div class="stars" aria-hidden="true">{stars}</div>
        <p>Rated RATING_VALUE from RATING_COUNT reviews on <a href="{gbp}" target="_blank" rel="noopener">Google</a> by Northern Gold Coast locals.</p>
      </div>
    </div>
    <div class="hero__form" id="quote">
      {form}
    </div>
  </div>
  <div class="hero__marquee" aria-hidden="true">
    <div class="marquee__track">{marq}{marq}</div>
  </div>
</section>""".format(
        img=IMG["hero"], citable=CITABLE, tel=TEL, phone=PHONE,
        ck=icon("check", "icon icon--sm icon--tick"),
        ph=icon("phone", "icon icon--sm"), gbp=BIZ["gbp"],
        stars="".join(icon("star", "icon icon--star") for _ in range(5)),
        form=quote_form("hero-quote", compact=True,
                        heading="Free estimate in your inbox"),
        marq="".join('<span>%s</span>' % s for s in ALL_SUBURBS))

    intro = """<section class="section section--intro">
  <div class="wrap intro">
    <div class="intro__copy reveal">
      <span class="eyebrow">Lawn mowing Gold Coast</span>
      <h2>A local family-owned business, not a franchise call centre</h2>
      <p>When you ring about <strong>lawn mowing on the Gold Coast</strong>, you get {owner} — the
      person who will actually be standing on your lawn. Enviro Garden Care &amp; Odd Jobs is a small
      family-owned business run out of Pimpama, servicing the Northern Gold Coast from Parkwood to
      Windaroo and all suburbs in between: Coomera, Upper Coomera, Ormeau, Helensvale, Hope Island,
      Oxenford, Yatala and the acreage belt around them.</p>
      <p>That means short drives, tight schedules and a mow that happens on the day we said it would.
      We cover everything from a courtyard in a new Coomera estate to five acres at Jacobs Well, plus the
      hedges, weeds, clean-ups and odd jobs that come with owning a block in south-east Queensland.</p>
      <ul class="ticks">
        <li>{ck} <strong>Fortnightly, three-weekly through winter, or one-off</strong> — your schedule, not a contract</li>
        <li>{ck} <strong>One point of contact</strong> from first call to invoice</li>
        <li>{ck} <strong>Green waste removal available</strong> for an additional charge</li>
        <li>{ck} <strong>Fully insured</strong> for residential, strata and commercial work</li>
      </ul>
      <a class="link-arrow" href="/about/">More about how we work {ar}</a>
    </div>
    <div class="intro__media reveal">
      <img src="{img}" alt="Enviro Garden Care &amp; Odd Jobs mowing a residential lawn — lawn mowing Gold Coast, Pimpama"
           loading="lazy" decoding="async" width="1200" height="900">
      <div class="intro__badge">
        {leaf}
        <div><strong>Family owned</strong><span>Run by {owner} of Pimpama</span></div>
      </div>
    </div>
  </div>
</section>""".format(owner=BIZ["owner"].split()[0], img=IMG["about"],
                     ck=icon("check", "icon icon--sm icon--tick"),
                     ar=icon("arrow", "icon icon--sm"), leaf=icon("home"))

    services = """<section class="section section--svcs" id="services">
  <div class="wrap">
    <div class="section__head reveal">
      <span class="eyebrow">What we do</span>
      <h2>Lawn, garden and grounds care across the Northern Gold Coast</h2>
      <p>Six services, one crew. Each one has its own page with what is included, the suburbs we
      cover and what it costs to get started.</p>
    </div>
    <div class="svcs">
      {cards}
    </div>
  </div>
</section>""".format(cards=_service_cards())

    why = """<section class="section section--why" id="why">
  <div class="wrap why">
    <div class="why__media reveal">
      <img src="{img}" alt="Enviro Garden Care &amp; Odd Jobs mowing equipment — lawn mowing Gold Coast, Pimpama"
           loading="lazy" decoding="async" width="1200" height="900">
    </div>
    <div class="why__copy reveal">
      <span class="eyebrow">{home} Why Enviro</span>
      <h2>Why locals keep us on the calendar</h2>
      <p>Most mowing businesses on the Gold Coast are a franchise badge and a rotating crew. This one
      is a family, a van and a trailer based in Pimpama, and the person who prices your block is the
      person who mows it. That changes how the job gets done: consistently, on the day we said, and
      by someone who will notice when the couch needs raising or the hedge is a week from getting away.</p>
      <div class="why__grid">
        <div class="why__item"><strong>One family, one phone number</strong><span>Ring {owner}. No dispatch queue, no "the crew will be in your area on Thursday".</span></div>
        <div class="why__item"><strong>Turns up on the day</strong><span>Fortnightly through summer, three-weekly through winter, or a one-off. You get a message when it is done.</span></div>
        <div class="why__item"><strong>Honest pricing</strong><span>An approximate price, pending inspection — then it stays that price.</span></div>
        <div class="why__item"><strong>Fully insured</strong><span>Public liability cover for residential, strata, commercial and acreage work. Certificate of currency on request.</span></div>
      </div>
    </div>
  </div>
</section>""".format(img=IMG["why"], home=icon("home", "icon icon--sm"), owner=BIZ["owner"])

    process = """<section class="section section--process">
  <div class="wrap">
    <div class="section__head reveal">
      <span class="eyebrow">How it works</span>
      <h2>Booking lawn mowing Gold Coast side is a three-step job</h2>
      <p>No contracts, no lock-in, and no waiting a week just to get a price.</p>
    </div>
    <ol class="steps">
      <li class="step reveal" style="--d:0ms"><span class="step__n">01</span>
        <h3>Tell us about the block</h3>
        <p>Call, or send the quote form with your address and rough property size. Photos help but are not required.</p></li>
      <li class="step reveal" style="--d:90ms"><span class="step__n">02</span>
        <h3>Get an approximate price</h3>
        <p>Usually the same day — an approximate price, pending inspection, whether it is a fortnightly mow, acreage or a clean-up.</p></li>
      <li class="step reveal" style="--d:180ms"><span class="step__n">03</span>
        <h3>We turn up and keep turning up</h3>
        <p>Booked in fortnightly, three-weekly through winter, or as a one-off. You get a message when it is done.</p></li>
    </ol>
  </div>
</section>"""

    reviews = """<section class="section section--reviews" id="reviews">
  <div class="wrap">
    <div class="section__head reveal">
      <span class="eyebrow">{stars} {rv} from {rc} Google reviews</span>
      <h2>What Northern Gold Coast locals say</h2>
      <p>Read all {rc} on our <a href="{gbp}" target="_blank" rel="noopener">Google Business Profile</a>
      or our <a href="{fb}" target="_blank" rel="noopener">Facebook page</a>.</p>
    </div>
    <div class="reviews">
      {quotes}
    </div>
    <p class="reviews__note reveal">Five-star Google reviews, quoted as written. Full, dated reviews live on Google — tap through to read them all.</p>
  </div>
</section>""".format(stars=icon("star", "icon icon--sm"), gbp=BIZ["gbp"], fb=BIZ["facebook"],
                     rv=GOOGLE_RATING["value"], rc=GOOGLE_RATING["count"],
                     quotes="\n      ".join(
                         '<blockquote class="review reveal" style="--d:%dms"><div class="stars" aria-hidden="true">%s</div>'
                         '<p>“%s”</p><cite>%s</cite></blockquote>'
                         % (i * 90, "".join(icon("star", "icon icon--star") for _ in range(5)), r["text"], r["who"])
                         for i, r in enumerate(REVIEWS)))

    hero = hero.replace("RATING_VALUE", GOOGLE_RATING["value"]).replace("RATING_COUNT", GOOGLE_RATING["count"])
    body = (header("/") + '<main id="main">' + hero + _trust_bar() + intro
            + services + why + process + gallery_section(GALLERY_HOME, feature=True)
            + areas_section("Where we mow on the Northern Gold Coast",
                            "Nineteen suburbs on one run. We cover lawn mowing Gold Coast north — "
                            "Coomera, Pimpama, Ormeau, Helensvale and the acreage belt out to Yatala "
                            "and Jacobs Well — with no travel surcharge anywhere inside that area.")
            + reviews
            + faq_block(HOME_FAQS,
                        "Lawn mowing on the Gold Coast — your questions answered",
                        "Straight answers on price, schedules, acreage and green waste.")
            + cta_band() + '</main>')
    return head(page) + body + footer()


# ==========================================================================
# ABOUT
# ==========================================================================
def about():
    trail = [("Home", "/"), ("About", page_url("about"))]
    faqs = [
        ("Who will actually turn up to mow my lawn?",
         "Shanon, the owner. Enviro Garden Care & Odd Jobs is a family-owned business based in "
         "Pimpama — the person who prices your job is the person who does it and the person you "
         "call if something is not right."),
        ("Are you insured?",
         "Yes. We carry public liability insurance covering residential, strata, commercial and "
         "acreage work, and can supply a current certificate of currency on request."),
        ("How far do you travel?",
         "We work 19 suburbs of the Northern Gold Coast, from Windaroo and Jacobs Well in the north "
         "down to Parkwood and Arundel, and any suburb in between. There is no travel surcharge "
         "inside that area."),
    ]
    page = {
        "title": "About Us | Family-Owned Lawn Mowing, Northern Gold Coast",
        "desc": ("Family-owned lawn mowing business run by Shanon of Pimpama, servicing the "
                 "Northern Gold Coast, Parkwood to Windaroo. Fortnightly, three-weekly in winter, or one-off."),
        "canonical": SITE + page_url("about"),
        "og_image": IMG["about"],
        "body_class": "page-about",
        "schema": [local_business_schema(), breadcrumbs(trail), faq_schema(faqs),
                   {"@type": "AboutPage", "@id": SITE + page_url("about") + "#webpage",
                    "url": SITE + page_url("about"),
                    "name": "About Enviro Garden Care & Odd Jobs",
                    "about": {"@id": SITE + "/#business"},
                    "speakable": speakable(), "inLanguage": "en-AU"}],
    }

    hero = """<section class="phero" style="--hero-img:url('{img}')">
  <div class="phero__bg" aria-hidden="true"></div>
  <div class="wrap phero__inner">
    <span class="tag">About us</span>
    <h1>Family-Owned Lawn Mowing on the Northern Gold Coast — the story behind the trailer</h1>
    <p class="phero__lead speakable">{citable}</p>
  </div>
</section>""".format(img=IMG["about"], citable=CITABLE_ABOUT)

    story = """<section class="section section--story">
  <div class="wrap intro">
    <div class="intro__copy reveal">
      <span class="eyebrow">Who we are</span>
      <h2>One family-owned business, nineteen suburbs</h2>
      <p>Enviro Garden Care &amp; Odd Jobs is a family-owned business, owned and run by
      <strong>{owner} of {sub}</strong>. There is no franchise fee baked into your price, no dispatch
      centre, and no different face each fortnight. You book, {first} turns up, and the lawn gets done.</p>
      <p>The business grew the way good local businesses do — one neighbour telling another. It now
      covers the Coomera to Pimpama growth belt, the Helensvale and Hope Island estates, and the acreage
      belt out through Ormeau, Yatala, Windaroo and Jacobs Well. Residential, strata, commercial and
      rural blocks all sit on the same schedule.</p>
      <p>The <em>&amp; Odd Jobs</em> on the sign is deliberate. Half our customers started with a mow and
      ended up asking whether we could put the flat pack together, paint the fence, or take a load to the
      tip. The answer is usually yes.</p>
      <div class="facts">
        <div class="fact"><strong>19</strong><span>Northern Gold Coast suburbs on the run</span></div>
        <div class="fact"><strong>6</strong><span>Services, from courtyards to five acres</span></div>
        <div class="fact"><strong>1</strong><span>Phone number, answered by the owner</span></div>
      </div>
    </div>
    <div class="intro__media reveal">
      <img src="{img}" alt="Enviro Garden Care &amp; Odd Jobs at work — lawn and garden maintenance Northern Gold Coast"
           loading="lazy" decoding="async" width="1200" height="900">
      <div class="intro__badge">
        {pin}
        <div><strong>Based in Pimpama</strong><span>{sub} {reg} {pc}</span></div>
      </div>
    </div>
  </div>
</section>""".format(owner=BIZ["owner"], first=BIZ["owner"].split()[0], img=IMG["why"],
                     sub=BIZ["suburb"], reg=BIZ["region"],
                     pc=BIZ["postcode"], pin=icon("pin"))

    values = """<section class="section section--values">
  <div class="wrap">
    <div class="section__head reveal">
      <span class="eyebrow">What you can count on</span>
      <h2>Four things we do not compromise on</h2>
    </div>
    <div class="values">
      <article class="value reveal" style="--d:0ms">{leaf}<h3>Environmentally considered</h3>
        <p>Clippings in your green bin rather than landfill, green waste disposed of properly rather
        than dumped, and mowing heights set to keep lawns healthy through a subtropical summer instead
        of scalping them.</p></article>
      <article class="value reveal" style="--d:70ms">{clock}<h3>We turn up</h3>
        <p>The single most common complaint about mowing contractors is that they vanish. You get a
        schedule, a message when the job is done, and a phone number that a human answers.</p></article>
      <article class="value reveal" style="--d:140ms">{check}<h3>Finished, not just mown</h3>
        <p>Edges trimmed, hard surfaces blown down, gates closed, clippings in the green bin. A job is not done until
        the property looks like we were never there — apart from the lawn.</p></article>
      <article class="value reveal" style="--d:210ms">{shield}<h3>Properly covered</h3>
        <p>Public liability insurance on every job, residential through to industrial estates, with a
        certificate of currency available whenever a body corporate or property manager asks.</p></article>
    </div>
  </div>
</section>""".format(leaf=icon("leaf"), clock=icon("clock"), check=icon("check"),
                     shield=icon("shield"))

    body = (header("/about/") + crumbs(trail) + '<main id="main">' + hero + story
            + _trust_bar() + values + gallery_section(GALLERY_ABOUT, "Recent jobs around the north")
            + areas_section("The suburbs we call home")
            + faq_block(faqs, "About Enviro Garden Care &amp; Odd Jobs",
                        "Who we are, how we work and what we are covered for.")
            + cta_band("Want the bloke who actually mows to price your block?",
                       "No call centre, no franchise mark-up. An approximate price, pending inspection — call Shanon direct or send the form.")
            + '</main>')
    return head(page) + body + footer()


# ==========================================================================
# SERVICES HUB
# ==========================================================================
def services_hub():
    trail = [("Home", "/"), ("Services", page_url("services"))]
    page = {
        "title": "Lawn &amp; Garden Services Gold Coast | Enviro Garden Care &amp; Odd Jobs",
        "desc": ("Lawn mowing, acreage mowing, garden maintenance, green waste removal, commercial "
                 "grounds care and odd jobs, Parkwood to Windaroo. Free estimate: 0407 276 574."),
        "canonical": SITE + page_url("services"),
        "body_class": "page-services",
        "schema": [local_business_schema(), breadcrumbs(trail),
                   {"@type": "CollectionPage", "@id": SITE + page_url("services") + "#webpage",
                    "url": SITE + page_url("services"),
                    "name": "Lawn & Garden Services Gold Coast",
                    "about": {"@id": SITE + "/#business"},
                    "inLanguage": "en-AU",
                    "mainEntity": {
                        "@type": "ItemList",
                        "itemListElement": [{
                            "@type": "ListItem", "position": i + 1,
                            "name": plain(s["name"]),
                            "url": SITE + svc_url(s["slug"]),
                        } for i, s in enumerate(SERVICES)]}}],
    }

    hero = """<section class="phero" style="--hero-img:url('{img}')">
  <div class="phero__bg" aria-hidden="true"></div>
  <div class="wrap phero__inner">
    <span class="tag">Services</span>
    <h1>Lawn &amp; Garden Services on the Northern Gold Coast</h1>
    <p class="phero__lead speakable">Six services covering everything from a fortnightly residential mow in
    Coomera to five acres at Jacobs Well, scheduled grounds care for body corporates, and the odd jobs
    we fit in through the quieter months — Parkwood to Windaroo and all suburbs in between.</p>
    <div class="phero__actions">
      <a class="btn btn--primary btn--lg" href="/contact/">Get a free estimate</a>
      <a class="btn btn--outline btn--lg" href="tel:{tel}">{ph}{phone}</a>
    </div>
  </div>
</section>""".format(img=IMG["services_hero"], tel=TEL, phone=PHONE,
                     ph=icon("phone", "icon icon--sm"))

    rows = []
    for i, s in enumerate(SERVICES):
        incl = s["body"][0][1][:4]
        subs = "".join('<li>%s</li>' % x for x in s["suburbs"])
        rows.append("""<article class="svcrow reveal" style="--d:{d}ms">
      <div class="svcrow__media">
        <img src="{img}" alt="{alt}" loading="lazy" decoding="async" width="1200" height="800">
      </div>
      <div class="svcrow__body">
        <span class="svc__icon">{ic}</span>
        <h2><a href="/services/{slug}/">{name}</a></h2>
        <p class="svcrow__tag">{tag}</p>
        <p>{intro}</p>
        <ul class="ticks ticks--tight">{incl}</ul>
        <ul class="chips chips--sm">{subs}</ul>
        <a class="btn btn--primary btn--sm" href="/services/{slug}/">{name} details {ar}</a>
      </div>
    </article>""".format(
            d=i * 60, img=IMG[s["img"]],
            alt="%s — %s, Northern Gold Coast" % (plain(s["name"]), plain(s["keyword"])),
            ic=icon(s["icon"]), slug=s["slug"], name=s["name"], tag=s["tagline"],
            intro=s["intro"],
            incl="".join('<li>%s %s</li>' % (icon("check", "icon icon--sm icon--tick"), x)
                         for x in incl),
            subs=subs, ar=icon("arrow", "icon icon--sm")))

    listing = ('<section class="section section--svcrows"><div class="wrap">%s</div></section>'
               % "\n    ".join(rows))

    body = (header("/services/") + crumbs(trail) + '<main id="main">' + hero
            + _trust_bar() + listing + areas_section() + cta_band() + '</main>')
    return head(page) + body + footer()


# ==========================================================================
# SERVICE PAGE
# ==========================================================================
def service_page(svc):
    trail = [("Home", "/"), ("Services", page_url("services")),
             (plain(svc["name"]), svc_url(svc["slug"]))]
    page = {
        "title": svc["title"],
        "desc": svc["desc"],
        "canonical": SITE + svc_url(svc["slug"]),
        "og_image": IMG[svc["img"]],
        "body_class": "page-service page-service--" + svc["slug"],
        "schema": [local_business_schema(), service_schema(svc), breadcrumbs(trail),
                   faq_schema(svc["faqs"]),
                   {"@type": "WebPage",
                    "@id": SITE + svc_url(svc["slug"]) + "#webpage",
                    "url": SITE + svc_url(svc["slug"]),
                    "name": plain(svc["title"]),
                    "about": {"@id": SITE + "/#business"},
                    "speakable": speakable(), "inLanguage": "en-AU"}],
    }

    subs = "".join('<li>%s</li>' % s for s in svc["suburbs"])
    hero = """<section class="phero phero--svc" style="--hero-img:url('{img}')">
  <div class="phero__bg" aria-hidden="true"></div>
  <div class="wrap phero__inner">
    <span class="tag">{ic}{name}</span>
    <h1>{h1}</h1>
    <p class="phero__lead speakable">{tag}</p>
    <ul class="chips chips--light">{subs}<li>+ all suburbs between Parkwood and Windaroo</li></ul>
    <div class="phero__actions">
      <a class="btn btn--primary btn--lg" href="#quote">Get a free estimate</a>
      <a class="btn btn--outline btn--lg" href="tel:{tel}">{ph}{phone}</a>
    </div>
  </div>
</section>""".format(img=IMG[svc["img"]], ic=icon(svc["icon"], "icon icon--sm"),
                     name=svc["name"], h1=svc["h1"], tag=svc["tagline"], subs=subs,
                     tel=TEL, phone=PHONE, ph=icon("phone", "icon icon--sm"))

    blocks = []
    for title, items in svc["body"]:
        blocks.append('<div class="prose__block reveal"><h2>%s</h2><ul class="ticks">%s</ul></div>'
                      % (title, "".join('<li>%s %s</li>'
                                        % (icon("check", "icon icon--sm icon--tick"), x)
                                        for x in items)))

    main_col = """<div class="lay__main">
      <div class="prose reveal">
        <p class="prose__lead">{intro}</p>
      </div>
      {blocks}
      <div class="prose__block reveal">
        <h2>{kwt} — the suburbs we cover</h2>
        <p>We provide {kw} across the Northern Gold Coast. These are the suburbs we visit most often
        for this service — if you are nearby and not listed, ring anyway; we probably drive past you.</p>
        <ul class="chips">{subs}</ul>
      </div>
      <div class="prose__block prose__block--note reveal">
        <h2>Why book Enviro Garden Care &amp; Odd Jobs</h2>
        <p>{citable} Book {kw} with us and you deal with {owner} from the first phone call to the
        invoice — there is no franchise fee in your price and no rotating crew. Green waste removal is
        available for an additional charge.</p>
      </div>
    </div>""".format(intro=svc["intro"], blocks="\n      ".join(blocks),
                     name=svc["name"], subs=subs, citable=CITABLE, owner=BIZ["owner"],
                     kw=svc["keyword"], kwt=svc["keyword"][0].upper() + svc["keyword"][1:])

    side = """<aside class="lay__side">
      <div class="sticky">
        <div id="quote">{form}</div>
        <div class="sidecard reveal">
          <h2>{pin} Straight from Pimpama</h2>
          <p>Family owned and run, {sub} {reg} {pc} — Parkwood to Windaroo and all suburbs in between.</p>
          {map}
        </div>
      </div>
    </aside>""".format(
        form=quote_form("svc-quote", compact=True,
                        preselect=svc["name"] if plain(svc["name"]) in [
                            "Lawn Mowing", "Acreage & Ride-On Mowing"] else None,
                        heading="Free estimate for " + plain(svc["name"]).lower()),
        pin=icon("pin", "icon icon--sm"), sub=BIZ["suburb"],
        reg=BIZ["region"], pc=BIZ["postcode"], map=map_embed())

    layout = ('<section class="section section--lay"><div class="wrap lay">%s%s</div></section>'
              % (main_col, side))

    others = """<section class="section section--svcs section--alt">
  <div class="wrap">
    <div class="section__head reveal">
      <span class="eyebrow">Also available</span>
      <h2>Other services on the same visit</h2>
      <p>Most clients bundle. It is cheaper than booking two separate trips.</p>
    </div>
    <div class="svcs">
      %s
    </div>
  </div>
</section>""" % _service_cards(featured=svc["slug"])

    body = (header("/services/") + crumbs(trail) + '<main id="main">' + hero
            + _trust_bar() + layout
            + gallery_section(GALLERY_BY_SERVICE[svc["slug"]], "Recent %s jobs" % plain(svc["name"]).lower(),
                              "A few of the blocks we have looked after — %s and the suburbs around it."
                              % svc["keyword"])
            + others
            + faq_block(svc["faqs"], "%s — common questions" % plain(svc["name"]),
                        "Everything people ask before booking %s." % plain(svc["name"]).lower())
            + cta_band("Get a price for %s" % svc["keyword"],
                       "Send the form or call — an approximate price, pending inspection, usually the same day.")
            + '</main>')
    return head(page) + body + footer()


# ==========================================================================
# CONTACT
# ==========================================================================
def contact():
    trail = [("Home", "/"), ("Contact", page_url("contact"))]
    faqs = [
        ("How fast will I get a price?",
         "Usually the same day, and almost always within one business day. Standard residential "
         "mowing gets an approximate price, pending inspection; acreage and clean-ups need a look "
         "at the block first. Photos of the property help us get it right."),
        ("What are your hours?",
         "We are on the tools Monday to Friday from 7am to 5pm. Saturday 7am to 3pm is phone "
         "enquiries only — no on-site work."),
        ("Which suburbs do you cover?",
         "Nineteen suburbs of the Northern Gold Coast: Coomera, Upper Coomera, Coomera Waters, "
         "Pimpama, Ormeau, Ormeau Hills, Oxenford, Helensvale, Hope Island, Sanctuary Cove, "
         "Pacific Pines, Parkwood, Arundel, Yatala, Stapylton, Jacobs Well, Willowvale, Windaroo "
         "and Mount Warren — Parkwood to Windaroo and any suburb in between."),
        ("Do you charge for estimates or travel?",
         "No. Estimates are free and there is no travel surcharge anywhere inside our service "
         "area — being based in Pimpama is the whole point."),
    ]
    page = {
        "title": "Contact Enviro Garden Care &amp; Odd Jobs | Free Estimate, Gold Coast",
        "desc": ("Get a free lawn mowing or garden care estimate on the Northern Gold Coast. "
                 "Call 0407 276 574 or send the form — approximate price, pending inspection."),
        "canonical": SITE + page_url("contact"),
        "body_class": "page-contact",
        "schema": [local_business_schema(), breadcrumbs(trail), faq_schema(faqs),
                   {"@type": "ContactPage", "@id": SITE + page_url("contact") + "#webpage",
                    "url": SITE + page_url("contact"),
                    "name": "Contact Enviro Garden Care & Odd Jobs",
                    "about": {"@id": SITE + "/#business"},
                    "speakable": speakable(), "inLanguage": "en-AU"}],
    }

    hours_rows = "".join(
        '<div class="hours__row"><span>%s</span><span>%s – %s</span></div>'
        % (label, o.lstrip("0"), c.lstrip("0")) for _, o, c, label in BIZ["hours"])

    hero = """<section class="phero phero--contact">
  <div class="wrap phero__inner">
    <span class="tag">Contact</span>
    <h1>Get a free estimate for lawn mowing on the Gold Coast</h1>
    <p class="phero__lead speakable">Tell us the address and roughly how big the block is, provide photos
    of the property in its current condition, and we will come back with an approximate price, pending
    inspection. Or just ring {owner} on {phone}.</p>
  </div>
</section>""".format(owner=BIZ["owner"].split()[0], phone=PHONE)

    cards = """<section class="section section--contact">
  <div class="wrap lay lay--contact">
    <div class="lay__main">
      {form}
    </div>
    <aside class="lay__side">
      <div class="sticky">
        <div class="sidecard reveal">
          <h2>Talk to a person</h2>
          <ul class="cinfo">
            <li>{ph}<div><span>Phone</span><a href="tel:{tel}">{phone}</a></div></li>
            <li>{ml}<div><span>Email</span><a href="mailto:{email}">{email}</a></div></li>
            <li>{pin}<div><span>Base</span>{sub} {reg} {pc}</div></li>
          </ul>
          <h3 class="sidecard__sub">{clock} Trading hours</h3>
          <div class="hours">{hours}</div>
          <div class="sidecard__links">
            <a class="btn btn--ghost btn--sm" href="{gbp}" target="_blank" rel="noopener">Google Business Profile</a>
            <a class="btn btn--ghost btn--sm" href="{fb}" target="_blank" rel="noopener">Facebook</a>
          </div>
        </div>
      </div>
    </aside>
  </div>
</section>""".format(form=quote_form("contact-quote",
                                     heading="Request a free estimate"),
                     ph=icon("phone"), ml=icon("mail"), pin=icon("pin"), clock=icon("clock", "icon icon--sm"),
                     tel=TEL, phone=PHONE, email=BIZ["email"],
                     sub=BIZ["suburb"], reg=BIZ["region"], pc=BIZ["postcode"],
                     hours=hours_rows, gbp=BIZ["gbp"], fb=BIZ["facebook"])

    body = (header("/contact/") + crumbs(trail) + '<main id="main">' + hero + cards
            + _trust_bar() + areas_section("Find us on the Northern Gold Coast")
            + faq_block(faqs, "Getting in touch", "Quotes, hours and where we go.")
            + cta_band() + '</main>')
    return head(page) + body + footer()


# ==========================================================================
# THANK YOU
# ==========================================================================
def thank_you():
    page = {
        "title": "Thank you — your quote request is in | Enviro Garden Care",
        "desc": ("Thanks for contacting Enviro Garden Care & Odd Jobs. Your quote request has been "
                 "received and we will be in touch, usually the same day."),
        "canonical": SITE + page_url("thank-you"),
        "body_class": "page-thanks",
        "schema": [local_business_schema(),
                   {"@type": "WebPage", "@id": SITE + page_url("thank-you") + "#webpage",
                    "url": SITE + page_url("thank-you"), "name": "Thank you",
                    "inLanguage": "en-AU"}],
    }
    extra = ('<meta name="robots" content="noindex, follow">')

    svc_links = "".join('<li><a href="%s">%s</a></li>' % (svc_url(s["slug"]), s["name"])
                        for s in SERVICES)

    body = """{hdr}
<main id="main">
<section class="thanks">
  <div class="wrap thanks__inner">
    <div class="thanks__mark" aria-hidden="true">{check}</div>
    <span class="tag tag--glow"><i></i>Request received</span>
    <h1>Thanks — that has come through</h1>
    <p class="thanks__lead">Your estimate request is with {owner} now. You will normally hear back the
    <strong>same day</strong>, and always within one business day.</p>
    <div class="thanks__next">
      <h2>What happens next</h2>
      <ol class="thanks__steps">
        <li><span>1</span><div><strong>We read the details</strong><p>Address, property size and the service you need — that is usually enough to price it.</p></div></li>
        <li><span>2</span><div><strong>We call or email an approximate price</strong><p>Pending inspection — whether it is fortnightly mowing, acreage, a clean-up or a commercial site.</p></div></li>
        <li><span>3</span><div><strong>You get booked in</strong><p>Pick fortnightly (three-weekly through winter) or a one-off. We confirm the first visit and you are away.</p></div></li>
      </ol>
    </div>
    <div class="thanks__urgent">
      <h2>In a hurry?</h2>
      <p>Storm damage, an inspection tomorrow, or a block that needs clearing this week — just ring.</p>
      <a class="btn btn--primary btn--lg" href="tel:{tel}">{ph}Call {phone}</a>
    </div>
    <div class="thanks__links">
      <h2>While you are here</h2>
      <ul>{svc}</ul>
      <p><a class="link-arrow" href="/">Back to the home page {ar}</a></p>
    </div>
  </div>
</section>
</main>
""".format(hdr=header(), check=icon("check", "icon"), owner=BIZ["owner"].split()[0],
           tel=TEL, phone=PHONE, ph=icon("phone", "icon icon--sm"), svc=svc_links,
           ar=icon("arrow", "icon icon--sm"))

    html = head(page).replace(
        '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">',
        extra)
    return html + body + footer()


# ==========================================================================
# 404
# ==========================================================================
def not_found():
    page = {
        "title": "Page not found | Enviro Garden Care &amp; Odd Jobs",
        "desc": ("That page does not exist. Find lawn mowing Gold Coast, acreage mowing, garden "
                 "maintenance and green waste removal across the Northern Gold Coast."),
        "canonical": SITE + "/404.html",
        "body_class": "page-thanks",
        "schema": [local_business_schema()],
    }
    svc_links = "".join('<li><a href="%s">%s</a></li>' % (svc_url(s["slug"]), s["name"])
                        for s in SERVICES)
    body = """{hdr}
<main id="main">
<section class="thanks">
  <div class="wrap thanks__inner">
    <span class="tag">404</span>
    <h1>That page has been mown down</h1>
    <p class="thanks__lead">The link you followed does not exist any more. Here is where everything lives.</p>
    <div class="thanks__links">
      <h2>Our services</h2>
      <ul>{svc}</ul>
      <p><a class="link-arrow" href="/">Back to the home page {ar}</a></p>
    </div>
    <div class="thanks__urgent">
      <h2>Need a price?</h2>
      <p>Call {owner} direct and skip the browsing.</p>
      <a class="btn btn--primary btn--lg" href="tel:{tel}">{ph}Call {phone}</a>
    </div>
  </div>
</section>
</main>
""".format(hdr=header(), svc=svc_links, ar=icon("arrow", "icon icon--sm"),
           owner=BIZ["owner"].split()[0], tel=TEL, phone=PHONE,
           ph=icon("phone", "icon icon--sm"))
    html = head(page).replace(
        '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">',
        '<meta name="robots" content="noindex, follow">')
    return html + body + footer()
