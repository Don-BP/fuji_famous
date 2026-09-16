"""Widescreen versions of every painted background plate.

The originals were drawn portrait, for a phone. On a desktop window the game now
runs edge to edge, so a portrait plate has to be cropped to a letterbox strip and
scaled up about twice - soft, and most of the painting thrown away.

Each existing plate is handed back to the model as the reference and re-painted
as the same scene in 16:9, then written next to the original as <name>_wide.jpg.
The game picks the wide plate above 1100px and the portrait one below it.
"""
import json, pathlib, sys
from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen

SITE = pathlib.Path(r"D:\Fuji_Famous\site\art")
MASTER = pathlib.Path(r"D:\Fuji_Famous\Fujie_Creative\06_game")
WIDE = MASTER / "wide"
WIDE.mkdir(parents=True, exist_ok=True)

OUT_W, Q = 1600, 80

PLATES = ["bg_tank_early", "bg_tank_grown", "bg_egg", "bg_shark", "bg_race",
          "bg_shell", "bg_result", "bg_lost", "bg_win", "bg_title", "bg_sheet"]

PROMPT = (
    "The attached image is an existing painted background plate from a Japanese mobile game, "
    "drawn in a tall portrait frame.\n\n"
    "Re-paint the SAME SCENE as a WIDESCREEN 16:9 plate. Same place, same subject, same palette, "
    "same light sources, same mood, same painterly brushwork and the same level of detail. Extend "
    "the scene outward to the left and right so it fills the wider frame naturally, as though the "
    "original painting had always been wider - do not crop it, do not stretch it, do not add a "
    "border, and do not invent a different location.\n\n"
    "Palette stays locked to dark teal and navy - #04121A, #07202B, #103544, #1D5566 - with cool "
    "cyan #3FB6EE light accents and pale silver #BFCFD6 highlights. Keep a gentle vignette toward "
    "the edges.\n\n"
    "ABSOLUTE RULES: NO characters. NO fish. NO creatures. NO people. NO text, letters, numbers, "
    "logos, watermarks or UI elements. Empty scenery only. The middle of the frame must stay "
    "calm, dark and uncluttered, because a character and body text sit on top of it.\n"
)


def publish(src, name):
    im = Image.open(src).convert("RGB")
    if im.width > OUT_W:
        im = im.resize((OUT_W, round(im.height * OUT_W / im.width)), Image.LANCZOS)
    dest = SITE / (name + "_wide.jpg")
    im.save(dest, "JPEG", quality=Q, optimize=True, progressive=True)
    print("   -> %-24s %dx%d  %.0f KB" % (dest.name, im.width, im.height,
                                          dest.stat().st_size / 1024))


for name in PLATES:
    ref = MASTER / (name + ".png")
    if not ref.exists():
        ref = SITE / (name + ".jpg")
    if not ref.exists():
        print("  ! no source for", name)
        continue
    target = WIDE / (name + ".png")
    r = gen(PROMPT, str(target), refs=[str(ref)], aspect="16:9")
    ok = not isinstance(r, dict)
    print(json.dumps({"plate": name, "ok": ok}, ensure_ascii=False), flush=True)
    if ok and target.exists():
        publish(target, name)
