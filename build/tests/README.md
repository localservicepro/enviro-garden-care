# Browser checks

These are development aids, not part of the deployed site.

```bash
# from the repository root
python3 -m http.server 8123 &
npm i -D playwright@1.49.1

node build/tests/formtest.js   # quote form: GHL fields, validation, thank-you redirect
node build/tests/shot.js       # screenshots + layout/JS error sweep
node build/tests/gcheck.js     # gallery grid geometry
```

Screenshots are written to the scratch directory set inside `shot.js`.

Note: Google Drive images, Google Fonts and the Maps embed are third-party
hosts. If your environment blocks them the pages still render and the scripts
ignore those specific `Failed to load resource` messages.
