"""Redo the larva and young expressions.

First pass drifted: passing the upright chibi master as a reference pulled both
stages into that silhouette, so a larva looked like a fry and the slim gliding
young looked like a chibi. This pass references ONLY the stage's own sprite and
locks the pose explicitly.
"""
import json, pathlib, shutil, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen
from cutout import cutout
from PIL import Image

SITE = pathlib.Path("D:/Fuji_Famous/site")
OUT = pathlib.Path("D:/Fuji_Famous/Fujie_Creative/06_game")
ART = SITE / "art"

STAGES = [
    ("larva", str(SITE / "stage_2_larva.png"),
     "*** POSE LOCK - THIS IS NOT THE UPRIGHT CHIBI MASCOT ***\n"
     "The attached creature is a tiny newly hatched sturgeon LARVA. It lies on its side, "
     "roughly HORIZONTAL, with an oversized rounded head, ONE large dark eye, a big round pale "
     "yellow YOLK SAC bulging under the head, and a thin wispy semi-transparent tail trailing "
     "behind. It has NO snout, NO barbel whiskers, NO scutes along the back, and NO proper fins "
     "- only faint buds. It is small, fragile and newborn.\n"
     "Do NOT stand it upright. Do NOT give it a long snout, whiskers, back bumps or arm-like "
     "fins. Do NOT make it look like a older fish. Keep the yolk sac and the wispy tail."),
    ("young", str(SITE / "stage_4_young.png"),
     "*** POSE LOCK - THIS IS NOT THE UPRIGHT CHIBI MASCOT ***\n"
     "The attached creature is a young sturgeon drawn HORIZONTALLY, gliding level and facing "
     "left, with a long slim streamlined body. It has a long flat paddle snout, four barbels "
     "beneath it, a full row of rounded scutes along the back, swept-back pectoral fins held "
     "close to the body and a crescent tail.\n"
     "Do NOT stand it upright. Do NOT make it short, round or chubby. Do NOT raise its fins like "
     "arms. Keep the exact same horizontal gliding pose, the same slim proportions, the same "
     "body length and the same size in frame."),
]

STATES = [
    ("hungry",
     "HUNGRY and asking to be fed: the eye wide, round and pleading, mouth open in a hopeful "
     "little O as if waiting for food, a small cartoon rumble mark near the belly. Endearing."),
    ("sleepy",
     "SLEEPY: the eye drooping to a heavy half-lidded slit, a small yawn, the body sagging and "
     "tipped slightly downward, and two or three small pale 'z' shapes drifting up beside the "
     "head. Drowsy and soft."),
    ("bored",
     "BORED and wanting to play: the eye half-lidded and rolled off to one side, the mouth a "
     "flat unimpressed line, the body slouching, and a small puff of a sigh. Deadpan and comic."),
    ("sick",
     "UNWELL because the water has gone foul: the eye squeezed into an uncomfortable squint, the "
     "mouth turned down in a queasy wobble, the silver body dulled with a faint sickly green-grey "
     "cast, and a few murky bubbles drifting past. Off-colour but still cute."),
]

STYLE = (
    "Match the art style of the attached image EXACTLY: bold dark navy outline, flat cel shading, "
    "polished chrome-silver body with a pale silver belly, crisp white specular highlights, clean "
    "vector-like Japanese mascot illustration.\n"
    "Render on a PURE WHITE background, centred, no text, no logo, no watermark, no cast shadow, "
    "nothing else in the frame.\n\n"
)

only = set(sys.argv[1:])
for stage, sprite, lock in STAGES:
    if only and stage not in only:
        continue
    for state, mood in STATES:
        name = "face_%s_%s.png" % (stage, state)
        prompt = (
            STYLE + lock + "\n\n"
            "Redraw THAT EXACT CREATURE in THAT EXACT POSE at the same size in frame. Change "
            "ONLY its expression and mood.\n\n"
            "The new expression: it is " + mood
        )
        dest = str(OUT / name)
        r = gen(prompt, dest, refs=[sprite], aspect="1:1")
        ok = not isinstance(r, dict)
        if ok:
            cutout(dest)
            im = Image.open(dest)
            if max(im.size) > 700:
                s = 700 / max(im.size)
                im = im.resize((round(im.width*s), round(im.height*s)), Image.LANCZOS)
            im.convert("RGBA").quantize(colors=200, method=Image.FASTOCTREE).save(
                dest, "PNG", optimize=True)
            shutil.copy(dest, ART / name)
        print(json.dumps({"out": name, "ok": ok}), flush=True)
print("DONE", flush=True)
