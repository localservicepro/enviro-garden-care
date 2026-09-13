# Enviro Garden Care & Odd Jobs — website

Static, dependency-free website for **Enviro Garden Care & Odd Jobs**, a Pimpama-based
lawn mowing and garden maintenance business servicing the Northern Gold Coast.

Built to the spec in **`build/seo-research-source.html`** (Local Service Pro SEO
Research & Strategy, 4 Sep 2026) — every meta title, H1, keyword target and FAQ answer
comes from that document.

---

## Pages

| URL | Primary keyword | Vol/mo | Difficulty |
|---|---|---|---|
| `index.html` | lawn mowing gold coast | 320 | 10 |
| `services/lawn-mowing.html` | lawn mowing coomera | 50 | 13 |
| `services/acreage-mowing.html` | acreage mowing gold coast | 70 | 12 |
| `services/garden-maintenance.html` | garden maintenance gold coast | 140 | 13 |
| `services/green-waste-removal.html` | green waste removal gold coast | 50 | 23 |
| `services/commercial-property-maintenance.html` | commercial property maintenance gold coast | high intent | — |
| `services/odd-jobs-handyman.html` | odd jobs handyman gold coast | long-tail | — |
| `services.html` | services hub (no competing target) | — | — |
| `about.html` | battery powered lawn mowing gold coast | differentiator | — |
| `contact.html` | quotes and contact | — | — |
| `thank-you.html` | form redirect target (`noindex`) | — | — |
| `404.html` | not found (`noindex`) | — | — |

No two pages share a primary target, per the research's keyword map.

> **Note on `odd-jobs-handyman.html`:** this page is *in addition* to the five service
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
pointing at `thank-you.html`, sitemap coverage, and keyword placement in
title / H1 / first 100 words.

Deploying is just uploading the repository root. There is no build step at runtime,
no framework and no npm dependency in the shipped site.

---

## ⚠️ Confirm before launch

Three items need the client's sign-off or a real value. Everything else is live-ready.

### 1. Wire the forms to GoHighLevel — **required, or leads are lost**

Open `assets/js/main.js` and set:

```js
var LEAD_ENDPOINT = 'https://services.leadconnectorhq.com/hooks/...';
```

Get it from **GHL → Automation → Workflows → new workflow → Inbound Webhook → copy URL**.

While it is an empty string the form validates and still sends the visitor to
`thank-you.html`, but **nothing is transmitted**.

The form posts JSON whose keys are exactly the GHL contact fields:

| Form label | `name` attribute | GHL merge field |
|---|---|---|
| Name | `full_name` | `{{contact.full_name}}` |
| Email | `email` | `{{contact.email}}` |
| Phone | `phone` | `{{contact.phone}}` |
| Property Address | `property_address` | `{{contact.property_address}}` |
| Property Size | `property_size` | `{{contact.property_size}}` |
| Service Needed | `service_needed` | `{{contact.service_needed}}` |
| Job Notes | `job_notes` | `{{contact.job_notes}}` |

Plus `page_url`, `page_title` and `submitted_at` for attribution. Each field also
carries a `data-ghl="{{contact.…}}"` attribute so the mapping is visible in the markup.

`property_size` and `service_needed` are custom fields — create them in GHL
(**Settings → Custom Fields**) before the first submission if they don't exist.

### 2. Trading hours — **assumed, not confirmed**

`Mon–Fri 7:00–17:00, Sat 7:00–15:00` is an assumption. It was not in the research
document and is published in the footer, on the contact page and in `LocalBusiness`
schema. Confirm with Shanon and correct `BIZ["hours"]` in `build/data.py`, then rebuild.
It must match the Google Business Profile exactly.

### 3. Images are hot-linked from Google Drive — **replace before launch**

The client photography is served from the Drive folder supplied
(`1fNAUinCZXQD56NgmTM1Dd5FK92IUXXuf`) via Drive's public image CDN:

```
https://lh3.googleusercontent.com/d/<FILE_ID>=w1600
```

This works, but Drive is not a production image host — it rate-limits and the
folder must stay shared as "anyone with the link". **Before launch:** download the
originals, compress them to WebP, drop them in `assets/img/`, and change the
`drive()` helper at the top of `build/data.py` to return a local path. Every image
on the site resolves through `IMG` and `GALLERY` in that one file, so it is a
single-function change.

Alt text is written per the research (service + suburb). Because the photographs
could not be viewed while building, **re-check that each alt line matches the image
it now sits on** once the files are local, and reorder `GALLERY` if any are mismatched.

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
- `sitemap.xml` (excludes `thank-you` / `404`) and `robots.txt`
- Zero render-blocking JS; all scripts `defer`/async, single 25 KB stylesheet
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
- Suburbs grouped as the research recommends: Coomera corridor / Helensvale–Hope Island /
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
