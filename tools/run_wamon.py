"""Fujie 和紋 - the traditional Japanese pattern collection.

Ten classical wamon, drawn precisely rather than generated, each seamless and
each chosen because it already means something for this fish: seigaiha is the
sea, uroko is scales, tatewaku is rising current, asanoha is growth. The
official illustration is then placed on top of those fields, unmodified.

Two colourways: vermilion on cream, the classic komon pairing, and Fujikin
indigo on cream.

Output: Fujie_Creative/11_wamon/  (tiles/ and plates)
"""
import math, pathlib, sys
from PIL import Image, ImageDraw

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from run_elegant_line import FUJIE, font, tracked, SS  # noqa: E402

OUT = pathlib.Path(r"D:\Fuji_Famous\Fujie_Creative\11_wamon")
TILES = OUT / "tiles"
TILES.mkdir(parents=True, exist_ok=True)

CREAM = (246, 241, 231)
VERM = (190, 52, 42)
INDIGO = (27, 61, 109)
SUMI = (38, 44, 50)
GOLD = (176, 141, 78)

T = 1000            # tile size before supersampling


def new(bg=CREAM, w=T, h=T):
    return Image.new("RGB", (w * SS, h * SS), bg)


def down(im):
    return im.resize((im.width // SS, im.height // SS), Image.LANCZOS)


def W(d, im, fn):
    """Draw fn at the tile and at its wrapped neighbours so the tile is seamless."""
    for ox in (-im.width, 0, im.width):
        for oy in (-im.height, 0, im.height):
            fn(ox, oy)


# ----------------------------------------------------------------- the patterns
def seigaiha(im, c, pitch=150, rings=5, w=3):
    """青海波 - the sea wave. Overlapping fans of concentric arcs."""
    d = ImageDraw.Draw(im)
    p = pitch * SS
    for row in range(-1, im.height // (p // 2) + 2):
        y = row * p / 2
        off = 0 if row % 2 == 0 else p / 2
        for col in range(-1, im.width // p + 2):
            cx = col * p + off
            for k in range(rings):
                r = p / 2 * (k + 1) / rings
                d.arc([cx - r, y - r, cx + r, y + r], 180, 360, fill=c, width=w * SS)


def asanoha(im, c, pitch=125, w=2):
    """麻の葉 - hemp leaf. A hex lattice with its spokes and star."""
    d = ImageDraw.Draw(im)
    R = pitch * SS / 2
    dx = R * math.sqrt(3)
    dy = R * 1.5
    for row in range(-2, int(im.height / dy) + 3):
        for col in range(-2, int(im.width / dx) + 3):
            cx = col * dx + (dx / 2 if row % 2 else 0)
            cy = row * dy
            v = [(cx + R * math.cos(math.pi / 6 + i * math.pi / 3),
                  cy + R * math.sin(math.pi / 6 + i * math.pi / 3)) for i in range(6)]
            d.polygon(v, outline=c, width=w * SS)
            for i in range(3):
                d.line([v[i], v[i + 3]], fill=c, width=w * SS)
            d.polygon([v[0], v[2], v[4]], outline=c, width=w * SS)
            d.polygon([v[1], v[3], v[5]], outline=c, width=w * SS)


def shippo(im, c, pitch=125, w=2):
    """七宝 - seven treasures. Circles overlapping into petals."""
    d = ImageDraw.Draw(im)
    p = pitch * SS
    r = p / math.sqrt(2)
    for row in range(-2, int(im.height / p) + 3):
        for col in range(-2, int(im.width / p) + 3):
            cx, cy = col * p, row * p
            d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=w * SS)


def kikko(im, c, pitch=120, w=2):
    """亀甲 - tortoise shell. Plain hexagon tiling."""
    d = ImageDraw.Draw(im)
    R = pitch * SS / 2
    dx = R * math.sqrt(3)
    dy = R * 1.5
    for row in range(-2, int(im.height / dy) + 3):
        for col in range(-2, int(im.width / dx) + 3):
            cx = col * dx + (dx / 2 if row % 2 else 0)
            cy = row * dy
            v = [(cx + R * math.cos(math.pi / 6 + i * math.pi / 3),
                  cy + R * math.sin(math.pi / 6 + i * math.pi / 3)) for i in range(6)]
            d.polygon(v, outline=c, width=w * SS)


def uroko(im, c, pitch=92):
    """鱗 - scales. Solid triangles, the oldest fish pattern there is."""
    d = ImageDraw.Draw(im)
    p = pitch * SS
    h = p * 0.86
    for row in range(-1, int(im.height / h) + 2):
        for col in range(-1, int(im.width / p) + 2):
            x = col * p + (p / 2 if row % 2 else 0)
            y = row * h
            d.polygon([(x, y + h), (x + p / 2, y), (x + p, y + h)], fill=c)


def tatewaku(im, c, pitch=118, w=3):
    """立涌 - rising steam. Pairs of curves that bulge and pinch."""
    d = ImageDraw.Draw(im)
    p = pitch * SS
    for col in range(-1, int(im.width / p) + 2):
        base = col * p
        for sign in (-1, 1):
            pts = []
            for yy in range(0, im.height + 8, 8):
                bulge = math.sin(yy / p * math.pi) * p * 0.22
                pts.append((base + sign * (p * 0.16 + abs(bulge)), yy))
            d.line(pts, fill=c, width=w * SS, joint="curve")


def yagasuri(im, c, pitch=88, w=0):
    """矢絣 - arrow feathers. Chevron columns, alternating direction."""
    d = ImageDraw.Draw(im)
    p = pitch * SS
    for col in range(-1, int(im.width / p) + 2):
        x = col * p
        up = col % 2 == 0
        for row in range(-1, int(im.height / p) + 2):
            y = row * p
            if up:
                d.polygon([(x, y + p), (x + p / 2, y + p * 0.45), (x + p, y + p),
                           (x + p, y + p * 0.62), (x + p / 2, y + p * 0.07), (x, y + p * 0.62)],
                          fill=c)
            else:
                d.polygon([(x, y), (x + p / 2, y + p * 0.55), (x + p, y),
                           (x + p, y + p * 0.38), (x + p / 2, y + p * 0.93), (x, y + p * 0.38)],
                          fill=c)


def ogi(im, c, pitch=175, ribs=8, w=2):
    """扇 - folding fans in rows, each with its ribs."""
    d = ImageDraw.Draw(im)
    p = pitch * SS
    for row in range(-1, int(im.height / (p * 0.55)) + 2):
        y = row * p * 0.55
        off = 0 if row % 2 == 0 else p / 2
        for col in range(-1, int(im.width / p) + 2):
            cx = col * p + off
            for k in (0.42, 1.0):
                r = p / 2 * k
                d.arc([cx - r, y - r, cx + r, y + r], 180, 360, fill=c, width=w * SS)
            for i in range(1, ribs):
                a = math.pi + math.pi * i / ribs
                d.line([(cx + p / 2 * 0.42 * math.cos(a), y + p / 2 * 0.42 * math.sin(a)),
                        (cx + p / 2 * math.cos(a), y + p / 2 * math.sin(a))],
                       fill=c, width=w * SS)


def kanoko(im, c, pitch=70, r=7):
    """鹿の子 - fawn spots. The small dot komon."""
    d = ImageDraw.Draw(im)
    p = pitch * SS
    rr = r * SS
    for row in range(-1, int(im.height / p) + 2):
        for col in range(-1, int(im.width / p) + 2):
            cx = col * p + (p / 2 if row % 2 else 0)
            cy = row * p
            d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=c)


def mizuwa(im, c, pitch=230, w=2):
    """水輪 - the ripple rings Fujikin already prints on everything."""
    d = ImageDraw.Draw(im)
    p = pitch * SS
    for row in range(-1, int(im.height / p) + 2):
        for col in range(-1, int(im.width / p) + 2):
            cx = col * p + (p / 2 if row % 2 else 0)
            cy = row * p
            for k in range(1, 6):
                r = p * 0.085 * k
                d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=w * SS)


def fujie_komon(im, c, pitch=175):
    """フジィ小紋 - the fish itself reduced to a flat komon motif."""
    art = Image.open(FUJIE).convert("RGBA")
    flat = Image.new("RGBA", art.size, c + (255,))
    flat.putalpha(art.getchannel("A"))
    p = pitch * SS
    d = ImageDraw.Draw(im)
    for row in range(-1, int(im.height / p) + 2):
        for col in range(-1, int(im.width / p) + 2):
            cx = col * p + (p / 2 if row % 2 else 0)
            cy = row * p
            w = int(p * 0.62)
            a = flat.resize((w, int(w * flat.height / flat.width)), Image.LANCZOS)
            if row % 2:
                a = a.transpose(Image.FLIP_LEFT_RIGHT)
            im.paste(a, (int(cx - a.width / 2), int(cy - a.height / 2)), a)
            for k in range(1, 4):
                r = p * 0.055 * k
                d.ellipse([cx + p * 0.30 - r, cy + p * 0.28 - r,
                           cx + p * 0.30 + r, cy + p * 0.28 + r], outline=c, width=1 * SS)


PATTERNS = [
    ("seigaiha", "青海波", "seigaiha", seigaiha),
    ("asanoha", "麻の葉", "asanoha", asanoha),
    ("shippo", "七宝", "shippo", shippo),
    ("kikko", "亀甲", "kikko", kikko),
    ("uroko", "鱗", "uroko", uroko),
    ("tatewaku", "立涌", "tatewaku", tatewaku),
    ("yagasuri", "矢絣", "yagasuri", yagasuri),
    ("ogi", "扇", "ogi", ogi),
    ("kanoko", "鹿の子", "kanoko", kanoko),
    ("mizuwa", "水輪", "mizuwa", mizuwa),
    ("fujie_komon", "フジィ小紋", "fujie komon", fujie_komon),
]


def field(fn, colour, w=T, h=T, bg=CREAM):
    im = new(bg, w, h)
    fn(im, colour)
    return im


# ------------------------------------------------------------------- the plates
def plate_furoshiki():
    im = field(seigaiha, (226, 208, 194), 1200, 1200)
    d = ImageDraw.Draw(im)
    m = 0.055
    d.rectangle([m * im.width, m * im.height, (1 - m) * im.width, (1 - m) * im.height],
                outline=VERM, width=3 * SS)
    art = Image.open(FUJIE).convert("RGBA")
    w = int(im.width * 0.62)
    a = art.resize((w, int(w * art.height / art.width)), Image.LANCZOS)
    a = a.rotate(8, resample=Image.BICUBIC, expand=True)
    im.paste(a, (int(im.width * 0.19), int(im.height * 0.40)), a)
    tracked(d, (im.width / 2, im.height * 0.86), "ながれを創る、世界へ",
            font(r"C:\Windows\Fonts\yuminl.ttf", 24), (120, 70, 60), track=9, anchor="ma")
    down(im).save(OUT / "plate_furoshiki_seigaiha.png")
    print("  plate_furoshiki_seigaiha")


def plate_giftbox():
    im = field(asanoha, (46, 78, 126), 1500, 1050, bg=(21, 44, 78))
    d = ImageDraw.Draw(im)
    band = Image.new("RGB", (im.width, int(im.height * 0.30)), (246, 241, 231))
    im.paste(band, (0, int(im.height * 0.35)))
    art = Image.open(FUJIE).convert("RGBA")
    w = int(im.width * 0.52)
    a = art.resize((w, int(w * art.height / art.width)), Image.LANCZOS)
    im.paste(a, (int(im.width * 0.24), int(im.height * 0.355)), a)
    tracked(d, (im.width / 2, im.height * 0.76), "F U J I E",
            font(r"C:\Windows\Fonts\YuGothL.ttc", 26), (232, 214, 176), track=13, anchor="ma")
    tracked(d, (im.width / 2, im.height * 0.83), "株式会社フジキン",
            font(r"C:\Windows\Fonts\yuminl.ttf", 14), (168, 186, 210), track=8, anchor="ma")
    down(im).save(OUT / "plate_giftbox_asanoha.png")
    print("  plate_giftbox_asanoha")


def plate_wrapping():
    im = field(fujie_komon, VERM, 1200, 1200)
    down(im).save(OUT / "plate_wrapping_komon.png")
    print("  plate_wrapping_komon")


def plate_noren():
    im = field(shippo, (58, 92, 140), 1400, 1000, bg=(27, 61, 109))
    d = ImageDraw.Draw(im)
    art = Image.open(FUJIE).convert("RGBA")
    w = int(im.width * 0.66)
    a = art.resize((w, int(w * art.height / art.width)), Image.LANCZOS)
    a = a.rotate(6, resample=Image.BICUBIC, expand=True)
    im.paste(a, (int(im.width * 0.17), int(im.height * 0.16)), a)
    d.line([(im.width / 2, im.height * 0.60), (im.width / 2, im.height)],
           fill=(20, 46, 84), width=7 * SS)
    tracked(d, (im.width / 2, im.height * 0.83), "フジィに会える場所",
            font(r"C:\Windows\Fonts\yuminl.ttf", 32), (232, 238, 244), track=12, anchor="ma")
    down(im).save(OUT / "plate_noren_shippo.png")
    print("  plate_noren_shippo")


def plate_sensu():
    im = new(CREAM, 1300, 800)
    fan = field(uroko, (232, 206, 198), 1300, 800)
    mask = Image.new("L", fan.size, 0)
    md = ImageDraw.Draw(mask)
    cx, cy = fan.width / 2, fan.height * 1.02
    R, r = fan.height * 0.98, fan.height * 0.24
    md.pieslice([cx - R, cy - R, cx + R, cy + R], 200, 340, fill=255)
    md.pieslice([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=0)
    im.paste(fan, (0, 0), mask)
    d = ImageDraw.Draw(im)
    d.pieslice([cx - R, cy - R, cx + R, cy + R], 200, 340, outline=VERM, width=3 * SS)
    for i in range(11):
        a = math.radians(200 + i * 14)
        d.line([(cx + r * math.cos(a), cy + r * math.sin(a)),
                (cx + R * math.cos(a), cy + R * math.sin(a))], fill=(214, 186, 176), width=2 * SS)
    art = Image.open(FUJIE).convert("RGBA")
    w = int(im.width * 0.46)
    a = art.resize((w, int(w * art.height / art.width)), Image.LANCZOS)
    a = a.rotate(-6, resample=Image.BICUBIC, expand=True)
    im.paste(a, (int(im.width * 0.27), int(im.height * 0.34)), a)
    down(im).save(OUT / "plate_sensu_uroko.png")
    print("  plate_sensu_uroko")


def plate_swatches():
    """One board showing the whole collection - the sheet a client would want."""
    cols, cell, pad, top = 4, 300, 26, 150
    rows = math.ceil(len(PATTERNS) / cols)
    Wp = cols * cell + pad * (cols + 1)
    Hp = top + rows * (cell + 62) + pad
    im = new((252, 250, 245), Wp, Hp)
    d = ImageDraw.Draw(im)
    tracked(d, (pad * SS, 52 * SS), "フジィ 和紋コレクション",
            font(r"C:\Windows\Fonts\yumin.ttf", 30), SUMI, track=6)
    tracked(d, (pad * SS, 100 * SS), "TRADITIONAL PATTERN COLLECTION",
            font(r"C:\Windows\Fonts\YuGothL.ttc", 12), (150, 140, 128), track=6)
    for i, (key, jp, romaji, fn) in enumerate(PATTERNS):
        r_, c_ = divmod(i, cols)
        x = pad + c_ * (cell + pad)
        y = top + r_ * (cell + 62)
        sw = field(fn, VERM if i % 2 == 0 else INDIGO, cell, cell)
        im.paste(sw, (x * SS, y * SS))
        d.rectangle([x * SS, y * SS, (x + cell) * SS, (y + cell) * SS],
                    outline=(226, 220, 208), width=1 * SS)
        tracked(d, (x * SS, (y + cell + 16) * SS), jp,
                font(r"C:\Windows\Fonts\yumin.ttf", 15), SUMI, track=3)
        tracked(d, (x * SS, (y + cell + 40) * SS), romaji.upper(),
                font(r"C:\Windows\Fonts\YuGothL.ttc", 9), (160, 150, 138), track=4)
    down(im).save(OUT / "wamon_collection_board.png")
    print("  wamon_collection_board")


if __name__ == "__main__":
    print("rendering wamon tiles ...")
    for key, jp, romaji, fn in PATTERNS:
        down(field(fn, VERM)).save(TILES / ("%s_vermilion.png" % key))
        down(field(fn, INDIGO)).save(TILES / ("%s_indigo.png" % key))
        print("  ", key)
    print("rendering plates ...")
    plate_furoshiki()
    plate_giftbox()
    plate_wrapping()
    plate_noren()
    plate_sensu()
    plate_swatches()
    print("done ->", OUT)
