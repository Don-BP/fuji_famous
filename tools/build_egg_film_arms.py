"""Turn the chosen "arms up" render into the film's animated Fujie.

Takes Fujie_Creative/22_egg_film/arms_src/arms_<n>.mp4 (tools/run_fujie_arms_up.py),
cuts the white away from every frame with the same background removal as the
hub's swimming Chibi (tools/run_buddy_swim.py - flood from the border, then
clear the daylight his own outline walls in), crops all frames to one shared
box so nothing wobbles, and packs them into one sprite sheet the film steps
through: promo/eggfilm/ef_arms.webp.

The sheet's layout is written into promo/eggfilm.js (the ARMS line), so the
film always matches the sheet.

  python tools/build_egg_film_arms.py 2      # use take 2
"""
import pathlib, re, sys
import numpy as np
from PIL import Image, ImageFilter

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import run_buddy_swim as swim

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "Fujie_Creative" / "22_egg_film" / "arms_src"
OUT = ROOT / "promo" / "eggfilm" / "ef_arms.webp"
JS = ROOT / "promo" / "eggfilm.js"
KEEP_EVERY = 2          # 24 fps render -> 12 drawings a second, like hand animation
FRAME_W = 380


def main(take):
    raw = swim.frames_from(SRC / ("arms_%d.mp4" % take))
    raw = raw[::KEEP_EVERY]
    cut, boxes, gapped = [], [], 0
    for im in raw:
        bg = swim.background_mask(im)
        if bg.mean() < 0.02:
            sys.exit("a frame is nearly all character - needs more margin")
        gaps = swim.walled_off_gaps(im, bg)
        if gaps.any():
            gapped += 1
            bg = bg | gaps
        alpha = Image.fromarray(np.where(bg, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(swim.FEATHER))
        rgba = im.convert("RGBA")
        rgba.putalpha(alpha)
        cut.append(rgba)
        ys, xs = (~bg).nonzero()
        boxes.append((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    b = np.array(boxes)
    x0, y0, x1, y1 = b[:, 0].min(), b[:, 1].min(), b[:, 2].max(), b[:, 3].max()
    pad = 6
    W, H = raw[0].size
    box = (max(0, x0 - pad), max(0, y0 - pad), min(W, x1 + pad), min(H, y1 + pad))
    fw = FRAME_W
    fh = round((box[3] - box[1]) * fw / (box[2] - box[0]))
    n = len(cut)
    cols = 8
    rows = (n + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * fw, rows * fh), (0, 0, 0, 0))
    for i, im in enumerate(cut):
        sheet.paste(im.crop(box).resize((fw, fh), Image.LANCZOS), ((i % cols) * fw, (i // cols) * fh))
    sheet.save(OUT, "WEBP", quality=88, method=6)
    fps = 24 / KEEP_EVERY
    meta = '  var ARMS = { n: %d, cols: %d, w: %d, h: %d, fps: %g };   /* written by tools/build_egg_film_arms.py */' % (n, cols, fw, fh, fps)
    js = JS.read_text(encoding="utf-8")
    js, k = re.subn(r"  var ARMS = \{[^\n]*", meta, js)
    if not k:
        sys.exit("no ARMS line in eggfilm.js")
    JS.write_text(js, encoding="utf-8", newline="")
    # a proof on the dark page colour, every fourth drawing
    strip = Image.new("RGBA", (fw * ((n + 3) // 4), fh), (4, 18, 26, 255))
    for j, i in enumerate(range(0, n, 4)):
        strip.alpha_composite(cut[i].crop(box).resize((fw, fh), Image.LANCZOS), (j * fw, 0))
    strip.convert("RGB").save(SRC / ("arms_%d_on_dark.jpg" % take), quality=85)
    print("%d drawings, %dx%d each, %d had walled-in white cleared" % (n, fw, fh, gapped))
    print("sheet %s  %.0f KB" % (OUT.name, OUT.stat().st_size / 1024))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
