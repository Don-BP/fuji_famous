"""Cut the generated sticker sheets into individual LINE-ready stickers.

The sheets are single flat images: every sticker shares one white field, and the
white die-cut borders merge into that field, so a plain background removal would
dissolve the borders too. Instead we find the *ink* (everything that is not the
white ground), group it into one cluster per grid cell, then rebuild each
sticker's die-cut silhouette by dilating its own ink. That gives a real
transparent cut-out with the white border intact.

Output follows the LINE Creators Market spec:
  sticker   370 x 320 max, PNG-32, ~10px transparent margin
  main       240 x 240
  tab         96 x  74

    python tools/slice_stickers.py            # all sheets + the singles
    python tools/slice_stickers.py sheets     # sheets only
"""
import json, pathlib, sys
import numpy as np
import cv2
from PIL import Image

ROOT = pathlib.Path(r"D:\Fuji_Famous")
SRC = ROOT / "Fujie_Creative" / "02_stickers"
ACT2 = ROOT / "Fujie_Creative" / "15_act2"
OUT = ROOT / "Fujie_Creative" / "16_line_set"

W, H, MARGIN = 370, 320, 10
INK_MAX = 236      # a pixel is ink if any channel is below this
MERGE = 3          # denoise only - the grid does the grouping, not the dilation
BORDER = 9         # dilation that becomes the white die-cut edge
MIN_AREA = 1500    # ignore specks

JP_01 = ["おはよう", "ありがとう", "おつかれさま", "OK", "りょうかい", "ごめんね", "よろしく",
         "いいね", "すごい", "がんばって", "まかせて", "うれしい", "えっ", "ねむい",
         "おなかすいた", "たすけて", "おやすみ", "いってきます", "かなしい", "だいじょうぶ"]
JP_02 = ["ながれにのれ", "きわみへ", "キャビア", "なるほど", "さすが", "ちょっとまって", "ほんと",
         "やったー", "つかれた", "あつい", "さむい", "おめでとう", "ファイト", "ごちそうさま",
         "ひさしぶり", "かんぱい", "がーん", "ぴかぴか", "だいすき", "またね"]
JP_03 = ["とんだー！", "くるくる", "いそげー", "サメじゃない！", "いくぞー", "ながれにのれ",
         "とうじょう！", "よっしゃ！", "きりもみ", "しゅっぱつ", "ドーン", "みて！", "ひらめいた",
         "パワー！", "ストップ！", "ハイタッチ", "ロケット", "こっそり", "わらう", "ヒーロー"]
EN_01 = ["Morning!", "Yay!", "Thank you!", "OK!", "Sorry!", "On it!", "Nice!", "So sleepy",
         "Hungry...", "No way!", "Really?", "Congrats!", "Good night", "Love it", "Help!",
         "I am here", "See you!", "Go team!", "Nope", "Take a break"]
EN_02 = ["Let us go!", "Making waves", "Deep dive", "Splash!", "Creating the flow", "Upstream",
         "Chill", "Focus", "Teamwork", "Big win", "Power up", "Brrr", "Too hot", "Study time",
         "So tired", "Spin!", "Got it!", "Stop!", "High five", "Hero"]

SHEETS = [
    ("sticker_sheet_01.png", "jp", JP_01),
    ("sticker_sheet_02.png", "jp", JP_02),
    ("sticker_sheet_03_action.png", "jp_action", JP_03),
    ("sticker_sheet_EN_01_chat.png", "en", EN_01),
    ("sticker_sheet_EN_02_action.png", "en", EN_02),
]

# A sheet cell we have redrawn on its own. The single replaces that cell in place,
# keeping its position and caption, so the sheets themselves are never touched.
OVERRIDE = {
    ("jp_action", "ロケット"): "rocket_straight.png",
    ("jp", "ファイト"): "fight_fixed.png",
}

SINGLES = [
    ("notshark_jp_01.png", "jp_action", "サメじゃないです"),
    ("notshark_jp_02.png", "jp_action", "サメじゃないってば"),
    ("notshark_jp_03.png", "jp_action", "チョウザメです"),
    ("notshark_jp_04.png", "jp_action", "２億年このまま"),
    ("notshark_en_01.png", "en_action", "Not a shark!"),
    ("notshark_en_02.png", "en_action", "I am a sturgeon"),
    ("notshark_en_03.png", "en_action", "Still not a shark"),
    ("notshark_en_04.png", "en_action", "200 million years"),
]


def ink_mask(rgb):
    """True wherever the image is not the flat white ground."""
    return (rgb.min(axis=2) < INK_MAX).astype(np.uint8)


def grow(mask, r):
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (r * 2 + 1, r * 2 + 1))
    return cv2.dilate(mask, k)


def fill_holes(mask):
    pad = cv2.copyMakeBorder(mask, 2, 2, 2, 2, cv2.BORDER_CONSTANT, value=0)
    ff = pad.copy()
    cv2.floodFill(ff, np.zeros((pad.shape[0] + 2, pad.shape[1] + 2), np.uint8), (0, 0), 1)
    holes = (ff == 0).astype(np.uint8)
    return (pad | holes)[2:-2, 2:-2]


def die_cut(rgb, ink):
    """RGBA where alpha is the sticker silhouette: the ink plus a white border."""
    sil = fill_holes(grow(ink, BORDER))
    ys, xs = np.where(sil > 0)
    if len(ys) == 0:
        return None
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    sub = sil[y0:y1, x0:x1]
    # drop a neighbouring sticker's pixels before feathering, or its edge shows
    col = rgb[y0:y1, x0:x1].copy()
    col[sub == 0] = 255
    alpha = cv2.GaussianBlur((sub * 255).astype(np.uint8), (0, 0), 0.8)
    return np.dstack([col, alpha])


def to_canvas(rgba, w=W, h=H, margin=MARGIN):
    im = Image.fromarray(rgba, "RGBA")
    box = (w - margin * 2, h - margin * 2)
    scale = min(box[0] / im.width, box[1] / im.height)
    im = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))),
                   Image.LANCZOS)
    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    canvas.paste(im, ((w - im.width) // 2, (h - im.height) // 2), im)
    return canvas


def cells_from_sheet(path, cols=4, rows=5):
    """Group every ink blob into its grid cell, then return one mask per cell."""
    rgb = np.array(Image.open(path).convert("RGB"))
    ih, iw = rgb.shape[:2]
    ink = ink_mask(rgb)
    n, lab, stats, cent = cv2.connectedComponentsWithStats(grow(ink, MERGE), 8)

    buckets = {}
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] < MIN_AREA:
            continue
        cx, cy = cent[i]
        col = min(cols - 1, int(cx / (iw / cols)))
        row = min(rows - 1, int(cy / (ih / rows)))
        buckets.setdefault(row * cols + col, []).append(i)

    out = {}
    for idx, comps in buckets.items():
        m = np.zeros(ink.shape, np.uint8)
        for i in comps:
            m |= (lab == i).astype(np.uint8)
        out[idx] = (rgb, ink & m)
    return out


def slice_sheet(name, group, captions):
    src = SRC / name
    dest = OUT / group
    dest.mkdir(parents=True, exist_ok=True)
    cells = cells_from_sheet(src)
    made = []
    for idx in sorted(cells):
        cap = captions[idx] if idx < len(captions) else ""
        sub = OVERRIDE.get((group, cap))
        if sub and (ACT2 / sub).exists():
            rgba = finish_single(ACT2 / sub)
            print(f"    cell {idx} ({cap}) replaced by {sub}")
        else:
            rgb, m = cells[idx]
            rgba = die_cut(rgb, m)
        if rgba is None:
            continue
        made.append((idx, cap, rgba))
    miss = [i for i in range(20) if i not in cells]
    print(f"  {name}: {len(made)}/20 cells" + (f"  MISSING {miss}" if miss else ""))
    return made


def finish_single(path):
    rgb = np.array(Image.open(path).convert("RGB"))
    ink = ink_mask(rgb)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(grow(ink, MERGE), 8)
    keep = np.zeros(ink.shape, np.uint8)
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] >= MIN_AREA:
            keep |= (lab == i).astype(np.uint8)
    return die_cut(rgb, ink & keep)


def main(what=None):
    OUT.mkdir(parents=True, exist_ok=True)
    sets = {}

    if what in (None, "sheets"):
        print("sheets:")
        for name, group, caps in SHEETS:
            if not (SRC / name).exists():
                print(f"  !! missing {name}")
                continue
            for idx, cap, rgba in slice_sheet(name, group, caps):
                sets.setdefault(group, []).append((cap, rgba))

    if what in (None, "singles"):
        print("singles:")
        for name, group, cap in SINGLES:
            p = ACT2 / name
            if not p.exists():
                print(f"  !! missing {name}")
                continue
            rgba = finish_single(p)
            if rgba is None:
                print(f"  !! no content in {name}")
                continue
            print(f"  {name}: ok")
            sets.setdefault(group, []).append((cap, rgba))

    manifest = {}
    for group, items in sets.items():
        d = OUT / group
        d.mkdir(parents=True, exist_ok=True)
        for old in d.glob("*.png"):
            old.unlink()
        rows = []
        for i, (cap, rgba) in enumerate(items, 1):
            f = d / f"{i:02d}.png"
            to_canvas(rgba).save(f, "PNG", optimize=True)
            rows.append({"file": f.name, "caption": cap})
        # main + tab images taken from the first sticker in the set
        cap0, first = items[0]
        to_canvas(first, 240, 240, 8).save(d / "main.png", "PNG", optimize=True)
        to_canvas(first, 96, 74, 4).save(d / "tab.png", "PNG", optimize=True)
        manifest[group] = rows
        print(f"{group}: {len(rows)} stickers -> {d}")

    (OUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    total = sum(len(v) for v in manifest.values())
    print(f"TOTAL {total} stickers")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
