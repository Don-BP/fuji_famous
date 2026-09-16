"""Print-ready plates for the grown-up Fujie line, built around the OFFICIAL artwork.

Nothing here redraws the official illustration. The PNG supplied by Fujikin is
placed unmodified and only uniformly scaled - no recolouring, no reshaping, no
text laid over it - as the character manual requires. Everything else on the
page (the flow field, the ripple rings, the type) is drawn here, in the visual
language Fujikin already uses on its own brochures, fans and gift boxes.

Output: Fujie_Creative/08_merch_official/
"""
import math, pathlib, random
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(r"D:\Fuji_Famous")
FUJIE = ROOT / "Documents_for_dev" / "05_fujie_絵柄例.png"
OUT = ROOT / "Fujie_Creative" / "08_merch_official"
OUT.mkdir(parents=True, exist_ok=True)

SS = 2                      # supersample factor - everything is drawn at 2x

WASHI = (244, 242, 236)
NAVY = (11, 36, 48)
INDIGO = (26, 54, 82)
BLUE = (0, 160, 233)        # Fujikin corporate blue
SILVER = (196, 206, 211)
INK = (26, 38, 44)

MINCHO_L = r"C:\Windows\Fonts\yuminl.ttf"
MINCHO = r"C:\Windows\Fonts\yumin.ttf"
GOTHIC_L = r"C:\Windows\Fonts\YuGothL.ttc"
GOTHIC_M = r"C:\Windows\Fonts\YuGothM.ttc"

TAG_JP = "ながれを創る、世界へ"
TAG_EN = "Creating the Flow for Sustainability"
CORP = "株式会社フジキン"


def font(path, size):
    try:
        return ImageFont.truetype(path, size * SS, index=0)
    except Exception:
        return ImageFont.truetype(MINCHO, size * SS)


def canvas(w, h, bg):
    return Image.new("RGB", (w * SS, h * SS), bg)


def finish(im, path):
    im = im.resize((im.width // SS, im.height // SS), Image.LANCZOS)
    im.save(path)
    print("  wrote", pathlib.Path(path).name, im.size)


def tracked(d, xy, text, f, fill, track=0, anchor="la"):
    """Draw text with extra letter-spacing - the wide tracking the brand uses."""
    if not track:
        d.text(xy, text, font=f, fill=fill, anchor=anchor)
        return
    track *= SS
    widths = [d.textlength(c, font=f) for c in text]
    total = sum(widths) + track * (len(text) - 1)
    x, y = xy
    if anchor[0] == "m":
        x -= total / 2
    elif anchor[0] == "r":
        x -= total
    for c, w in zip(text, widths):
        d.text((x, y), c, font=f, fill=fill, anchor="l" + anchor[1])
        x += w + track


def flow_field(im, colour, rows=46, amp=1.0, centres=None, width=1, margin=0.0):
    """Raked-sand / current lines: straight lines bent around a few still points."""
    d = ImageDraw.Draw(im)
    W, H = im.size
    centres = centres or [(0.30, 0.42, 0.26), (0.74, 0.66, 0.20)]
    top, bot = H * margin, H * (1 - margin)
    for i in range(rows):
        base = top + (bot - top) * (i + 0.5) / rows
        pts = []
        for px in range(0, W + 8, 8):
            y = base
            for cx, cy, s in centres:
                dx = (px - W * cx) / W
                dy = (base - H * cy) / H
                r2 = (dx * dx + dy * dy) / (s * s)
                y += math.sin(dx * 7.5) * H * 0.055 * amp * math.exp(-r2)
            pts.append((px, y))
        d.line(pts, fill=colour, width=width * SS, joint="curve")


def rings(im, cx, cy, colour, n=14, r0=0.04, step=0.030, width=1, jitter=0.35, seed=3):
    """Concentric water rings, unevenly spaced like raked gravel around a stone."""
    d = ImageDraw.Draw(im)
    W, H = im.size
    rnd = random.Random(seed)
    r = r0 * W
    for i in range(n):
        d.ellipse([cx * W - r, cy * H - r, cx * W + r, cy * H + r],
                  outline=colour, width=width * SS)
        r += step * W * (1 + rnd.uniform(-jitter, jitter))


def fujie(im, box, flip=False, rot=0):
    """Place the official illustration - uniform scale, mirror and rotation only.

    Fujikin's own brochures and packaging swim the fish across the page at an
    angle, so a rigid rotation is in keeping; nothing about the drawing itself
    is altered.
    """
    art = Image.open(FUJIE).convert("RGBA")
    if flip:
        art = art.transpose(Image.FLIP_LEFT_RIGHT)
    x, y, w = box[0] * im.width, box[1] * im.height, box[2] * im.width
    h = w * art.height / art.width
    art = art.resize((int(w), int(h)), Image.LANCZOS)
    if rot:
        art = art.rotate(rot, resample=Image.BICUBIC, expand=True)
    im.paste(art, (int(x), int(y)), art)
    return art.height / im.height


# ------------------------------------------------------------------ the plates
def poster():
    im = canvas(1240, 1754, WASHI)                       # A-series proportions
    flow_field(im, (219, 226, 230), rows=54, amp=1.25,
               centres=[(0.30, 0.44, 0.30), (0.80, 0.26, 0.15)], margin=0.06)
    rings(im, 0.66, 0.30, (196, 209, 216), n=16, r0=0.04, step=0.037, width=1)
    rings(im, 0.26, 0.60, (206, 217, 223), n=9, r0=0.03, step=0.030, seed=12)
    fujie(im, (0.13, 0.36, 0.62), rot=9)
    d = ImageDraw.Draw(im)
    tracked(d, (0.5 * im.width, 0.755 * im.height), TAG_JP, font(MINCHO_L, 40), INK,
            track=10, anchor="ma")
    tracked(d, (0.5 * im.width, 0.795 * im.height), TAG_EN.upper(), font(GOTHIC_L, 13),
            (120, 140, 150), track=5, anchor="ma")
    d.line([(0.42 * im.width, 0.845 * im.height), (0.58 * im.width, 0.845 * im.height)],
           fill=BLUE, width=2 * SS)
    tracked(d, (0.5 * im.width, 0.875 * im.height), CORP, font(MINCHO, 15), (90, 110, 120),
            track=8, anchor="ma")
    finish(im, OUT / "poster_flow.png")


def furoshiki(name, bg, line, ring, art_flip=False):
    im = canvas(1200, 1200, bg)
    flow_field(im, line, rows=42, amp=1.0,
               centres=[(0.30, 0.34, 0.26), (0.70, 0.74, 0.22)], margin=0.035)
    rings(im, 0.70, 0.70, ring, n=13, r0=0.04, step=0.033, seed=7)
    rings(im, 0.24, 0.26, ring, n=7, r0=0.03, step=0.026, seed=15)
    fujie(im, (0.14, 0.38, 0.56), flip=art_flip, rot=-8 if art_flip else 8)
    d = ImageDraw.Draw(im)
    tracked(d, (0.5 * im.width, 0.90 * im.height), TAG_JP, font(MINCHO_L, 26),
            line if bg == NAVY else (110, 128, 138), track=9, anchor="ma")
    # selvedge line, as a printed cloth would have
    m = 0.045
    d.rectangle([m * im.width, m * im.height, (1 - m) * im.width, (1 - m) * im.height],
                outline=line, width=1 * SS)
    finish(im, OUT / name)


def tenugui():
    im = canvas(1900, 620, WASHI)
    flow_field(im, (219, 227, 231), rows=26, amp=0.55,
               centres=[(0.22, 0.5, 0.30), (0.62, 0.42, 0.22), (0.90, 0.60, 0.16)],
               margin=0.05)
    rings(im, 0.62, 0.45, (198, 211, 218), n=12, r0=0.015, step=0.017, seed=11)
    rings(im, 0.17, 0.62, (205, 216, 222), n=7, r0=0.012, step=0.014, seed=21)
    fujie(im, (0.03, 0.24, 0.34), rot=7)
    fujie(im, (0.42, 0.46, 0.20), rot=-6, flip=True)
    fujie(im, (0.70, 0.18, 0.28), rot=5)
    d = ImageDraw.Draw(im)
    tracked(d, (0.955 * im.width, 0.86 * im.height), CORP, font(MINCHO_L, 15),
            (130, 148, 158), track=6, anchor="ra")
    finish(im, OUT / "tenugui.png")


def noren():
    im = canvas(1400, 1000, INDIGO)
    flow_field(im, (46, 78, 110), rows=34, amp=1.0,
               centres=[(0.5, 0.52, 0.34)], margin=0.02)
    rings(im, 0.5, 0.52, (58, 92, 126), n=10, r0=0.06, step=0.036, seed=5)
    fujie(im, (0.16, 0.16, 0.68), rot=6)
    d = ImageDraw.Draw(im)
    # the split between the two hanging panels, starting below the artwork
    d.line([(im.width / 2, im.height * 0.62), (im.width / 2, im.height)],
           fill=(18, 40, 62), width=6 * SS)
    tracked(d, (0.5 * im.width, 0.845 * im.height), "フジィに会える場所",
            font(MINCHO_L, 34), (226, 234, 238), track=12, anchor="ma")
    tracked(d, (0.5 * im.width, 0.905 * im.height), "SATOMI FISH FARM",
            font(GOTHIC_L, 13), (140, 176, 200), track=6, anchor="ma")
    finish(im, OUT / "noren.png")


def giftbox():
    im = canvas(1500, 1050, NAVY)
    flow_field(im, (28, 62, 78), rows=30, amp=0.8,
               centres=[(0.34, 0.5, 0.30), (0.78, 0.4, 0.18)], margin=0.04)
    rings(im, 0.66, 0.34, (44, 86, 104), n=14, r0=0.03, step=0.032, seed=2)
    fujie(im, (0.15, 0.30, 0.58), rot=7)
    d = ImageDraw.Draw(im)
    tracked(d, (0.5 * im.width, 0.755 * im.height), "F U J I E", font(GOTHIC_L, 30),
            (240, 245, 248), track=14, anchor="ma")
    d.line([(0.44 * im.width, 0.815 * im.height), (0.56 * im.width, 0.815 * im.height)],
           fill=BLUE, width=2 * SS)
    tracked(d, (0.5 * im.width, 0.845 * im.height), "SELECTED GIFT", font(GOTHIC_L, 12),
            (150, 176, 190), track=7, anchor="ma")
    tracked(d, (0.5 * im.width, 0.895 * im.height), CORP, font(MINCHO_L, 14),
            (130, 156, 170), track=8, anchor="ma")
    finish(im, OUT / "giftbox_lid.png")


def caviar_tin():
    im = canvas(1100, 1100, WASHI)
    d = ImageDraw.Draw(im)
    cx = cy = 0.5
    R = int(0.44 * im.width)
    lid = Image.new("RGB", (2 * R, 2 * R), NAVY)
    flow_field(lid, (30, 64, 80), rows=22, amp=0.7, centres=[(0.5, 0.5, 0.36)], margin=0.0)
    rings(lid, 0.5, 0.5, (40, 80, 98), n=7, r0=0.10, step=0.055, seed=4)
    fujie(lid, (0.10, 0.40, 0.80))
    ld = ImageDraw.Draw(lid)
    tracked(ld, (lid.width / 2, lid.height * 0.245), "F U J I E", font(GOTHIC_L, 22),
            (226, 234, 238), track=10, anchor="ma")
    tracked(ld, (lid.width / 2, lid.height * 0.70), "CAVIAR", font(GOTHIC_L, 15),
            (150, 180, 196), track=9, anchor="ma")
    tracked(ld, (lid.width / 2, lid.height * 0.755), "里美養魚場", font(MINCHO_L, 13),
            (130, 158, 172), track=7, anchor="ma")
    mask = Image.new("L", lid.size, 0)
    ImageDraw.Draw(mask).ellipse([0, 0, lid.width - 1, lid.height - 1], fill=255)
    im.paste(lid, (int(cx * im.width) - R, int(cy * im.height) - R), mask)
    d.ellipse([cx * im.width - R, cy * im.height - R, cx * im.width + R, cy * im.height + R],
              outline=(210, 218, 222), width=2 * SS)
    finish(im, OUT / "caviar_tin.png")


def stationery():
    im = canvas(1600, 1000, WASHI)
    d = ImageDraw.Draw(im)
    # business card, front
    card = Image.new("RGB", (int(0.34 * im.width), int(0.21 * im.width)), (255, 255, 255))
    flow_field(card, (228, 234, 237), rows=16, amp=0.5, centres=[(0.68, 0.5, 0.30)], margin=0.0)
    fujie(card, (0.04, 0.30, 0.44))
    cd = ImageDraw.Draw(card)
    tracked(cd, (card.width * 0.55, card.height * 0.22), CORP, font(MINCHO_L, 11),
            INK, track=4)
    tracked(cd, (card.width * 0.55, card.height * 0.40), TAG_JP, font(MINCHO_L, 9),
            (130, 148, 158), track=3)
    im.paste(card, (int(0.06 * im.width), int(0.14 * im.height)))
    d.rectangle([0.06 * im.width, 0.14 * im.height,
                 0.06 * im.width + card.width, 0.14 * im.height + card.height],
                outline=(215, 221, 224), width=1 * SS)
    # envelope
    env = Image.new("RGB", (int(0.44 * im.width), int(0.30 * im.width)), (252, 251, 248))
    flow_field(env, (226, 233, 236), rows=20, amp=0.6, centres=[(0.30, 0.62, 0.30)], margin=0.0)
    rings(env, 0.30, 0.62, (214, 223, 228), n=6, r0=0.05, step=0.035, seed=9)
    fujie(env, (0.42, 0.20, 0.50))
    ed = ImageDraw.Draw(env)
    tracked(ed, (env.width * 0.07, env.height * 0.82), CORP, font(MINCHO_L, 11),
            (110, 128, 138), track=4)
    im.paste(env, (int(0.47 * im.width), int(0.44 * im.height)))
    d.rectangle([0.47 * im.width, 0.44 * im.height,
                 0.47 * im.width + env.width, 0.44 * im.height + env.height],
                outline=(215, 221, 224), width=1 * SS)
    tracked(d, (0.06 * im.width, 0.06 * im.height), "STATIONERY", font(GOTHIC_L, 13),
            (150, 166, 174), track=7)
    finish(im, OUT / "stationery_plate.png")


def pattern():
    """Seamless-feel repeat for wrapping paper, scarves and packaging linings."""
    im = canvas(1200, 1200, (250, 250, 248))
    W, H = im.size
    art = Image.open(FUJIE).convert("RGBA")
    cols, rows_n = 5, 7
    cw = W / cols
    for r in range(rows_n):
        for c in range(cols):
            scale = (0.82, 0.58, 0.70)[(r + c) % 3]
            w = int(cw * scale)
            h = int(w * art.height / art.width)
            a = art.resize((w, h), Image.LANCZOS)
            if (r + c) % 2:
                a = a.transpose(Image.FLIP_LEFT_RIGHT)
            a = a.rotate((-7, 5, 0, 9)[(r * 2 + c) % 4], resample=Image.BICUBIC, expand=True)
            w, h = a.size
            x = int(c * cw + (cw - w) / 2 + (cw * 0.5 if r % 2 else 0)) % W
            y = int(r * (H / rows_n) + (H / rows_n - h) / 2)
            im.paste(a, (x, y), a)
            if x + w > W:
                im.paste(a, (x - W, y), a)
    finish(im, OUT / "pattern_repeat.png")


def uchiwa():
    im = canvas(1100, 1200, (255, 255, 255))
    face = Image.new("RGB", (int(0.86 * im.width), int(0.72 * im.height)), WASHI)
    flow_field(face, (216, 226, 231), rows=30, amp=0.9,
               centres=[(0.34, 0.46, 0.28), (0.76, 0.58, 0.20)], margin=0.0)
    rings(face, 0.70, 0.56, (194, 208, 216), n=13, r0=0.035, step=0.031, seed=6)
    fujie(face, (0.10, 0.32, 0.56), rot=8)
    fd = ImageDraw.Draw(face)
    tracked(fd, (face.width * 0.5, face.height * 0.80), TAG_JP, font(MINCHO_L, 22),
            (110, 128, 138), track=8, anchor="ma")
    mask = Image.new("L", face.size, 0)
    ImageDraw.Draw(mask).ellipse([0, 0, face.width - 1, face.height - 1], fill=255)
    ox, oy = int(0.07 * im.width), int(0.03 * im.height)
    im.paste(face, (ox, oy), mask)
    d = ImageDraw.Draw(im)
    d.ellipse([ox, oy, ox + face.width, oy + face.height], outline=(205, 214, 219),
              width=2 * SS)
    hw = int(0.035 * im.width)
    d.rounded_rectangle([im.width / 2 - hw / 2, oy + face.height - 10 * SS,
                         im.width / 2 + hw / 2, im.height * 0.97],
                        radius=hw / 2, fill=(228, 224, 214), outline=(205, 200, 188),
                        width=1 * SS)
    finish(im, OUT / "uchiwa_fan.png")


def notebook():
    im = canvas(1000, 1340, NAVY)
    flow_field(im, (26, 58, 74), rows=44, amp=0.85,
               centres=[(0.30, 0.34, 0.26), (0.72, 0.70, 0.22)], margin=0.03)
    rings(im, 0.70, 0.66, (40, 80, 98), n=14, r0=0.035, step=0.033, seed=8)
    fujie(im, (0.13, 0.27, 0.66), rot=7)
    d = ImageDraw.Draw(im)
    tracked(d, (0.5 * im.width, 0.60 * im.height), TAG_EN.upper(), font(GOTHIC_L, 12),
            (128, 158, 174), track=6, anchor="ma")
    tracked(d, (0.5 * im.width, 0.885 * im.height), CORP, font(MINCHO_L, 14),
            (120, 148, 162), track=8, anchor="ma")
    d.line([(0.09 * im.width, 0), (0.09 * im.width, im.height)], fill=(20, 48, 62),
           width=3 * SS)
    finish(im, OUT / "notebook_cover.png")


if __name__ == "__main__":
    print("rendering the official line ...")
    poster()
    furoshiki("furoshiki_white.png", WASHI, (214, 224, 229), (198, 211, 218))
    furoshiki("furoshiki_navy.png", NAVY, (34, 70, 88), (44, 84, 104), art_flip=True)
    tenugui()
    noren()
    giftbox()
    caviar_tin()
    stationery()
    pattern()
    uchiwa()
    notebook()
    print("done ->", OUT)
