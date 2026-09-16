"""Expression variants of each growth stage, so the fish's face tells you what it
needs before you look at the bars.

Only the chibi stages get variants. The adult stage is Fujikin's official mascot
artwork and is never redrawn (manual Article 7).
"""
import json, pathlib, shutil, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen
from cutout import cutout
from PIL import Image

M = "D:/Fuji_Famous/Fujie_Creative/01_character/master_v3_wave.png"
SITE = pathlib.Path("D:/Fuji_Famous/site")
OUT = pathlib.Path("D:/Fuji_Famous/Fujie_Creative/06_game")
ART = SITE / "art"

STAGES = [
    ("larva", str(SITE / "stage_2_larva.png"),
     "a tiny newly hatched sturgeon larva - an oversized rounded head with one large black eye, "
     "a round yolk sac beneath it and a thin wispy transparent tail. It has no snout, no barbels "
     "and no proper fins. Do NOT give it features it does not have."),
    ("fry", str(SITE / "stage_3_fry.png"),
     "a small slim sturgeon fry with a short stubby snout, two tiny barbels, faint ridges along "
     "the back and small swept-back fins."),
    ("young", str(SITE / "stage_4_young.png"),
     "a young sturgeon with a clearly formed long flat snout, four barbels, a full row of rounded "
     "scutes along the back and well-defined swept-back fins."),
]

STATES = [
    ("hungry",
     "HUNGRY and asking to be fed: the eye wide, round and pleading, looking up at the viewer, "
     "mouth open in a hopeful little O as if waiting for food, a small cartoon rumble mark near "
     "the belly and one tiny sparkle of hope in the eye. Endearing, not distressed."),
    ("sleepy",
     "SLEEPY and ready for bed: the eye drooping to a heavy half-lidded slit, a small open-mouthed "
     "yawn, the body sagging and tipped slightly downward, and two or three small pale 'z' shapes "
     "drifting up beside the head. Drowsy and soft."),
    ("bored",
     "BORED and wanting to play: the eye half-lidded and rolled off to one side, the mouth a flat "
     "unimpressed line, the body slouching, and a small puff of a sigh escaping. Deadpan and "
     "faintly grumpy, comic rather than sad."),
    ("sick",
     "UNWELL because the water has gone foul: the eye squeezed into an uncomfortable squint, the "
     "mouth turned down in a queasy wobble, the silver body dulled with a faint sickly green-grey "
     "cast, and two or three murky bubbles drifting past. Off-colour and uncomfortable, but still "
     "cute - never gruesome or distressing."),
]

STYLE = (
    "Match the art style of the attached references EXACTLY: bold dark navy outline, flat cel "
    "shading, polished chrome-silver body with a pale silver belly, crisp white specular "
    "highlights, clean vector-like Japanese mascot illustration.\n"
    "Render on a PURE WHITE background, centred, no text, no logo, no watermark, no cast shadow, "
    "nothing else in the frame.\n"
    "FIN RULE: no legs, no feet, no hands, no fingers. Fins only, swept backward.\n\n"
)

only = set(sys.argv[1:])
for stage, sprite, desc in STAGES:
    for state, mood in STATES:
        name = "face_%s_%s.png" % (stage, state)
        if only and name not in only and stage not in only and state not in only:
            continue
        prompt = (
            STYLE
            + "One attached image is the creature to redraw. It is " + desc + "\n"
            "Redraw THAT EXACT CREATURE: the same body, the same pose, the same angle, the same "
            "size in frame and the same framing as the reference sprite. Change ONLY its "
            "EXPRESSION and mood.\n\n"
            "The new expression: it is " + mood
        )
        dest = str(OUT / name)
        r = gen(prompt, dest, refs=[M, sprite], aspect="1:1")
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
        print(json.dumps({"out": name, "ok": ok,
                          "err": "" if ok else r.get("error", "")[:140]}), flush=True)
print("DONE", flush=True)
