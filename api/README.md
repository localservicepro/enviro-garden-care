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
| `GHL_JOB_PHOTOS_FIELD_ID` | *optional* — the Job Photos field's ID, **or** its key (`job_photos`, `contact.job_photos` or `{{contact.job_photos}}`) |

Missing `GHL_LOCATION_ID` or `GHL_PIT_TOKEN` → `500 server_misconfigured`, logged.

The upload endpoint needs the field **ID**. If `GHL_JOB_PHOTOS_FIELD_ID` holds an ID it is
used as-is. If it holds the key, or is unset, the function looks the ID up once via
`GET /locations/{locationId}/customFields`, picks the **contact** field with key
`contact.job_photos` (ignoring an opportunity twin), and caches it for the life of the
function instance. A failed lookup only costs the photos: the contact is still created
and the response carries `photoError:true`, with the reason in the function log.

## Getting the Job Photos field ID (optional)

Not required any more (see above), but pinning the ID saves one lookup per cold start
and removes any doubt about which field is used.

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

## What GHL's API spec requires (checked against GoHighLevel/highlevel-api-docs)

| Call | Endpoint | Token scope |
|---|---|---|
| List contact custom fields | `GET /locations/{locationId}/customFields?model=contact` | `locations/customFields.readonly` |
| Find-or-create the contact | `POST /contacts/upsert` | `contacts.write` |
| Upload photos | `POST /forms/upload-custom-files?contactId=&locationId=` (multipart, parts keyed `<fieldId>_<uuid>`) | `forms.write` |

All with `Authorization: Bearer <Private Integration token>` and `Version: 2021-07-28`.

Custom fields in the upsert must be `{ id, key, field_value }`. GHL marks `id` as
required, so the function looks every field's ID up from the listing (cached 10 minutes
per warm instance). If GHL still rejects the custom fields, the contact is saved again
without them, so the lead is never lost, and the photos still upload. A Job Photos field
set to one file only receives the first photo; the check page flags that.

## Photos not arriving? Open the setup check

`GET /api/quote?check` (e.g. `https://enviro-garden-care.vercel.app/api/quote?check`)
returns a read-only report: which GHL variables the function can see (names only, the
token is never shown), whether GHL accepts the token, the Job Photos field it found, a
one-line verdict, and the last photo-upload error if this function instance has had
one. It makes one read call to GHL and writes nothing. Paste the output to LSP.

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
