# -*- coding: utf-8 -*-
"""Page bodies. One function per page; each returns the <main> markup."""

from data import (SITE, BIZ, IMG, SERVICES, GALLERY, HOME_FAQS, ALL_SUBURBS,
                  AREA_GROUPS, KEY_SUBURBS, CITABLE)
from templates import (areas_section, cta_band, crumbs, faq_block, gallery_section,
                       icon, lower_name, map_embed, marquee, ndis_band, plain,
                       quote_form, section_head, service_cards, stats_strip, svc_url)

PHONE = BIZ["phone_display"]
TEL = BIZ["phone_e164"]
ADDRESS = "%s, %s %s %s" % (BIZ["street"], BIZ["suburb"], BIZ["region"], BIZ["postcode"])


def _hero_chips(items):
    return "".join('<li>%s%s</li>' % (icon("check", "icon icon--xs"), t) for t in items)


def _steps(steps):
    out = []
    for i, (title, text) in enumerate(steps):
        out.append("""<li class="step reveal" style="--d:%dms">
        <span class="step__num">%02d</span>
        <h3>%s</h3>
        <p>%s</p>
      </li>""" % (i * 90, i + 1, title, text))
    return "\n      ".join(out)


def _points(points, cls="points"):
    out = []
    for i, (ic, title, text) in enumerate(points):
        out.append("""<article class="point reveal" style="--d:%dms">
        <span class="point__icon">%s</span>
        <h3>%s</h3>
        <p>%s</p>
      </article>""" % (i * 70, icon(ic), title, text))
    return "\n      ".join(out)


# --------------------------------------------------------------------------
# Home
# --------------------------------------------------------------------------
def home():
    return """<main id="main">

<section class="hero">
  <div class="hero__bg" aria-hidden="true"></div>
  <div class="hero__glow" aria-hidden="true"><span></span><span></span></div>
  <div class="wrap hero__inner">
    <div class="hero__copy">
      <span class="eyebrow eyebrow--light rise" style="--d:0ms">{pin} Mount Gravatt · Brisbane south side</span>
      <h1 class="rise" style="--d:80ms">Professional Lawn Mowing Services in Brisbane &amp; Surrounding Suburbs</h1>
      <p class="hero__lead rise speakable" style="--d:160ms">
        A1 Lawn Care Pty Ltd provides lawn mowing services in Brisbane from a depot at
        1593 Logan Rd, Mount Gravatt — an NDIS registered provider covering more than 150
        suburbs across Brisbane&#39;s south side, Bayside, Logan and the Redlands.
      </p>
      <ul class="hero__chips rise" style="--d:240ms">{chips}</ul>
      <div class="hero__actions rise" style="--d:320ms">
        <a class="btn btn--primary btn--lg" href="#quote">Get a free quote</a>
        <a class="btn btn--outline btn--lg" href="tel:{tel}">{ph}{phone}</a>
      </div>
      <p class="hero__micro rise" style="--d:400ms">
        Quotes answered seven days · Green waste always taken away · Plan managed invoicing
      </p>
    </div>
    <div class="hero__media rise" style="--d:220ms">
      <figure class="hero__shot">
        <img src="{hero}" width="1000" height="700" loading="eager" decoding="async" fetchpriority="high"
             alt="A1 Lawn Care mowing and tidying a Brisbane lawn — lawn mowing services Brisbane, Mount Gravatt">
      </figure>
      <div class="hero__badge hero__badge--ndis">
        <img src="{ndis}" width="104" height="42" loading="eager" decoding="async"
             alt="NDIS registered provider logo">
        <span>Registered provider</span>
      </div>
      <div class="hero__badge hero__badge--call">
        <strong>{phone}</strong>
        <span>Steve answers, not a call centre</span>
      </div>
    </div>
  </div>
  <div class="hero__ticker">{marquee}</div>
</section>

{ndis_band}

{stats}

<section class="section section--services" id="services">
  <div class="wrap">
    {svc_head}
    <div class="cards">
      {cards}
    </div>
    <p class="section__foot reveal"><a class="link-arrow" href="/services/">See how every service works {ar}</a></p>
  </div>
</section>

<section class="section section--why">
  <div class="wrap">
    {why_head}
    <div class="points">
      {points}
    </div>
  </div>
</section>

<section class="section section--split">
  <div class="wrap split">
    <figure class="split__media reveal">
      <img src="{about}" width="900" height="700" loading="lazy" decoding="async"
           alt="A1 Lawn Care crew at work on a Brisbane southside property — Mount Gravatt lawn and garden care">
      <figcaption class="split__tag">{pinsm} 1593 Logan Rd, Mount Gravatt</figcaption>
    </figure>
    <div class="split__copy reveal">
      <span class="eyebrow">Local, not a franchise</span>
      <h2>A Mount Gravatt crew that actually lives on this side of town</h2>
      <p>A1 Lawn Care is run by {owner} out of {street}, {suburb}. That address matters more
         than it sounds: half our weekly run is inside ten minutes of it, which is why we can
         hold a schedule through the wet season when the grass is growing faster than anybody
         can keep up with.</p>
      <p>We are an <strong>NDIS registered provider</strong>, and yard maintenance for
         participants sits alongside the domestic, strata and commercial work on the same run —
         same crew, same standard, same week.</p>
      <ul class="ticks">
        <li>{ck}Mowing, gardens, hedges, palms and clean-ups from one crew</li>
        <li>{ck}Green waste and clippings leave with us every visit</li>
        <li>{ck}A straight price quoted before we start, and no surprises on the invoice</li>
        <li>{ck}Quotes answered seven days on {phone}</li>
      </ul>
      <a class="btn btn--ghost" href="/about/">More about A1 Lawn Care</a>
    </div>
  </div>
</section>

<section class="section section--process">
  <div class="wrap">
    {process_head}
    <ol class="steps">
      {steps}
    </ol>
  </div>
</section>

{gallery}

{areas}

<section class="section section--quote" id="quote">
  <div class="wrap quote-wrap">
    <div class="quote-wrap__copy reveal">
      <span class="eyebrow">Free quote</span>
      <h2>Tell us about the property, get a price</h2>
      <p>Fill this in and we will come back with a number — usually the same day. If it is
         easier, ring {owner} on <a href="tel:{tel}">{phone}</a> or send a photo of the job.</p>
      <ul class="ticks">
        <li>{ck}No obligation, and no sales call afterwards</li>
        <li>{ck}Plan managed, self managed and NDIA managed NDIS participants welcome</li>
        <li>{ck}One-off, fortnightly, monthly or a standing commercial schedule</li>
      </ul>
      <div class="quote-wrap__nap">
        <p><strong>{biz}</strong><br>{address}</p>
        <p><a href="tel:{tel}">{phone}</a> · <a href="mailto:{email}">{email}</a></p>
      </div>
    </div>
    <div class="reveal">
      {form}
    </div>
  </div>
</section>

{faq}

{cta}

</main>
""".format(
        pin=icon("pin", "icon icon--sm"), pinsm=icon("pin", "icon icon--xs"),
        ph=icon("phone", "icon icon--sm"), ck=icon("check", "icon icon--xs"),
        ar=icon("arrow", "icon icon--sm"),
        tel=TEL, phone=PHONE, email=BIZ["email"], biz=BIZ["name"], address=ADDRESS,
        owner=BIZ["owner"].split()[0], street=BIZ["street"], suburb=BIZ["suburb"],
        hero=IMG["hero"], ndis=IMG["ndis_white"], about=IMG["about"],
        chips=_hero_chips(["NDIS registered provider", "150+ suburbs covered",
                           "Green waste taken away", "Quotes answered 7 days"]),
        marquee=marquee(KEY_SUBURBS + ["Mount Gravatt"]),
        ndis_band=ndis_band(),
        stats=stats_strip(),
        svc_head=section_head(
            "What we do",
            "Six services, one local crew",
            "Every job on this list is quoted, scheduled and finished by the same Mount Gravatt "
            "crew — including the green waste at the end of it."),
        cards=service_cards(),
        why_head=section_head(
            "Why A1",
            "The reasons people keep us on the run",
            "Lawn care is not complicated. Turning up, pricing honestly and cleaning up "
            "properly is where most of it is won or lost."),
        points=_points([
            ("shield", "NDIS registered provider",
             "Not a sideline — NDIS yard and garden maintenance is part of the weekly run, with "
             "invoices sent straight to plan managers."),
            ("pin", "Based at Mount Gravatt",
             "1593 Logan Rd is a real depot on this side of town, not a phone number redirecting "
             "to a franchisee two suburbs over."),
            ("truck", "The waste leaves with us",
             "Clippings, prunings and palm fronds go in the trailer. Nothing is bagged into your "
             "bin or stacked on the verge."),
            ("mower", "Every service from one crew",
             "Mowing, gardens, hedges, palms, coring and clean-ups — one contact, one invoice, "
             "one standard across the lot."),
            ("clock", "A schedule you can plan around",
             "Weekly, fortnightly or monthly, adjusted for the season so you are not paying for "
             "cuts the grass did not need."),
            ("chat", "Straight answers on price",
             "You get a number before we start, and an honest call if a job needs an arborist or "
             "council approval instead of us."),
        ]),
        process_head=section_head(
            "How it works",
            "From first call to finished yard",
            "Four steps, no back and forth, and nobody chasing you afterwards."),
        steps=_steps([
            ("Call or send the form",
             "Ring %s or fill in the quote form. A photo of the job gets you a faster, "
             "firmer price." % PHONE),
            ("We price it properly",
             "Straightforward jobs are quoted off the details and photos. Bigger ones get a "
             "site visit — either way the number comes before any work."),
            ("We book you in",
             "A day you can plan around, on a schedule that suits the season, with plan managed "
             "invoicing set up if you are an NDIS participant."),
            ("Mow, tidy, take the waste",
             "Cut, edge, blow down, and every bit of green waste loaded out. You come home to a "
             "yard that looks finished."),
        ]),
        # 8 photos in a 4-column grid: a 2x2 featured tile would consume 4 cells
        # and leave a hole in the last row. See gallery_section().
        gallery=gallery_section(GALLERY, feature=False),
        areas=areas_section(),
        form=quote_form("quote-home"),
        faq=faq_block(HOME_FAQS,
                      title="Lawn care questions, answered",
                      intro="Prices, NDIS bookings, suburbs and green waste — the six things "
                            "people ask before they book."),
        cta=cta_band(),
    )


# --------------------------------------------------------------------------
# Services hub
# --------------------------------------------------------------------------
def services_hub():
    rows = []
    for i, s in enumerate(SERVICES):
        subs = ", ".join(s["suburbs"][:5])
        rows.append("""<article class="svcrow reveal" style="--d:{d}ms">
      <div class="svcrow__media">
        <img src="{img}" alt="{alt}" loading="lazy" decoding="async" width="800" height="600">
      </div>
      <div class="svcrow__copy">
        <span class="svcrow__icon">{ic}</span>
        <h3><a href="{url}">{name}</a></h3>
        <p>{tag}</p>
        <p class="svcrow__areas">{pin} {subs} and surrounds</p>
        <a class="link-arrow" href="{url}">See {name} {ar}</a>
      </div>
    </article>""".format(d=i * 60, img=IMG[s["img"]], url=svc_url(s["slug"]),
                         alt="%s — A1 Lawn Care Brisbane" % plain(s["name"]),
                         ic=icon(s["icon"]), name=s["name"], tag=s["tagline"],
                         subs=subs, pin=icon("pin", "icon icon--xs"),
                         ar=icon("arrow", "icon icon--sm")))

    return """{crumbs}
<main id="main">

<section class="pagehead">
  <div class="pagehead__glow" aria-hidden="true"></div>
  <div class="wrap pagehead__inner">
    <span class="eyebrow eyebrow--light rise">Services</span>
    <h1 class="rise" style="--d:80ms">Lawn &amp; Garden Services Across Brisbane&#39;s South Side</h1>
    <p class="rise speakable" style="--d:160ms">Six specialist services run out of Mount Gravatt —
      lawn mowing, NDIS yard maintenance, garden maintenance, tree and palm removal, green waste
      removal, and hedging with lawn treatments. One crew, one invoice, the same standard on all
      of them.</p>
    <div class="pagehead__actions rise" style="--d:240ms">
      <a class="btn btn--primary" href="/contact/">Get a free quote</a>
      <a class="btn btn--outline" href="tel:{tel}">{ph}{phone}</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="svcrows">
      {rows}
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="wrap wrap--narrow">
    {head}
    <div class="prose reveal">
      <p>Every service page names the suburbs it covers, what is included, what changes the
         price, and the questions we get asked about it. If the job crosses two of them — a
         clean-up that turns into a palm removal, or a mow that needs the hedges done at the same
         time — it is still one quote and one visit.</p>
      <p>Work that we cannot safely do, we say so: anything close to powerlines, large-canopy
         trees needing a climbing arborist, or protected vegetation that needs Brisbane City
         Council or Redland City Council approval first. You will get pointed in the right
         direction rather than sold something.</p>
    </div>
  </div>
</section>

{areas}

{cta}

</main>
""".format(crumbs=crumbs([("Home", "/"), ("Services", "/services/")]),
           rows="\n    ".join(rows), tel=TEL, phone=PHONE,
           ph=icon("phone", "icon icon--sm"),
           head=section_head("How we work",
                             "One crew for the whole yard",
                             "Six services that overlap the way real jobs do."),
           areas=areas_section(heading="Suburbs these services cover",
                               intro="Every service on this page runs across the same four "
                                     "regions, out of the Mount Gravatt depot."),
           cta=cta_band(title="Not sure which service you need?",
                        text="Describe the job and we will tell you what it actually needs — "
                             "and what it does not."))


# --------------------------------------------------------------------------
# Service page
# --------------------------------------------------------------------------
def service_page(svc):
    blocks = []
    for title, items in svc["body"]:
        lis = "".join("<li>%s%s</li>" % (icon("check", "icon icon--xs"), t) for t in items)
        blocks.append("""<div class="block reveal">
        <h2>%s</h2>
        <ul class="ticks ticks--two">%s</ul>
      </div>""" % (title, lis))

    others = [s for s in SERVICES if s["slug"] != svc["slug"]][:3]
    related = "".join(
        """<a class="related__item" href="{url}">
        <span class="related__icon">{ic}</span>
        <span><strong>{name}</strong><em>{tag}</em></span>
        {ar}
      </a>""".format(url=svc_url(s["slug"]), ic=icon(s["icon"], "icon icon--sm"),
                     name=s["name"], tag=s["tagline"], ar=icon("arrow", "icon icon--sm"))
        for s in others)

    chips = "".join("<li>%s</li>" % s for s in svc["suburbs"])

    return """{crumbs}
<main id="main">

<section class="pagehead pagehead--svc">
  <div class="pagehead__glow" aria-hidden="true"></div>
  <div class="wrap pagehead__inner pagehead__inner--split">
    <div>
      <span class="eyebrow eyebrow--light rise">{ic} {name}</span>
      <h1 class="rise" style="--d:80ms">{h1}</h1>
      <p class="rise speakable" style="--d:160ms">{intro}</p>
      <div class="pagehead__actions rise" style="--d:240ms">
        <a class="btn btn--primary" href="#quote">Get a free quote</a>
        <a class="btn btn--outline" href="tel:{tel}">{ph}{phone}</a>
      </div>
      <ul class="pagehead__chips rise" style="--d:320ms">
        <li>{ck}NDIS registered</li>
        <li>{ck}Green waste removed</li>
        <li>{ck}Mount Gravatt based</li>
      </ul>
    </div>
    <figure class="pagehead__media rise" style="--d:220ms">
      <img src="{img}" width="900" height="700" loading="eager" decoding="async" fetchpriority="high"
           alt="{alt}">
    </figure>
  </div>
</section>

<section class="section">
  <div class="wrap svc">
    <div class="svc__main">
      {blocks}
      <div class="block block--areas reveal">
        <h2>Suburbs we cover for {name_l}</h2>
        <p>Run out of {street}, {suburb} — these are the suburbs this service is in most weeks,
           and we cover more than 150 across Brisbane south, Bayside, Logan and the Redlands.</p>
        <ul class="chips">{chips}</ul>
      </div>
    </div>
    <aside class="svc__side">
      <div class="sticky">
        <div class="sidecard reveal">
          <h2>Get a price for {name_l}</h2>
          <p>Send the details and we will come back the same day, or ring
             <a href="tel:{tel}">{phone}</a>.</p>
          <a class="btn btn--primary btn--block" href="#quote">Request a free quote</a>
          <a class="btn btn--ghost btn--block" href="tel:{tel}">{ph}Call {phone}</a>
          <dl class="sidecard__meta">
            <div><dt>Target area</dt><dd>{first_sub} &amp; Brisbane south</dd></div>
            <div><dt>Best for</dt><dd>{audience}</dd></div>
            <div><dt>Waste</dt><dd>Taken away, every visit</dd></div>
          </dl>
        </div>
        <div class="related reveal">
          <h2>Related services</h2>
          {related}
        </div>
      </div>
    </aside>
  </div>
</section>

<section class="section section--quote section--tint" id="quote">
  <div class="wrap quote-wrap">
    <div class="quote-wrap__copy reveal">
      <span class="eyebrow">Free quote</span>
      <h2>Book {name_l} in {suburb} or anywhere on the southside</h2>
      <p>Tell us about the property and we will price it properly. Photos help, especially for
         palms, hedges and anything overgrown.</p>
      <div class="quote-wrap__nap">
        <p><strong>{biz}</strong><br>{address}</p>
        <p><a href="tel:{tel}">{phone}</a> · <a href="mailto:{email}">{email}</a></p>
      </div>
    </div>
    <div class="reveal">
      {form}
    </div>
  </div>
</section>

{faq}

{cta}

</main>
""".format(crumbs=crumbs([("Home", "/"), ("Services", "/services/"), (svc["name"], svc_url(svc["slug"]))]),
           ic=icon(svc["icon"], "icon icon--sm"), name=svc["name"],
           name_l=lower_name(svc["name"]), h1=svc["h1"], intro=svc["intro"],
           img=IMG[svc["img"]],
           alt="%s — A1 Lawn Care, %s Brisbane" % (plain(svc["h1"]), plain(svc["suburbs"][0])),
           blocks="\n      ".join(blocks), chips=chips, related=related,
           first_sub=svc["suburbs"][0], audience=svc["audience"],
           tel=TEL, phone=PHONE, email=BIZ["email"], biz=BIZ["name"], address=ADDRESS,
           street=BIZ["street"], suburb=BIZ["suburb"],
           ph=icon("phone", "icon icon--sm"), ck=icon("check", "icon icon--xs"),
           form=quote_form("quote-" + svc["slug"], preselect=svc["nav"]),
           faq=faq_block(svc["faqs"],
                         title="%s — your questions" % plain(svc["name"]),
                         intro="Straight answers on price, coverage and what is included.",
                         eyebrow="Answers"),
           cta=cta_band(title="Want this off your list?",
                        text="Free quote, no obligation, and an honest answer on when we can "
                             "get there."))


# --------------------------------------------------------------------------
# About
# --------------------------------------------------------------------------
def about():
    return """{crumbs}
<main id="main">

<section class="pagehead">
  <div class="pagehead__glow" aria-hidden="true"></div>
  <div class="wrap pagehead__inner">
    <span class="eyebrow eyebrow--light rise">About us</span>
    <h1 class="rise" style="--d:80ms">About A1 Lawn Care — Mount Gravatt&#39;s Lawn &amp; Garden Crew</h1>
    <p class="rise speakable" style="--d:160ms">{citable}</p>
    <div class="pagehead__actions rise" style="--d:240ms">
      <a class="btn btn--primary" href="/contact/">Get a free quote</a>
      <a class="btn btn--outline" href="tel:{tel}">{ph}{phone}</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split split--reverse">
    <figure class="split__media reveal">
      <img src="{about}" width="900" height="700" loading="lazy" decoding="async"
           alt="A1 Lawn Care working on a Brisbane southside yard — Mount Gravatt lawn and garden maintenance">
      <figcaption class="split__tag">{pin} {street}, {suburb}</figcaption>
    </figure>
    <div class="split__copy reveal">
      <span class="eyebrow">Who you are dealing with</span>
      <h2>One local crew, run by {owner}</h2>
      <p>A1 Lawn Care Pty Ltd is a local lawn and garden business working out of
         {street}, {suburb} QLD {pc}. When you ring {first}, you get {first} — not a call centre
         booking a franchisee who has never seen your street.</p>
      <p>The work is straightforward and we keep it that way: mowing on a schedule, gardens kept
         in shape, hedges square, palms and small trees taken out, and yards cleared when they
         have got away. Every job finishes the same way — edges trimmed, hard surfaces blown
         down, and the green waste in the trailer rather than in your bin.</p>
      <p>We are <strong>NDIS registered</strong>, and that side of the business has grown for a
         simple reason: participants need someone who turns up on the day they said, does the
         same job every time, and invoices the plan manager without a fuss.</p>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="wrap">
    {values_head}
    <div class="points points--two">
      {points}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap wrap--narrow">
    {std_head}
    <div class="prose reveal">
      <p>Most complaints about lawn care businesses are the same three things: they did not turn
         up, they did not clean up, or the price changed when the invoice arrived. So those are
         the three we hold ourselves to.</p>
      <p><strong>Turning up.</strong> Schedules move for weather, not for a better-paying job
         across town. If a storm week pushes your visit, you hear about it from us first.</p>
      <p><strong>Cleaning up.</strong> A mow is not finished at the last pass of the mower. Edges,
         blow-down and green waste are part of the price, not extras.</p>
      <p><strong>The price.</strong> You get a number before we start. If something on site
         changes the job — a stump nobody mentioned, or a palm hard against a pool fence — we
         stop and talk to you rather than adding it to the bill.</p>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="wrap">
    {find_head}
    <div class="areas">
      <div class="areas__list">
        <article class="area reveal">
          <h3>Visit or send post to</h3>
          <p class="speakable"><strong>{biz}</strong><br>{street}<br>{suburb} {reg} {pc}</p>
          <ul class="ticks">
            <li>{ck}<a href="tel:{tel}">{phone}</a></li>
            <li>{ck}<a href="mailto:{email}">{email}</a></li>
            <li>{ck}{hours_txt}</li>
          </ul>
        </article>
        <article class="area reveal" style="--d:80ms">
          <h3>Regions we run</h3>
          <p>{regions}</p>
          <ul class="chips">{chips}</ul>
        </article>
      </div>
      <div class="areas__map">
        {map}
      </div>
    </div>
  </div>
</section>

{cta}

</main>
""".format(crumbs=crumbs([("Home", "/"), ("About", "/about/")]),
           citable=CITABLE, about=IMG["about"], tel=TEL, phone=PHONE, email=BIZ["email"],
           biz=BIZ["name"], street=BIZ["street"], suburb=BIZ["suburb"], reg=BIZ["region"],
           pc=BIZ["postcode"], owner=BIZ["owner"], first=BIZ["owner"].split()[0],
           ph=icon("phone", "icon icon--sm"), pin=icon("pin", "icon icon--xs"),
           ck=icon("check", "icon icon--xs"),
           hours_txt="%s, %s" % (
               "Mon – Fri 6:30 – 5:00", "Sat 7:00 – 2:00"),
           regions=", ".join(name for name, _, _ in AREA_GROUPS) + " — more than 150 suburbs.",
           chips="".join("<li>%s</li>" % s for s in KEY_SUBURBS),
           map=map_embed(),
           values_head=section_head(
               "What we stand on",
               "Four things we do not cut corners on",
               "None of this is remarkable. It is just rarer than it should be."),
           points=_points([
               ("shield", "NDIS registered provider",
                "Registered, and used to working with plan managers, support "
                "coordinators and participants directly."),
               ("truck", "Green waste always removed",
                "Every clipping, frond and pruning leaves with us. It is quoted in, never added "
                "on afterwards."),
               ("clock", "Reliable scheduling",
                "Weekly, fortnightly or monthly visits that hold through the growing season, "
                "adjusted honestly when the weather forces it."),
               ("star", "One standard for every job",
                "The NDIS yard, the strata block and the family home all get the same finish — "
                "cut, edged, blown down, cleared."),
           ]),
           std_head=section_head("Our standard",
                                 "Three promises, kept boringly",
                                 "Turn up, clean up, and quote it straight."),
           find_head=section_head("Find us",
                                  "Based on Logan Rd at Mount Gravatt",
                                  "A real address on the south side — which is why we can hold "
                                  "a schedule out here."),
           cta=cta_band(title="Ready to hand the yard over?",
                        text="Free quote, no obligation, and a straight answer about when we "
                             "can start."))


# --------------------------------------------------------------------------
# Contact
# --------------------------------------------------------------------------
def contact():
    hours_rows = "".join('<div class="hours__row"><span>%s</span><span>%s – %s</span></div>'
                         % (label, o.lstrip("0"), c.lstrip("0"))
                         for _, o, c, label in BIZ["hours"])
    return """{crumbs}
<main id="main">

<section class="pagehead">
  <div class="pagehead__glow" aria-hidden="true"></div>
  <div class="wrap pagehead__inner">
    <span class="eyebrow eyebrow--light rise">Contact</span>
    <h1 class="rise" style="--d:80ms">Contact A1 Lawn Care — Free Quotes Across Brisbane</h1>
    <p class="rise speakable" style="--d:160ms">Call {phone}, email {email}, or send the form
      below. Quotes are answered seven days, and most come back the same day — including NDIS
      enquiries from participants, plan managers and support coordinators.</p>
    <div class="pagehead__actions rise" style="--d:240ms">
      <a class="btn btn--primary" href="tel:{tel}">{ph}Call {phone}</a>
      <a class="btn btn--outline" href="mailto:{email}">{mail}Email us</a>
    </div>
  </div>
</section>

<section class="section section--quote" id="quote">
  <div class="wrap quote-wrap">
    <div class="quote-wrap__copy reveal">
      <span class="eyebrow">Free quote</span>
      <h2>Send the details, get a price</h2>
      <p>The more you can tell us about the property, the tighter the quote. Photos of anything
         overgrown, or of a palm you want gone, get you a firm number instead of a range.</p>
      <div class="contactcards">
        <a class="contactcard" href="tel:{tel}">
          <span class="contactcard__icon">{ph}</span>
          <span><strong>{phone}</strong><em>Seven days · {first} answers</em></span>
        </a>
        <a class="contactcard" href="mailto:{email}">
          <span class="contactcard__icon">{mail}</span>
          <span><strong>{email}</strong><em>Email a photo of the job</em></span>
        </a>
        <div class="contactcard">
          <span class="contactcard__icon">{pin}</span>
          <span class="speakable"><strong>{street}, {suburb} {reg} {pc}</strong><em>{biz}</em></span>
        </div>
      </div>
      <div class="hours hours--card">
        <h3>{clock} Trading hours</h3>
        {hours_rows}
        <p class="hours__note">{hnote}</p>
      </div>
    </div>
    <div class="reveal">
      {form}
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="wrap">
    {map_head}
    {map}
  </div>
</section>

{faq}

{cta}

</main>
""".format(crumbs=crumbs([("Home", "/"), ("Contact", "/contact/")]),
           tel=TEL, phone=PHONE, email=BIZ["email"], biz=BIZ["name"],
           street=BIZ["street"], suburb=BIZ["suburb"], reg=BIZ["region"], pc=BIZ["postcode"],
           first=BIZ["owner"].split()[0], hours_rows=hours_rows, hnote=BIZ["hours_note"],
           ph=icon("phone", "icon icon--sm"), mail=icon("mail", "icon icon--sm"),
           pin=icon("pin", "icon icon--sm"), clock=icon("clock", "icon icon--sm"),
           form=quote_form("quote-contact"),
           map_head=section_head("Where we are",
                                 "1593 Logan Rd, Mount Gravatt QLD 4122",
                                 "The depot the whole run is built around."),
           map=map_embed(),
           faq=faq_block(HOME_FAQS[:4],
                         title="Before you call",
                         intro="Four things worth knowing about price, NDIS bookings and "
                               "coverage."),
           cta=cta_band(title="Rather just talk it through?",
                        text="Ring %s — you will get a person who has mown in your suburb this "
                             "week." % PHONE))


# --------------------------------------------------------------------------
# Thank you (form redirect target, noindex)
# --------------------------------------------------------------------------
def thank_you():
    cards = "".join(
        '<a class="related__item" href="%s">%s<span><strong>%s</strong><em>%s</em></span>%s</a>'
        % (svc_url(s["slug"]), '<span class="related__icon">%s</span>' % icon(s["icon"], "icon icon--sm"),
           s["name"], s["tagline"], icon("arrow", "icon icon--sm"))
        for s in SERVICES[:3])
    return """<main id="main">
<section class="thanks">
  <div class="wrap thanks__inner">
    <span class="thanks__tick">{ck}</span>
    <h1>Thanks — your quote request is in</h1>
    <p class="thanks__lead">We have got your details and {first} will come back to you, usually
       the same day and always within one business day.</p>
    <div class="thanks__grid">
      <div class="thanks__card">
        <h2>What happens next</h2>
        <ul class="ticks">
          <li>{ck}We read the job details and check the address against this week&#39;s run</li>
          <li>{ck}You get a price — or a couple of questions if the job needs them</li>
          <li>{ck}If you are happy, we book a day and put you on the schedule</li>
        </ul>
      </div>
      <div class="thanks__card">
        <h2>Need it sooner?</h2>
        <p>Ring {first} directly on <a href="tel:{tel}">{phone}</a>, or email
           <a href="mailto:{email}">{email}</a> with a photo of the job.</p>
        <a class="btn btn--primary" href="tel:{tel}">{ph}Call {phone}</a>
      </div>
    </div>
    <div class="related related--wide">
      <h2>While you are here</h2>
      {cards}
    </div>
    <p class="thanks__back"><a class="link-arrow" href="/">Back to the home page {ar}</a></p>
  </div>
</section>
</main>
""".format(ck=icon("check", "icon icon--xs"), first=BIZ["owner"].split()[0], tel=TEL,
           phone=PHONE, email=BIZ["email"], ph=icon("phone", "icon icon--sm"),
           cards=cards, ar=icon("arrow", "icon icon--sm"))


# --------------------------------------------------------------------------
# 404 (noindex)
# --------------------------------------------------------------------------
def not_found():
    links = "".join('<li><a href="%s">%s</a></li>' % (svc_url(s["slug"]), s["name"])
                    for s in SERVICES)
    return """<main id="main">
<section class="thanks">
  <div class="wrap thanks__inner">
    <span class="thanks__code">404</span>
    <h1>That page has been mown down</h1>
    <p class="thanks__lead">The link is broken or the page has moved. Here is everything that
       does exist.</p>
    <div class="thanks__grid">
      <div class="thanks__card">
        <h2>Services</h2>
        <ul class="plainlist">{links}</ul>
      </div>
      <div class="thanks__card">
        <h2>Or just ask</h2>
        <p>Ring {phone} and tell us what you were after — it is quicker than hunting through a
           menu.</p>
        <a class="btn btn--primary" href="tel:{tel}">{ph}Call {phone}</a>
        <a class="btn btn--ghost" href="/contact/">Contact page</a>
      </div>
    </div>
    <p class="thanks__back"><a class="link-arrow" href="/">Back to the home page {ar}</a></p>
  </div>
</section>
</main>
""".format(links=links, phone=PHONE, tel=TEL, ph=icon("phone", "icon icon--sm"),
           ar=icon("arrow", "icon icon--sm"))
