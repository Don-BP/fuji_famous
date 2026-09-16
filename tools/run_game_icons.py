"""Replace the emoji in the care bar with real icons in the game's own style."""
import json, pathlib, shutil, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen
from cutout import cutout
from PIL import Image

M = "D:/Fuji_Famous/Fujie_Creative/01_character/master_v3_wave.png"
OUT = pathlib.Path("D:/Fuji_Famous/Fujie_Creative/06_game/")
SITE = pathlib.Path("D:/Fuji_Famous/site/art/")

STYLE = (
    "A single clean mobile-game UI ICON in the style of the attached reference: bold dark navy "
    "outline, flat cel shading, polished chrome-silver and cool cyan surfaces, crisp white "
    "specular highlights, simple and instantly readable at small size.\n"
    "*** DRAW THE OBJECT ONLY. NO FISH, NO CHARACTER, NO FACE, NO EYES, NO TEXT. ***\n"
    "Render on a PURE WHITE background, centred, filling most of the frame, no cast shadow, "
    "nothing else in the frame.\n\n"
)

JOBS = [
    (STYLE + "Subject: a small heap of fish feed - a scatter of pale amber-brown pellets and two "
     "tiny pink shrimp, piled together in a neat mound.", "ico_feed.png"),
    (STYLE + "Subject: a game controller rendered as a chunky chrome-silver toy with cyan "
     "buttons, tilted at a jaunty three-quarter angle, with two small white sparkles beside it.",
     "ico_play.png"),
    (STYLE + "Subject: a crescent moon in pale silver-cream with three small rounded 'z' shapes "
     "rising from it in cyan, arranged diagonally.", "ico_sleep.png"),
    (STYLE + "Subject: a precision stainless steel valve handwheel seen at a slight three-quarter "
     "angle - a polished spoked circular wheel on a short hexagonal valve body, with a small cyan "
     "indicator band. Industrial, precise and premium.", "ico_flow.png"),
]

for prompt, name in JOBS:
    dest = str(OUT / name)
    r = gen(prompt, dest, refs=[M], aspect="1:1")
    ok = not isinstance(r, dict)
    if ok:
        cutout(dest)
        im = Image.open(dest)
        s = 220 / max(im.size)
        im = im.resize((round(im.width*s), round(im.height*s)), Image.LANCZOS)
        im.convert("RGBA").quantize(colors=180, method=Image.FASTOCTREE).save(
            dest, "PNG", optimize=True)
        shutil.copy(dest, SITE / name)
    print(json.dumps({"out": name, "ok": ok}), flush=True)
print("DONE", flush=True)
