"""Second pass of game art: reaction sprites and the sea-urchin hazard.

Each sprite is framed to match the sprite it swaps with, so the swap reads as a
change of expression rather than a jump cut.
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

SHELL = str(OUT / "fujie_shell.png")
SHARK = str(OUT / "shark_pop.png")
WHACK = str(OUT / "fujie_whack.png")

STYLE = (
    "Match the art style of the attached references EXACTLY: bold dark navy outline, flat cel "
    "shading, polished chrome-silver surfaces with a pale silver belly, crisp white specular "
    "highlights and small white sparkle stars, clean vector-like Japanese mascot illustration.\n"
    "Render on a PURE WHITE background, centred, no text, no logo, no watermark, no cast shadow, "
    "nothing else in the frame.\n\n"
)

FINS = (
    "FIN RULE - ABSOLUTE: no legs, no feet, no hands, no fingers. The character has fins only, "
    "thin and swept backward along the body.\n"
)

JOBS = [
    (
        STYLE + FINS
        + "One attached image is the character holding an open scallop shell like a bowl. Redraw "
        "THAT EXACT SPRITE - the same body angle, the same framing, the same size in frame, the "
        "same shell held in the same place - and change ONLY the expression to pure delight: the "
        "eye squeezed shut into a happy upward curve, mouth open in a big joyful grin, cheeks "
        "lifted, head tipped back slightly. Add a scatter of white four-point sparkle stars and "
        "two or three small golden sturgeon eggs tumbling down into the shell. Everything else is "
        "identical to the reference sprite.",
        "fujie_shell_happy.png", [M, SHELL], "1:1",
    ),
    (
        STYLE
        + "One attached image is a comic cartoon shark bursting up out of the water toward the "
        "viewer. Redraw THAT EXACT SHARK in the same framing, the same size and the same pose, but "
        "just after being whacked on the head: both eyes screwed shut into tight X shapes, mouth "
        "pulled into a pained lopsided 'ouch' grimace showing gritted teeth, a small round red "
        "bump on top of its head, both pectoral fins flung outward, a ring of little yellow "
        "cartoon stars and birds circling above its head, and a couple of comic pain marks. Dazed "
        "and funny, not gory. It is clearly a SHARK: short blunt snout, no long paddle snout, no "
        "barbel whiskers, no scute bumps.",
        "shark_hurt.png", [M, SHARK], "1:1",
    ),
    (
        STYLE
        + "*** DRAW A SEA URCHIN. NO FISH. NO SHARK. NO SNOUT. ***\n"
        "Subject: a spiky SEA URCHIN rising up out of the water toward the viewer, framed exactly "
        "like the attached shark sprite - seen from the front and slightly above, body cut off at "
        "the bottom of the frame as if still emerging, with a small water splash around its base. "
        "A round dark plum-purple and near-black glossy shell completely covered in long, sharp, "
        "menacing black spines radiating outward in every direction. Two small round glaring white "
        "eyes with narrowed angry pupils on the front of the shell and a tiny scowling mouth. It "
        "looks spiky and dangerous - something you would NOT want to hit. Bold dark navy outline, "
        "flat cel shading, sharp white highlights on the spine tips.",
        "urchin.png", [M, SHARK], "1:1",
    ),
    (
        STYLE + FINS
        + "One attached image is the character in an annoyed, fired-up pose with a fin raised. "
        "Redraw THAT EXACT CHARACTER in the same framing and the same size in frame, but now in "
        "comic PAIN: recoiling backwards, the raised fin now clutched against the body, the eye "
        "screwed tightly shut, mouth wide open in a yelp, a fat cartoon tear squeezing out, a "
        "throbbing red pain mark near the hurt fin and a few motion lines. Funny and exaggerated, "
        "not distressing.",
        "fujie_ouch.png", [M, WHACK], "1:1",
    ),
    (
        STYLE
        + "*** DRAW ONLY AN IMPACT EFFECT. NO CHARACTER, NO CREATURE, NO FACE, NO EYES. ***\n"
        "Subject: a single comic-book IMPACT STARBURST - a jagged spiky explosion shape radiating "
        "out from the centre, filled with bright white fading to pale cyan at the edges, with a "
        "bold dark navy outline, and a scatter of small white four-point sparkle stars flying "
        "outward around it. Flat, graphic and punchy, like a manga hit effect. Centred and alone.",
        "hit_burst.png", [M], "1:1",
    ),
]

SPRITE_MAX = 700
only = set(sys.argv[1:])
for prompt, name, refs, aspect in JOBS:
    if only and name not in only:
        continue
    dest = str(OUT / name)
    r = gen(prompt, dest, refs=refs, aspect=aspect)
    ok = not isinstance(r, dict)
    if ok:
        cutout(dest)
        im = Image.open(dest)
        if max(im.size) > SPRITE_MAX:
            s = SPRITE_MAX / max(im.size)
            im = im.resize((round(im.width*s), round(im.height*s)), Image.LANCZOS)
        im.convert("RGBA").quantize(colors=200, method=Image.FASTOCTREE).save(
            dest, "PNG", optimize=True)
        shutil.copy(dest, SITE / name)
    print(json.dumps({"out": name, "ok": ok,
                      "err": "" if ok else r.get("error", "")[:160]}, ensure_ascii=False),
          flush=True)
print("DONE", flush=True)
