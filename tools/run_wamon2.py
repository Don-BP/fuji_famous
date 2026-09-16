"""Fujie 和紋 II - patterns invented for this fish.

The first collection is the classical grammar. This one bends it: the fish is
hidden inside the waves, the tortoise-shell nodes become valve handwheels, the
plover flock becomes a shoal, the arrows point upstream, and the caviar becomes
a komon of its own.

Colourways: vermilion on cream, indigo on cream, gold on sumi black.

Output: Fujie_Creative/11_wamon/ (tiles2/ and plates)
"""
import math, pathlib, sys
from PIL import Image, ImageDraw

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from run_elegant_line import FUJIE, font, tracked, SS            # noqa: E402
from run_wamon import (new, down, field, OUT, CREAM, VERM, INDIGO, SUMI, GOLD,
                       seigaiha, kikko, uroko)                    # noqa: E402

TILES2 = OUT / "tiles2"
TILES2.mkdir(parents=True, exist_ok=True)

CYAN = (0, 150, 210)
SNOW = (250, 250, 248)


def flat_fish(colour, width, flip=False, rot=0):
    art = Image.open(FUJIE).convert("RGBA")
    f = Image.new("RGBA", art.size, tuple(colour) + (255,))
    f.putalpha(art.getchannel("A"))
    if flip:
        f = f.transpose(Image.FLIP_LEFT_RIGHT)
    f = f.resize((int(width), int(width * f.height / f.width)), Image.LANCZOS)
    if rot:
        f = f.rotate(rot, resample=Image.BICUBIC, expand=True)
    return f


# --------------------------------------------------------------- new patterns
def seigaiha_fujie(im, c, pitch=200):
    """青海波フジィ - a fish resting inside every other wave fan."""
    seigaiha(im, c, pitch=pitch, rings=4, w=3)
    p = pitch * SS
    fish = flat_fish(c, p * 0.52)
    for row in range(-1, int(im.height / (p / 2)) + 2):
        y = row * p / 2
        off = 0 if row % 2 == 0 else p / 2
        for col in range(-1, int(im.width / p) + 2):
            if (row + col) % 2:
                continue
            cx = col * p + off
            im.paste(fish, (int(cx - fish.width / 2), int(y - fish.height * 1.05)), fish)


def chidori_fujie(im, c, pitch=118):
    """千鳥 - the plover flock, swum by sturgeon instead."""
    p = pitch * SS
    small = flat_fish(c, p * 0.86, rot=12)
    small2 = flat_fish(c, p * 0.66, flip=True, rot=-9)
    d = ImageDraw.Draw(im)
    for row in range(-1, int(im.height / p) + 2):
        for col in range(-1, int(im.width / p) + 2):
            cx = col * p + (p / 2 if row % 2 else 0)
            cy = row * p
            f = small if (row + col) % 2 == 0 else small2
            im.paste(f, (int(cx - f.width / 2), int(cy - f.height / 2)), f)
            r = p * 0.06
            d.ellipse([cx + p * .30 - r, cy + p * .30 - r, cx + p * .30 + r, cy + p * .30 + r],
                      outline=c, width=1 * SS)


def kikko_valve(im, c, pitch=140, w=2):
    """亀甲弁 - tortoise shell with a valve handwheel at every node."""
    kikko(im, c, pitch=pitch, w=w)
    d = ImageDraw.Draw(im)
    R = pitch * SS / 2
    dx, dy = R * math.sqrt(3), R * 1.5
    rr = R * 0.30
    for row in range(-2, int(im.height / dy) + 3):
        for col in range(-2, int(im.width / dx) + 3):
            cx = col * dx + (dx / 2 if row % 2 else 0)
            cy = row * dy
            d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=c, width=w * SS)
            d.ellipse([cx - rr * .34, cy - rr * .34, cx + rr * .34, cy + rr * .34],
                      outline=c, width=w * SS)
            for i in range(6):
                a = i * math.pi / 3
                d.line([(cx + rr * .34 * math.cos(a), cy + rr * .34 * math.sin(a)),
                        (cx + rr * math.cos(a), cy + rr * math.sin(a))], fill=c, width=w * SS)


def ichimatsu_fujie(im, c, pitch=95):
    """市松 - the chequer, with a fish reserved out of every filled square."""
    p = pitch * SS
    d = ImageDraw.Draw(im)
    bg = im.getpixel((0, 0))
    fish_on_block = flat_fish(bg, p * 0.80, rot=6)
    fish_on_ground = flat_fish(c, p * 0.80, flip=True, rot=-6)
    for row in range(-1, int(im.height / p) + 2):
        for col in range(-1, int(im.width / p) + 2):
            x, y = col * p, row * p
            filled = (row + col) % 2 == 0
            if filled:
                d.rectangle([x, y, x + p, y + p], fill=c)
            f = fish_on_block if filled else fish_on_ground
            im.paste(f, (int(x + (p - f.width) / 2), int(y + (p - f.height) / 2)), f)


def roe_komon(im, c, pitch=48):
    """魚卵小紋 - caviar. Dots that swell and shrink across the field."""
    d = ImageDraw.Draw(im)
    p = pitch * SS
    for row in range(-1, int(im.height / p) + 2):
        for col in range(-1, int(im.width / p) + 2):
            cx = col * p + (p / 2 if row % 2 else 0)
            cy = row * p
            k = 0.5 + 0.5 * math.sin(cx / (p * 3.1)) * math.cos(cy / (p * 2.4))
            r = p * (0.07 + 0.31 * k)
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
            d.ellipse([cx - r * .34 - r * .18, cy - r * .34 - r * .18,
                       cx - r * .34 + r * .18, cy - r * .34 + r * .18],
                      fill=im.getpixel((0, 0)))


def yagasuri_nagare(im, c, pitch=120, w=4):
    """矢絣ながれ - the arrow feather redrawn as a current, all pointing upstream."""
    d = ImageDraw.Draw(im)
    p = pitch * SS
    for col in range(-1, int(im.width / p) + 2):
        x = col * p
        for row in range(-1, int(im.height / (p * 0.62)) + 2):
            y = row * p * 0.62 + (p * 0.31 if col % 2 else 0)
            d.line([(x, y + p * .30), (x + p * .5, y), (x + p, y + p * .30)],
                   fill=c, width=w * SS, joint="curve")
            d.line([(x + p * .18, y + p * .46), (x + p * .5, y + p * .18),
                    (x + p * .82, y + p * .46)], fill=c, width=max(1, w - 2) * SS,
                   joint="curve")


def karakusa_nagare(im, c, pitch=300, w=3):
    """唐草ながれ - the scrolling vine, grown out of moving water.

    A continuous wave spine with a spiral curl at every crest and trough, and a
    ripple bead tucked into each curl.
    """
    d = ImageDraw.Draw(im)
    p = pitch * SS

    def spiral(cx, cy, r, turns=2.1, start=0.0, cw=1):
        pts = []
        n = 56
        for i in range(n + 1):
            t = i / n * turns * math.pi * 2
            rr = r * (1 - i / n * 0.86)
            pts.append((cx + math.cos(start + cw * t) * rr,
                        cy + math.sin(start + cw * t) * rr))
        d.line(pts, fill=c, width=max(1, w - 1) * SS, joint="curve")

    for row in range(-1, int(im.height / (p * 0.5)) + 2):
        y0 = row * p * 0.5
        shift = 0 if row % 2 == 0 else p * 0.5
        pts = []
        for x in range(-int(p), im.width + int(p), 10):
            pts.append((x, y0 + math.sin((x + shift) / p * math.pi * 2) * p * 0.17))
        d.line(pts, fill=c, width=w * SS, joint="curve")
        k = -1
        while True:
            k += 1
            cx = -p + shift + k * p * 0.5
            if cx > im.width + p:
                break
            up = k % 2 == 0
            cy = y0 + (-1 if up else 1) * p * 0.17
            spiral(cx, cy + (-1 if up else 1) * p * 0.10, p * 0.11,
                   start=math.pi / 2 if up else -math.pi / 2, cw=1 if up else -1)
            for j in range(1, 4):
                rr = p * 0.016 * j
                d.ellipse([cx - rr, cy + (-1 if up else 1) * p * 0.10 - rr,
                           cx + rr, cy + (-1 if up else 1) * p * 0.10 + rr],
                          outline=c, width=1 * SS)


NEW = [
    ("seigaiha_fujie", "青海波フジィ", "seigaiha fujie", seigaiha_fujie),
    ("chidori_fujie", "千鳥フジィ", "chidori fujie", chidori_fujie),
    ("kikko_valve", "亀甲弁", "kikko valve", kikko_valve),
    ("ichimatsu_fujie", "市松フジィ", "ichimatsu fujie", ichimatsu_fujie),
    ("roe_komon", "魚卵小紋", "roe komon", roe_komon),
    ("yagasuri_nagare", "矢絣ながれ", "yagasuri nagare", yagasuri_nagare),
    ("karakusa_nagare", "唐草ながれ", "karakusa nagare", karakusa_nagare),
]

WAYS = [("vermilion", VERM, CREAM), ("indigo", INDIGO, CREAM), ("gold", GOLD, (22, 22, 24))]


# ------------------------------------------------------------------- new plates
def plate_haori():
    """A haori back panel - one big field, one big fish, the way a crest sits."""
    im = new((20, 22, 26), 1000, 1340)
    karakusa_nagare(im, (58, 62, 70))
    d = ImageDraw.Draw(im)
    r = im.width * 0.30
    cx, cy = im.width / 2, im.height * 0.40
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(246, 241, 231))
    art = Image.open(FUJIE).convert("RGBA")
    w = int(r * 1.72)
    a = art.resize((w, int(w * art.height / art.width)), Image.LANCZOS)
    im.paste(a, (int(cx - a.width / 2), int(cy - a.height / 2)), a)
    tracked(d, (cx, im.height * 0.80), "ながれを創る、世界へ",
            font(r"C:\Windows\Fonts\yuminl.ttf", 26), (198, 206, 214), track=10, anchor="ma")
    down(im).save(OUT / "plate_haori_karakusa.png")
    print("  plate_haori_karakusa")


def plate_sake():
    """A bottle label: black, gold, and a lot of restraint."""
    im = new((246, 241, 231), 1200, 800)
    lab = new((18, 20, 24), 760, 640)
    roe_komon(lab, (52, 44, 32), pitch=46)
    ld = ImageDraw.Draw(lab)
    art = Image.open(FUJIE).convert("RGBA")
    w = int(lab.width * 0.66)
    a = art.resize((w, int(w * art.height / art.width)), Image.LANCZOS)
    lab.paste(a, (int(lab.width * 0.17), int(lab.height * 0.30)), a)
    tracked(ld, (lab.width / 2, lab.height * 0.13), "F U J I E",
            font(r"C:\Windows\Fonts\YuGothL.ttc", 22), GOLD, track=12, anchor="ma")
    ld.line([(lab.width * .38, lab.height * .245), (lab.width * .62, lab.height * .245)],
            fill=GOLD, width=2 * SS)
    tracked(ld, (lab.width / 2, lab.height * 0.70), "純米大吟醸",
            font(r"C:\Windows\Fonts\yumin.ttf", 22), (232, 226, 214), track=10, anchor="ma")
    tracked(ld, (lab.width / 2, lab.height * 0.82), "里美",
            font(r"C:\Windows\Fonts\yuminl.ttf", 14), (168, 160, 146), track=8, anchor="ma")
    im.paste(down(lab).resize((760 * SS, 640 * SS), Image.LANCZOS),
             (int((im.width - 760 * SS) / 2), int((im.height - 640 * SS) / 2)))
    down(im).save(OUT / "plate_sake_label.png")
    print("  plate_sake_label")


def plate_chiyogami():
    """A chiyogami paper pack - six of the patterns as folded sheets."""
    cols, cell, pad = 3, 400, 34
    picks = [(seigaiha_fujie, VERM, CREAM), (chidori_fujie, INDIGO, CREAM),
             (kikko_valve, GOLD, (22, 22, 24)), (ichimatsu_fujie, VERM, CREAM),
             (roe_komon, INDIGO, CREAM), (yagasuri_nagare, CYAN, SNOW)]
    rows = 2
    Wp = cols * cell + pad * (cols + 1)
    Hp = rows * cell + pad * (rows + 1)
    im = new((238, 234, 226), Wp, Hp)
    for i, (fn, col, bg) in enumerate(picks):
        r_, c_ = divmod(i, cols)
        x, y = pad + c_ * (cell + pad), pad + r_ * (cell + pad)
        sh = field(fn, col, cell, cell, bg=bg)
        im.paste(sh, (x * SS, y * SS))
        d = ImageDraw.Draw(im)
        d.rectangle([x * SS, y * SS, (x + cell) * SS, (y + cell) * SS],
                    outline=(214, 208, 198), width=1 * SS)
    down(im).save(OUT / "plate_chiyogami_pack.png")
    print("  plate_chiyogami_pack")


def board2():
    cols, cell, pad, top = 4, 300, 26, 150
    rows = math.ceil(len(NEW) / cols)
    Wp = cols * cell + pad * (cols + 1)
    Hp = top + rows * (cell + 62) + pad
    im = new((252, 250, 245), Wp, Hp)
    d = ImageDraw.Draw(im)
    tracked(d, (pad * SS, 52 * SS), "フジィ 和紋コレクション 弐",
            font(r"C:\Windows\Fonts\yumin.ttf", 30), SUMI, track=6)
    tracked(d, (pad * SS, 100 * SS), "PATTERNS INVENTED FOR THIS FISH",
            font(r"C:\Windows\Fonts\YuGothL.ttc", 12), (150, 140, 128), track=6)
    ways = [(VERM, CREAM), (INDIGO, CREAM), (GOLD, (22, 22, 24)), (CYAN, SNOW)]
    for i, (key, jp, romaji, fn) in enumerate(NEW):
        r_, c_ = divmod(i, cols)
        x = pad + c_ * (cell + pad)
        y = top + r_ * (cell + 62)
        col, bg = ways[i % len(ways)]
        im.paste(field(fn, col, cell, cell, bg=bg), (x * SS, y * SS))
        d.rectangle([x * SS, y * SS, (x + cell) * SS, (y + cell) * SS],
                    outline=(226, 220, 208), width=1 * SS)
        tracked(d, (x * SS, (y + cell + 16) * SS), jp,
                font(r"C:\Windows\Fonts\yumin.ttf", 15), SUMI, track=3)
        tracked(d, (x * SS, (y + cell + 40) * SS), romaji.upper(),
                font(r"C:\Windows\Fonts\YuGothL.ttc", 9), (160, 150, 138), track=4)
    down(im).save(OUT / "wamon_collection_board_2.png")
    print("  wamon_collection_board_2")


if __name__ == "__main__":
    print("rendering invented wamon ...")
    for key, jp, romaji, fn in NEW:
        for wname, col, bg in WAYS:
            down(field(fn, col, bg=bg)).save(TILES2 / ("%s_%s.png" % (key, wname)))
        print("  ", key)
    print("rendering plates ...")
    plate_haori()
    plate_sake()
    plate_chiyogami()
    board2()
    print("done ->", OUT)
