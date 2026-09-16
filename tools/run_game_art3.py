"""Third pass: a painted plate behind every remaining screen, plus the two
emotional reaction sprites for the win and loss endings.

Covers the raising (tank) screen at two life stages, the mini-game result, the
1992 loss, the win, and the modal sheets.
"""
import json, pathlib, shutil, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen
from cutout import cutout
from PIL import Image

CHAR = "D:/Fuji_Famous/Fujie_Creative/01_character/"
M = CHAR + "master_v3_wave.png"
OUT = pathlib.Path("D:/Fuji_Famous/Fujie_Creative/06_game/")
SITE = pathlib.Path("D:/Fuji_Famous/site/art/")

BG = (
    "A painterly vertical background plate for a Japanese mobile game. Palette locked to dark "
    "teal and navy: #04121A, #07202B, #103544, #1D5566, with cool cyan #3FB6EE light accents and "
    "pale silver #BFCFD6 highlights. Soft, atmospheric, gentle vignette toward the edges so "
    "bright UI text stays readable on top.\n"
    "ABSOLUTE RULES: NO characters. NO fish. NO creatures. NO people. NO text, letters, numbers, "
    "logos, watermarks or UI elements. Empty scenery only. The middle of the frame must stay "
    "visually calm, dark and uncluttered so a character and body text sit on top of it.\n\n"
)

SPR = (
    "Match the art style of the attached reference character EXACTLY: bold dark navy outline, "
    "flat cel shading, polished chrome-silver body with a pale silver belly, crisp white specular "
    "highlights, clean vector-like Japanese mascot illustration. Long flat paddle snout, four "
    "barbel whiskers, a row of rounded scute bumps along the back, one large round eye.\n"
    "FIN RULE - ABSOLUTE: no legs, no feet, no hands, no fingers. Fins only, thin and swept back.\n"
    "Render on a PURE WHITE background, centred, no text, no logo, no watermark, no cast shadow, "
    "nothing else in the frame.\n\n"
)

JOBS = [
    # ---------- the raising screen, early and late ----------
    (BG + "Scene: the inside of a small, dim indoor aquaculture hatchery tank, seen through the "
     "water. Smooth pale concrete tank walls curve away at the far left and right edges. A single "
     "soft overhead lamp throws a narrow pool of cool light down through the water into darkness "
     "below. A slender stainless steel inlet pipe enters high at one side with a faint stream of "
     "fine bubbles rising from it. Quiet, clinical, protective. The whole centre of the frame is "
     "open dark water.",
     "bg_tank_early.png", None, "3:4", False),
    (BG + "Scene: the inside of a large, deep indoor aquaculture rearing tank, seen through the "
     "water. Broad pale concrete walls fall away into deep blue-green water. Several bright cool "
     "light panels above cast wide overlapping pools of light and soft rippling caustics down the "
     "walls. A bank of polished stainless steel pipes and valve fittings runs along the upper "
     "right edge. Streams of fine bubbles drift up the sides. Spacious and hopeful. The centre of "
     "the frame is wide open water.",
     "bg_tank_grown.png", None, "3:4", False),

    # ---------- result / endings / modals ----------
    (BG + "Scene: gentle open water lit from above, with a soft cyan glow spreading outward from "
     "the middle of the frame and a slow drift of small bright bubbles and tiny light motes rising "
     "through it. Calm, warm and congratulatory. Nothing solid in the scene at all.",
     "bg_result.png", None, "3:4", False),
    (BG + "Scene: a cold, empty, abandoned hatchery tank at night. Bare pale concrete walls, "
     "still black water with no bubbles and no movement, a fine layer of silt settled on the "
     "floor, and one weak failing overhead lamp throwing a small dim circle of light. Deeply "
     "quiet, sombre and still. Much darker and emptier than the other plates.",
     "bg_lost.png", None, "3:4", False),
    (BG + "Scene: looking up through clear open river water toward a bright rippling surface high "
     "above, broad golden-cyan shafts of morning light pouring down through it, a rising column "
     "of silver bubbles, and a scatter of glittering light motes. Bright, expansive and "
     "triumphant - the brightest plate in the set. No solid objects.",
     "bg_win.png", None, "3:4", False),
    (BG + "Scene: a very simple, very dark abstract underwater texture - near-black deep water "
     "with faint slow-moving currents, a soft cyan glow bleeding in from the top edge only, and a "
     "few small far-off bubbles. Almost empty, deliberately plain and unobtrusive, meant to sit "
     "behind a dialogue panel. No detail in the centre at all.",
     "bg_sheet.png", None, "3:4", False),

    # ---------- ending reaction sprites ----------
    (SPR + "Subject: this character in deep quiet SADNESS, for a story beat about a fish that did "
     "not survive. Small and hunched, curled slightly in on itself, head lowered, the eye closed "
     "or downcast with a single fat tear welling at the corner, mouth a small downward curve, "
     "fins drooping limply against the body, tail hanging low. Gentle and moving, not gruesome "
     "and not comic. Full body, seen in three-quarter view.",
     "fujie_sad.png", [M], "1:1", True),
    (SPR + "Subject: this character CHEERING with delight. Body tilted back mid-bounce, both "
     "pectoral fins thrown up and outward in celebration, eye squeezed shut into a happy curve, "
     "mouth wide open in a joyful shout, cheeks lifted. A ring of white four-point sparkle stars "
     "and a few confetti flecks burst around it. Bright and energetic. Full body.",
     "fujie_cheer.png", [M], "1:1", True),
]

only = set(sys.argv[1:])
for prompt, name, refs, aspect, sprite in JOBS:
    if only and name not in only:
        continue
    dest = str(OUT / name)
    r = gen(prompt, dest, refs=refs, aspect=aspect)
    ok = not isinstance(r, dict)
    if ok:
        if sprite:
            cutout(dest)
            im = Image.open(dest)
            if max(im.size) > 700:
                s = 700 / max(im.size)
                im = im.resize((round(im.width*s), round(im.height*s)), Image.LANCZOS)
            im.convert("RGBA").quantize(colors=200, method=Image.FASTOCTREE).save(
                dest, "PNG", optimize=True)
            shutil.copy(dest, SITE / name)
        else:
            im = Image.open(dest)
            if max(im.size) > 1100:
                s = 1100 / max(im.size)
                im = im.resize((round(im.width*s), round(im.height*s)), Image.LANCZOS)
            im.convert("RGB").save(str(SITE / name.replace(".png", ".jpg")),
                                   "JPEG", quality=82, optimize=True, progressive=True)
    print(json.dumps({"out": name, "ok": ok,
                      "err": "" if ok else r.get("error", "")[:160]}, ensure_ascii=False),
          flush=True)
print("DONE", flush=True)
