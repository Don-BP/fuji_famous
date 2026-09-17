"""Cut the upright hero film into stills for phones.

The desktop film is a wide 1.95:1 frame. A phone held upright would have to
crop that down to a sliver, so the owner shot a second pass in portrait.
This turns it into the same kind of numbered WebP stills the landscape film
uses, at two widths, plus a poster for the CSS fallback:

  promo/film/m480/f_001.webp ... 73 frames, for ordinary phones
  promo/film/m720/f_001.webp ... 73 frames, for retina phones
  promo/film/poster_m.jpg    ... the first frame, the still fallback

Frames are drawn to a canvas on scroll, never played as a video: seeking a
video on scroll is unreliable on Safari and stutters on touch.

Run it again only if the source video changes.
"""
import pathlib, shutil, subprocess, sys, tempfile
from PIL import Image

ROOT = pathlib.Path(r"D:\Fuji_Famous")
SRC = ROOT / "Documents_for_dev" / "mobile background video.mp4"
OUT = ROOT / "promo" / "film"

COUNT = 73                  # must match the landscape film and hero.js
WIDTHS = {"m480": 480, "m720": 720}
# The frame is mostly a smooth dark gradient, which is the expensive kind of
# picture for WebP - push the quality lower and the file barely shrinks, but
# the banding in the water shows up at once. 60 is where that trade stops
# paying.
QUALITY = 60


def main():
    if not SRC.exists():
        sys.exit("missing source video: %s" % SRC)

    tmp = pathlib.Path(tempfile.mkdtemp())
    try:
        subprocess.run(
            ["ffmpeg", "-v", "error", "-i", str(SRC),
             "-vsync", "0", str(tmp / "raw_%03d.png")],
            check=True)

        raw = sorted(tmp.glob("raw_*.png"))
        if len(raw) != COUNT:
            sys.exit("expected %d frames, got %d" % (COUNT, len(raw)))

        for name, w in WIDTHS.items():
            d = OUT / name
            if d.exists():
                shutil.rmtree(d)
            d.mkdir(parents=True)
            total = 0
            for i, p in enumerate(raw, 1):
                im = Image.open(p).convert("RGB")
                h = round(im.height * w / im.width)
                im = im.resize((w, h), Image.LANCZOS)
                dest = d / ("f_%03d.webp" % i)
                im.save(dest, "WEBP", quality=QUALITY, method=6)
                total += dest.stat().st_size
            print("%s  %d frames, %dx%d, %.1f MB"
                  % (name, COUNT, w, h, total / 1048576))

        poster = Image.open(raw[0]).convert("RGB")
        pw = 832
        poster = poster.resize((pw, round(poster.height * pw / poster.width)),
                               Image.LANCZOS)
        poster.save(OUT / "poster_m.jpg", "JPEG", quality=82,
                    optimize=True, progressive=True)
        print("poster_m.jpg  %dx%d" % poster.size)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
