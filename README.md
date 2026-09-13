# A1 Lawn Care Pty Ltd — website

Static, dependency-free website for **A1 Lawn Care Pty Ltd**, an NDIS registered lawn
mowing and garden maintenance business at 1593 Logan Rd, Mount Gravatt QLD 4122,
servicing Brisbane south, Bayside, Logan and the Redlands.

Built to the spec in **`build/seo-research-source.html`** (Local Service Pro SEO
Research & Strategy for A1 Lawn Care, 10 September 2026) — every meta title, H1,
keyword target and FAQ question comes from that document.

> **Repository note:** this branch lives in the `enviro-garden-care` repository because
> that is the repo the session was given. The content is entirely A1 Lawn Care and shares
> nothing with the Enviro site on `main` except the build tooling. Before launch, move
> this branch into its own `a1-lawn-care` repository.

---

## Pages

| URL | Served by | Primary keyword | Vol/mo | Difficulty |
|---|---|---|---|---|
| `/` | `index.html` | lawn mowing services brisbane | 590 | 22 |
| `/services/` | `services/index.html` | services hub (no competing target) | — | — |
| `/services/lawn-mowing/` | …`/index.html` | lawn mowing mount gravatt | below floor | 4 |
| `/services/ndis-yard-garden-maintenance/` | …`/index.html` | ndis mowing | 70 | 20 |
| `/services/garden-maintenance/` | …`/index.html` | garden maintenance brisbane | 170 | 30 |
| `/services/tree-palm-removal/` | …`/index.html` | palm tree removal brisbane | 110 | 27 |
| `/services/green-waste-removal/` | …`/index.html` | green waste removal brisbane | 210 | 31 |
| `/services/hedging-lawn-treatments/` | …`/index.html` | hedge trimming services brisbane | 30 | 18 |
| `/about/` | `about/index.html` | brand + NDIS entity page | — | — |
| `/contact/` | `contact/index.html` | quotes and contact | — | — |
| `/thank-you/` | `thank-you/index.html` | form redirect target (`noindex`) | — | — |
| `/404.html` | `404.html` | not found (`noindex`) | — | — |

No two pages share a primary target, per the research's keyword-to-page map.
`build/check.py` fails the build if that ever stops being true.

---

## Build

The HTML is **generated**. Edit the Python source, not the `.html` files, or your
changes are overwritten on the next build.

```bash
python3 build/build.py     # writes all HTML + sitemap.xml + robots.txt
python3 build/check.py     # validates the output (must exit 0)
```

| File | What lives there |
|---|---|
| `build/data.py` | All business facts, services, suburbs, FAQs, form fields, image IDs |
| `build/templates.py` | Head, header, footer, schema, reusable components |
| `build/pages.py` | Page bodies and copy |
| `build/build.py` | Orchestrator |
| `build/check.py` | Post-build validation |
| `build/tests/` | Browser checks (see its README) |

`check.py` enforces: valid JSON-LD with `LocalBusiness` on every page, `Service` +
`FAQPage` on every service page, one `<h1>` per page, `lang="en-AU"`, a viewport that
allows pinch-zoom, no broken internal links, no `.html` in any URL, no duplicate
titles/descriptions/canonicals, alt text on every image, NAP on every page, the tracking
script exactly once per page, every form action pointing at `/thank-you/`, all seven GHL
fields present, `noindex` on exactly the two pages that should have it, and the primary
keyword in each page's title, H1 and first 100 words.

---

## Lead capture

Forms are captured by the GoHighLevel external-tracking script, installed **once
globally** at the end of `<body>` on every page:

```html
<script src="https://link.msgsndr.com/js/external-tracking.js"
        data-tracking-id="tk_6582cb70c3d84289821c555a3d8691f9"></script>
```

Field names are the GHL contact fields exactly, so no endpoint or mapping config is
needed:

| Form label | `name` | Merge field |
|---|---|---|
| Name | `full_name` | `{{contact.full_name}}` |
| Email | `email` | `{{contact.email}}` |
| Phone | `phone` | `{{contact.phone}}` |
| Property Address | `property_address` | `{{contact.property_address}}` |
| Property Size | `property_size` | `{{contact.property_size}}` |
| Service Needed | `service_needed` | `{{contact.service_needed}}` |
| Job Notes | `job_notes` | `{{contact.job_notes}}` |

Every form redirects to `/thank-you/` on success. Two details in
`assets/js/main.js` keep capture working and must not be "tidied" away: the submit
event is never stopped from propagating (the tracker listens for it), and the redirect
is held for 900ms so the tracking request leaves the browser before the page unloads.

A hidden honeypot field (`company_website`) sends bots to the thank-you page without
letting the tracker log a junk contact.

---

## What the research asked for, and where it landed

| Research item | Where it is |
|---|---|
| Homepage H1, title, description deployed verbatim | `build/build.py`, `build/pages.py` |
| One H1 per page, clean H1→H2→H3 order | enforced by `check.py` |
| Areas-served section, suburbs as readable text | `/#areas`, footer on every page |
| Business address on the site | header topbar, footer, contact page, schema |
| `LocalBusiness` JSON-LD with geo, hours, `areaServed` | `templates.local_business_schema()` |
| `Service` + `FAQPage` schema on service pages | `templates.service_schema()`, `faq_schema()` |
| Quote form on the homepage, not a link out | `/#quote` |
| Six service pages replacing one 234-word page | `/services/*` |
| Six-question FAQ set, written as final copy | `data.HOME_FAQS` |
| NDIS trust strip above the fold | `templates.ndis_band()` |
| `en-AU`, pinch-zoom enabled, self-referencing canonical | `templates.head()` |
| Answer-engine `speakable` + citable entity sentence | `data.CITABLE`, `.speakable` blocks |

---

## Images

A1's own photography, copied from the client's
`A1 Lawn Care Pty Ltd / Photos` folder into the public Drive folder and served through
Drive's image CDN (`lh3.googleusercontent.com/d/<id>=w<width>`). IDs are in
`data.IMG` and `data.GALLERY`.

**Before launch, move these onto the site's own host.** Drive is fine for a preview but
it is a third-party CDN with no cache headers you control, and the research puts mobile
LCP under 2.5s as a target. Download each file, compress to WebP at the widths used in
`data.IMG`, drop them in `assets/img/`, and change `data.drive()` to return a local path.
`assets/js/main.js` paints a brand gradient if an image ever fails to load, so a broken
Drive link degrades quietly rather than showing a broken-image icon.

---

## Confirm before launch

Everything below is an assumption or an approximation. It is all in `build/data.py`.

1. **Trading hours** — Mon–Fri 6:30am–5:00pm, Sat 7:00am–2:00pm is a guess. These are
   published in `LocalBusiness` schema, so wrong hours are worse than none.
2. **Geo coordinates** — `-27.5413, 153.0789` is the Logan Rd block at Mount Gravatt,
   not surveyed off the title. Check the pin against the Google Business Profile.
3. **Image alt text** — written from the service context each photo is used in. Someone
   who can see the photos should confirm each one actually shows what its alt text says.
4. **Suburb list** — 123 real suburbs across the four regions the research names. The
   business claims 150+; confirm the list matches the run and add or remove suburbs in
   `data.AREA_GROUPS`.
5. **Google Business Profile link** — the profile still points at a dead
   `business.site` URL (research, critical issue 03). The footer and areas section link
   to a Maps search for the address until the real profile URL is known. Fix the GBP
   website field to `https://www.a1lawncare.net.au/` at the same time.
6. **Reviews** — no review content or `AggregateRating` is published, because none has
   been supplied. Add it once reviews are being collected on-site (research, Phase 3).
7. **Credentials the research does not evidence** — "fully insured", a founding year, staff
   numbers and similar claims are deliberately absent from the copy. The research confirms the
   NDIS registration and nothing else of that kind, and an unverified credential on a live site
   is a liability. Add them to `data.BIZ` and the relevant copy once the client confirms.
   One exception: the palm page H1, *"Palm Tree Removal Brisbane — Fast, Insured, Fully Cleaned
   Up"*, is prescribed word-for-word by the research (section 07) and is deployed as written.
   Confirm the insurance before that page goes live, or change the H1 in `data.SERVICES`.

## After launch

From the research's Phase 3, none of which is code:

- Verify the domain in Google Search Console and submit `/sitemap.xml`
- Install GA4 and add conversion events on `tel:` clicks and form submits
- Baseline the 16 suburb keywords before anything changes
- Request indexing on each new service page

---

## Deploying

It is a static site with extensionless URLs and no build step at serve time. Any static
host works (Netlify, Cloudflare Pages, Vercel, S3, Nginx). Point the host at the
repository root and set `404.html` as the not-found page.
