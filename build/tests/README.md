# Browser checks

These are development aids, not part of the deployed site.

```bash
# from the repository root
python3 -m http.server 8123 &
npm i -D playwright@1.49.1

node --test build/tests/quote.test.js   # api/quote.js: mocked GHL, no browser, no server needed
node build/tests/formtest.js   # quote form: GHL fields, validation, mocked /api/quote, photos → base64 JPEG, redirect
node build/tests/navtest.js    # services dropdown + mobile drawer submenu
node build/tests/shot.js       # screenshots + layout/JS error sweep
node build/tests/gcheck.js     # gallery grid geometry
```

Screenshots are written to the scratch directory set inside `shot.js`.

Note: Google Drive images, Google Fonts and the Maps embed are third-party
hosts. If your environment blocks them the pages still render and the scripts
ignore those specific `Failed to load resource` messages.

## navtest.js

Guards the services menu, which has broken twice in ways a page-level check
missed:

- the dropdown was bound with a URL selector (`a[href$="services.html"]`) that a
  routing change invalidated, so it silently stopped opening;
- the mobile drawer is `position:fixed`, and `backdrop-filter` on `.site-header`
  made the header its containing block, clipping the drawer to ~120px so only
  the first nav item was reachable.

So the test opens the menu for real rather than asserting the markup exists:
hover and keyboard-focus open the panel, Escape and mouse-out close it, the six
service links are present, correct and actually hit-testable, the drawer spans
the viewport, and no nav link falls outside the drawer's visible box.
