"""Re-proportion pill-shaped UI art (buttons, gauge tracks) to the shape it is
actually drawn at.

A pill is two round caps with a uniform band between them. Stretching the whole
image smears the caps; this keeps the caps intact and rebuilds the band from a
single column, so the result can be 9-sliced and drawn at any width with no
distortion at all.
"""
import pathlib, sys
from PIL import Image

OUT = pathlib.Path("D:/Fuji_Famous/Fujie_Creative/06_game")
SITE = pathlib.Path("D:/Fuji_Famous/site/art")


def repill(name, ratio, out_h):
    src = OUT / name
    im = Image.open(src).convert("RGBA")
    w, h = im.size
    cap = h // 2
    band_w = max(4, int(h * ratio) - cap * 2)
    left = im.crop((0, 0, cap, h))
    right = im.crop((w - cap, 0, w, h))
    band = im.crop((w // 2 - 1, 0, w // 2 + 1, h)).resize((band_w, h), Image.LANCZOS)

    new_w = cap * 2 + band_w
    out = Image.new("RGBA", (new_w, h), (0, 0, 0, 0))
    out.paste(band, (cap, 0))
    out.paste(left, (0, 0))
    out.paste(right, (new_w - cap, 0))

    out = out.resize((round(new_w * out_h / h), out_h), Image.LANCZOS)
    dst = SITE / name
    out.save(dst, "PNG", optimize=True)
    print(f"  {name}: {w}x{h} -> {out.size[0]}x{out.size[1]}  (cap {out_h//2}px)")
    return out.size


if __name__ == "__main__":
    repill("ui_btn.png", 5.0, 96)
    repill("ui_btn_ghost.png", 5.0, 96)
    repill("ui_gauge.png", 14.0, 64)
