"""Compose the five Hitachiota cover designs.

Takes the generated cast-iron blanks and drops the real Fujie artwork into
each coloured field - the official fish at its exact original colours on
three covers, Chibi Fujie on two. Nothing about either character is redrawn.

Output: Fujie_Creative/20_new_ideas/cover_*.png  and  cover_set_sheet.png
"""
import pathlib
import numpy as np
from PIL import Image, ImageFilter, ImageChops

ROOT = pathlib.Path("D:/Fuji_Famous")
OUT = ROOT / "Fujie_Creative" / "20_new_ideas"
OFFICIAL = ROOT / "Documents_for_dev" / "05_fujie_\u7d75\u67c4\u4f8b.png"
CHIBI = ROOT / "Fujie_Creative" / "01_character" / "chibi_neutral.png"

SS = 3


def cutout(path, white_key=False):
    im = Image.open(path).convert("RGBA")
    if white_key:
        n = np.asarray(im.convert("RGB")).astype(np.float32)
        a = 255 - np.clip((n.min(axis=2) - 232) / 18 * 255, 0, 255)
        im = Image.fromarray(np.dstack([n, a]).astype(np.uint8)).convert("RGBA")
    return im.crop(im.getchannel("A").point(lambda p: 255 if p > 6 else 0).getbbox())


def field_circle(im):
    """Find the coloured resin field: centre and radius, in pixels."""
    a = np.asarray(im.convert("RGB")).astype(int)
    m = ((a[:, :, 2] > a[:, :, 0] + 10) | (a[:, :, 1] > a[:, :, 0] + 10))
    h, w = m.shape
    m[: int(h * .04)] = False; m[int(h * .96):] = False
    m[:, : int(w * .04)] = False; m[:, int(w * .96):] = False
    ys, xs = np.nonzero(m)
    cx, cy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
    r = min(xs.max() - xs.min(), ys.max() - ys.min()) / 2
    return cx, cy, r


def lay(base, art, cx, cy, r, wu, dy=0, flip=False, outline=2.4, shade=0.7):
    art = art.transpose(Image.FLIP_LEFT_RIGHT) if flip else art
    fa = art.size[0] / art.size[1]
    W = 2 * wu * r
    H = W / fa
    f = art.resize((int(W * SS), max(1, int(H * SS))), Image.LANCZOS)
    al = f.getchannel("A")
    grow = al.filter(ImageFilter.MaxFilter(int(outline * SS) | 1))
    edge = ImageChops.subtract(grow, al).filter(ImageFilter.GaussianBlur(SS * .6))
    dark = Image.new("RGBA", f.size, (22, 30, 44, 0)); dark.putalpha(edge)
    plate = Image.new("RGBA", f.size, (0, 0, 0, 0))
    plate.alpha_composite(dark); plate.alpha_composite(f)
    f = plate.resize((int(round(W)), max(1, int(round(H)))), Image.LANCZOS)

    W, H = f.size
    x0, y0 = int(round(cx - W / 2)), int(round(cy + dy - H / 2))
    out = base.copy().convert("RGBA")
    under = np.asarray(out.crop((x0, y0, x0 + W, y0 + H)).convert("RGB")).astype(np.float32)
    lum = under.mean(axis=2)
    g = 1.0 + (np.clip(lum / max(lum.mean(), 1.0), .55, 1.45) - 1.0) * shade
    fn = np.asarray(f).astype(np.float32)
    fn[..., :3] = np.clip(fn[..., :3] * g[..., None], 0, 255)
    f = Image.fromarray(fn.astype(np.uint8))
    out.alpha_composite(f, (x0, y0))
    return out.convert("RGB")


# blank, character, width across the field, vertical nudge, mirrored, how much
# of the cover's own light and texture the design picks up
COVERS = [
    ("cover_station",  "cover_blank_river",   "official", 0.60, -0.22, False, 0.70),
    ("cover_cityhall", "cover_blank_wave",    "official", 0.62,  0.00, False, 0.70),
    ("cover_farmgate", "cover_blank_hills",   "official", 0.62,  0.08, True,  0.70),
    ("cover_park",     "cover_blank_bubbles", "chibi",    0.58,  0.02, False, 0.60),
    ("cover_street",   "cover_blank_reeds",   "chibi",    0.60, -0.02, True,  0.12),
]

if __name__ == "__main__":
    art = {"official": cutout(OFFICIAL), "chibi": cutout(CHIBI, white_key=True)}
    made = []
    for name, blank, who, wu, dyf, flip, shade in COVERS:
        base = Image.open(OUT / (blank + ".png")).convert("RGB")
        cx, cy, r = field_circle(base)
        o = lay(base, art[who], cx, cy, r, wu, dy=dyf * r, flip=flip, shade=shade)
        o.save(OUT / (name + ".png"))
        made.append((name, o))
        print(f"{name:16s} {who:9s} field r={r:.0f}")

    # the sheet the hub shows: three covers across the top, two below,
    # each still sitting in its own bit of pavement
    W, H, BG = 1200, 896, (243, 242, 237)
    sheet = Image.new("RGB", (W, H), BG)
    T, GAP = 356, 22
    top_y, bot_y = 40, 40 + T + GAP
    xs_top = [(W - (3 * T + 2 * GAP)) // 2 + i * (T + GAP) for i in range(3)]
    xs_bot = [(W - (2 * T + GAP)) // 2 + i * (T + GAP) for i in range(2)]
    for (name, o), (x, y) in zip(made, [(x, top_y) for x in xs_top] + [(x, bot_y) for x in xs_bot]):
        sheet.paste(o.resize((T, T), Image.LANCZOS), (x, y))
    sheet.save(OUT / "cover_set_sheet.png")
    print("sheet ok")
