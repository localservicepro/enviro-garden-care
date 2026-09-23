# Enviro Garden Care & Odd Jobs — website

Static, dependency-free website for **Enviro Garden Care & Odd Jobs**, a Pimpama-based
lawn mowing and garden maintenance business servicing the Northern Gold Coast.

Built to the spec in **`build/seo-research-source.html`** (Local Service Pro SEO
Research & Strategy, 4 Sep 2026) — every meta title, H1, keyword target and FAQ answer
comes from that document.

---

## Pages

| URL | Served by | Primary keyword | Vol/mo | Difficulty |
|---|---|---|---|---|
| `/` | `index.html` | lawn mowing gold coast | 320 | 10 |
| `/services/lawn-mowing/` | `services/lawn-mowing/index.html` | lawn mowing coomera | 50 | 13 |
| `/services/acreage-mowing/` | `services/acreage-mowing/index.html` | acreage mowing gold coast | 70 | 12 |
| `/services/garden-maintenance/` | `services/garden-maintenance/index.html` | garden maintenance gold coast | 140 | 13 |
| `/services/green-waste-removal/` | `services/green-waste-removal/index.html` | green waste removal gold coast | 50 | 23 |
| `/services/commercial-property-maintenance/` | …`/index.html` | commercial property maintenance gold coast | high intent | — |
| `/services/odd-jobs-handyman/` | …`/index.html` | odd jobs handyman gold coast | long-tail | — |
| `/services/` | `services/index.html` | services hub (no competing target) | — | — |
| `/about/` | `about/index.html` | family-owned lawn mowing (was *battery powered* — see Strategy flags) | differentiator | — |
| `/contact/` | `contact/index.html` | quotes and contact | — | — |
| `/thank-you/` | `thank-you/index.html` | form redirect target (`noindex`) | — | — |
| `/404.html` | `404.html` | not found (`noindex`) | — | — |

No two pages share a primary target, per the research's keyword map.

> **Note on `/services/odd-jobs-handyman/`:** this page is *in addition* to the five service
> pages the research specifies. "& Odd Jobs" is half the business name and a real
> revenue line (flat pack and trampoline assembly, fence painting, flyscreens, local
> transport), so it earned a page. It targets a distinct long-tail term and cannibalises
> nothing. Remove it from `SERVICES` in `build/data.py` if you'd rather stick to five.

---

## Build

The HTML is **generated** — edit the Python source, not the `.html` files, or your
changes will be overwritten on the next build.

```bash
python3 build/build.py    # writes all HTML + sitemap.xml + robots.txt
python3 build/check.py     # validates the output (must exit 0)
```

| File | What lives there |
|---|---|
| `build/data.py` | All business facts, services, suburbs, FAQs, form fields |
| `build/templates.py` | Header, footer, schema, reusable components |
| `build/pages.py` | Page bodies and copy |
| `build/build.py` | Orchestrator |
| `build/check.py` | Post-build validation |
| `build/tests/` | Browser checks (see its README) |

`check.py` enforces: valid JSON-LD, one `<h1>` per page, no broken internal links,
no duplicate titles/descriptions/canonicals, alt text on every image, the tracking
script exactly once per page, map embeds on home/about/contact, every form action
pointing at `/thank-you/`, sitemap coverage, and keyword placement in
title / H1 / first 100 words. It also asserts that **no link, asset or form action
exposes a `.html` extension** (only `/404.html` is allowed) and that every internal
reference is root-relative and resolves to a real file.

### URLs

Every page is written as a **directory index** (`about/index.html`), so URLs are
extensionless on any static host — Apache, nginx, GitHub Pages, Netlify, Vercel,
Cloudflare Pages — with **no rewrite rules and no "pretty URLs" setting**. There is
nothing to configure.

All internal links, assets and form actions are **root-relative** (`/about/`,
`/assets/css/style.css`), which assumes the site is served from the domain root. It is
— canonicals are already absolute at `envirogardencare.com.au`. If it ever moves to a
subdirectory, `page_url()` in `build/templates.py` is the one place to change.

URLs carry a trailing slash (`/about/`) because that is the literal path the directory
index serves, and canonicals and `sitemap.xml` match it exactly. Most hosts redirect
`/about` → `/about/` automatically. If yours is configured the other way round and
strips trailing slashes, change `page_url()` and rebuild so canonicals keep matching
the URL actually served — a mismatch there splits ranking signals.

`404.html` stays a flat file at the root because that is where hosts look for it.

### Deploying

Upload the repository root. There is no build step at runtime, no framework and no npm
dependency in the shipped site.

---

## Client review — Change Doc applied

The client's review (Google Sheet **Change Doc – Enviro Garden Care & Odd Jobs**, rows
7–94, from the 15 Sep Loom plus LSP's 21 Sep additions) has been applied. Every row is
cited in the source as `CD r<n>` where it lands. In summary:

| Theme | Rows | What changed |
|---|---|---|
| Service area wording | 7, 17, 18, 22, 32, 37, 47–48, 51–52, 56, 59–60, 67, 76, 79 | "Parkwood to Windaroo and all suburbs in between" everywhere; no "corridor" |
| Brisbane | 8, 21, 40, 87 | Every mention removed |
| Frequencies | 9, 23, 30, 33, 38, 42, 65, 93 | Fortnightly, three-weekly through winter, or one-off (confirmed 23 Sep). No "monthly" |
| Sundays | 10, 29, 34, 77, 81, 86 | Every mention removed |
| Green waste | 11, 26, 30, 36, 39, 41, 43, 46, 49, 54, 57, 62, 84 | Default is the customer's green bin; removal only "for an additional charge"; trust-bar item gone |
| Battery | 12, 29, 34, 43, 61, 63, 64, 71, 78, 89, 90 | Removed entirely (client, 23 Sep) — `check.py` fails on the word |
| Pricing language | 13, 19, 45, 80, 82, 85 | "An approximate price, pending inspection"; buttons say *free estimate*, never *free quote* |
| Owner & address | 14, 73, 88, 94 | "Shanon of Pimpama"; "Pimpama QLD 4209" only in visible copy |
| "Round" → "business" | 15, 72, 74 | Family-owned business wording |
| Odd jobs | 68, 69 | "…during the quieter months"; fence painting and picture hanging removed |
| Form | 20, 83 | Job type dropdown; property-photo upload (see Lead capture) |
| Metas & schema | 89, 90, 91 | Rewritten to match |
| Photos | 16, 23–28, 31, 44, 50, 55, 58, 66, 70, 75 | Every slot assigned by eye from the full folder (23 Sep) — see **Photos** |

`build/check.py` now fails the build if any banned phrase (corridor, Brisbane, monthly,
Sunday, surname, street, "free quote", "no extra charge", …) reappears in visible copy,
if "battery" reappears anywhere, if green-waste removal is stated
without "additional charge", or if any photo is used twice on a page.

**Rows 92–94 closed by the client on 23 Sep:** "corridor" is out site-wide (row 92,
enforced by `check.py`); frequencies are fortnightly, three-weekly through winter, or
one-off (row 93); the street address stays in the hidden schema and the Google map but
out of visible copy (row 94).

### Strategy flags — resolved by the client on 23 Sep

Three of the client's review requests cut against the SEO research. They were raised
with the client; the outcomes:

1. **Battery-powered mowing is gone for good.** The research's differentiator ("nobody
   on page one owns the quiet/battery angle") was never true — petrol does most jobs and
   the client does not want battery mentioned at all. Every battery line and the battery
   FAQ have been removed; `check.py` now fails the build on the word. The About page
   targets *family-owned lawn mowing* instead.
2. **The homepage H1 has its suburbs back.** The client agreed: the H1 is *Lawn Mowing
   Gold Coast — Pimpama to Coomera and the Northern Suburbs*, with *Parkwood to Windaroo
   and all suburbs in between* as a smaller line directly beneath it (`.hero__range`).
   The CD r17 ban on "Pimpama to Coomera" in `check.py` was lifted for this.
3. **Street address stays behind the scenes.** In `LocalBusiness` schema and the Google
   map embed, out of visible copy. The GBP keeps its physical address, so NAP stays
   consistent.

Minor, no action needed: "Get a free quote" became "Get a free estimate" on every
button (an estimate *is* an approximate price, and it keeps the CTA short); the odd-jobs
page now says those jobs are seasonal, which will reduce enquiries but is the truth.

### Photos — assigned by eye on 23 Sep

Every file in both Drive folders (47) was downloaded through the Drive connector and
looked at, then every slot was reassigned to match its section. The catalogue lives as
comments in `POOL` in `build/data.py`. What the look revealed:

- Four of the "originals" are the same before/after collage at four sizes; the
  four ride-on shots are one riverside scene; `hero` and one 14 Sep upload are the same
  house-14 lawn; `van 2`/`van 3` are 640px copies of a 14 Sep upload. Only the largest
  copy of each scene is used now.
- The file labelled "mower close-up" was actually Shanon's daughter hosing the lawn. It is
  no longer the home-page "why" image (that is now the top-down manicured lawn, `resi 3`).
- **Deliberately not used:** `commercial 3` (night shot, readable number plate on a
  parked car), `commercial 2` (other businesses' signage and a "FOR SALE" sign in the ute),
  two 14 Sep uploads with readable plates on customers'/neighbours' cars, and the sunset
  trailer frame whose own plate is readable (the side-on frame from the same evening is
  used instead). `garden cleanup.png` (7.5 MB) could not be fetched to check and is unused
  — a JPG export of it would be usable.
- **Two things for the client to confirm:** (1) the About-page gallery now uses the photo
  of Shanon with his two children behind the mower, and the daughter thumbs-up photo stays
  on the home, lawn-mowing and odd-jobs pages as requested in the Loom — both show
  children's faces, which is his call; (2) the van photo at the industrial estate shows the
  van's own number plate. Both are one-line swaps in `IMG`/galleries if he prefers not.

| Slot | Now |
|---|---|
| Home hero | house-14 lawn with the EGC "proudly maintained by" sign |
| Home "why" | top-down manicured lawn + box hedge with the ute and trailer (`resi 3`) |
| About image | elevated mown front lawn, ute + trailer kerbside (`resi 2`) |
| CTA band | side-on branded trailer against cane at sunset |
| Lawn Mowing card | `resi 1` — mown small front lawn from the carport |
| Acreage card | `acreage 1` — zero-turn on a mown acreage lawn, blue sky |
| Garden card | close-up of a freshly squared-off hedge |
| Green Waste card | trailer tipping green waste, sunny |
| Commercial card | `commercial 1` — branded trailer outside industrial units |
| Odd Jobs card | nature strip along a stone-clad house with the EGC ute (residential) |
| Galleries | hedges on the garden page, acreage on the acreage page, trailer + before/after on green waste, vehicles on commercial — see `GALLERY_*` |

Alt text now describes what is in frame. No suburb is claimed for a photo unless the
client says where it was taken; earlier alts had guessed suburbs and those are gone.

Hot-linking still depends on the client's **Review images** folder staying shared
"anyone with the link". Before launch, download everything, convert to WebP, drop it in
`assets/img/` and repoint `drive()` in `build/data.py`.

An **NDIS Registered Provider** badge sits in the Temporary Photos folder. If Shanon is
NDIS-registered, *ndis lawn mowing gold coast* (50/mo, difficulty 5) is the easiest term
in the whole research and deserves a page — confirm before using the badge.

---

## ⚠️ Before launch

### 1. Lead capture — two paths, one form

Every quote form is `method="post" action="/api/quote"`. With JavaScript running the
submit is intercepted and sent as JSON to **`api/quote.js`**, a Vercel serverless
function that upserts the contact into GHL and uploads the photos into the **Job
Photos** file field. Full details, env vars and the iPhone test are in
[`api/README.md`](api/README.md). No Zapier, no webhook, no npm dependencies.

The **GHL external-tracking script** still sees the same submit event (the handler
never calls `stopPropagation()`), so the text fields are captured twice — belt and
braces. The redirect to `/thank-you/` waits for the API response plus
`CAPTURE_GRACE_MS` (900ms) so neither path is cut off by the unload.

Input `name` attributes are the GHL contact field keys exactly:

| Form label | `name` attribute | GHL merge field |
|---|---|---|
| Name | `full_name` | `{{contact.full_name}}` |
| Email | `email` | `{{contact.email}}` |
| Phone | `phone` | `{{contact.phone}}` |
| Property Address | `property_address` | `{{contact.property_address}}` |
| Property Size | `property_size` | `{{contact.property_size}}` |
| Service Needed | `service_needed` | `{{contact.service_needed}}` |
| Job Type *(CD r83)* | `job_type` | `{{contact.job_type}}` |
| Photos of the property *(CD r20)* | `property_photos` | `{{contact.job_photos}}` (file field, via the API) |
| Job Notes | `job_notes` | `{{contact.job_notes}}` |

Each field also carries `data-ghl="{{contact.…}}"` so the mapping is readable in the
markup. The server-side mapping lives in the `FIELDS` object at the top of
`api/quote.js` — change it there, not in the templates.

**Photos.** Up to 6, resized in the browser (1600px longest side, JPEG q0.82, ~3 MB
total) before they are sent as base64 — that keeps the request under Vercel's 4.5 MB
cap and turns iPhone HEIC into JPEG, which GHL accepts. The server re-checks type by
magic bytes and size. Contact first, photos second: a failed upload still returns
`ok:true` with `photoError:true`, so a bad image never loses a lead.

**Spam.** A visually hidden honeypot (`company_website`, off-screen, not
`display:none`) and a minimum fill time (`_t`, stamped at render). Both are handled
client-side *and* server-side, and both send the bot to `/thank-you/` without creating a
contact; the honeypot path also calls `stopImmediatePropagation()` so the tracker never
sees it.

**No-JS fallback.** The native urlencoded POST hits the same function, which upserts the
text fields and answers `303 → /thank-you/`. Nothing ever lands in the URL.

**Two things in `assets/js/main.js` exist to keep capture working. Don't "tidy" them away:**

- the submit handler never calls `stopPropagation()` on a genuine submit;
- `goToThankYou()` always navigates to `/thank-you/`, never to the form's `action`
  (that is the API — a GET on it is a 405).

Load order matters and is already correct: the tracking script is a plain
(non-deferred) tag at the end of `<body>`, and `main.js` is deferred, so the tracker
registers its listeners first.

**Deploy checklist:** `GHL_LOCATION_ID`, `GHL_PIT_TOKEN`, `GHL_JOB_PHOTOS_FIELD_ID` set in
the Vercel project (done, per client); run `scripts/list-custom-fields.mjs` once to
confirm the Job Photos field **ID** and that the duplicated custom-field keys resolve
to the intended twins; then the iPhone test in `api/README.md`.

### 2. Trading hours — confirmed, but the GBP disagrees

The client confirmed `Mon–Fri 7:00–17:00, Sat 7:00–15:00` on 23 Sep and added that
**Saturday is phone enquiries only — no on-site work**. The footer now labels Saturday
"phone only" with a note, and the contact FAQ says the same. Both stay in
`openingHoursSpecification` because the business is reachable on Saturdays.

**Mismatch to fix on Google:** the Business Profile listing data (checked 23 Sep) shows
Mon–Fri 8:00–17:00 and Sat 8:00–12:00. The site and the GBP must match — either the
client corrects the GBP to 7–5 / 7–3, or tells us the GBP is right and `BIZ["hours"]` in
`build/data.py` changes. Until then Google may show the site's hours as inconsistent.

### 3. Review quotes — rating verified, quotes still placeholders

The **4.9 from 62 Google reviews** in the hero and the Reviews header is real: it comes
from the Business Profile listing data on 23 Sep (60 five-star, 1 two-star, 1 one-star).
It is visible text only — it is deliberately *not* in schema, because Google disallows
self-serving `aggregateRating` on a `LocalBusiness`.

The client has approved picking any three five-star reviews. The review text itself could
not be fetched from the build environment (Google Maps, Localsearch, Needa Trades and
Growerslink are all blocked, and the Zapier Google Business Profile app needs an OAuth
connection that cannot be completed non-interactively). So the three quotes are still the
representative placeholders, now held in `REVIEWS` in `build/data.py` with
`placeholder: True`, and **`check.py` warns on every build until they are replaced**.
To finish: open the GBP reviews, copy three five-star reviews verbatim (text, first
name, suburb if given), paste them into `REVIEWS`, set `placeholder` to `False`, rebuild.

### 4. Images — localise before launch

See **Photos** above. Everything is hot-linked from Google Drive's image CDN, which
rate-limits and depends on folder sharing. Download, convert to WebP, drop in
`assets/img/`, and change `drive()` in `build/data.py`. Two photos are portrait
(the family photo and the sunset ride-on); the gallery tiles crop them with
`object-fit: cover`, so check them once on a phone.

---

## SEO / GEO / AEO implemented

**On-page**
- Primary keyword in meta title, H1 and first 100 words of every money page (verified by `check.py`)
- Unique title, meta description and self-referencing canonical per page
- Clean `H1 → H2 → H3` hierarchy — no skipped levels
- 1,000+ words per service page, ~1,650 on the homepage
- All 19 suburbs in body copy, footer and schema `areaServed`
- Descriptive alt text carrying service + suburb
- Internal linking: homepage → services → siblings → home, plus breadcrumbs

**Technical**
- Extensionless URLs throughout; `sitemap.xml` (excludes `/thank-you/` and `404`) and `robots.txt`
- Zero render-blocking JS; site script is `defer`, single stylesheet
- Every image lazy-loaded with explicit `width`/`height` to hold CLS near zero
- `preconnect` to fonts and the image CDN
- Responsive from 320px up; no horizontal scroll at any width

**GEO (AI / generative engines)**
- `LocalBusiness` + `HomeAndConstructionBusiness` JSON-LD with NAP, geo, hours,
  `sameAs`, `areaServed` (19 suburbs), `knowsAbout` and an `OfferCatalog`
- `Service` schema on each service page; `WebSite`, `WebPage`, `BreadcrumbList` throughout
- Consistent entity name — "Enviro Garden Care & Odd Jobs" — across site, GBP and Facebook
- The citable sentence the research specifies, marked `.speakable`, in every hero
- `robots.txt` explicitly allows GPTBot, OAI-SearchBot, PerplexityBot, ClaudeBot, Google-Extended

**AEO (answer engines / voice)**
- `FAQPage` schema on the homepage, about, contact and all six service pages
- Questions phrased the way people say them aloud; answers 40–60 words
- `SpeakableSpecification` targeting `.speakable` and `.faq__a`

**Local**
- Full street address in the footer, contact page and schema
- Google Maps embed on home (service areas), about and contact
- Suburbs grouped as the research recommends: Coomera growth belt / Helensvale–Hope Island /
  Ormeau–Yatala acreage belt

---

## Tracking

The GoHighLevel tracking script is installed once on every page, immediately before
`</body>`:

```html
<script src="https://link.msgsndr.com/js/external-tracking.js"
        data-tracking-id="tk_5bee5316dafc4ac09c8e0e20ec24e0e4"></script>
```

Still to add at launch: Google Search Console (the existing verification tag on the old
site can be reused), GA4 with call and form conversions, and Bing Webmaster Tools.

---

## Business details used

| | |
|---|---|
| Name | Enviro Garden Care & Odd Jobs |
| Owner | Shanon Hopton |
| Address | 14 Cullen Street, Pimpama QLD 4209 |
| Phone | 0407 276 574 (`+61407276574`) |
| Email | hello@envirogardencare.com.au |
| Coordinates | -27.8326247, 153.32468 |
| Google Business Profile | https://maps.app.goo.gl/Q28zDvYDuuXLZRQh9 |

Source: `build/seo-research-source.html`.
