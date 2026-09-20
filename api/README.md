# api/quote.js — quote form → GoHighLevel

Vercel serverless function. The quote form POSTs JSON here; the function upserts
the contact into the GHL sub-account and uploads the customer's photos into the
**Job Photos** file-upload custom field. Zero dependencies, Node 18+.

Order of operations: **contact first, photos second.** A photo failure returns
`ok:true, photoError:true` — a bad image never loses a lead.

## Env vars (Vercel → Project → Settings → Environment Variables)

| Name | Value |
|---|---|
| `GHL_LOCATION_ID` | `T4thSQ8YoNDiusrGSEhY` |
| `GHL_PIT_TOKEN` | Private Integration Token (server-side only, never in the browser) |
| `GHL_JOB_PHOTOS_FIELD_ID` | the **ID** (not the key) of the Job Photos field — see below |

Missing any of them → the function answers `500 server_misconfigured` and logs
which ones.

## Getting the Job Photos field ID

The upload endpoint takes the custom field **ID**. `contact.job_photos` is the
merge-field *key* and will not work there.

```bash
GHL_PIT_TOKEN=... GHL_LOCATION_ID=T4thSQ8YoNDiusrGSEhY node scripts/list-custom-fields.mjs
```

Prints every field's id / name / key / type, flags duplicate names, shows which
twin each of the duplicated keys (`service_needed`, `property_size`,
`property_address`) resolves to, and ends with a ready-to-paste line:

```
GHL_JOB_PHOTOS_FIELD_ID=<id>
```

If a key resolves to the wrong twin, switch that entry in the `FIELDS` map at
the top of `api/quote.js` from `{ key: '…' }` to `{ id: '…' }`.

## Request contract

`POST /api/quote`, `Content-Type: application/json`:

```json
{
  "full_name": "Jane Citizen", "email": "…", "phone": "0412 345 678",
  "property_address": "…", "property_size": "…", "service_needed": "…",
  "job_type": "…", "job_notes": "…",
  "_t": 1789900000000,
  "photos": [ { "name": "front.jpg", "type": "image/jpeg", "data": "data:image/jpeg;base64,…" } ]
}
```

Server-side validation (the endpoint is public): phone required and normalised
to E.164 (`0412 345 678` → `+61412345678`); email lowercased; photos ≤ 6,
≤ 1.5 MB each, ≤ 3.2 MB total, types `image/jpeg|png|gif` **checked by magic
bytes**, filenames sanitised. Body cap 4.4 MB (Vercel's limit is 4.5).

Spam: honeypot `company_website` and a minimum fill time via `_t` (page-render
timestamp, set by the site script). Both answer `200 ok:true` without calling
GHL.

Responses: `200 {ok, contactId, photos:{received,uploaded}, photoError?}` ·
`400 {error}` (`phone_required`, `email_invalid`, `name_required`, `photo_type`,
`photo_too_large`, `too_many_photos`, …) · `405` · `413` · `500` · `502 upsert_failed`.

No-JS fallback: the form's native `POST` (urlencoded) hits the same function,
which upserts the text fields and answers `303 → /thank-you/`.

## Client side (`assets/js/main.js`)

Photos are resized in the browser before sending: canvas, 1600 px longest side,
JPEG q0.82 (stepping down if a file is still over 1.4 MB), max 6, ~3 MB total.
This keeps the body under Vercel's cap and turns iPhone HEIC into JPEG, which
GHL accepts (HEIC is not on its list). EXIF orientation is honoured.

The GHL tracking script still receives the submit event; the redirect waits for
the API response plus a short grace so nothing is cancelled by the unload.

## Tests

```bash
node --test build/tests/quote.test.js
```

Mocks `fetch`; asserts E.164, lowercased email, every custom field mapped,
non-image rejected, every multipart part prefixed with the field ID with a
unique v4 uuid, `locationId` in the upload query, honeypot and min-fill short-
circuit without calling GHL, missing phone → 400, upload failure → `photoError`,
upsert failure → 502, no-JS fallback → 303.

## Testing from a real iPhone

1. Deploy a preview (any branch push). Open the preview URL on the phone.
2. Fill the form, attach 2–3 photos straight from the camera roll (HEIC).
   Thumbnails should appear within a second or two — that's the resize.
3. Submit. You should land on `/thank-you/`.
4. In GHL, open the contact: name/phone (E.164)/email/custom fields populated,
   and the **Job Photos** field showing the images.
5. If photos are missing but the contact exists, check the function logs in
   Vercel for `[quote] photo upload failed` — the response will have carried
   `photoError:true`. Usual causes: wrong `GHL_JOB_PHOTOS_FIELD_ID` (key used
   instead of ID), or the field is not a file-upload type.
6. Try once on mobile data, not Wi-Fi, to confirm the payload size is fine.
