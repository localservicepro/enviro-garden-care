# Browser checks

Development aids, not part of the deployed site. They drive a real Chromium via
Playwright against a local static server.

```bash
# from the repository root
python3 build/build.py
python3 -m http.server 8123 &

node build/tests/formtest.js   # quote form: GHL fields, validation, capture, redirect
node build/tests/navtest.js    # megamenu, mobile drawer, internal link graph
node build/tests/shot.js       # screenshots + layout/JS error sweep
node build/tests/gcheck.js     # gallery mosaic geometry
```

Each script exits non-zero on failure, so they can gate a deploy alongside
`build/check.py`.

Environment variables:

| Variable | Default | Use |
|---|---|---|
| `BASE` | `http://127.0.0.1:8123` | Server to test against |
| `CHROME` | `/opt/pw-browsers/chromium-1194/chrome-linux/chrome` | Chromium binary |
| `SHOT_OUT` | `/tmp/a1-shots` | Where screenshots are written |

Playwright is expected to be available (`npm i -D playwright`, or set `NODE_PATH`
to a global install).

**Third-party hosts.** Google Drive images, Google Fonts, the Maps embed and the
GoHighLevel tracking script are all external. In a sandbox with no egress they
fail to load; the pages still render and `shot.js` ignores those specific
resource errors. `formtest.js` stands in for the GHL tracker with its own
document-level submit listener, so lead capture is tested without the network.
