# -*- coding: utf-8 -*-
"""Page bodies. Copy follows the SEO research spec in build/seo-research-source.html."""

from data import (SITE, BIZ, IMG, GALLERY, SERVICES, ALL_SUBURBS, HOME_FAQS, CITABLE)
from templates import (head, header, footer, icon, quote_form, map_embed, faq_block,
                       areas_section, cta_band, gallery_section, crumbs, plain,
                       local_business_schema, website_schema, breadcrumbs,
                       faq_schema, service_schema, speakable)

TEL = BIZ["phone_e164"]
PHONE = BIZ["phone_display"]


def _trust_bar():
    items = [
        ("leaf", "Battery or petrol", "Quiet, fume-free gear at no extra charge"),
        ("pin", "Based in Pimpama", "Local runs — no Brisbane travel surcharge"),
        ("truck", "Green waste gone", "Taken away in our enclosed trailer"),
        ("shield", "Fully insured", "Public liability cover on every job"),
    ]
    cells = "".join(
        '<li class="trust__item reveal" style="--d:%dms">%s<div><strong>%s</strong>'
        '<span>%s</span></div></li>' % (i * 70, icon(k), t, d)
        for i, (k, t, d) in enumerate(items))
    return '<section class="trust"><div class="wrap"><ul class="trust__list">%s</ul></div></section>' % cells


def _service_cards(depth=0, featured=None):
    up = "../" * depth
    cards = []
    for i, s in enumerate(SERVICES):
        if featured and s["slug"] == featured:
            continue
        cards.append("""<article class="svc reveal" style="--d:{d}ms">
        <a class="svc__link" href="{up}services/{slug}.html">
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
            d=i * 70, up=up, slug=s["slug"], img=IMG[s["img"]],
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
        "desc": ("Reliable lawn mowing Gold Coast north: Pimpama, Coomera, Ormeau &amp; "
                 "Helensvale. Acreage mowing, hedges, garden care. Quiet battery gear. "
                 "Get a free quote today."),
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
      <h1>Lawn Mowing Gold Coast — <span class="hl">Northern Suburbs</span> from Pimpama to Coomera</h1>
      <p class="hero__lead speakable">{citable}</p>
      <ul class="hero__ticks">
        <li>{ck} Mow, edge, blow down &amp; green waste taken away</li>
        <li>{ck} Residential, acreage, strata and commercial</li>
        <li>{ck} Quiet battery equipment at no extra charge</li>
      </ul>
      <div class="hero__actions">
        <a class="btn btn--primary btn--lg" href="#quote">Get a free quote</a>
        <a class="btn btn--outline btn--lg" href="tel:{tel}">{ph}{phone}</a>
      </div>
      <div class="hero__proof">
        <div class="stars" aria-hidden="true">{stars}</div>
        <p>Rated by Gold Coast locals on <a href="{gbp}" target="_blank" rel="noopener">Google</a> — mowing the north since day one.</p>
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
        form=quote_form(0, "hero-quote", compact=True,
                        heading="Free quote in your inbox"),
        marq="".join('<span>%s</span>' % s for s in ALL_SUBURBS))

    intro = """<section class="section section--intro">
  <div class="wrap intro">
    <div class="intro__copy reveal">
      <span class="eyebrow">Lawn mowing Gold Coast</span>
      <h2>A local mowing round, not a franchise call centre</h2>
      <p>When you ring about <strong>lawn mowing on the Gold Coast</strong>, you get {owner} — the
      person who will actually be standing on your lawn. Enviro Garden Care &amp; Odd Jobs runs out of
      Pimpama and works the northern corridor: Coomera, Upper Coomera, Ormeau, Helensvale, Hope Island,
      Oxenford, Yatala and the acreage belt in between.</p>
      <p>That means short drives, tight schedules and a mow that happens on the day we said it would.
      We cover everything from a courtyard in a new Coomera estate to five acres at Jacobs Well, plus the
      hedges, weeds, clean-ups and odd jobs that come with owning a block in south-east Queensland.</p>
      <ul class="ticks">
        <li>{ck} <strong>Fortnightly, monthly or one-off</strong> — your schedule, not a contract</li>
        <li>{ck} <strong>One point of contact</strong> from quote to invoice</li>
        <li>{ck} <strong>Green waste removed</strong> on the same visit, every visit</li>
        <li>{ck} <strong>Fully insured</strong> for residential, strata and commercial work</li>
      </ul>
      <a class="link-arrow" href="about.html">More about how we work {ar}</a>
    </div>
    <div class="intro__media reveal">
      <img src="{img}" alt="Enviro Garden Care &amp; Odd Jobs mowing a residential lawn — lawn mowing Gold Coast, Pimpama"
           loading="lazy" decoding="async" width="1200" height="900">
      <div class="intro__badge">
        {leaf}
        <div><strong>Battery powered</strong><span>No fumes. No 7am roar.</span></div>
      </div>
    </div>
  </div>
</section>""".format(owner=BIZ["owner"].split()[0], img=IMG["about"],
                     ck=icon("check", "icon icon--sm icon--tick"),
                     ar=icon("arrow", "icon icon--sm"), leaf=icon("leaf"))

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
</section>""".format(cards=_service_cards(0))

    why = """<section class="section section--why" id="why">
  <div class="wrap why">
    <div class="why__media reveal">
      <img src="{img}" alt="Battery powered lawn mower in use — quiet lawn mowing Gold Coast by Enviro Garden Care"
           loading="lazy" decoding="async" width="1200" height="900">
    </div>
    <div class="why__copy reveal">
      <span class="eyebrow">{leaf} Why Enviro</span>
      <h2>The quiet option — and it does not cost you extra</h2>
      <p>Most mowing businesses on the Gold Coast run petrol and only petrol. We run both, and we let
      you choose. For the vast majority of residential and commercial sites the battery gear cuts just as
      well, and it changes what is possible: early starts without waking the street, Sunday mows,
      tenanted units, retail frontages, and no two-stroke haze through your open windows.</p>
      <div class="why__grid">
        <div class="why__item"><strong>Quiet enough for shift workers</strong><span>Roughly half the noise of a petrol mower — no complaints from the neighbours.</span></div>
        <div class="why__item"><strong>No fumes, no fuel smell</strong><span>Better for kids, pets, alfresco areas and anyone with asthma.</span></div>
        <div class="why__item"><strong>Zero extra charge</strong><span>Same price as petrol. You just tell us which you would prefer.</span></div>
        <div class="why__item"><strong>Petrol when it is the right tool</strong><span>Big acreage and heavy slashing still get the ride-on and the two-stroke.</span></div>
      </div>
      <p class="why__note">Nobody else on page one of Google owns this. We do — because we actually do it.</p>
    </div>
  </div>
</section>""".format(img=IMG["battery"], leaf=icon("leaf", "icon icon--sm"))

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
        <h3>Get a straight price</h3>
        <p>Usually the same day. A per-visit price for regular mowing, or a quoted figure for acreage and clean-ups.</p></li>
      <li class="step reveal" style="--d:180ms"><span class="step__n">03</span>
        <h3>We turn up and keep turning up</h3>
        <p>Booked into the round on a fortnightly or monthly cycle. You get a message when it is done. Green waste leaves with us.</p></li>
    </ol>
  </div>
</section>"""

    reviews = """<section class="section section--reviews" id="reviews">
  <div class="wrap">
    <div class="section__head reveal">
      <span class="eyebrow">{stars} Reviews</span>
      <h2>What Northern Gold Coast locals say</h2>
      <p>Read the full set on our <a href="{gbp}" target="_blank" rel="noopener">Google Business Profile</a>
      and <a href="{fb}" target="_blank" rel="noopener">Facebook page</a>.</p>
    </div>
    <div class="reviews">
      <blockquote class="review reveal" style="--d:0ms">
        <div class="stars" aria-hidden="true">{s5}</div>
        <p>“Turns up when he says he will, which is more than I can say for the last three mowers I tried. Lawn looks sharp and the clippings go with him.”</p>
        <cite>Verified Google review · Coomera</cite>
      </blockquote>
      <blockquote class="review reveal" style="--d:90ms">
        <div class="stars" aria-hidden="true">{s5}</div>
        <p>“We have just over an acre at Ormeau Hills that had got away from us. Slashed, cut back and cleaned up in a day, and now he keeps it on a cycle.”</p>
        <cite>Verified Google review · Ormeau Hills</cite>
      </blockquote>
      <blockquote class="review reveal" style="--d:180ms">
        <div class="stars" aria-hidden="true">{s5}</div>
        <p>“The battery mower is the reason we booked. Kids nap in the afternoon and we can still get the yard done without the racket.”</p>
        <cite>Verified Google review · Upper Coomera</cite>
      </blockquote>
    </div>
    <p class="reviews__note reveal">Reviews are shown in summary. Full, dated reviews live on Google — tap through to read them all.</p>
  </div>
</section>""".format(stars=icon("star", "icon icon--sm"), gbp=BIZ["gbp"], fb=BIZ["facebook"],
                     s5="".join(icon("star", "icon icon--star") for _ in range(5)))

    body = (header("index.html", 0) + '<main id="main">' + hero + _trust_bar() + intro
            + services + why + process + gallery_section(GALLERY, feature=True)
            + areas_section(0, "Where we mow on the Northern Gold Coast",
                            "Nineteen suburbs on one run. We cover lawn mowing Gold Coast north — "
                            "Coomera, Pimpama, Ormeau, Helensvale and the acreage belt out to Yatala "
                            "and Jacobs Well — with no travel surcharge anywhere inside that area.")
            + reviews
            + faq_block(HOME_FAQS,
                        "Lawn mowing on the Gold Coast — your questions answered",
                        "Straight answers on price, schedules, acreage and the battery gear.")
            + cta_band(0) + '</main>')
    return head(page, 0) + body + footer(0)


# ==========================================================================
# ABOUT
# ==========================================================================
def about():
    trail = [("Home", "/"), ("About", "/about.html")]
    faqs = [
        ("Who will actually turn up to mow my lawn?",
         "Shanon Hopton, the owner. Enviro Garden Care & Odd Jobs is an owner-operated business "
         "based in Pimpama — the person who quotes your job is the person who does it and the "
         "person you call if something is not right."),
        ("Is battery-powered lawn mowing as good as petrol?",
         "For most residential and commercial sites, yes — and there's no extra charge. Battery "
         "equipment is quieter and produces no fumes, which suits early starts, Sundays, shift "
         "workers and customer-facing businesses. Large acreage jobs still use petrol ride-on gear."),
        ("Are you insured?",
         "Yes. We carry public liability insurance covering residential, strata, commercial and "
         "acreage work, and can supply a current certificate of currency on request."),
        ("How far do you travel?",
         "We work 19 suburbs of the Northern Gold Coast, from Yatala and Jacobs Well in the north "
         "down to Parkwood and Arundel. There is no travel surcharge inside that area."),
    ]
    page = {
        "title": "About Us | Battery Powered Lawn Mowing Gold Coast",
        "desc": ("Owner-operated lawn mowing Gold Coast north, run out of Pimpama. Battery powered "
                 "equipment at no extra charge across 19 northern suburbs. Meet Shanon."),
        "canonical": SITE + "/about.html",
        "og_image": IMG["about"],
        "body_class": "page-about",
        "schema": [local_business_schema(), breadcrumbs(trail), faq_schema(faqs),
                   {"@type": "AboutPage", "@id": SITE + "/about.html#webpage",
                    "url": SITE + "/about.html",
                    "name": "About Enviro Garden Care & Odd Jobs",
                    "about": {"@id": SITE + "/#business"},
                    "speakable": speakable(), "inLanguage": "en-AU"}],
    }

    hero = """<section class="phero" style="--hero-img:url('{img}')">
  <div class="phero__bg" aria-hidden="true"></div>
  <div class="wrap phero__inner">
    <span class="tag">About us</span>
    <h1>Battery Powered Lawn Mowing Gold Coast — the story behind the trailer</h1>
    <p class="phero__lead speakable">{citable}</p>
  </div>
</section>""".format(img=IMG["about"], citable=CITABLE)

    story = """<section class="section section--story">
  <div class="wrap intro">
    <div class="intro__copy reveal">
      <span class="eyebrow">Who we are</span>
      <h2>One bloke, one round, nineteen suburbs</h2>
      <p>Enviro Garden Care &amp; Odd Jobs is owned and run by <strong>{owner}</strong> out of
      {street}, {sub}. There is no franchise fee baked into your quote, no dispatch centre, and no
      different face each fortnight. You book, {first} turns up, and the lawn gets done.</p>
      <p>The round grew the way good local businesses do — one neighbour telling another. It now covers
      the Coomera corridor, the Helensvale and Hope Island estates, and the acreage belt out through
      Ormeau, Yatala and Jacobs Well. Residential, strata, commercial and rural blocks all sit on the
      same schedule.</p>
      <p>The <em>&amp; Odd Jobs</em> on the sign is deliberate. Half our customers started with a mow and
      ended up asking whether we could put the flat pack together, paint the fence, or take a load to the
      tip. The answer is usually yes.</p>
      <div class="facts">
        <div class="fact"><strong>19</strong><span>Northern Gold Coast suburbs on the run</span></div>
        <div class="fact"><strong>6</strong><span>Services, from courtyards to five acres</span></div>
        <div class="fact"><strong>0</strong><span>Extra charge for the quiet battery gear</span></div>
      </div>
    </div>
    <div class="intro__media reveal">
      <img src="{img}" alt="Enviro Garden Care &amp; Odd Jobs at work — lawn and garden maintenance Northern Gold Coast"
           loading="lazy" decoding="async" width="1200" height="900">
      <div class="intro__badge">
        {pin}
        <div><strong>Based in Pimpama</strong><span>{street}, {sub} {reg} {pc}</span></div>
      </div>
    </div>
  </div>
</section>""".format(owner=BIZ["owner"], first=BIZ["owner"].split()[0], img=IMG["battery"],
                     street=BIZ["street"], sub=BIZ["suburb"], reg=BIZ["region"],
                     pc=BIZ["postcode"], pin=icon("pin"))

    values = """<section class="section section--values">
  <div class="wrap">
    <div class="section__head reveal">
      <span class="eyebrow">What you can count on</span>
      <h2>Four things we do not compromise on</h2>
    </div>
    <div class="values">
      <article class="value reveal" style="--d:0ms">{leaf}<h3>Environmentally considered</h3>
        <p>Battery equipment wherever it is the right tool, green waste disposed of properly rather than
        dumped, and mowing heights set to keep lawns healthy through a subtropical summer instead of
        scalping them.</p></article>
      <article class="value reveal" style="--d:70ms">{clock}<h3>We turn up</h3>
        <p>The single most common complaint about mowing contractors is that they vanish. You get a
        schedule, a message when the job is done, and a phone number that a human answers.</p></article>
      <article class="value reveal" style="--d:140ms">{check}<h3>Finished, not just mown</h3>
        <p>Edges trimmed, hard surfaces blown down, gates closed, clippings gone. A job is not done until
        the property looks like we were never there — apart from the lawn.</p></article>
      <article class="value reveal" style="--d:210ms">{shield}<h3>Properly covered</h3>
        <p>Public liability insurance on every job, residential through to industrial estates, with a
        certificate of currency available whenever a body corporate or property manager asks.</p></article>
    </div>
  </div>
</section>""".format(leaf=icon("leaf"), clock=icon("clock"), check=icon("check"),
                     shield=icon("shield"))

    body = (header("about.html", 0) + crumbs(trail, 0) + '<main id="main">' + hero + story
            + _trust_bar() + values + gallery_section(GALLERY[:4], "Recent jobs around the north")
            + areas_section(0, "The suburbs we call home")
            + faq_block(faqs, "About Enviro Garden Care &amp; Odd Jobs",
                        "Who we are, how we work and what we are covered for.")
            + cta_band(0, "Want the bloke who actually mows to quote your block?",
                       "No call centre, no franchise mark-up. Call Shanon direct or send the form.")
            + '</main>')
    return head(page, 0) + body + footer(0)


# ==========================================================================
# SERVICES HUB
# ==========================================================================
def services_hub():
    trail = [("Home", "/"), ("Services", "/services.html")]
    page = {
        "title": "Lawn &amp; Garden Services Gold Coast | Enviro Garden Care &amp; Odd Jobs",
        "desc": ("Lawn mowing, acreage mowing, garden maintenance, green waste removal, commercial "
                 "grounds care and odd jobs across the Northern Gold Coast. Free quotes: 0407 276 574."),
        "canonical": SITE + "/services.html",
        "body_class": "page-services",
        "schema": [local_business_schema(), breadcrumbs(trail),
                   {"@type": "CollectionPage", "@id": SITE + "/services.html#webpage",
                    "url": SITE + "/services.html",
                    "name": "Lawn & Garden Services Gold Coast",
                    "about": {"@id": SITE + "/#business"},
                    "inLanguage": "en-AU",
                    "mainEntity": {
                        "@type": "ItemList",
                        "itemListElement": [{
                            "@type": "ListItem", "position": i + 1,
                            "name": plain(s["name"]),
                            "url": "%s/services/%s.html" % (SITE, s["slug"]),
                        } for i, s in enumerate(SERVICES)]}}],
    }

    hero = """<section class="phero" style="--hero-img:url('{img}')">
  <div class="phero__bg" aria-hidden="true"></div>
  <div class="wrap phero__inner">
    <span class="tag">Services</span>
    <h1>Lawn &amp; Garden Services on the Northern Gold Coast</h1>
    <p class="phero__lead speakable">Six services covering everything from a fortnightly residential mow in
    Coomera to five acres at Jacobs Well, scheduled grounds care for body corporates, and the odd jobs
    that have been on the list since Christmas.</p>
    <div class="phero__actions">
      <a class="btn btn--primary btn--lg" href="contact.html">Get a free quote</a>
      <a class="btn btn--outline btn--lg" href="tel:{tel}">{ph}{phone}</a>
    </div>
  </div>
</section>""".format(img=IMG["svc_mowing"], tel=TEL, phone=PHONE,
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
        <h2><a href="services/{slug}.html">{name}</a></h2>
        <p class="svcrow__tag">{tag}</p>
        <p>{intro}</p>
        <ul class="ticks ticks--tight">{incl}</ul>
        <ul class="chips chips--sm">{subs}</ul>
        <a class="btn btn--primary btn--sm" href="services/{slug}.html">{name} details {ar}</a>
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

    body = (header("services.html", 0) + crumbs(trail, 0) + '<main id="main">' + hero
            + _trust_bar() + listing + areas_section(0) + cta_band(0) + '</main>')
    return head(page, 0) + body + footer(0)


# ==========================================================================
# SERVICE PAGE
# ==========================================================================
def service_page(svc):
    trail = [("Home", "/"), ("Services", "/services.html"),
             (plain(svc["name"]), "/services/%s.html" % svc["slug"])]
    page = {
        "title": svc["title"],
        "desc": svc["desc"],
        "canonical": "%s/services/%s.html" % (SITE, svc["slug"]),
        "og_image": IMG[svc["img"]],
        "body_class": "page-service page-service--" + svc["slug"],
        "schema": [local_business_schema(), service_schema(svc), breadcrumbs(trail),
                   faq_schema(svc["faqs"]),
                   {"@type": "WebPage",
                    "@id": "%s/services/%s.html#webpage" % (SITE, svc["slug"]),
                    "url": "%s/services/%s.html" % (SITE, svc["slug"]),
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
    <ul class="chips chips--light">{subs}</ul>
    <div class="phero__actions">
      <a class="btn btn--primary btn--lg" href="#quote">Get a free quote</a>
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
        invoice — there is no franchise fee in your price and no rotating crew. Green waste leaves with
        us on every visit, and the quiet battery equipment is available at no extra charge.</p>
      </div>
    </div>""".format(intro=svc["intro"], blocks="\n      ".join(blocks),
                     name=svc["name"], subs=subs, citable=CITABLE, owner=BIZ["owner"],
                     kw=svc["keyword"], kwt=svc["keyword"][0].upper() + svc["keyword"][1:])

    side = """<aside class="lay__side">
      <div class="sticky">
        <div id="quote">{form}</div>
        <div class="sidecard reveal">
          <h2>{pin} Straight from Pimpama</h2>
          <p>{street}, {sub} {reg} {pc}</p>
          {map}
        </div>
      </div>
    </aside>""".format(
        form=quote_form(1, "svc-quote", compact=True,
                        preselect=svc["name"] if plain(svc["name"]) in [
                            "Lawn Mowing", "Acreage & Ride-On Mowing"] else None,
                        heading="Free quote for " + plain(svc["name"]).lower()),
        pin=icon("pin", "icon icon--sm"), street=BIZ["street"], sub=BIZ["suburb"],
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
</section>""" % _service_cards(1, featured=svc["slug"])

    body = (header("services.html", 1) + crumbs(trail, 1) + '<main id="main">' + hero
            + _trust_bar() + layout
            + gallery_section(GALLERY[:4], "Recent %s jobs" % plain(svc["name"]).lower(),
                              "A few of the blocks we have looked after — %s and the suburbs around it."
                              % svc["keyword"])
            + others
            + faq_block(svc["faqs"], "%s — common questions" % plain(svc["name"]),
                        "Everything people ask before booking %s." % plain(svc["name"]).lower())
            + cta_band(1, "Get a price for %s" % svc["keyword"],
                       "Send the form or call — most quotes go back out the same day.")
            + '</main>')
    return head(page, 1) + body + footer(1)


# ==========================================================================
# CONTACT
# ==========================================================================
def contact():
    trail = [("Home", "/"), ("Contact", "/contact.html")]
    faqs = [
        ("How fast will I get a quote?",
         "Usually the same day, and almost always within one business day. Standard residential "
         "mowing can often be priced over the phone; acreage and clean-ups may need a quick look "
         "at the block first."),
        ("What are your hours?",
         "We are on the tools Monday to Friday from 7am to 5pm and Saturday from 7am to 3pm. "
         "Sunday work is available by arrangement — the battery equipment is quiet enough that it "
         "is not a problem for the neighbours."),
        ("Which suburbs do you cover?",
         "Nineteen suburbs of the Northern Gold Coast: Coomera, Upper Coomera, Coomera Waters, "
         "Pimpama, Ormeau, Ormeau Hills, Oxenford, Helensvale, Hope Island, Sanctuary Cove, "
         "Pacific Pines, Parkwood, Arundel, Yatala, Stapylton, Jacobs Well, Willowvale, Windaroo "
         "and Mount Warren."),
        ("Do you charge for quotes or travel?",
         "No. Quotes are free and there is no travel surcharge anywhere inside our 19-suburb "
         "service area — being based in Pimpama is the whole point."),
    ]
    page = {
        "title": "Contact Enviro Garden Care &amp; Odd Jobs | Free Quote, Gold Coast",
        "desc": ("Get a free lawn mowing or garden care quote on the Northern Gold Coast. "
                 "Call 0407 276 574, email hello@envirogardencare.com.au, or send the form — "
                 "same-day replies."),
        "canonical": SITE + "/contact.html",
        "body_class": "page-contact",
        "schema": [local_business_schema(), breadcrumbs(trail), faq_schema(faqs),
                   {"@type": "ContactPage", "@id": SITE + "/contact.html#webpage",
                    "url": SITE + "/contact.html",
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
    <h1>Get a free quote for lawn mowing on the Gold Coast</h1>
    <p class="phero__lead speakable">Tell us the address and roughly how big the block is, and we will
    come back with a price — usually the same day. Or just ring {owner} on {phone}.</p>
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
            <li>{pin}<div><span>Base</span>{street}<br>{sub} {reg} {pc}</div></li>
          </ul>
          <h3 class="sidecard__sub">{clock} Trading hours</h3>
          <div class="hours">{hours}</div>
          <p class="hours__note">{hnote}</p>
          <div class="sidecard__links">
            <a class="btn btn--ghost btn--sm" href="{gbp}" target="_blank" rel="noopener">Google Business Profile</a>
            <a class="btn btn--ghost btn--sm" href="{fb}" target="_blank" rel="noopener">Facebook</a>
          </div>
        </div>
      </div>
    </aside>
  </div>
</section>""".format(form=quote_form(0, "contact-quote",
                                     heading="Request your free quote"),
                     ph=icon("phone"), ml=icon("mail"), pin=icon("pin"), clock=icon("clock", "icon icon--sm"),
                     tel=TEL, phone=PHONE, email=BIZ["email"], street=BIZ["street"],
                     sub=BIZ["suburb"], reg=BIZ["region"], pc=BIZ["postcode"],
                     hours=hours_rows, hnote=BIZ["hours_note"], gbp=BIZ["gbp"], fb=BIZ["facebook"])

    body = (header("contact.html", 0) + crumbs(trail, 0) + '<main id="main">' + hero + cards
            + _trust_bar() + areas_section(0, "Find us on the Northern Gold Coast")
            + faq_block(faqs, "Getting in touch", "Quotes, hours and where we go.")
            + cta_band(0) + '</main>')
    return head(page, 0) + body + footer(0)


# ==========================================================================
# THANK YOU
# ==========================================================================
def thank_you():
    page = {
        "title": "Thank you — your quote request is in | Enviro Garden Care",
        "desc": ("Thanks for contacting Enviro Garden Care & Odd Jobs. Your quote request has been "
                 "received and we will be in touch, usually the same day."),
        "canonical": SITE + "/thank-you.html",
        "body_class": "page-thanks",
        "schema": [local_business_schema(),
                   {"@type": "WebPage", "@id": SITE + "/thank-you.html#webpage",
                    "url": SITE + "/thank-you.html", "name": "Thank you",
                    "inLanguage": "en-AU"}],
    }
    extra = ('<meta name="robots" content="noindex, follow">')

    svc_links = "".join('<li><a href="services/%s.html">%s</a></li>' % (s["slug"], s["name"])
                        for s in SERVICES)

    body = """{hdr}
<main id="main">
<section class="thanks">
  <div class="wrap thanks__inner">
    <div class="thanks__mark" aria-hidden="true">{check}</div>
    <span class="tag tag--glow"><i></i>Request received</span>
    <h1>Thanks — that has come through</h1>
    <p class="thanks__lead">Your quote request is with {owner} now. You will normally hear back the
    <strong>same day</strong>, and always within one business day.</p>
    <div class="thanks__next">
      <h2>What happens next</h2>
      <ol class="thanks__steps">
        <li><span>1</span><div><strong>We read the details</strong><p>Address, property size and the service you need — that is usually enough to price it.</p></div></li>
        <li><span>2</span><div><strong>We call or email your price</strong><p>A per-visit rate for regular mowing, or a quoted figure for acreage, clean-ups and commercial sites.</p></div></li>
        <li><span>3</span><div><strong>You get booked into the round</strong><p>Pick fortnightly, monthly or a one-off. We confirm the first visit and you are away.</p></div></li>
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
      <p><a class="link-arrow" href="index.html">Back to the home page {ar}</a></p>
    </div>
  </div>
</section>
</main>
""".format(hdr=header("", 0), check=icon("check", "icon"), owner=BIZ["owner"].split()[0],
           tel=TEL, phone=PHONE, ph=icon("phone", "icon icon--sm"), svc=svc_links,
           ar=icon("arrow", "icon icon--sm"))

    html = head(page, 0).replace(
        '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">',
        extra)
    return html + body + footer(0)


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
    svc_links = "".join('<li><a href="services/%s.html">%s</a></li>' % (s["slug"], s["name"])
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
      <p><a class="link-arrow" href="index.html">Back to the home page {ar}</a></p>
    </div>
    <div class="thanks__urgent">
      <h2>Need a quote?</h2>
      <p>Call {owner} direct and skip the browsing.</p>
      <a class="btn btn--primary btn--lg" href="tel:{tel}">{ph}Call {phone}</a>
    </div>
  </div>
</section>
</main>
""".format(hdr=header("", 0), svc=svc_links, ar=icon("arrow", "icon icon--sm"),
           owner=BIZ["owner"].split()[0], tel=TEL, phone=PHONE,
           ph=icon("phone", "icon icon--sm"))
    html = head(page, 0).replace(
        '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">',
        '<meta name="robots" content="noindex, follow">')
    return html + body + footer(0)
