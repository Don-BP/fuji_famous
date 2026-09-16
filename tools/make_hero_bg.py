"""Render the studio site's hero backdrop as a flat image file.

The hero on the site is painted entirely by the stylesheet - there is no
background file to export. This rebuilds the same thing from the same numbers
(promo/hub.css) at whatever size you ask for, so the image and the live page
stay the same design rather than a lookalike.

    python tools/make_hero_bg.py            # 2560x1440 and 1920x1080, three variants

Output: Fujie_Creative/18_backgrounds/
"""
import math, pathlib
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = pathlib.Path(r"D:\Fuji_Famous")
OUT = ROOT / "Fujie_Creative" / "18_backgrounds"
OFFICIAL = ROOT / "site" / "fujie-official.png"
CHIBI = ROOT / "Fujie_Creative" / "01_character" / "chibi_neutral.png"

# Everything below is lifted straight from .hero / .hero::after / .heroArt.
TOP, BOTTOM = (0x06, 0x20, 0x2E), (0x04, 0x12, 0x1A)
BOTTOM_AT = 0.78

GLOWS = [  # (rx%, ry%, cx%, cy%, rgb, alpha, stop%)
    (0.90, 0.70, 0.72, 0.40, (0, 160, 233), 0.22, 0.62),
    (0.80, 0.70, 0.08, 0.88, (73, 210, 240), 0.10, 0.58),
]
SHAFTS = [  # (deg, rgb, peak alpha, from%, peak%, to%)
    (103, (150, 225, 255), 0.07, 0.44, 0.48, 0.53),
    (94,  (150, 225, 255), 0.05, 0.64, 0.68, 0.73),
]
SHAFT_INSET = 0.25            # .hero::after { inset:-25% }
RINGS = [  # (right%, top%, width px at a 1920 viewport, alpha)
    (0.04, 0.08, 560, 0.13),
    (0.12, 0.24, 360, 0.10),
    (0.19, 0.36, 200, 0.08),
]
REF_W = 1920.0                # the width those ring pixel sizes were written for


def base(w, h):
    y = np.linspace(0, 1, h)[:, None]
    t = np.clip(y / BOTTOM_AT, 0, 1)
    img = np.zeros((h, w, 3), np.float64)
    for c in range(3):
        img[..., c] = TOP[c] + (BOTTOM[c] - TOP[c]) * t
    return img


def over(img, rgb, alpha):
    """Source-over with a per-pixel alpha, the way the browser stacks the layers."""
    a = alpha[..., None]
    return img * (1 - a) + np.array(rgb, np.float64) * a


def add_glows(img, w, h):
    xs = np.arange(w)[None, :] / w
    ys = np.arange(h)[:, None] / h
    for rx, ry, cx, cy, rgb, a0, stop in GLOWS:
        d = np.sqrt(((xs - cx) / rx) ** 2 + ((ys - cy) / ry) ** 2)
        img = over(img, rgb, a0 * np.clip(1 - d / stop, 0, 1))
    return img


def add_shafts(img, w, h):
    """Two soft diagonal light bands. The layer is 1.5x the frame, as in the CSS."""
    ew, eh = w * (1 + SHAFT_INSET * 2), h * (1 + SHAFT_INSET * 2)
    xs = np.arange(w)[None, :] + w * SHAFT_INSET
    ys = np.arange(h)[:, None] + h * SHAFT_INSET
    for deg, rgb, a0, p0, p1, p2 in SHAFTS:
        r = math.radians(deg)
        sx, cy_ = math.sin(r), math.cos(r)
        L = abs(ew * sx) + abs(eh * cy_)
        p = ((xs - ew / 2) * sx - (ys - eh / 2) * cy_) / L + 0.5
        a = np.where(p < p1,
                     np.clip((p - p0) / max(p1 - p0, 1e-6), 0, 1),
                     np.clip((p2 - p) / max(p2 - p1, 1e-6), 0, 1))
        img = over(img, rgb, a0 * np.clip(a, 0, 1))
    return img


def add_grain(img, w, h, amount=1.5):
    rng = np.random.default_rng(1987)
    return np.clip(img + rng.normal(0, amount, (h, w, 1)), 0, 255)


def add_rings(im, w, h):
    """Drawn at 3x and shrunk, so the hairlines stay smooth."""
    S = 3
    layer = Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    scale = w / REF_W
    for right, top, px, a in RINGS:
        size = px * scale * S
        x1 = (1 - right) * w * S - size
        y1 = top * h * S
        d.ellipse([x1, y1, x1 + size, y1 + size],
                  outline=(150, 215, 240, int(round(a * 255))), width=max(1, int(1.2 * scale * S)))
    layer = layer.resize((w, h), Image.LANCZOS)
    im.alpha_composite(layer)
    return im


def place(im, art, w, h, width_px, centre, rotate=0, shadow=(0, 34, 60, 0.65)):
    """Composite one piece of art, with the same drop shadow the CSS gives it.
    `centre` is (x, y) as a fraction of the frame."""
    k = w / REF_W
    src = Image.open(art).convert("RGBA")
    tw = int(round(width_px * k))
    src = src.resize((tw, max(1, round(src.height * tw / src.width))), Image.LANCZOS)
    if rotate:
        src = src.rotate(rotate, resample=Image.BICUBIC, expand=True)
    x = int(round(centre[0] * w - src.width / 2))
    y = int(round(centre[1] * h - src.height / 2))

    if shadow:
        dx, dy, blur, a = shadow
        pad = int(blur * k * 3)
        sil = Image.new("RGBA", (src.width + pad * 2, src.height + pad * 2), (0, 0, 0, 0))
        sil.paste((0, 0, 0, int(round(a * 255))), (pad, pad), src.getchannel("A"))
        sil = sil.filter(ImageFilter.GaussianBlur(blur * k / 2))
        im.alpha_composite(sil, (x - pad + int(dx * k), y - pad + int(dy * k)))

    im.alpha_composite(src, (x, y))
    return im


def build(w, h):
    a = base(w, h)
    a = add_glows(a, w, h)
    a = add_shafts(a, w, h)
    a = add_grain(a, w, h)
    im = Image.fromarray(a.round().astype(np.uint8), "RGB").convert("RGBA")
    return add_rings(im, w, h)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for w, h in [(2560, 1440), (1920, 1080)]:
        plain = build(w, h)
        save(plain, f"hero_bg_{w}x{h}")

        withfish = place(plain.copy(), OFFICIAL, w, h, 1010, (0.712, 0.50), rotate=6)
        save(withfish, f"hero_bg_fujie_{w}x{h}")

        both = place(withfish.copy(), CHIBI, w, h, 138, (0.590, 0.285),
                     shadow=(0, 12, 22, 0.45))
        save(both, f"hero_bg_fujie_chibi_{w}x{h}")


def save(im, stem):
    p = OUT / (stem + ".jpg")
    im.convert("RGB").save(p, "JPEG", quality=94, optimize=True, progressive=True)
    q = OUT / (stem + ".png")
    im.convert("RGB").save(q, "PNG", optimize=True)
    print(f"  {p.name}  {p.stat().st_size // 1024} KB   |  {q.name}  {q.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
