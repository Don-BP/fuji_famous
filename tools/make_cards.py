"""The two cover images for the hub's feature cards.

Composed from the same art the pages themselves use, so the cards show what the
visitor is about to open.
"""
import pathlib
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(r"D:\Fuji_Famous")
ART = ROOT / "site" / "art"
OUT = ROOT / "promo" / "shots"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1400, 875                                  # 16:10, the card aspect
SS = 2
DELA = ROOT / "tools" / "_fontcache" / "DelaGothicOne-Regular.ttf"
ZEN = ROOT / "tools" / "_fontcache" / "ZenMaruGothic-Bold.ttf"
MINCHO = r"C:\Windows\Fonts\yuminl.ttf"


def f(path, size):
    return ImageFont.truetype(str(path), size * SS)


def base(bg_name, dim=0.42):
    im = Image.open(ART / bg_name).convert("RGB").resize((W * SS, H * SS), Image.LANCZOS)
    veil = Image.new("RGB", im.size, (4, 18, 26))
    return Image.blend(im, veil, dim)


def place(im, png, cx, cy, w):
    a = Image.open(png).convert("RGBA")
    ww = int(w * im.width)
    a = a.resize((ww, int(ww * a.height / a.width)), Image.LANCZOS)
    im.paste(a, (int(cx * im.width - a.width / 2), int(cy * im.height - a.height / 2)), a)


def tracked(d, xy, text, font, fill, track=0, anchor="ma"):
    if not track:
        d.text(xy, text, font=font, fill=fill, anchor=anchor)
        return
    track *= SS
    ws = [d.textlength(c, font=font) for c in text]
    total = sum(ws) + track * (len(text) - 1)
    x, y = xy
    if anchor[0] == "m":
        x -= total / 2
    for c, w in zip(text, ws):
        d.text((x, y), c, font=font, fill=fill, anchor="l" + anchor[1])
        x += w + track


def game_card():
    im = base("bg_title.jpg", 0.34)
    place(im, ART / "title_fujie.png", 0.5, 0.36, 0.26)
    d = ImageDraw.Draw(im)
    tracked(d, (im.width / 2, im.height * 0.585), "1987 — FUJIKIN", f(ZEN, 15),
            (140, 200, 220), track=7)
    tracked(d, (im.width / 2, im.height * 0.645), "フジィを育てよう", f(DELA, 40),
            (238, 246, 248), track=3)
    # the start button, as the screen actually draws it
    bw, bh = int(im.width * 0.22), int(im.height * 0.085)
    bx, by = int(im.width / 2 - bw / 2), int(im.height * 0.78)
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=bh // 2, fill=(46, 186, 220))
    tracked(d, (im.width / 2, by + bh * 0.28), "はじめる", f(ZEN, 19), (4, 33, 46), track=2)
    im.resize((W, H), Image.LANCZOS).save(OUT / "shot_game.jpg", quality=88)
    print("  shot_game.jpg")


def timeline_card():
    im = base("bg_egg.jpg", 0.30)
    place(im, ROOT / "site" / "stage_1_egg.png", 0.5, 0.42, 0.22)
    d = ImageDraw.Draw(im)
    tracked(d, (im.width / 2, im.height * 0.685), "1987", f(DELA, 58),
            (150, 205, 228), track=6)
    tracked(d, (im.width / 2, im.height * 0.80), "一粒の卵から", f(MINCHO, 34),
            (232, 242, 246), track=12)
    im.resize((W, H), Image.LANCZOS).save(OUT / "shot_timeline.jpg", quality=88)
    print("  shot_timeline.jpg")


if __name__ == "__main__":
    print("composing feature cards ...")
    game_card()
    timeline_card()
    print("done ->", OUT)
