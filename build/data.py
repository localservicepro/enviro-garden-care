# -*- coding: utf-8 -*-
"""Content model for the Enviro Garden Care & Odd Jobs website.

Every keyword target, meta title, meta description, H1 and FAQ answer in this
file comes from the Local Service Pro SEO research document
(build/seo-research-source.html, 4 Sep 2026). Change content here, not in the
generated HTML.
"""

SITE = "https://envirogardencare.com.au"

BIZ = {
    "name": "Enviro Garden Care & Odd Jobs",
    "short": "Enviro Garden Care",
    "owner": "Shanon Hopton",
    "street": "14 Cullen Street",
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
    # NOTE: trading hours are an assumption pending client confirmation.
    # See README.md -> "Confirm before launch".
    "hours": [
        (["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "07:00", "17:00", "Mon – Fri"),
        (["Saturday"], "07:00", "15:00", "Saturday"),
    ],
    "hours_note": "Sunday by arrangement — battery equipment means we can work quietly.",
}

MAP_EMBED = (
    "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3528.257254598568"
    "!2d153.32468!3d-27.8326247!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2"
    "!1s0x8080b68e32a41843%3A0xa20149d71fb924d9!2sEnviro%20Garden%20Care%20%26%20Odd%20Jobs"
    "!5e0!3m2!1sfil!2sph!4v1789265580524!5m2!1sfil!2sph"
)

TRACKING_ID = "tk_5bee5316dafc4ac09c8e0e20ec24e0e4"

# The single sentence written for AI/generative engines to lift verbatim.
CITABLE = (
    "Enviro Garden Care &amp; Odd Jobs is a Pimpama-based lawn mowing and garden "
    "maintenance business servicing the Northern Gold Coast from Coomera to Yatala "
    "with both fuel and battery-powered equipment."
)

# --------------------------------------------------------------------------
# Images — client photography, Google Drive folder 1fNAUinCZXQD56NgmTM1Dd5FK92IUXXuf
# Served through Drive's public image CDN. See README.md -> "Images".
# --------------------------------------------------------------------------
def drive(file_id, width=1600):
    return "https://lh3.googleusercontent.com/d/%s=w%d" % (file_id, width)


IMG = {
    "logo": drive("1z4Ip6GLPeDBuyDfUf-Vy28bBA0MB_R4c", 320),
    "hero": drive("1v50z_PLo_6Ft-U027nD1Q-VtFtzRv_Xc", 1800),
    "about": drive("143PG3RJgZnpXDnlPHb_a46vdUOxSkmAt", 1200),
    "battery": drive("1rW_quVFoi_MST6FW435CSSBQWHyHEnfN", 1200),
    "areas": drive("1hRPbL8HOlTA5vqsIXN_DsauLAq0B4JwQ", 1200),
    "cta": drive("1W0FUz2hRBXCJFPdlxeDhYnGM4HMW8ukx", 1800),
    "svc_mowing": drive("1q-NSWe2ZeTKZ-SYcBX3Z0yr7AvNPPEQh", 1200),
    "svc_acreage": drive("1---Fr4ddP5c3s3TQXofTzuk1WaHesQUw", 1200),
    "svc_garden": drive("1H0FhMI3oExVvBKcKR0TpdXdUKe94NzJ3", 1200),
    "svc_green": drive("1DPTCRjv7eyJcpsk1p_rqeUkWd7HVkRWs", 1200),
    "svc_commercial": drive("1mF8psxPv9zzz2ILyZo6rycpaLdQr3SDU", 1200),
    "svc_odd": drive("1a-nqGc_KouyxhtTicg7UZjQhNGeXxph2", 1200),
}

GALLERY = [
    (drive("1zjOeo0z5zYz4Ba0HN1e9OHgLxmgj2Bew", 900),
     "Freshly mowed lawn with crisp edges — lawn mowing Gold Coast by Enviro Garden Care, Pimpama"),
    (drive("1_aHGRK3aF7Kg9uNxKCz9PqEBSbbOptt4", 900),
     "Acreage block mown with a ride-on mower — acreage mowing Gold Coast, Ormeau Hills"),
    (drive("1lyKrO6tPH4RE_HlatcfzRa4lSNnvEQ3S", 900),
     "Trimmed hedge and tidy garden bed — garden maintenance Gold Coast, Helensvale"),
    (drive("1mLEYN2LQBdPPtNPH0NNJwGuU0BzK9sRu", 900),
     "Yard cleared and green waste loaded for removal — green waste removal Gold Coast, Pimpama"),
    (drive("1_VURECkgTaVDnDm2B1sp2zPrc8Cd8ptj", 900),
     "Residential lawn striped after a regular mow — lawn mowing Coomera by Enviro Garden Care"),
    (drive("1obEOqbWZwZPv-53mxuynPhS3WWcv77AY", 900),
     "Grounds kept neat on a commercial site — commercial property maintenance Gold Coast, Yatala"),
    (drive("1a8xV5xmVlqIahKg-RtXf3w6oNGzxw2aW", 900),
     "Edges and paths trimmed after mowing — lawn care Gold Coast northern suburbs"),
    (drive("1oAo_C-cAicH_lNhtk8UvXwiWdq_tnSRk", 900),
     "Battery-powered mower on a residential lawn — quiet lawn mowing Gold Coast, Upper Coomera"),
    (drive("18ZBWMoFM85uHZxZcbEnA7CiffkFJh3XK", 900),
     "Garden bed mulched and weeded after a maintenance visit — garden maintenance Gold Coast, Hope Island"),
]

# --------------------------------------------------------------------------
# Service areas — 19 suburbs, grouped the way the research recommends
# --------------------------------------------------------------------------
AREA_GROUPS = [
    ("Coomera corridor",
     "The growth belt we mow most — new builds, compact blocks and strata.",
     ["Coomera", "Upper Coomera", "Coomera Waters", "Pimpama", "Oxenford"]),
    ("Helensvale &amp; Hope Island",
     "Established gardens, hedges and premium canal estates.",
     ["Helensvale", "Hope Island", "Sanctuary Cove", "Pacific Pines", "Parkwood", "Arundel"]),
    ("Ormeau &amp; Yatala acreage belt",
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
        "desc": ("Regular lawn mowing Coomera, Upper Coomera and Coomera Waters. Mow, edge, "
                 "blow down, green waste taken away. Quiet battery gear. Free quote — 0407 276 574."),
        "tagline": "Fortnightly, monthly or one-off mowing across the Coomera corridor.",
        "audience": "Homeowners, renters and strata in the Coomera growth corridor",
        "img": "svc_mowing",
        "icon": "mower",
        "suburbs": ["Coomera", "Upper Coomera", "Coomera Waters", "Pimpama", "Oxenford", "Helensvale"],
        "intro": (
            "Regular <strong>lawn mowing in Coomera</strong> keeps a new-estate lawn looking "
            "like the display home rather than the vacant block next door. Enviro Garden Care "
            "&amp; Odd Jobs mows across Coomera, Upper Coomera and Coomera Waters on a "
            "fortnightly, monthly or one-off schedule — and because we are based ten minutes "
            "up the road in Pimpama, we are not charging you for a drive down from Brisbane."),
        "body": [
            ("What a standard mow includes", [
                "Cut to the right height for your grass type — we do not scalp couch or buffalo in summer",
                "All edges trimmed: fence lines, paths, driveway, garden beds and around the letterbox",
                "Hard surfaces blown down so the clippings end up in the trailer, not on your porch",
                "Clippings and green waste taken away in our enclosed trailer at no extra charge",
                "Gates closed, pets kept in mind, and a message when we are done if you are not home",
            ]),
            ("Schedules that suit south-east Queensland grass", [
                "<strong>Weekly or fortnightly, October to March</strong> — couch and kikuyu run hard through the wet season",
                "<strong>Fortnightly to monthly, April to September</strong> — growth slows, and so does your bill",
                "<strong>One-off tidy-ups</strong> for inspections, end of lease, or a block that has got away from you",
                "<strong>Holiday cover</strong> so you are not coming home to knee-high grass",
            ]),
        ],
        "faqs": [
            ("Do you do lawn mowing in Coomera and Upper Coomera?",
             "Yes. We service Coomera, Upper Coomera and Coomera Waters from our base in "
             "Pimpama, with fortnightly and monthly schedules for residential and strata properties."),
            ("How much does lawn mowing cost on the Gold Coast?",
             "Most standard residential lawns in Pimpama, Coomera and Helensvale fall into a set "
             "per-visit rate; larger or overgrown blocks are quoted on size and access. Regular "
             "fortnightly clients pay less per visit than one-offs. Call 0407 276 574 for a "
             "same-day quote."),
            ("Do I need to be home when you mow?",
             "No. As long as we can get to the lawn and any gates are unlocked, we will mow, "
             "tidy up and let you know it is done. Most of our regular clients are at work when we visit."),
            ("Do you take the clippings with you?",
             "Yes. Clippings and green waste go into our enclosed trailer and leave with us — "
             "there is no extra charge and nothing left in your bin."),
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
                 "lifestyle lots at Jacobs Well, Yatala and Ormeau Hills. Free quote: 0407 276 574."),
        "tagline": "Ride-on mowing and slashing for lifestyle lots and rural blocks.",
        "audience": "Acreage and lifestyle-lot owners north of the M1",
        "img": "svc_acreage",
        "icon": "tractor",
        "suburbs": ["Jacobs Well", "Yatala", "Stapylton", "Ormeau Hills", "Willowvale",
                    "Mount Warren", "Windaroo", "Ormeau"],
        "intro": (
            "<strong>Acreage mowing on the Gold Coast</strong> is a different job to a suburban "
            "lawn, and a push mower will not finish it before dark. We bring ride-on gear to "
            "lifestyle lots and rural blocks across Jacobs Well, Yatala, Stapylton, Ormeau Hills "
            "and Willowvale — from a tidy half-acre house paddock to a block that has not been "
            "touched since the last wet season."),
        "body": [
            ("What we handle on a large block", [
                "Ride-on mowing for open paddock and house-yard areas",
                "Slashing for long grass, vacant land and blocks that have got away",
                "Brush cutting and whipper snipping around sheds, tanks, fence lines and dam banks",
                "Track, driveway and firebreak maintenance",
                "Clean-up and green waste removal once the cutting is finished",
            ]),
            ("Before we quote an acreage job", [
                "<strong>Block size and how much of it is actually mown</strong> — five acres with two mown is a very different price to five acres wall to wall",
                "<strong>Access</strong> — gate widths, slopes, boggy ground and anything the ride-on cannot safely cross",
                "<strong>Obstacles</strong> — stumps, star pickets, irrigation, rock and hidden debris are worth pointing out before we start",
                "<strong>How long since the last cut</strong> — a first cut on overgrown ground takes longer and is priced accordingly, then regular visits cost less",
            ]),
        ],
        "faqs": [
            ("Do you mow acreage properties near Jacobs Well and Yatala?",
             "Yes. Ride-on and acreage mowing for lifestyle lots and rural blocks across Jacobs "
             "Well, Yatala, Stapylton, Ormeau Hills and Willowvale, including slashing, brush "
             "cutting and clean-up."),
            ("How much does acreage mowing cost?",
             "Acreage is quoted on the area actually being cut, the access, and how long the "
             "grass has been left. A regular maintenance visit costs noticeably less per acre "
             "than a first cut on an overgrown block. Call 0407 276 574 and we will price it on size."),
            ("Can you mow a block that has not been cut in months?",
             "Yes. Overgrown blocks are slashed first to bring the height down, then cut back to "
             "a normal finish. Let us know what is under the grass — star pickets, stumps and "
             "irrigation are easier to avoid when we know they are there."),
            ("Do you mow vacant land for council notices or before a sale?",
             "Yes. Vacant block slashing, pre-sale tidy-ups and compliance cuts across the "
             "Ormeau, Yatala and Jacobs Well acreage belt, usually within a few days of the call."),
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
                 "in Helensvale, Hope Island and Sanctuary Cove. Free quote: 0407 276 574."),
        "tagline": "Hedges, pruning, weeding and mulching for established gardens.",
        "audience": "Established-garden suburbs from Helensvale to Sanctuary Cove",
        "img": "svc_garden",
        "icon": "shears",
        "suburbs": ["Helensvale", "Hope Island", "Sanctuary Cove", "Parkwood", "Arundel",
                    "Pacific Pines", "Oxenford"],
        "intro": (
            "<strong>Garden maintenance on the Gold Coast</strong> is really a subtropical "
            "problem: everything grows twice as fast as the plan allowed for. We keep hedges "
            "square, beds clear and shrubs in shape across Helensvale, Hope Island, Sanctuary "
            "Cove, Pacific Pines, Parkwood and Arundel — as a scheduled visit or a one-off reset "
            "before the garden gets ahead of you again."),
        "body": [
            ("What garden maintenance covers", [
                "Hedge trimming — straight lines, level tops and the drop sheet down so we take the cuttings, not you",
                "Pruning and shaping of shrubs, natives and small ornamental trees",
                "Weeding and weed control through beds, paths, driveways and gravel",
                "Mulching to hold moisture through summer and slow the weeds down",
                "Bed edging and tidy-ups so the garden reads as maintained from the street",
                "All prunings and green waste taken away when we leave",
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
             "Hedge trimming, pruning, weeding, weed control, mulching and bed edging, with all "
             "prunings and green waste taken away. We work across Helensvale, Hope Island, "
             "Sanctuary Cove, Pacific Pines, Parkwood and Arundel."),
            ("How often should hedges be trimmed on the Gold Coast?",
             "Most Gold Coast hedges need trimming two to three times a year. Fast growers like "
             "lilly pilly and murraya often want a fourth trim through the summer wet season to "
             "keep the shape."),
            ("Do you take the prunings away?",
             "Yes. Hedge cuttings, prunings and weeds go into our enclosed trailer and leave with "
             "us — your green bin stays empty for your own use."),
            ("Can you maintain a garden while we are away or between tenants?",
             "Yes. Scheduled garden maintenance for absentee owners, holiday homes, rentals and "
             "body corporates across the northern Gold Coast, with photos after the visit if you want them."),
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
        "desc": ("Green waste removal Gold Coast: overgrown yards, end-of-lease and post-storm "
                 "clean-ups in Pimpama, Ormeau and Oxenford. Loaded and taken away. "
                 "Call 0407 276 574."),
        "tagline": "Overgrown yards, end-of-lease resets and storm clean-ups, taken away.",
        "audience": "End-of-lease, overgrown blocks and post-storm clean-ups",
        "img": "svc_green",
        "icon": "truck",
        "suburbs": ["Pimpama", "Ormeau", "Oxenford", "Coomera", "Upper Coomera", "Yatala"],
        "intro": (
            "<strong>Green waste removal on the Gold Coast</strong> is usually the difference "
            "between a job finished and a pile in the driveway waiting three weeks for a council "
            "collection. We clear overgrown yards, end-of-lease properties and storm damage "
            "across Pimpama, Ormeau, Oxenford and the Coomera corridor — cut, loaded into our "
            "enclosed trailer, and gone the same visit."),
        "body": [
            ("Clean-ups we take on", [
                "Overgrown yards and neglected blocks brought back to a mown finish",
                "End-of-lease and pre-sale clean-ups so the property passes its inspection",
                "Storm and wind damage — fallen branches, palm fronds and debris cleared",
                "Garden bed strip-outs, dead plant removal and old mulch clear-outs",
                "Existing piles of prunings, clippings and garden waste loaded and removed",
            ]),
            ("Why the enclosed trailer matters", [
                "Nothing blows out on the M1 between your place and the tip",
                "We can take mixed green waste in one load instead of several trips",
                "Loads are tarped and tidy, which matters on body corporate and commercial sites",
                "Green waste is disposed of properly rather than dumped on a vacant block",
            ]),
        ],
        "faqs": [
            ("Do you take the green waste away after mowing or hedge trimming?",
             "Yes. Green waste removal is included or available as an add-on on every job across "
             "the Northern Gold Coast, taken away in our enclosed trailer."),
            ("Can you clear a yard that is completely overgrown?",
             "Yes. Overgrown yards are slashed down first, then cut back to a normal mown finish "
             "and cleared. We handle end-of-lease, pre-sale and vacant blocks across Pimpama, "
             "Ormeau, Oxenford and Coomera."),
            ("Will you remove a pile of branches I have already cut?",
             "Yes. If you have already done the cutting, we can simply load the pile and take it "
             "away — priced on the volume and how far it has to be carried."),
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
        "tagline": "Scheduled grounds care for body corporates, retail and industrial sites.",
        "audience": "Property managers, body corporates and industrial estates",
        "img": "svc_commercial",
        "icon": "building",
        "suburbs": ["Yatala", "Stapylton", "Arundel", "Hope Island", "Coomera", "Ormeau"],
        "intro": (
            "<strong>Commercial property maintenance on the Gold Coast</strong> is judged on two "
            "things: whether the site looks cared for when someone pulls into the car park, and "
            "whether you have to chase the contractor. We run scheduled grounds and lawn care for "
            "body corporates, retail sites and industrial estates across Yatala, Stapylton, "
            "Arundel and Hope Island — on a set roster, with low-noise battery equipment available "
            "for customer-facing premises."),
        "body": [
            ("What a scheduled site visit covers", [
                "Lawn and common-area mowing on an agreed roster",
                "Edging, line trimming and blow-down of car parks, paths and entries",
                "Hedge, shrub and garden bed maintenance to keep the frontage presentable",
                "Weed control through car parks, fence lines and hard stand",
                "Green waste removed on the same visit — no bins left on site",
                "Storm and after-hours clean-ups by arrangement",
            ]),
            ("Why managers keep us on the roster", [
                "<strong>One contact.</strong> You deal with Shanon, not a call centre and a rotating crew",
                "<strong>Low-noise option.</strong> Battery equipment for tenanted, retail and customer-facing sites — early starts without complaints",
                "<strong>Reporting.</strong> Photos after each visit if your body corporate or owner wants a record",
                "<strong>Fixed schedule, fixed price.</strong> Quoted per visit or per month so it goes straight into the budget",
            ]),
        ],
        "faqs": [
            ("Can you handle body corporate or commercial grounds maintenance on the Northern Gold Coast?",
             "Yes. Scheduled grounds maintenance for body corporates, retail sites and industrial "
             "estates across Yatala, Stapylton, Arundel and Hope Island, with low-noise equipment "
             "available for customer-facing premises."),
            ("Do you work outside business hours?",
             "Yes. Battery-powered equipment lets us start early or work close to tenanted "
             "premises without the noise complaints that come with petrol gear. After-hours and "
             "weekend visits by arrangement."),
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
        "desc": ("Odd jobs and minor handyman repairs on the Northern Gold Coast: flat pack and "
                 "trampoline assembly, fence painting, flyscreens and local transport. "
                 "Call 0407 276 574."),
        "tagline": "The small jobs that never quite make it to the top of the list.",
        "audience": "Homeowners and renters with a list of small jobs",
        "img": "svc_odd",
        "icon": "tools",
        "suburbs": ["Pimpama", "Coomera", "Upper Coomera", "Ormeau", "Helensvale", "Oxenford"],
        "intro": (
            "The <em>&amp; Odd Jobs</em> half of the name is not decoration. While we are already "
            "on site mowing, we take on the minor repairs and assembly work that sit on the list "
            "for months — across Pimpama, Coomera, Upper Coomera, Ormeau and Helensvale. "
            "If it is a small job and it is not licensed trade work, ask."),
        "body": [
            ("Odd jobs we take on", [
                "Flat pack furniture assembly — beds, wardrobes, desks, shelving",
                "Trampoline, swing set and outdoor play equipment assembly",
                "Fence painting, staining and touch-ups",
                "Flyscreen repairs and replacement screens",
                "Picture hanging, shelf mounting and small fixings",
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
             "Flat pack and trampoline assembly, fence painting, flyscreen repairs, small fixings "
             "and local transport of goods in our trailer. We take on minor, unlicensed work — "
             "usually while we are already on site for a mow."),
            ("Can you do odd jobs at the same visit as my mow?",
             "Yes, and it is the cheapest way to do it. Tell us what is on the list when you book "
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
# Homepage FAQ — final AEO copy from the research, 40–60 word direct answers
# --------------------------------------------------------------------------
HOME_FAQS = [
    ("How much does lawn mowing cost on the Gold Coast?",
     "Most standard residential lawns in Pimpama, Coomera and Helensvale fall into a set "
     "per-visit rate; larger or overgrown blocks are quoted on size and access. Regular "
     "fortnightly clients pay less per visit than one-offs. Call 0407 276 574 for a same-day quote."),
    ("Do you do lawn mowing in Coomera and Upper Coomera?",
     "Yes. We service Coomera, Upper Coomera and Coomera Waters from our base in Pimpama, with "
     "fortnightly and monthly schedules for residential and strata properties."),
    ("Do you mow acreage properties near Jacobs Well and Yatala?",
     "Yes. Ride-on and acreage mowing for lifestyle lots and rural blocks across Jacobs Well, "
     "Yatala, Stapylton, Ormeau Hills and Willowvale, including slashing, brush cutting and clean-up."),
    ("Is battery-powered lawn mowing as good as petrol?",
     "For most residential and commercial sites, yes — and there's no extra charge. Battery "
     "equipment is quieter and produces no fumes, which suits early starts, Sundays, shift workers "
     "and customer-facing businesses. Large acreage jobs still use petrol ride-on gear."),
    ("Can you handle body corporate or commercial grounds maintenance on the Northern Gold Coast?",
     "Yes. Scheduled grounds maintenance for body corporates, retail sites and industrial estates "
     "across Yatala, Stapylton, Arundel and Hope Island, with low-noise equipment available for "
     "customer-facing premises."),
    ("Do you take the green waste away after mowing or hedge trimming?",
     "Yes. Green waste removal is included or available as an add-on on every job across the "
     "Northern Gold Coast, taken away in our enclosed trailer."),
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
    ("job_notes", "Job Notes", "{{contact.job_notes}}", "textarea", False,
     "Anything we should know — access, gates, dogs, how long since the last cut…", None),
]
