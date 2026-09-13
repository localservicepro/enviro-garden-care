# -*- coding: utf-8 -*-
"""Content model for the A1 Lawn Care Pty Ltd website.

Every keyword target, meta title, meta description, H1 and FAQ question in this
file comes from the Local Service Pro SEO research document
(build/seo-research-source.html, 10 September 2026). Change content here, not in
the generated HTML — the HTML is overwritten on every build.
"""

SITE = "https://www.a1lawncare.net.au"

BIZ = {
    "name": "A1 Lawn Care Pty Ltd",
    "short": "A1 Lawn Care",
    "owner": "Steve Cope",
    "street": "1593 Logan Rd",
    "suburb": "Mount Gravatt",
    "region": "QLD",
    "region_full": "Queensland",
    "postcode": "4122",
    "country": "AU",
    "phone_display": "0456 198 080",
    "phone_e164": "+61456198080",
    "email": "info@a1lawncare.net.au",
    # NOTE: coordinates are the Logan Rd / Mount Gravatt shopping strip, accurate
    # to the block but not surveyed off the title. Confirm before launch —
    # see README.md -> "Confirm before launch".
    "lat": "-27.5413",
    "lng": "153.0789",
    "facebook": "https://www.facebook.com/NDISmowing",
    # The Google Business Profile still points at a dead business.site URL
    # (research, critical issue 03). Until that is fixed and the real profile
    # link is known, we link to a Maps search for the business rather than
    # inventing a short link.
    "gbp": ("https://www.google.com/maps/search/?api=1&amp;query="
            "A1+Lawn+Care+1593+Logan+Rd+Mount+Gravatt+QLD+4122"),
    # NOTE: trading hours are an assumption pending client confirmation.
    # They are published in LocalBusiness schema, so check them first.
    "hours": [
        (["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "06:30", "17:00", "Mon – Fri"),
        (["Saturday"], "07:00", "14:00", "Saturday"),
    ],
    "hours_note": "Sunday and after-hours by arrangement — quotes answered seven days.",
    "abn_note": "NDIS registered provider · ABN available on request",
}

# A keyless Maps embed: no API key, no expiring "pb=" blob, and it resolves to
# the same pin as the address in LocalBusiness schema.
MAP_EMBED = ("https://www.google.com/maps?q=1593+Logan+Rd,+Mount+Gravatt+QLD+4122"
             "&amp;hl=en-AU&amp;z=15&amp;output=embed")

TRACKING_ID = "tk_6582cb70c3d84289821c555a3d8691f9"

# The sentence written for AI assistants and answer engines to lift verbatim.
# Research section 10: "An AI cannot infer what a website does not say."
CITABLE = (
    "A1 Lawn Care Pty Ltd is an NDIS registered lawn mowing and garden maintenance "
    "business at 1593 Logan Rd, Mount Gravatt QLD 4122, servicing more than 150 "
    "suburbs across Brisbane&#39;s south side, Bayside, Logan and the Redlands."
)

# --------------------------------------------------------------------------
# Images
#
# A1's own photography, copied into the client's public Google Drive folder
# (1fNAUinCZXQD56NgmTM1Dd5FK92IUXXuf) and served through Drive's image CDN.
# See README.md -> "Images" for why, and for the move to host-served WebP that
# the speed work in the research depends on.
# --------------------------------------------------------------------------
def drive(file_id, width=1600):
    return "https://lh3.googleusercontent.com/d/%s=w%d" % (file_id, width)


IMG = {
    "logo": drive("1U2I-VOzL-3t1cL8IC5AHD7wQLIVPmn8m", 320),
    "ndis": drive("195PxNdASaGEg3ybUK_4Gqlw0npgq32A3", 420),
    "ndis_white": drive("1mz4OKQJRkENypVqIYE__fkN_sotfs-Oh", 420),
    "hero": drive("170uaoPJkAeuJx3wKXO4H5_13k6NxT_KU", 1400),
    "about": drive("1Wkzjny6oQMAgS-HoSPJnIcfanEJCw7-l", 1200),
    "svc_mowing": drive("17LLWEtvi9r4KdrjcqiGAOt_PiONjtiQ0", 1100),
    "svc_ndis": drive("19SyrnQZQpxBKBpipU_KgQMwRtLEAuPce", 1100),
    "svc_garden": drive("1RXVN3O2REW9lZ0jWIMfZhNf41-IoVnPD", 1100),
    "svc_palm": drive("1QNMD5WrtvtFSxCQpWRZAf2MCoRSqMBpd", 1100),
    "svc_green": drive("1QFPH82fEOQVvwXgYmja6EgPX5h3e0Rxi", 1100),
    "svc_hedging": drive("1m4r-v_9F_t-q5BlJHFkRe9TnJe6w2Tjn", 1100),
    "cta": drive("1uDMkA_7zfHl2Ny0j_u0avcdzErlo3jYt", 1600),
    "work_extra": drive("1Iq1K5Gqmy-TxXCuS3Jkfs4AoX8PiaRMe", 1100),
}

# Gallery — A1's own job photos. Alt text names the service and the area the
# way the research asks for; it is deliberately not claiming a specific suburb
# for a specific photo. See README.md -> "Confirm before launch".
GALLERY = [
    (IMG["svc_mowing"],
     "Lawn mown and edged by A1 Lawn Care — lawn mowing Mount Gravatt, Brisbane"),
    (IMG["svc_ndis"],
     "Yard kept tidy on a regular NDIS maintenance visit — A1 Lawn Care Brisbane"),
    (IMG["svc_garden"],
     "Garden beds weeded and edged — garden maintenance Brisbane by A1 Lawn Care"),
    (IMG["svc_palm"],
     "Palm and tree work on a Brisbane property — palm tree removal by A1 Lawn Care"),
    (IMG["svc_green"],
     "Yard cleared and green waste loaded out — green waste removal Brisbane"),
    (IMG["svc_hedging"],
     "Hedge trimmed square and level — hedge trimming Brisbane southside, A1 Lawn Care"),
    (IMG["cta"],
     "Lawn cut and cleaned up after a service — lawn care Brisbane south side"),
    (IMG["work_extra"],
     "Finished lawn and garden on a Brisbane southside property — A1 Lawn Care"),
]

# --------------------------------------------------------------------------
# Service areas
#
# Research, critical issue 01: not one suburb appears anywhere on the current
# site. These are the four regions the business works, grouped the way the
# research specifies (Brisbane South, Bayside, Logan, Redlands).
# --------------------------------------------------------------------------
AREA_GROUPS = [
    ("Brisbane South",
     "Our home ground — ten minutes from the Logan Rd depot at Mount Gravatt.",
     ["Mount Gravatt", "Mount Gravatt East", "Upper Mount Gravatt", "Wishart",
      "Mansfield", "Holland Park", "Holland Park West", "Tarragindi", "Greenslopes",
      "Coorparoo", "Camp Hill", "Carina", "Carina Heights", "Moorooka", "Salisbury",
      "Coopers Plains", "Annerley", "Fairfield", "Yeronga", "Yeerongpilly", "Nathan",
      "Rocklea", "Archerfield", "Acacia Ridge", "Sunnybank", "Sunnybank Hills",
      "Robertson", "MacGregor", "Eight Mile Plains", "Runcorn", "Kuraby", "Calamvale",
      "Stretton", "Algester", "Parkinson", "Drewvale", "Karawatha", "Larapinta",
      "Willawong", "Pallara", "Heathwood", "Doolandella", "Durack", "Inala",
      "Richlands", "Ellen Grove", "Forest Lake", "Rochedale", "Mackenzie", "Burbank"]),
    ("Bayside",
     "Carindale across to the water — established gardens, hedges and canal blocks.",
     ["Carindale", "Cannon Hill", "Tingalpa", "Murarrie", "Hemmant", "Wynnum",
      "Wynnum West", "Manly", "Manly West", "Lota", "Wakerley", "Gumdale", "Chandler",
      "Belmont", "Ransome", "Bulimba", "Balmoral", "Hawthorne", "Morningside",
      "Norman Park", "Seven Hills", "Lytton"]),
    ("Logan",
     "Down the highway from Springwood to Beenleigh, including the newer estates.",
     ["Springwood", "Slacks Creek", "Underwood", "Daisy Hill", "Shailer Park",
      "Loganholme", "Tanah Merah", "Rochedale South", "Priestdale", "Logan Central",
      "Woodridge", "Kingston", "Marsden", "Crestmead", "Berrinba", "Browns Plains",
      "Regents Park", "Heritage Park", "Hillcrest", "Boronia Heights", "Park Ridge",
      "Munruben", "Greenbank", "Logan Reserve", "Waterford", "Waterford West",
      "Bethania", "Edens Landing", "Holmview", "Beenleigh", "Eagleby",
      "Mount Warren Park", "Windaroo", "Bannockburn", "Yarrabilba", "Cornubia",
      "Carbrook", "Loganlea", "Meadowbrook"]),
    ("Redlands",
     "Capalaba through to the bay — acreage, coastal blocks and holiday properties.",
     ["Capalaba", "Alexandra Hills", "Cleveland", "Ormiston", "Wellington Point",
      "Birkdale", "Thorneside", "Thornlands", "Victoria Point", "Redland Bay",
      "Sheldon", "Mount Cotton"]),
]

ALL_SUBURBS = [s for _, _, group in AREA_GROUPS for s in group]

# Suburbs the research names as keyword targets — these must appear in body copy,
# not only in a footer list.
KEY_SUBURBS = ["Mount Gravatt", "Mount Gravatt East", "Sunnybank", "Carindale",
               "Coorparoo", "Greenslopes", "Tarragindi", "Wynnum", "Cannon Hill",
               "Tingalpa", "Wakerley", "Bulimba", "Moorooka", "Coopers Plains",
               "Acacia Ridge", "Inala", "Springwood", "Slacks Creek",
               "Browns Plains", "Capalaba"]

# --------------------------------------------------------------------------
# Services — six pages, one distinct primary keyword each, no overlap.
# Page spec: research section 07, Phase 4.
# --------------------------------------------------------------------------
SERVICES = [
    {
        "slug": "lawn-mowing",
        "nav": "Lawn Mowing",
        "name": "Lawn Mowing",
        "keyword": "lawn mowing mount gravatt",
        "volume": "difficulty 4 — the address suburb",
        "h1": "Lawn Mowing Mount Gravatt — Domestic, Acreage &amp; Commercial",
        "title": "Lawn Mowing Mount Gravatt | A1 Lawn Care Brisbane",
        "desc": ("Lawn mowing Mount Gravatt and Brisbane southside — domestic, acreage and "
                 "commercial mowing, edging and clean-up. NDIS registered. Free quote: "
                 "0456 198 080."),
        "tagline": "Domestic, acreage and commercial mowing on a schedule that suits the grass.",
        "audience": "Homeowners and body corporates in Mount Gravatt, Holland Park and Wishart",
        "img": "svc_mowing",
        "icon": "mower",
        "suburbs": ["Mount Gravatt", "Mount Gravatt East", "Upper Mount Gravatt", "Wishart",
                    "Holland Park", "Tarragindi", "Coorparoo", "Greenslopes", "Mansfield"],
        "intro": (
            "<strong>Lawn mowing in Mount Gravatt</strong> starts at our own front door — the "
            "depot is at 1593 Logan Rd, so half our regular run is inside a ten-minute drive. "
            "A1 Lawn Care mows domestic blocks, acreage and commercial grounds across Mount "
            "Gravatt, Mount Gravatt East, Upper Mount Gravatt, Wishart, Holland Park, "
            "Tarragindi, Coorparoo and Greenslopes, weekly, fortnightly, monthly or as a "
            "one-off tidy-up."),
        "body": [
            ("What every mow includes", [
                "Cut at the right height for your grass — we do not scalp buffalo or couch through a Brisbane summer",
                "Edges trimmed along fences, paths, driveway, beds and around the letterbox",
                "Paths, drive and patio blown down so the clippings leave with us",
                "Clippings and green waste taken away — nothing left filling your wheelie bin",
                "Gates shut, pets kept in mind, and a message when we are done if you are out",
            ]),
            ("Domestic, acreage and commercial", [
                "<strong>Domestic blocks</strong> — standard suburban yards across the southside, on a schedule that changes with the season",
                "<strong>Acreage mowing Brisbane</strong> — lifestyle lots and larger holdings cut with ride-on gear and slashed where it has got away",
                "<strong>Commercial mowing Brisbane</strong> — body corporate grounds, strata, childcare, rentals and small industrial sites on a maintenance contract",
                "<strong>One-off and end-of-lease cuts</strong> — inspections, sales, or a block nobody has touched since the last wet season",
            ]),
            ("Schedules that match Brisbane grass", [
                "<strong>Weekly or fortnightly, October to March</strong> — couch, kikuyu and buffalo run hard through the storm season",
                "<strong>Fortnightly to monthly, April to September</strong> — growth slows and so does the cost",
                "<strong>Holiday cover</strong> so you are not coming home to a paddock",
            ]),
        ],
        "faqs": [
            ("Do you mow lawns in Mount Gravatt and Mount Gravatt East?",
             "Yes. A1 Lawn Care is based at 1593 Logan Rd, Mount Gravatt QLD 4122, and Mount "
             "Gravatt, Mount Gravatt East and Upper Mount Gravatt are on our weekly run, along "
             "with Wishart, Holland Park, Tarragindi, Coorparoo and Greenslopes."),
            ("How much does lawn mowing cost in Brisbane?",
             "Lawn mowing in Brisbane is quoted per visit on the size of the lawn, the access, "
             "and how long it has been since the last cut. Regular fortnightly clients pay less "
             "per visit than one-off jobs, and an overgrown first cut costs more than the visits "
             "that follow. Call 0456 198 080 for a price on your block."),
            ("Do I need to be home when you mow?",
             "No. As long as we can reach the lawn and any side gates are unlocked, we mow, tidy "
             "up and let you know it is finished. Most of our regular clients are at work when "
             "we visit."),
            ("Do you do commercial and acreage mowing?",
             "Yes. We mow body corporate and strata grounds, rental portfolios and small "
             "industrial sites on a maintenance schedule, and we have the gear for acreage and "
             "lifestyle blocks across Brisbane&#39;s south side, Logan and the Redlands."),
        ],
    },
    {
        "slug": "ndis-yard-garden-maintenance",
        "nav": "NDIS Yard &amp; Garden",
        "name": "NDIS Yard &amp; Garden Maintenance",
        "keyword": "ndis mowing",
        "volume": "70 searches/mo · difficulty 20",
        "h1": "NDIS Registered Lawn Mowing &amp; Yard Maintenance in Brisbane",
        "title": "NDIS Lawn Mowing Brisbane | A1 Lawn Care",
        "desc": ("NDIS mowing and yard maintenance in Brisbane from a registered provider. "
                 "Plan managed, self managed or NDIA managed. Mount Gravatt based — "
                 "0456 198 080."),
        "tagline": "Registered provider — plan managed, self managed or NDIA managed.",
        "audience": "NDIS participants, plan managers and support coordinators",
        "img": "svc_ndis",
        "icon": "shield",
        "suburbs": ["Mount Gravatt", "Sunnybank", "Springwood", "Capalaba", "Wynnum",
                    "Browns Plains", "Coorparoo", "Slacks Creek", "Carindale"],
        "intro": (
            "A1 Lawn Care is an <strong>NDIS registered provider</strong>, and "
            "<strong>NDIS mowing</strong> and yard maintenance is a core part of what we do "
            "every week — not a sideline. We work with participants, plan managers and support "
            "coordinators across Brisbane&#39;s south side, Bayside, Logan and the Redlands, on "
            "the same regular schedule and the same standard as every other job on the run."),
        "body": [
            ("What NDIS mowing and yard maintenance covers", [
                "Regular lawn mowing, edging and blow-down on a set schedule you can plan around",
                "Garden tidy-ups — weeding, pruning, bed edging and mulching",
                "Hedge and shrub trimming so paths, windows and clotheslines stay clear",
                "Green waste and clippings taken away every visit",
                "Yard clean-ups and clearing where a property has got away or access has become unsafe",
            ]),
            ("How booking works with your plan", [
                "<strong>Plan managed</strong> — we invoice your plan manager directly, with the service dates and NDIS details they need",
                "<strong>Self managed</strong> — we invoice you and you claim it back through the portal",
                "<strong>NDIA managed</strong> — talk to us and we will walk through what your plan allows before anything is booked",
                "<strong>Support coordinators</strong> — one contact, consistent crew, and reporting on visits if a participant needs it",
            ]),
            ("Why participants stay with us", [
                "The same person turns up, so nobody is explaining the property again every visit",
                "Set schedule, so the yard never gets to the point where it is a hazard",
                "Quiet, tidy, and out of the way — we work around the household, not through it",
                "Straight answers on what is claimable and what is not, before we start",
            ]),
        ],
        "faqs": [
            ("Is A1 Lawn Care an NDIS registered provider, and how do I book with my plan?",
             "Yes — A1 Lawn Care is an NDIS registered provider. If your plan is plan managed we "
             "invoice your plan manager directly; if it is self managed we invoice you to claim "
             "through the portal; and if it is NDIA managed, call us on 0456 198 080 and we will "
             "go through what your plan covers before booking anything in."),
            ("What does NDIS lawn mowing cost?",
             "NDIS lawn mowing is quoted the same way as any other job — on lawn size, access and "
             "how often we visit — and the quote is written so a plan manager can see exactly what "
             "is being charged. Regular scheduled visits cost less per visit than one-off clean-ups."),
            ("Do you do NDIS yard maintenance near me in Brisbane?",
             "We cover more than 150 suburbs across Brisbane&#39;s south side, Bayside, Logan and "
             "the Redlands from our base at Mount Gravatt, including Sunnybank, Carindale, "
             "Springwood, Capalaba, Wynnum and Browns Plains."),
            ("Can support coordinators set up a recurring service?",
             "Yes. Support coordinators and plan managers can set up a recurring fortnightly or "
             "monthly service with one point of contact, a consistent crew and invoices that "
             "match the service dates."),
        ],
    },
    {
        "slug": "garden-maintenance",
        "nav": "Garden Maintenance",
        "name": "Garden Maintenance",
        "keyword": "garden maintenance brisbane",
        "volume": "170 searches/mo · difficulty 30",
        "h1": "Garden Maintenance Brisbane — Pruning, Weeding &amp; Edging",
        "title": "Garden Maintenance Brisbane | A1 Lawn Care",
        "desc": ("Garden maintenance Brisbane — pruning, weeding, edging and mulching across "
                 "Mount Gravatt, Carindale, Sunnybank and Bayside. Free quote: 0456 198 080."),
        "tagline": "Pruning, weeding, edging and mulching on a schedule.",
        "audience": "Homeowners, strata managers and rental property managers",
        "img": "svc_garden",
        "icon": "shears",
        "suburbs": ["Carindale", "Bulimba", "Coorparoo", "Sunnybank", "Wishart",
                    "Holland Park", "Cleveland", "Wellington Point", "Mansfield"],
        "intro": (
            "<strong>Garden maintenance in Brisbane</strong> is really a subtropical problem: "
            "everything grows twice as fast as the landscape plan allowed for, and two wet weeks "
            "in February will undo a season of tidy. A1 Lawn Care keeps beds clear, shrubs in "
            "shape and edges sharp across Carindale, Bulimba, Coorparoo, Sunnybank, Wishart and "
            "the Redlands — as a standing visit or a one-off reset."),
        "body": [
            ("What garden maintenance services in Brisbane cover", [
                "Pruning and shaping of shrubs, natives and small ornamental trees",
                "Weeding through beds, paths, driveways and gravel — by hand where spraying is not appropriate",
                "Bed edging so the garden reads as maintained from the street",
                "Mulching to hold moisture through summer and slow the weeds down",
                "Seasonal cut-backs before the wet, and again before spring growth",
                "All prunings and green waste taken away the same visit",
            ]),
            ("Rentals, strata and managed properties", [
                "<strong>Property managers</strong> — routine inspections passed without a last-minute scramble",
                "<strong>Body corporate and strata</strong> — common areas, entry gardens and verges on a fixed schedule",
                "<strong>Pre-sale presentation</strong> — the garden tidied and edged before photography",
                "<strong>Between tenancies</strong> — reset overgrown beds and hand the property back presentable",
            ]),
            ("When to book what in south-east Queensland", [
                "<strong>September to November</strong> — cut back, mulch and edge before the growing season takes off",
                "<strong>December to March</strong> — regular visits; this is when a garden gets away fastest",
                "<strong>April to August</strong> — shaping, weed control and structural pruning while growth is slow",
            ]),
        ],
        "faqs": [
            ("What does garden maintenance in Brisbane include?",
             "Our garden maintenance covers pruning and shaping, weeding, bed edging, mulching and "
             "seasonal cut-backs, with all prunings and green waste taken away at the end of the "
             "visit. It can run as a standing fortnightly or monthly service, or as a one-off reset."),
            ("Do you maintain gardens for rentals and body corporates?",
             "Yes. We work with property managers, landlords and body corporates across Brisbane&#39;s "
             "south side and Bayside on fixed schedules, which keeps routine inspections and common "
             "areas from becoming a problem."),
            ("Can you take on a garden that has been neglected?",
             "Yes. Overgrown gardens are quoted as a first-visit reset — cut back, weeded, edged and "
             "cleared — and regular visits after that cost noticeably less."),
            ("Do you do garden maintenance in Carindale and Sunnybank?",
             "Yes. Carindale, Sunnybank, Bulimba, Coorparoo, Wishart and Mansfield are all on our "
             "regular run, along with the Redlands from Capalaba out to Cleveland."),
        ],
    },
    {
        "slug": "tree-palm-removal",
        "nav": "Tree &amp; Palm Removal",
        "name": "Tree &amp; Palm Removal",
        "keyword": "palm tree removal brisbane",
        "volume": "110 searches/mo · difficulty 27",
        "h1": "Palm Tree Removal Brisbane — Fast, Insured, Fully Cleaned Up",
        "title": "Palm Tree Removal Brisbane | A1 Lawn Care",
        "desc": ("Palm tree removal Brisbane — palms, small trees and stumps removed and the "
                 "whole mess taken away. Mount Gravatt based, NDIS registered. Free quote: "
                 "0456 198 080."),
        "tagline": "Palms, small trees and the whole mess gone the same day.",
        "audience": "Homeowners, acreage owners and commercial site managers",
        "img": "svc_palm",
        "icon": "palm",
        "suburbs": ["Mount Gravatt", "Sunnybank", "Carindale", "Wynnum", "Springwood",
                    "Capalaba", "Coorparoo", "Runcorn", "Redland Bay"],
        "intro": (
            "<strong>Palm tree removal in Brisbane</strong> is the job people put off, usually "
            "until fronds are dropping on the roof or the trunk is lifting a path. A1 Lawn Care "
            "removes palms and small trees across Brisbane&#39;s south side, Bayside, Logan and "
            "the Redlands — cleaned up properly, with the green waste loaded out rather than "
            "stacked on the verge."),
        "body": [
            ("What we remove", [
                "Cocos, Alexandra, Bangalow, Golden Cane and Foxtail palms — single specimens or a whole row",
                "Small and medium trees within safe working reach of the ground and our gear",
                "Storm-damaged and leaning palms that have become a risk to a roof, fence or pool",
                "Stumps ground or dug out where access allows, so you can turf or replant over the top",
                "Dead fronds, seed pods and self-seeded palm suckers cleared at the same time",
            ]),
            ("What the price depends on", [
                "<strong>Height and species</strong> — a three-metre Golden Cane and a fifteen-metre Cocos are different jobs entirely",
                "<strong>Access</strong> — whether we can get a machine to it, or it has to be roped down over a pool and carried out by hand",
                "<strong>What is underneath</strong> — roofs, fences, pools, sheds and power lines all change the method",
                "<strong>Stump and waste</strong> — whether the stump is ground out and how much material has to leave the site",
            ]),
            ("Work we will not quote over the phone", [
                "Anything near powerlines, which is Energex-adjacent work and gets assessed on site",
                "Large-canopy trees needing a climbing arborist and a traffic plan — we will tell you straight and point you to one",
                "Protected vegetation, where Brisbane City Council or Redland City Council approval is needed before anything is cut",
            ]),
        ],
        "faqs": [
            ("How much does palm tree removal cost in Brisbane?",
             "Palm tree removal in Brisbane is priced on the height and species of the palm, how "
             "much access there is for machinery, what is underneath it, and whether the stump is "
             "removed. A single small Golden Cane in an open yard is a very different price to a "
             "tall Cocos roped down over a pool. Send a photo to 0456 198 080 and we will give you "
             "a figure."),
            ("Do you take the palm away or leave it on the verge?",
             "We take it with us. Fronds, trunk sections and debris are loaded out and the area is "
             "raked and blown down before we leave — removal and clean-up are quoted as one job."),
            ("Can you remove the stump as well?",
             "Usually, yes — stumps are ground or dug out where access allows, so the area can be "
             "turfed or replanted. If access is too tight for a grinder we will say so up front."),
            ("Do you remove palms in Sunnybank, Carindale and the Redlands?",
             "Yes. Palm and small tree removal runs across the same area as the rest of our work: "
             "Brisbane south, Bayside, Logan and the Redlands, from Mount Gravatt out to Redland Bay."),
        ],
    },
    {
        "slug": "green-waste-removal",
        "nav": "Green Waste &amp; Clean-Ups",
        "name": "Green Waste Removal &amp; Site Clean-Ups",
        "keyword": "green waste removal brisbane",
        "volume": "210 searches/mo · difficulty 31",
        "h1": "Green Waste Removal Brisbane — Yard &amp; Site Clean-Ups",
        "title": "Green Waste Removal Brisbane | A1 Lawn Care",
        "desc": ("Green waste removal Brisbane — yard clean-ups, storm debris, end of lease and "
                 "pre-sale clearing, loaded and taken away. Free quote: 0456 198 080."),
        "tagline": "Yard clean-ups, storm debris and end-of-lease clearing, loaded and gone.",
        "audience": "Vendors preparing to sell, landlords, builders and end-of-lease tenants",
        "img": "svc_green",
        "icon": "truck",
        "suburbs": ["Mount Gravatt", "Moorooka", "Acacia Ridge", "Inala", "Slacks Creek",
                    "Beenleigh", "Wynnum", "Capalaba", "Browns Plains"],
        "intro": (
            "<strong>Green waste removal in Brisbane</strong> is usually the difference between a "
            "yard that has been worked on and a yard that looks finished. A1 Lawn Care clears and "
            "carts away prunings, clippings, storm debris, old garden beds and general yard rubbish "
            "across the south side, Logan, Bayside and the Redlands — either as part of a job we "
            "are already doing, or as a clean-up on its own."),
        "body": [
            ("What we clear and cart away", [
                "Prunings, clippings, palm fronds and hedge cuttings",
                "Storm debris and fallen branches after a Brisbane summer blow-through",
                "Overgrown beds, dead plants and self-seeded growth pulled out and removed",
                "General yard rubbish that has accumulated behind the shed",
                "Whole-site clean-ups where a property has been vacant or neglected",
            ]),
            ("When people call us for a clean-up", [
                "<strong>Before a sale</strong> — vendors getting a yard photograph-ready in one visit",
                "<strong>End of lease</strong> — tenants and property managers clearing a yard back to inspection standard",
                "<strong>Builders and trades</strong> — site tidy-ups and vegetation clearing before or after work",
                "<strong>After a storm</strong> — debris and damaged growth cleared so the yard is safe to use again",
                "<strong>Deceased estates and vacant homes</strong> — handled quietly and without fuss",
            ]),
            ("How a clean-up is quoted", [
                "<strong>Volume</strong> — how many trailer loads are actually leaving the site",
                "<strong>Access</strong> — whether we can back a trailer in or everything is carried out by hand",
                "<strong>What is in it</strong> — green waste is straightforward; mixed rubbish needs a different tip run",
                "<strong>Cutting versus carting</strong> — whether we are clearing growth first or only removing what is already on the ground",
            ]),
        ],
        "faqs": [
            ("Do you take away the green waste and clippings after a job?",
             "Yes. Clippings, prunings and green waste leave with us on every visit at no extra "
             "charge — nothing is bagged up and left in your wheelie bin or stacked on the verge."),
            ("How much does green waste removal cost in Brisbane?",
             "Green waste removal is quoted on volume and access — how many loads are going out, and "
             "whether we can reach it with a trailer. A one-off yard clean-up is quoted as a job "
             "rather than an hourly rate, so you know the number before we start."),
            ("Can you clear a yard before a sale or an end-of-lease inspection?",
             "Yes, and it is one of the most common jobs we do. Pre-sale and end-of-lease clean-ups "
             "are usually booked within a few days, and we will tell you honestly what can be done "
             "in one visit."),
            ("Do you clear storm damage and fallen branches?",
             "Yes. After a summer storm we clear fallen branches, damaged growth and debris so the "
             "yard is usable again, across Brisbane south, Logan, Bayside and the Redlands."),
        ],
    },
    {
        "slug": "hedging-lawn-treatments",
        "nav": "Hedging &amp; Lawn Treatments",
        "name": "Hedging &amp; Lawn Treatments",
        "keyword": "hedge trimming services brisbane",
        "volume": "30 searches/mo · difficulty 18",
        "h1": "Hedge Trimming &amp; Lawn Treatments — Brisbane Southside",
        "title": "Hedge Trimming Services Brisbane | A1 Lawn Care",
        "desc": ("Hedge trimming services Brisbane southside, plus lawn coring, top dressing and "
                 "weed control across Mount Gravatt and Bayside. Free quote: 0456 198 080."),
        "tagline": "Hedges kept square, plus coring, top dressing and weed control.",
        "audience": "Homeowners wanting hedging, coring, top dressing and weed control",
        "img": "svc_hedging",
        "icon": "leaf",
        "suburbs": ["Mount Gravatt", "Holland Park", "Carina", "Camp Hill", "Coorparoo",
                    "Wishart", "Carindale", "Tarragindi", "Sunnybank"],
        "intro": (
            "<strong>Hedge trimming services in Brisbane</strong> — and the lawn treatments that "
            "go with them, coring, top dressing and weed control — are the jobs that lift a yard "
            "from mown to maintained. A1 Lawn Care keeps hedges square and lawns healthy right "
            "across the Brisbane southside: Mount Gravatt, Holland Park, Carina, Camp Hill, "
            "Coorparoo, Wishart and Carindale."),
        "body": [
            ("Hedge trimming services, Brisbane southside", [
                "Lilly pilly, murraya, viburnum, photinia and box — kept level, square and off the paths",
                "Screening hedges cut back to line without opening holes in the middle",
                "Height reductions on hedges that have grown past the fence line or the windows",
                "Drop sheets down and every cutting taken away — you are not left with the pile",
                "Two to three trims a year is normal in Brisbane; more for lilly pilly through the wet",
            ]),
            ("Lawn coring and top dressing", [
                "<strong>Coring</strong> pulls plugs out of compacted soil so water, air and fertiliser reach the root zone instead of running off",
                "<strong>Top dressing</strong> levels the hollows and bumps a mower scalps, and feeds new growth into the surface",
                "<strong>Best done in warm growing weather</strong> — September through March in Brisbane, when the lawn can knit back together quickly",
                "<strong>Usually paired</strong> — coring then top dressing in the same visit gets far more out of both",
            ]),
            ("Weed control that actually holds", [
                "Broadleaf weed control through the lawn, matched to your grass type",
                "Bindii treated before it seeds — late autumn and winter, not when it is already hurting bare feet",
                "Nut grass and creeping weeds treated repeatedly rather than once and hoped for",
                "Paths, driveways and gravel kept clear between visits",
            ]),
        ],
        "faqs": [
            ("How often should a hedge be trimmed in Brisbane?",
             "Most hedges on the Brisbane southside need two to three trims a year, and fast growers "
             "like lilly pilly and murraya need more through the wet season. Trimming little and "
             "often keeps the hedge dense; letting it run and then cutting hard opens holes that take "
             "a season to fill."),
            ("When is the best time to top dress a lawn in Brisbane?",
             "The best time to top dress a lawn in Brisbane is in warm growing weather, roughly "
             "September through March, when the grass is actively growing and can knit through the "
             "new soil quickly. Coring first and top dressing straight after gets far more out of "
             "both jobs than doing either alone."),
            ("What does lawn coring do?",
             "Coring pulls plugs out of compacted soil so water, air and fertiliser reach the roots "
             "instead of running off the surface. On heavy Brisbane clay soils it is the single "
             "biggest improvement you can make to a tired lawn."),
            ("Do you do weed control as well as mowing?",
             "Yes. Weed control is matched to your grass type and the weed — broadleaf through the "
             "lawn, bindii treated before it seeds, and paths and driveways kept clear between "
             "visits."),
        ],
    },
]

# --------------------------------------------------------------------------
# Homepage FAQ — research section 10, "FAQ set to deploy", written as final copy.
# --------------------------------------------------------------------------
HOME_FAQS = [
    ("How much does lawn mowing cost in Brisbane?",
     "Lawn mowing in Brisbane is quoted per visit on the size of the lawn, how easy it is to get "
     "to, and how long it has been since the last cut. A standard suburban block on a regular "
     "fortnightly schedule costs less per visit than a one-off cut on a yard that has got away. "
     "Call A1 Lawn Care on 0456 198 080 and you will get a price, not a range."),
    ("Is A1 Lawn Care an NDIS registered provider, and how do I book with my plan?",
     "Yes — A1 Lawn Care is an NDIS registered provider. Plan managed participants have invoices "
     "sent straight to their plan manager, self managed participants are invoiced directly to "
     "claim through the portal, and NDIA managed participants can call us on 0456 198 080 to go "
     "through what the plan covers before anything is booked."),
    ("Do you mow lawns in Sunnybank, Carindale and Springwood?",
     "Yes. Sunnybank, Carindale and Springwood are all on our regular run, along with more than "
     "150 other suburbs across Brisbane&#39;s south side, Bayside, Logan and the Redlands — all "
     "serviced from our base at 1593 Logan Rd, Mount Gravatt."),
    ("How much does palm tree removal cost in Brisbane?",
     "Palm tree removal in Brisbane is priced on the height and species of the palm, the access "
     "for machinery, what sits underneath it, and whether the stump is ground out. A small Golden "
     "Cane in an open yard is a very different job to a tall Cocos roped down over a pool. Send a "
     "photo to 0456 198 080 for a firm price."),
    ("When is the best time to top dress a lawn in Brisbane?",
     "Top dress a Brisbane lawn in the warm growing months, roughly September through March, so "
     "the grass grows through the new soil rather than sitting under it. Coring first and top "
     "dressing immediately after gets far more out of both jobs."),
    ("Do you take away the green waste and clippings after a job?",
     "Yes. Clippings, prunings and green waste leave with us on every visit at no extra charge. "
     "Nothing is bagged and left in your wheelie bin, and nothing is stacked on the verge."),
]

# --------------------------------------------------------------------------
# Quote form — field names are the GoHighLevel contact fields exactly, so the
# external-tracking script maps them without any extra configuration.
# (name, label, merge field, input type, required, placeholder, options)
# --------------------------------------------------------------------------
FORM_FIELDS = [
    ("full_name", "Name", "{{contact.full_name}}", "text", True,
     "Your name", None),
    ("email", "Email", "{{contact.email}}", "email", True,
     "you@example.com", None),
    ("phone", "Phone", "{{contact.phone}}", "tel", True,
     "0400 000 000", None),
    ("property_address", "Property Address", "{{contact.property_address}}", "text", True,
     "Street and suburb", None),
    ("property_size", "Property Size", "{{contact.property_size}}", "select", False, None,
     ["Courtyard or townhouse",
      "Standard block (up to 600m²)",
      "Large block (600 – 1,000m²)",
      "Half to 1 acre",
      "1 – 5 acres",
      "5+ acres",
      "Commercial or strata site",
      "Not sure"]),
    ("service_needed", "Service Needed", "{{contact.service_needed}}", "select", True, None,
     ["Lawn mowing",
      "NDIS yard &amp; garden maintenance",
      "Garden maintenance",
      "Tree &amp; palm removal",
      "Green waste removal / clean-up",
      "Hedging &amp; lawn treatments",
      "Something else"]),
    ("job_notes", "Job Notes", "{{contact.job_notes}}", "textarea", False,
     "Anything we should know — access, gates, dogs, how long since the last cut…", None),
]

# --------------------------------------------------------------------------
# Trust / differentiator strip. Figures are facts from the research document
# or counts derived from this file — nothing invented.
# --------------------------------------------------------------------------
STATS = [
    ("150", "+", "suburbs serviced", "Brisbane south, Bayside, Logan &amp; Redlands"),
    ("6", "", "specialist services", "Mowing through to palm removal"),
    ("7", "", "days for quotes", "Calls and forms answered seven days"),
    ("1", "", "local crew", "Steve and the team, not a call centre"),
]
