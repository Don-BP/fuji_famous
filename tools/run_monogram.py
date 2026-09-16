"""The monogram canvas for the Maison Fujie line.

A luxury house builds its goods on one repeating mark. This renders that mark
from the OFFICIAL illustration - placed unmodified, only scaled, mirrored and
rotated - interleaved with the ripple rings Fujikin already uses, plus a small
drawn crest. Two colourways: ecru coated canvas and midnight.

The sheets are then handed to the product shots as a reference so every bag in
the line carries the same canvas.
"""
import math, pathlib, sys
from PIL import Image, ImageDraw

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from run_elegant_line import FUJIE, font, tracked, SS, OUT as ELEGANT_OUT  # noqa: E402

OUT = pathlib.Path(r"D:\Fuji_Famous\Fujie_Creative\09_merch_maison")
OUT.mkdir(parents=True, exist_ok=True)

ECRU = (196, 166, 122)          # coated canvas tan
ECRU_INK = (74, 52, 34)
MID = (16, 26, 38)              # midnight canvas
MID_INK = (176, 186, 198)


def crest(d, cx, cy, r, colour, w=2):
    """A small drawn house mark: a ring with a flow line through it."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=colour, width=w * SS)
    d.ellipse([cx - r * .58, cy - r * .58, cx + r * .58, cy + r * .58],
              outline=colour, width=max(1, w - 1) * SS)
    pts = [(cx - r * 1.25 + i * r * 2.5 / 18,
            cy + math.sin(i / 18 * math.pi * 2) * r * .30) for i in range(19)]
    d.line(pts, fill=colour, width=max(1, w - 1) * SS, joint="curve")


def monogram(name, bg, ink, tile=1400):
    im = Image.new("RGB", (tile * SS, tile * SS), bg)
    d = ImageDraw.Draw(im)
    art = Image.open(FUJIE).convert("RGBA")

    # the fish motif, tinted to a single flat ink so it reads as printed canvas
    flat = Image.new("RGBA", art.size, ink + (255,))
    flat.putalpha(art.getchannel("A"))

    cols, rows = 4, 5
    cw, ch = im.width / cols, im.height / rows
    for r in range(rows):
        for c in range(cols):
            cx = c * cw + cw / 2 + (cw / 2 if r % 2 else 0)
            cy = r * ch + ch / 2
            kind = (r + c) % 3
            if kind == 0:
                w = int(cw * 0.70)
                a = flat.resize((w, int(w * flat.height / flat.width)), Image.LANCZOS)
                a = a.rotate(-8, resample=Image.BICUBIC, expand=True)
            elif kind == 1:
                w = int(cw * 0.52)
                a = flat.transpose(Image.FLIP_LEFT_RIGHT)
                a = a.resize((w, int(w * flat.height / flat.width)), Image.LANCZOS)
                a = a.rotate(9, resample=Image.BICUBIC, expand=True)
            else:
                a = None
                crest(d, cx, cy, cw * 0.17, ink, w=2)
            if a is not None:
                for ox in (-im.width, 0, im.width):
                    im.paste(a, (int(cx - a.width / 2 + ox), int(cy - a.height / 2)), a)
            # small ripple punctuation between the motifs
            if kind != 2:
                rr = cw * 0.07
                for k in range(3):
                    d.ellipse([cx + cw * .34 - rr - k * rr * .5, cy + ch * .30 - rr - k * rr * .5,
                               cx + cw * .34 + rr + k * rr * .5, cy + ch * .30 + rr + k * rr * .5],
                              outline=ink, width=1 * SS)

    im = im.resize((tile, tile), Image.LANCZOS)
    im.save(OUT / name)
    print("  wrote", name, im.size)


if __name__ == "__main__":
    print("rendering monogram canvas ...")
    monogram("monogram_ecru.png", ECRU, ECRU_INK)
    monogram("monogram_midnight.png", MID, MID_INK)
    print("done ->", OUT)
