"""Remove the flat white studio background from generated art, keeping interior whites.

Flood-fills inward from the image border so the character's own pale belly and white
highlights survive. Produces a soft anti-aliased alpha edge.
"""
import sys, pathlib
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

SENTINEL = (255, 0, 255)


def cutout(src, dst=None, thresh=32, feather=1.0):
    src = pathlib.Path(src)
    dst = pathlib.Path(dst) if dst else src
    im = Image.open(src).convert("RGB")
    w, h = im.size

    work = im.copy()
    # Seed from a ring of points around the border, not just corners, so a shape
    # touching one corner does not block the fill.
    seeds = []
    for x in range(0, w, max(1, w // 24)):
        seeds += [(x, 0), (x, h - 1)]
    for y in range(0, h, max(1, h // 24)):
        seeds += [(0, y), (w - 1, y)]

    for s in seeds:
        if work.getpixel(s) != SENTINEL:
            ImageDraw.floodfill(work, s, SENTINEL, thresh=thresh)

    a = np.array(work)
    bg = np.all(a == np.array(SENTINEL), axis=-1)

    if bg.mean() < 0.02:
        print(f"  !! {src.name}: only {bg.mean()*100:.1f}% detected as background - skipped")
        return None

    alpha = np.where(bg, 0, 255).astype(np.uint8)
    am = Image.fromarray(alpha, "L")
    if feather:
        am = am.filter(ImageFilter.GaussianBlur(feather))

    out = im.convert("RGBA")
    out.putalpha(am)

    # Trim fully transparent margins so the art fills its box.
    box = out.getbbox()
    if box:
        out = out.crop(box)

    dst.parent.mkdir(parents=True, exist_ok=True)
    out.save(dst, "PNG", optimize=True)
    print(f"  {src.name}: bg {bg.mean()*100:.0f}% removed -> {out.size[0]}x{out.size[1]}")
    return dst


if __name__ == "__main__":
    for p in sys.argv[1:]:
        cutout(p)
