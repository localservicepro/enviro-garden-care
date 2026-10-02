#!/usr/bin/env python3
"""Generate the site's WebP images from the original photos.

    python3 build/images.py --src /path/to/originals

--src holds one original per POOL key, named <key>.<ext> (jpg, png or webp),
e.g. resi_1.jpg, hero.webp, logo.jpg. The originals live in the client's
Google Drive folders; POOL in build/data.py records each file's Drive ID.

For every (key, width) the build asks for through P(), this writes
assets/img/<key>-<width>.webp: EXIF rotation applied, then all metadata
dropped (phone photos carry GPS coordinates of customers' homes), resized to
that width (never upscaled), WebP quality 80. Re-run after adding a photo or
changing a width in data.py, then run build.py.
"""
import argparse
import glob
import os
import sys

from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "assets", "img")
sys.path.insert(0, HERE)
import data  # noqa: E402  (populates data.IMAGE_SIZES on import)


def find_source(src, key):
    hits = [p for p in glob.glob(os.path.join(src, key + ".*"))
            if p.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))]
    if len(hits) != 1:
        sys.exit("expected exactly one original for %r in %s, found %d" % (key, src, len(hits)))
    return hits[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="folder of originals named <POOL key>.<ext>")
    ap.add_argument("--quality", type=int, default=80)
    args = ap.parse_args()

    os.makedirs(OUT, exist_ok=True)
    wanted = set()
    total = 0
    for key in sorted(data.IMAGE_SIZES):
        src_key, crop = data.IMAGE_CROPS.get(key, (key, None))
        with Image.open(find_source(args.src, src_key)) as im:
            im = ImageOps.exif_transpose(im)
            if crop:
                im = im.crop(crop)
            im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") and "transparency" in im.info or im.mode == "RGBA" else "RGB")
            for width in sorted(data.IMAGE_SIZES[key]):
                name = "%s-%d.webp" % (key.replace("_", "-"), width)
                wanted.add(name)
                out = im
                if im.width > width:
                    out = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
                path = os.path.join(OUT, name)
                q = data.IMAGE_QUALITY.get(key, args.quality)
                out.save(path, "WEBP", quality=q, method=6)  # no exif= -> metadata stripped
                total += os.path.getsize(path)
                print("%-34s %4dx%-4d %6.0f KB" % (name, out.width, out.height, os.path.getsize(path) / 1024))

    stale = [f for f in os.listdir(OUT) if f.endswith(".webp") and f not in wanted]
    for f in stale:
        os.remove(os.path.join(OUT, f))
        print("removed stale", f)
    print("%d files, %.1f MB total" % (len(wanted), total / 1024 / 1024))


if __name__ == "__main__":
    main()
