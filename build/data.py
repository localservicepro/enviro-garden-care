# -*- coding: utf-8 -*-
"""Content model for the Enviro Garden Care & Odd Jobs website.

Keyword targets, meta titles, H1s and FAQ structure come from the Local
Service Pro SEO research (build/seo-research-source.html, 4 Sep 2026).

Copy amendments from the client's review are applied per the Change Doc
(Google Sheet "Change Doc - Enviro Garden Care & Odd Jobs", rows 7-94,
15 & 21 Sep 2026). Where a row is cited below it is as "CD r<n>".

Change content here, not in the generated HTML.
"""

SITE = "https://envirogardencare.com.au"

BIZ = {
    "name": "Enviro Garden Care & Odd Jobs",
    "short": "Enviro Garden Care",
    # CD r14 / r73: first name only in visible copy. Spelling is Shanon (one n).
    "owner": "Shanon",
    # CD r88: the street never appears in visible copy — "Pimpama QLD 4209" only.
    # CD r94 (awaiting client): it stays in the hidden LocalBusiness schema so the
    # NAP matches the Google Business Profile. Set show_street_in_schema=False
    # if Shanon says no.
    "street": "14 Cullen Street",
    "show_street_in_schema": True,
    "suburb": "Pimpama",
    "region": "QLD",
    "region_full": "Queensland",
    "postcode": "4209",
    "country": "AU",
    "phone_display": "0407 276 574",
    "phone_e164": "+61407276574",
    "email": "hello@envirogardencare.com.au",
    "lat": "-27.8326247",
    "lng": "153.32468",
    "facebook": "https://www.facebook.com/p/Enviro-Garden-Care-Odd-Jobs-100088271821117/",
    "gbp": "https://maps.app.goo.gl/Q28zDvYDuuXLZRQh9",
    # Confirmed by the client (23 Sep): these hours are correct. Saturday is
    # phone enquiries only — no on-site work. NOTE: the Google Business Profile
    # currently shows Mon–Fri 8–5, Sat 8–12; the client should align it.
    "hours": [
        (["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "07:00", "17:00", "Mon – Fri"),
        (["Saturday"], "07:00", "15:00", "Saturday (phone only)"),
    ],
    # CD r10 / r81 / r86: no Sunday wording, no battery wording here.
    "hours_note": "Saturday is phone enquiries only — no on-site work.",
}

MAP_EMBED = (
    "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3528.257254598568"
    "!2d153.32468!3d-27.8326247!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2"
    "!1s0x8080b68e32a41843%3A0xa20149d71fb924d9!2sEnviro%20Garden%20Care%20%26%20Odd%20Jobs"
    "!5e0!3m2!1sfil!2sph!4v1789265580524!5m2!1sfil!2sph"
)

TRACKING_ID = "tk_5bee5316dafc4ac09c8e0e20ec24e0e4"

# --------------------------------------------------------------------------
# Service-area phrasing — CD r7. The client's range is Parkwood (south) to
# Windaroo (north). "Corridor" wording is gone site-wide.
# --------------------------------------------------------------------------
RANGE = "Parkwood to Windaroo"
RANGE_TAIL = "and all suburbs in between"
ANY_SUBURB = "any other suburb between Parkwood and Windaroo"

# The single sentence written for AI/generative engines to lift verbatim.
# CD r18 / r71 / r90: family-owned, Parkwood to Windaroo, no battery claim.
CITABLE = (
    "Enviro Garden Care &amp; Odd Jobs is a Pimpama-based, family-owned lawn mowing "
    "and garden maintenance business servicing the Northern Gold Coast from "
    "Parkwood to Windaroo and all suburbs in between."
)
# CD r71 gives the About page its own, tighter version.
CITABLE_ABOUT = (
    "Enviro Garden Care &amp; Odd Jobs is a Pimpama-based, small family-owned lawn "
    "mowing business servicing the Northern Gold Coast from Parkwood to Windaroo "
    "and all suburbs in between."
)

# Mowing frequencies — CD r9, confirmed by the client 23 Sep (closes r93):
# fortnightly, three-weekly through winter, or one-off. Never monthly.
FREQ = "fortnightly, three-weekly through winter, or one-off"
FREQ_SHORT = "fortnightly or one-off"

# Google rating — verified from the Business Profile listing data on 23 Sep 2026
# (4.9 from 62 reviews, 60 of them five-star). Visible text only; NOT put into
# schema — Google disallows self-serving aggregateRating on LocalBusiness.
GOOGLE_RATING = {"value": "4.9", "count": "62"}

# Three five-star Google reviews for the homepage. The client has approved
# picking any three (23 Sep). The review text could not be fetched from this
# build environment (Google Maps and every review aggregator are blocked), so
# these three are PLACEHOLDERS — the build prints a warning while
# "placeholder" is True. Paste the real text, first name and suburb, then flip
# the flag. Keep them verbatim; do not tidy the customer's wording.
REVIEWS = [
    {"placeholder": True, "who": "Google review · Coomera",
     "text": "Turns up when he says he will, which is more than I can say for the last three mowers I tried. Lawn looks sharp and the edges are actually done."},
    {"placeholder": True, "who": "Google review · Ormeau Hills",
     "text": "We have just over an acre at Ormeau Hills that had got away from us. Slashed, cut back and cleaned up in a day, and now he keeps it on a cycle."},
    {"placeholder": True, "who": "Google review · Upper Coomera",
     "text": "Fortnightly through summer and he has not missed one. The yard is done before we get home from work and the price has never changed."},
]

# Pricing language — CD r13: a property cannot be quoted without inspection.
PRICE = "an approximate price, pending inspection"

# --------------------------------------------------------------------------
# Images
# --------------------------------------------------------------------------
# All client photography is served from Google Drive's public image CDN.
# Two folders:
#   TEMP   = "Temporary Photos"  1fNAUinCZXQD56NgmTM1Dd5FK92IUXXuf  (originals from old site)
#   REVIEW = "Review images"     1V6Bf9lBqDxaI-CE35rUcyfAPFJ7UvBCl  (client uploads, 14 + 22 Sep)
#
# CD r16: no photo used more than once per page; every photo must match its section.
#
# HOW THESE WERE ASSIGNED — every file below was downloaded through the Drive
# connector and looked at on 23 Sep 2026. Subjects are what is actually in
# frame. Several "originals" turned out to be the same picture at different
# sizes; only the largest copy of each is kept. See README "Photos" for the
# full catalogue, including the files deliberately NOT used (readable number
# plates, third-party branding, a night shot).
def drive(file_id, width=1600):
    return "https://lh3.googleusercontent.com/d/%s=w%d" % (file_id, width)


POOL = {
    # ---- Client uploads 22 Sep, named by the client (all 1920x1440 JPG) ----
    "resi_1":        "14xziNswK0nBuYw_EmJEV9WuOL9qiRYyk",  # mown small front lawn from the carport, EGC trailer at edge
    "resi_2":        "1TExm0WDLLzCpPTlPjBgbp0IQwYfBnrQf",  # elevated view, mown front lawn, ute + trailer kerbside
    "resi_3":        "1kBkZeMU73WmPeNEsJITK8_shqnIOaI9H",  # near top-down: manicured lawn, clipped box hedge, ute + trailer
    "acreage_1":     "1teoT6Wp1pMou3r89v0PHOOD1dZEQTZF8",  # Hustler zero-turn on mown acreage lawn, gums, cane, blue sky
    "acreage_2":     "1kA25zHtvNTMa4nXHo0saucEXvgbfADqs",  # Hustler beside a wall of unmown chest-high grass
    "garden_mulch":  "1-NptyUyR1DZT8ub444JoBER1JVny8fGT",  # freshly mulched bed of golden canes along a colorbond fence
    "commercial_1":  "1iacBzoG5NBUfnn2uMoH8kNWj0Yo_kgTY",  # branded trailer outside industrial units at sunset
    # not used: "commercial 2" (third-party signage, FOR SALE sign), "commercial 3"
    # (night shot, readable plate), "garden cleanup.png" (7.5 MB, could not be
    # fetched to check), "van 3"/"sunset 1"/"sunset 2"/"image0 (6)" (640px copies).
    # ---- Client uploads 14 Sep (UUID filenames, all 1920x1440 JPG) ----
    "trailer_tip_sun": "1h79qYOoDPBng6SSenOEHcYIfUZ2vZ-nW",  # trailer tipping green waste at the facility, sunny
    "hedge_tall":      "1gmsb2rpSRSp25MnY89K-IOVxYegYmqfI",  # tall clipped lilly-pilly hedge beside a driveway
    "acreage_dam":     "14TsqNanmSn5YDJ1hcwNf4crnbG87GIBr",  # wide acreage lawn sloping to a dam, horse yards, shed
    "hedge_waterfront":"1d7XgBEn2duZCx_54PMXAs01Zl0RSeusU",  # long box hedge along a waterfront house
    "topiary":         "1FvgsB5hdp5EGRDScfq12RWdaBJ-_oMnQ",  # three ball-clipped topiary shrubs in a pebble bed
    "family_mower":    "1E4B0dz7DFxZYvmN_NhpTjWPZt99k1JvI",  # Shanon with two young children behind the stand-on mower (PORTRAIT, faces)
    "lawn_sign_14":    "1_kih-rfuc8AmFUwv49v24EG8TVry-W-a",  # immaculate front lawn with the EGC "proudly maintained by" sign
    "naturestrip_56":  "1x6_wqV7i5fBQA61vTA1tU8BKnKARp0SI",  # mown nature strip on a new-estate street, EGC yard sign
    "hedge_beds":      "1Y2xndc22sPNQ1ffGEVwh4l7XZxADWg-u",  # clipped box hedges + grass tree in raised timber beds
    "naturestrip_16":  "1PRrgncT5s_zPnrIQNyB6weiGnKAgQKwK",  # nature strip along a stone-clad house, EGC ute + trailer
    "van_estate":      "1xv1OlHToJ3W-MuFg0suMa_tGB_HG0A-3",  # branded van at the industrial estate (own van plate readable)
    "hedge_squared":   "1WdN_2XoR--tN9ui3N789wQFj52P4U-mb",  # close-up of a freshly squared-off tall hedge
    "trailer_sunset":  "1z7ntkfjfHxIbfLLfOLpgcqRPS7MGlCBT",  # side-on branded trailer, cane field, orange sunset (no plate)
    # not used: 1ORgY0NvlAxy05ZaSelqmi4rAqqtUBE3F (readable plate on a customer's
    # car + dog), 1-OvA64ri2XSv9rpxudLJPIklDXgON57I (neighbours' plates readable).
    # ---- Originals from the old site (webp) — largest copy of each scene ----
    "hero":            "1v50z_PLo_6Ft-U027nD1Q-VtFtzRv_Xc",  # 2560px: same house-14 lawn + sign as lawn_sign_14
    "rideon_river":    "143PG3RJgZnpXDnlPHb_a46vdUOxSkmAt",  # 2016px: Hustler on a huge mown riverside field, daytime
    "rideon_sunset":   "1q-NSWe2ZeTKZ-SYcBX3Z0yr7AvNPPEQh",  # 1920x2560 PORTRAIT: Hustler on the riverside field at sunset
    "trailer_tip_grey":"1DPTCRjv7eyJcpsk1p_rqeUkWd7HVkRWs",  # 2560px: trailer tipping green waste, overcast
    "before_after":    "1---Fr4ddP5c3s3TQXofTzuk1WaHesQUw",  # 1176px square: before/after collage of an overgrown nature strip
    "daughter":        "1oAo_C-cAicH_lNhtk8UvXwiWdq_tnSRk",  # 1200px square: Shanon's daughter, thumbs up, hosing the lawn (face)
    "lawn_best":       "1zjOeo0z5zYz4Ba0HN1e9OHgLxmgj2Bew",  # 1200px: striped front lawn, colorbond fence — the client's "keep the first photo"
    "van_low":         "1msGblCcKbIJUURADZPt0EWK7zRLytb4L",  # 640px: low-angle branded van over a mown lawn ("van 1.jpg")
    # not used: 1W0FUz2hRBXCJFPdlxeDhYnGM4HMW8ukx (trailer plate readable; trailer_sunset
    # is the same evening), 1rW_quVFoi_MST6FW435CSSBQWHyHEnfN (child's face, alternate
    # frame of "daughter"), and the smaller copies of the scenes above:
    # 1H0FhMI3oExVvBKcKR0TpdXdUKe94NzJ3, 1_aHGRK3aF7Kg9uNxKCz9PqEBSbbOptt4,
    # 1mLEYN2LQBdPPtNPH0NNJwGuU0BzK9sRu, 1a-nqGc_KouyxhtTicg7UZjQhNGeXxph2,
    # 1_VURECkgTaVDnDm2B1sp2zPrc8Cd8ptj, 1obEOqbWZwZPv-53mxuynPhS3WWcv77AY,
    # 1a8xV5xmVlqIahKg-RtXf3w6oNGzxw2aW, 1lyKrO6tPH4RE_HlatcfzRa4lSNnvEQ3S,
    # 11ZFwWYMrZXG9iJ8TFCCzAlPlMUB_vrN9.
    "logo":   "1z4Ip6GLPeDBuyDfUf-Vy28bBA0MB_R4c",
}


def P(key, width=1200):
    return drive(POOL[key], width)


IMG = {
    "logo":           P("logo", 320),
    "hero":           P("hero", 1800),          # house-14 lawn with the EGC sign
    "about":          P("resi_2"),              # elevated mown lawn with the ute + trailer
    "why":            P("resi_3"),              # manicured lawn + box hedge, top-down
    "cta":            P("trailer_sunset", 1800),
    # Service cards — CD r23-r28, each matching its service.
    "svc_mowing":     P("resi_1"),              # residential front lawn
    "svc_acreage":    P("acreage_1"),           # zero-turn on an acreage lawn
    "svc_garden":     P("hedge_squared"),       # hedge (CD r23)
    "svc_green":      P("trailer_tip_sun"),     # trailer tipping green waste
    "svc_commercial": P("commercial_1"),        # branded trailer at an industrial estate
    "svc_odd":        P("naturestrip_16"),      # residential, not acreage (CD r28)
    # Services hub hero — must not be any of the six card images above.
    "services_hero":  P("lawn_best", 1800),
}

# Per-page galleries — CD r31, r44, r50, r55, r58, r66, r70, r75.
# Each list is unique within itself and against that page's hero/cards;
# cross-page reuse is fine. Alt text describes what is in frame; no suburb is
# claimed for a photo unless the client tells us where it was taken.
def _g(key, alt, width=900):
    return (P(key, width), alt)


GALLERY_HOME = [  # 9 tiles: first is the 2x2 feature (CD r31: one of each only)
    _g("lawn_best",       "Freshly mowed front lawn with crisp edges — lawn mowing Gold Coast by Enviro Garden Care, Pimpama"),
    _g("acreage_dam",     "Acreage lawn mown down to the dam, horse yards behind — acreage mowing Gold Coast"),
    _g("hedge_tall",      "Tall lilly-pilly hedge clipped straight beside a driveway — hedge trimming Northern Gold Coast"),
    _g("trailer_tip_grey","Enviro Garden Care trailer tipping green waste at the facility — green waste removal Gold Coast"),
    _g("lawn_sign_14",    "Immaculate front lawn with the Enviro Garden Care yard sign — regular lawn mowing Northern Gold Coast"),
    _g("van_estate",      "Enviro Garden Care van at an industrial estate — commercial property maintenance Gold Coast"),
    _g("garden_mulch",    "Garden bed freshly mulched along a colorbond fence — garden maintenance Gold Coast"),
    _g("daughter",        "Thumbs up on a freshly mowed lawn — family-owned lawn mowing on the Northern Gold Coast"),
    _g("topiary",         "Ball-clipped topiary shrubs in a pebble bed — garden maintenance Northern Gold Coast"),
]

GALLERY_ABOUT = [  # CD r75: keep the first, then nice lawns and hedges
    _g("lawn_best",       "Freshly mowed front lawn with crisp edges — Enviro Garden Care &amp; Odd Jobs, Pimpama"),
    _g("family_mower",    "Shanon and the kids with the stand-on mower — family-owned lawn mowing, Northern Gold Coast"),
    _g("lawn_sign_14",    "Front lawn kept immaculate, with the Enviro Garden Care yard sign — regular mowing clients"),
    _g("hedge_beds",      "Clipped box hedges and a grass tree in raised timber beds — garden maintenance Northern Gold Coast"),
]

GALLERY_BY_SERVICE = {
    "lawn-mowing": [  # CD r44: keep first + daughter; ride-ons out, real lawns in
        _g("lawn_best",      "Freshly mowed front lawn with crisp edges — lawn mowing Coomera by Enviro Garden Care"),
        _g("daughter",       "Thumbs up on a freshly mowed lawn — family-owned lawn mowing, Northern Gold Coast"),
        _g("lawn_sign_14",   "Front lawn after a regular mow, Enviro Garden Care yard sign on the retaining wall — lawn mowing Northern Gold Coast"),
        _g("naturestrip_56", "Nature strip and front lawn mown on a new-estate street — lawn mowing Coomera growth belt"),
    ],
    "acreage-mowing": [  # CD r50: keep the ride-on, everything else acreage
        # acreage_1 is this page's hero/card image, so it is not repeated here.
        _g("rideon_river",   "Zero-turn ride-on on a large mown riverside block — acreage mowing Gold Coast"),
        _g("acreage_dam",    "Acreage lawn mown down to the dam with horse yards behind — acreage mowing Gold Coast"),
        _g("acreage_2",      "Zero-turn beside chest-high unmown grass — before and after on an acreage block"),
        _g("rideon_sunset",  "Ride-on mower on a riverside paddock at sunset — acreage mowing Northern Gold Coast"),
    ],
    "garden-maintenance": [  # CD r55: all hedge trimming and garden photos
        # hedge_squared is this page's hero/card image, so it is not repeated here.
        _g("hedge_tall",       "Tall lilly-pilly hedge clipped straight beside a driveway — hedge trimming Gold Coast"),
        _g("hedge_waterfront", "Long box hedge trimmed level along a waterfront home — hedge trimming Northern Gold Coast"),
        _g("topiary",          "Ball-clipped topiary shrubs in a white-pebble bed — garden maintenance Gold Coast"),
        _g("garden_mulch",     "Golden cane palms in a freshly mulched bed — mulching and garden maintenance Gold Coast"),
    ],
    "green-waste-removal": [  # CD r58: mix of lawns, hedges, acreage + trailer tipping green waste.
        # trailer_tip_sun is this page's hero/card image, so it is not repeated here.
        _g("trailer_tip_grey", "Trailer tipping a load of green waste at the facility — green waste removal Gold Coast"),
        _g("before_after",     "Before and after: overgrown nature strip and front yard cut back and tidied — yard clean-up Gold Coast"),
        _g("acreage_dam",      "Acreage block cut back to the dam — site clean-up Northern Gold Coast"),
        _g("hedge_beds",       "Hedges clipped and beds tidied after a clean-up — green waste removal Northern Gold Coast"),
    ],
    "commercial-property-maintenance": [  # CD r66: vehicles outside commercial properties.
        # commercial_1 is this page's hero/card image, so it is not repeated here.
        _g("van_estate",     "Enviro Garden Care van at an industrial estate — commercial grounds maintenance Gold Coast"),
        _g("van_low",        "Branded van parked over a freshly mown verge — commercial lawn care Gold Coast"),
        _g("naturestrip_56", "Street verge mown on a new estate — body corporate and estate grounds maintenance Gold Coast"),
        _g("resi_3",         "Lawn and box hedge kept sharp, ute and trailer on site — scheduled grounds maintenance Gold Coast"),
    ],
    "odd-jobs-handyman": [  # CD r70: no handyman photos exist — all different, no doubles.
        # naturestrip_16 is this page's hero/card image, so it is not repeated here.
        _g("before_after",  "Before and after: an overgrown yard brought back — odd jobs and yard clean-ups, Northern Gold Coast"),
        _g("daughter",      "Happy customer — odd jobs and handyman help, Northern Gold Coast"),
        _g("topiary",       "Topiary shrubs and pebble bed tidied — odd jobs and garden care Gold Coast"),
        _g("resi_2",        "Front lawn mown, ute and trailer kerbside — odd jobs and lawn care, Northern Gold Coast"),
    ],
}

# --------------------------------------------------------------------------
# Service areas — 19 suburbs, grouped as the research recommends. CD r7:
# no "corridor" wording.
# --------------------------------------------------------------------------
AREA_GROUPS = [
    ("Coomera to Pimpama",
     "The growth belt we mow most — new builds, compact blocks and strata.",
     ["Coomera", "Upper Coomera", "Coomera Waters", "Pimpama", "Oxenford"]),
    ("Helensvale &amp; Hope Island",
     "Established gardens, hedges and premium canal estates.",
     ["Helensvale", "Hope Island", "Sanctuary Cove", "Pacific Pines", "Parkwood", "Arundel"]),
    ("Ormeau, Yatala &amp; Windaroo acreage belt",
     "Lifestyle lots, rural blocks and industrial estates north of the M1.",
     ["Ormeau", "Ormeau Hills", "Yatala", "Stapylton", "Jacobs Well", "Willowvale",
      "Windaroo", "Mount Warren"]),
]

ALL_SUBURBS = [s for _, _, group in AREA_GROUPS for s in group]

# --------------------------------------------------------------------------
# Services — one distinct primary keyword per page, no overlap
# --------------------------------------------------------------------------
SERVICES = [
    {
        "slug": "lawn-mowing",
        "nav": "Lawn Mowing",
        "name": "Lawn Mowing",
        "keyword": "lawn mowing Coomera",
        "volume": "50 searches/mo",
        "h1": "Lawn Mowing Coomera &amp; Upper Coomera — Regular Residential Mowing",
        "title": "Lawn Mowing Coomera | Enviro Garden Care &amp; Odd Jobs",
        # CD r91: no battery / monthly / taken-away wording in metas.
        "desc": ("Regular lawn mowing Coomera, Upper Coomera and Coomera Waters. Mow, edge and "
                 "blow down, fortnightly or one-off. Approximate price, pending inspection — "
                 "0407 276 574."),
        # CD r37 / r38 / r92: no "corridor", no "monthly".
        "tagline": ("Fortnightly, three-weekly through winter, or one-off mowing across Coomera, Upper Coomera "
                    "and any other suburb between Parkwood and Windaroo."),
        "audience": "Homeowners, renters and strata in the Coomera growth belt",
        "img": "svc_mowing",
        "icon": "mower",
        "suburbs": ["Coomera", "Upper Coomera", "Coomera Waters", "Pimpama", "Oxenford", "Helensvale"],
        # CD r40: Brisbane sentence removed.
        "intro": (
            "Regular <strong>lawn mowing in Coomera</strong> keeps a new-estate lawn looking "
            "like the display home rather than the vacant block next door. Enviro Garden Care "
            "&amp; Odd Jobs mows across Coomera, Upper Coomera, Coomera Waters and any other "
            "suburb between Parkwood and Windaroo on a fortnightly (three-weekly through winter) or one-off "
            "schedule, from our base ten minutes up the road in Pimpama."),
        "body": [
            ("What a standard mow includes", [
                "Cut to the right height for your grass type — we do not scalp couch or buffalo in summer",
                "All edges trimmed: fence lines, paths, driveway, garden beds and around the letterbox",
                "Hard surfaces blown down so the clippings end up in the bin, not on your porch",
                # CD r41
                "Clippings and green waste placed in your green waste bin",
                "Gates closed, pets kept in mind, and a message when we are done if you are not home",
            ]),
            # CD r42, simplified by the client 23 Sep: fortnightly; three-weekly through winter; one-off.
            ("Schedules that suit south-east Queensland grass", [
                "<strong>Fortnightly through the growing season</strong> — couch and kikuyu run hard through the wet season",
                "<strong>Three-weekly through winter</strong> — growth slows, and so does your bill",
                "<strong>One-off tidy-ups</strong> for inspections, end of lease, or a block that has got away from you",
                "<strong>Holiday cover</strong> so you are not coming home to knee-high grass",
            ]),
        ],
        "faqs": [
            ("Do you do lawn mowing in Coomera and Upper Coomera?",
             "Yes. We service Coomera, Upper Coomera, Coomera Waters and any other suburb "
             "between Parkwood and Windaroo from our base in Pimpama, with fortnightly "
             "schedules (three-weekly through winter) for residential and strata properties."),
            ("How much does lawn mowing cost on the Gold Coast?",
             "Most standard residential lawns in Pimpama, Coomera and Helensvale fall into a set "
             "per-visit rate; larger or overgrown blocks are priced on size and access. Regular "
             "fortnightly clients pay less per visit than one-offs. Call 0407 276 574 for an "
             "approximate price, pending inspection."),
            ("Do I need to be home when you mow?",
             "No. As long as we can get to the lawn and any gates are unlocked, we will mow, "
             "tidy up and let you know it is done. Most of our regular clients are at work when we visit."),
            # CD r46
            ("Do you take the clippings with you?",
             "No. Grass clippings go in your green waste bin unless arranged otherwise, as "
             "there is an extra charge for removal. Ask when you book if you would like it "
             "taken away."),
        ],
    },
    {
        "slug": "acreage-mowing",
        "nav": "Acreage &amp; Ride-On",
        "name": "Acreage &amp; Ride-On Mowing",
        "keyword": "acreage mowing Gold Coast",
        "volume": "70 searches/mo",
        "h1": "Acreage Mowing Gold Coast — Ride-On Mowing for Large Blocks",
        "title": "Acreage Mowing Gold Coast | Enviro Garden Care &amp; Odd Jobs",
        "desc": ("Acreage mowing Gold Coast — ride-on mowing, slashing and brush cutting for "
                 "lifestyle lots at Jacobs Well, Yatala and Ormeau Hills. Free estimate: 0407 276 574."),
        # CD r47
        "tagline": ("Ride-on mowing and slashing for lifestyle lots and rural blocks — "
                    "all suburbs between Parkwood and Windaroo."),
        "audience": "Acreage and lifestyle-lot owners north of the M1",
        "img": "svc_acreage",
        "icon": "tractor",
        "suburbs": ["Jacobs Well", "Yatala", "Stapylton", "Ormeau Hills", "Willowvale",
                    "Mount Warren", "Windaroo", "Ormeau"],
        # CD r48
        "intro": (
            "<strong>Acreage mowing on the Gold Coast</strong> is a different job to a suburban "
            "lawn, and a push mower will not finish it before dark. We bring ride-on gear to "
            "lifestyle lots and rural blocks across Jacobs Well, Yatala, Stapylton, Ormeau Hills, "
            "Willowvale and all other suburbs between Parkwood and Windaroo — from a tidy "
            "half-acre house paddock to a block that has not been touched since the last wet season."),
        "body": [
            ("What we handle on a large block", [
                "Ride-on mowing for open paddock and house-yard areas",
                "Slashing for long grass, vacant land and blocks that have got away",
                "Brush cutting and whipper snipping around sheds, tanks, fence lines and dam banks",
                "Track, driveway and firebreak maintenance",
                # CD r49
                "Clean-up and green waste removal once the cutting is finished, for an additional charge",
            ]),
            ("Before we price an acreage job", [
                "<strong>Block size and how much of it is actually mown</strong> — five acres with two mown is a very different price to five acres wall to wall",
                "<strong>Access</strong> — gate widths, slopes, boggy ground and anything the ride-on cannot safely cross",
                "<strong>Obstacles</strong> — stumps, star pickets, irrigation, rock and hidden debris are worth pointing out before we start",
                "<strong>How long since the last cut</strong> — a first cut on overgrown ground takes longer and is priced accordingly, then regular visits cost less",
            ]),
        ],
        "faqs": [
            ("Do you mow acreage properties near Jacobs Well and Yatala?",
             "Yes. Ride-on and acreage mowing for lifestyle lots and rural blocks across Jacobs "
             "Well, Yatala, Stapylton, Ormeau Hills and Willowvale, and all other suburbs between "
             "Parkwood and Windaroo, including slashing, brush cutting and clean-up."),
            ("How much does acreage mowing cost?",
             "Acreage is priced on the area actually being cut, the access, and how long the "
             "grass has been left. A regular maintenance visit costs noticeably less per acre "
             "than a first cut on an overgrown block. Call 0407 276 574 for an approximate "
             "price, pending inspection."),
            ("Can you mow a block that has not been cut in months?",
             "Yes. Overgrown blocks are slashed first to bring the height down, then cut back to "
             "a normal finish. Let us know what is under the grass — star pickets, stumps and "
             "irrigation are easier to avoid when we know they are there."),
            ("Do you mow vacant land for council notices or before a sale?",
             "Yes. Vacant block slashing, pre-sale tidy-ups and compliance cuts across the "
             "Ormeau, Yatala, Windaroo and Jacobs Well acreage belt, usually within a few days of the call."),
        ],
    },
    {
        "slug": "garden-maintenance",
        "nav": "Garden &amp; Hedges",
        "name": "Garden Maintenance &amp; Hedge Trimming",
        "keyword": "garden maintenance Gold Coast",
        "volume": "140 searches/mo",
        "h1": "Garden Maintenance Gold Coast — Hedges, Pruning &amp; Weed Control",
        "title": "Garden Maintenance Gold Coast | Enviro Garden Care &amp; Odd Jobs",
        "desc": ("Garden maintenance Gold Coast — hedge trimming, pruning, weeding and mulching "
                 "in Helensvale, Hope Island and Sanctuary Cove. Free estimate: 0407 276 574."),
        # CD r51
        "tagline": ("Hedges, pruning, weeding and mulching for established gardens — "
                    "servicing all suburbs between Parkwood and Windaroo."),
        "audience": "Established-garden suburbs from Helensvale to Sanctuary Cove",
        "img": "svc_garden",
        "icon": "shears",
        "suburbs": ["Helensvale", "Hope Island", "Sanctuary Cove", "Parkwood", "Arundel",
                    "Pacific Pines", "Oxenford"],
        # CD r52
        "intro": (
            "<strong>Garden maintenance on the Gold Coast</strong> is really a subtropical "
            "problem: everything grows twice as fast as the plan allowed for. We keep hedges "
            "square, beds clear and shrubs in shape across Helensvale, Hope Island, Sanctuary "
            "Cove, Pacific Pines, Parkwood and Arundel, also servicing all suburbs between "
            "Parkwood and Windaroo — as a scheduled visit or a one-off reset before the garden "
            "gets ahead of you again."),
        "body": [
            ("What garden maintenance covers", [
                # CD r53: no drop sheet is used.
                "Hedge trimming — straight lines and level tops",
                "Pruning and shaping of shrubs, natives and small ornamental trees",
                "Weeding and weed control through beds, paths, driveways and gravel",
                "Mulching to hold moisture through summer and slow the weeds down",
                "Bed edging and tidy-ups so the garden reads as maintained from the street",
                # CD r54
                "All prunings and green waste taken away when we leave, for an additional charge",
            ]),
            ("When to book what", [
                "<strong>Hedges</strong> — two to three trims a year on the Gold Coast; more for lilly pilly and murraya through the wet",
                "<strong>Mulch</strong> — top up before summer to cut watering and suppress weeds",
                "<strong>Pruning</strong> — late winter for most shrubs, straight after flowering for the rest",
                "<strong>Pre-sale and pre-inspection resets</strong> — book a week out so the garden has time to settle and look established, not freshly attacked",
            ]),
        ],
        "faqs": [
            ("What does garden maintenance include?",
             "Hedge trimming, pruning, weeding, weed control, mulching and bed edging. Green "
             "waste removal is available for an additional charge. We work across Helensvale, "
             "Hope Island, Sanctuary Cove, Pacific Pines, Parkwood and Arundel, and all suburbs "
             "between Parkwood and Windaroo."),
            ("How often should hedges be trimmed on the Gold Coast?",
             "Most Gold Coast hedges need trimming two to three times a year. Fast growers like "
             "lilly pilly and murraya often want a fourth trim through the summer wet season to "
             "keep the shape."),
            ("Do you take the prunings away?",
             "Yes, for an additional charge. Hedge cuttings, prunings and weeds can be loaded "
             "into our enclosed trailer and taken away — tell us when you book so we allow for "
             "it. Otherwise they go in your green waste bin."),
            ("Can you maintain a garden while we are away or between tenants?",
             "Yes. Scheduled garden maintenance for absentee owners, holiday homes, rentals and "
             "body corporates across the Northern Gold Coast, with photos after the visit if you want them."),
        ],
    },
    {
        "slug": "green-waste-removal",
        "nav": "Green Waste &amp; Clean-Ups",
        "name": "Green Waste &amp; Site Clean-Ups",
        "keyword": "green waste removal Gold Coast",
        "volume": "50 searches/mo",
        "h1": "Green Waste Removal Gold Coast — Yard &amp; Site Clean-Ups",
        "title": "Green Waste Removal Gold Coast | Enviro Garden Care &amp; Odd Jobs",
        "desc": ("Green waste removal Gold Coast: overgrown yards, end-of-lease and storm clean-ups "
                 "in Pimpama, Ormeau and Oxenford. Removal at an additional charge. 0407 276 574."),
        # CD r26
        "tagline": ("Overgrown yards, end-of-lease resets and storm clean-ups — "
                    "green waste removal available at an additional charge."),
        "audience": "End-of-lease, overgrown blocks and post-storm clean-ups",
        "img": "svc_green",
        "icon": "truck",
        "suburbs": ["Pimpama", "Ormeau", "Oxenford", "Coomera", "Upper Coomera", "Yatala"],
        # CD r11 / r56
        "intro": (
            "<strong>Green waste removal on the Gold Coast</strong> is usually the difference "
            "between a job finished and a pile in the driveway waiting three weeks for a council "
            "collection. We clear overgrown yards, end-of-lease properties and storm damage "
            "across Pimpama, Ormeau, Oxenford and all suburbs between Parkwood and Windaroo. "
            "Clippings normally go in your green waste bin; for bigger clean-ups we load it into "
            "our enclosed trailer and take it away the same visit, for an additional charge."),
        "body": [
            ("Clean-ups we take on", [
                "Overgrown yards and neglected blocks brought back to a mown finish",
                "End-of-lease and pre-sale clean-ups so the property passes its inspection",
                "Storm and wind damage — fallen branches, palm fronds and debris cleared",
                "Garden bed strip-outs, dead plant removal and old mulch clear-outs",
                "Existing piles of prunings, clippings and garden waste loaded and removed, for an additional charge",
            ]),
            ("Why the enclosed trailer matters", [
                "Nothing blows out on the M1 between your place and the tip",
                # CD r57
                "We can take mixed green waste in one load instead of several trips, at an additional charge",
                "Loads are tarped and tidy, which matters on body corporate and commercial sites",
                "Green waste is disposed of properly rather than dumped on a vacant block",
            ]),
        ],
        "faqs": [
            # CD r36
            ("Do you take the green waste away after mowing or hedge trimming?",
             "Mostly it goes in your green waste bin. We can take it away for an additional "
             "charge, and a special booking is normally needed — usually as part of a bigger "
             "garden clean-up."),
            ("Can you clear a yard that is completely overgrown?",
             "Yes. Overgrown yards are slashed down first, then cut back to a normal mown finish "
             "and cleared. We handle end-of-lease, pre-sale and vacant blocks across Pimpama, "
             "Ormeau, Oxenford and Coomera."),
            ("Will you remove a pile of branches I have already cut?",
             "Yes, for an additional charge. If you have already done the cutting, we can load "
             "the pile and take it away — priced on the volume and how far it has to be carried."),
            ("How quickly can you do a storm clean-up?",
             "We prioritise storm and access-blocking work. Call 0407 276 574 and we will tell "
             "you honestly when we can get there rather than booking you in and not turning up."),
        ],
    },
    {
        "slug": "commercial-property-maintenance",
        "nav": "Commercial",
        "name": "Commercial &amp; Industrial Maintenance",
        "keyword": "commercial property maintenance Gold Coast",
        "volume": "high intent",
        "h1": "Commercial Property Maintenance Gold Coast — Grounds &amp; Lawn Care",
        "title": "Commercial Property Maintenance Gold Coast | Enviro Garden Care",
        "desc": ("Commercial property maintenance Gold Coast — scheduled grounds and lawn care for "
                 "body corporates and industrial estates in Yatala and Stapylton. Call 0407 276 574."),
        # CD r59
        "tagline": ("Scheduled grounds care for body corporates, retail and industrial sites — "
                    "servicing all suburbs between Parkwood and Windaroo."),
        "audience": "Property managers, body corporates and industrial estates",
        "img": "svc_commercial",
        "icon": "building",
        "suburbs": ["Yatala", "Stapylton", "Arundel", "Hope Island", "Coomera", "Ormeau"],
        # CD r60 / r61
        "intro": (
            "<strong>Commercial property maintenance on the Gold Coast</strong> is judged on two "
            "things: whether the site looks cared for when someone pulls into the car park, and "
            "whether you have to chase the contractor. We run scheduled grounds and lawn care for "
            "body corporates, retail sites and industrial estates across Yatala, Stapylton, "
            "Arundel, Hope Island and all other suburbs between Parkwood and Windaroo — on a set "
            "roster you can put straight into the budget."),
        "body": [
            ("What a scheduled site visit covers", [
                "Lawn and common-area mowing on an agreed roster",
                "Edging, line trimming and blow-down of car parks, paths and entries",
                "Hedge, shrub and garden bed maintenance to keep the frontage presentable",
                "Weed control through car parks, fence lines and hard stand",
                # CD r62
                "Green waste removed on the same visit, for an additional charge",
                "Storm and after-hours clean-ups by arrangement",
            ]),
            # CD r63 / r64 / r65
            ("Why managers keep us on the roster", [
                "<strong>One contact.</strong> You deal with Shanon, not a call centre and a rotating crew",
                "<strong>Timed around tenants.</strong> Early or after-hours weekday visits by arrangement for retail and customer-facing sites",
                "<strong>Reporting.</strong> Photos after each visit if your body corporate or owner wants a record",
                "<strong>Fixed schedule, fixed price.</strong> Priced per fortnight so it goes straight into the budget",
            ]),
        ],
        "faqs": [
            # CD r35
            ("Can you handle body corporate or commercial grounds maintenance on the Northern Gold Coast?",
             "Yes. Scheduled grounds maintenance for body corporates, retail sites and industrial "
             "estates across Yatala, Stapylton, Arundel and Hope Island, and any other suburb "
             "between Parkwood and Windaroo, on a set roster with one point of contact."),
            ("Do you work outside business hours?",
             "By arrangement, yes. Early-morning or after-hours weekday visits can be scheduled "
             "for tenanted premises where a mid-day mow would get in the way."),
            ("Do you provide photos or reports after each visit?",
             "Yes, on request. Many of our body corporate and property manager clients get photos "
             "after every scheduled visit as a record for owners."),
            ("Are you insured for commercial sites?",
             "Yes — we carry public liability insurance and can provide a current certificate of "
             "currency before work starts on your site."),
        ],
    },
    {
        "slug": "odd-jobs-handyman",
        "nav": "Odd Jobs",
        "name": "Odd Jobs &amp; Handyman Repairs",
        "keyword": "odd jobs handyman Gold Coast",
        "volume": "long-tail / high intent",
        "h1": "Odd Jobs &amp; Handyman Repairs — Northern Gold Coast",
        "title": "Odd Jobs &amp; Handyman Gold Coast | Enviro Garden Care",
        # CD r69: no fence painting.
        "desc": ("Odd jobs and minor handyman repairs on the Northern Gold Coast: flat pack and "
                 "trampoline assembly, flyscreens and local transport. Call 0407 276 574."),
        # CD r67
        "tagline": ("The small jobs that never quite make it to the top of the list — "
                    "servicing all suburbs between Parkwood and Windaroo."),
        "audience": "Homeowners and renters with a list of small jobs",
        "img": "svc_odd",
        "icon": "tools",
        "suburbs": ["Pimpama", "Coomera", "Upper Coomera", "Ormeau", "Helensvale", "Oxenford"],
        # CD r67 / r68
        "intro": (
            "The <em>&amp; Odd Jobs</em> half of the name is not decoration. In the quieter "
            "months we take on the minor repairs and assembly work that sit on the list for "
            "ages — across Pimpama, Coomera, Upper Coomera, Ormeau, Helensvale and all suburbs "
            "between Parkwood and Windaroo. If it is a small job and it is not licensed trade "
            "work, ask."),
        "body": [
            # CD r68 / r69
            ("Odd jobs we take on during the quieter months", [
                "Flat pack furniture assembly — beds, wardrobes, desks, shelving",
                "Trampoline, swing set and outdoor play equipment assembly",
                "Flyscreen repairs and replacement screens",
                "Local transport of goods in our semi-enclosed trailer — pickups, deliveries and tip runs",
            ]),
            ("What we do not do", [
                "Licensed electrical work",
                "Licensed plumbing or gas work",
                "Structural building work or anything requiring certification",
                "Roof work and anything needing height safety equipment",
            ]),
        ],
        "faqs": [
            ("What kind of odd jobs do you do?",
             "Flat pack and trampoline assembly, flyscreen repairs and local transport of goods "
             "in our trailer. We take on minor, unlicensed work in the quieter months — often "
             "while we are already on site for a mow."),
            ("Can you do odd jobs at the same visit as my mow?",
             "Often, yes, outside peak mowing season. Tell us what is on the list when you book "
             "and we will allow the extra time rather than making a second trip."),
            ("Do you do electrical or plumbing work?",
             "No. Licensed electrical, plumbing, gas, roof and structural work is outside what we "
             "take on. We will tell you straight away if a job needs a licensed trade."),
            ("Can you pick something up and deliver it locally?",
             "Yes. We run a semi-enclosed trailer and can collect and deliver goods locally across "
             "the Northern Gold Coast — marketplace pickups, deliveries and tip runs."),
        ],
    },
]

SERVICE_BY_SLUG = {s["slug"]: s for s in SERVICES}

# --------------------------------------------------------------------------
# Homepage FAQ — AEO copy from the research, amended per CD r33-r36.
# --------------------------------------------------------------------------
HOME_FAQS = [
    ("How much does lawn mowing cost on the Gold Coast?",
     "Most standard residential lawns in Pimpama, Coomera and Helensvale fall into a set "
     "per-visit rate; larger or overgrown blocks are priced on size and access. Regular "
     "fortnightly clients pay less per visit than one-offs. Call 0407 276 574 for an "
     "approximate price, pending inspection."),
    ("Do you do lawn mowing in Coomera and Upper Coomera?",
     "Yes. We service Coomera, Upper Coomera, Coomera Waters and any other suburb between "
     "Parkwood and Windaroo from our base in Pimpama, with fortnightly schedules "
     "(three-weekly through winter) for residential and strata properties."),
    ("Do you mow acreage properties near Jacobs Well and Yatala?",
     "Yes. Ride-on and acreage mowing for lifestyle lots and rural blocks across Jacobs Well, "
     "Yatala, Stapylton, Ormeau Hills, Willowvale and Windaroo, including slashing, brush "
     "cutting and clean-up."),
    # CD r35
    ("Can you handle body corporate or commercial grounds maintenance on the Northern Gold Coast?",
     "Yes. Scheduled grounds maintenance for body corporates, retail sites and industrial estates "
     "across Yatala, Stapylton, Arundel and Hope Island, and any other suburb between Parkwood "
     "and Windaroo, on a set roster with one point of contact."),
    # CD r36
    ("Do you take the green waste away after mowing or hedge trimming?",
     "Mostly it goes in your green waste bin. We can take it away for an additional charge, "
     "and a special booking is normally needed."),
]

# --------------------------------------------------------------------------
# Quote form — GoHighLevel contact field mapping
# name attribute  ->  GHL merge field
# --------------------------------------------------------------------------
FORM_FIELDS = [
    ("full_name", "Name", "{{contact.full_name}}", "text", True,
     "Your name", None),
    ("email", "Email", "{{contact.email}}", "email", True,
     "you@example.com", None),
    ("phone", "Phone", "{{contact.phone}}", "tel", True,
     "0400 000 000", None),
    ("property_address", "Property Address", "{{contact.property_address}}", "text", True,
     "Street, suburb", None),
    ("property_size", "Property Size", "{{contact.property_size}}", "select", False, None,
     ["Small yard (courtyard / townhouse)",
      "Standard residential block (up to 600m²)",
      "Large residential block (600 – 1,000m²)",
      "Half to 1 acre",
      "1 – 5 acres",
      "5+ acres",
      "Commercial / industrial site",
      "Not sure"]),
    ("service_needed", "Service Needed", "{{contact.service_needed}}", "select", True, None,
     ["Lawn mowing",
      "Acreage / ride-on mowing",
      "Garden maintenance &amp; hedge trimming",
      "Green waste removal / clean-up",
      "Commercial &amp; industrial maintenance",
      "Odd jobs &amp; handyman repairs",
      "Something else"]),
    # CD r83: once-off vs regular. New custom field in GHL.
    ("job_type", "Job Type", "{{contact.job_type}}", "select", True, None,
     ["One-off job",
      "Regular maintenance (fortnightly, three-weekly in winter)"]),
    # CD r20: photos of the property. Files cannot travel through the tracking
    # script — uploaded by api/quote.js into the "Job Photos" file field (key contact.job_photos).
    ("property_photos", "Photos of the property", "{{contact.job_photos}}", "file", False,
     "Up to 6 photos of the current condition — front, back, anything overgrown. "
     "Phone photos are fine; we shrink them before sending.", None),
    ("job_notes", "Job Notes", "{{contact.job_notes}}", "textarea", False,
     "Anything we should know — access, gates, dogs, how long since the last cut…", None),
]
