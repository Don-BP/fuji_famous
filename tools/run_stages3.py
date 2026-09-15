import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen
from cutout import cutout

M = "D:/Fuji_Famous/Fujie_Creative/01_character/master_v3_wave.png"

STYLE = (
    "Match the art style of the attached reference exactly: bold dark navy outline, flat cel "
    "shading, polished chrome-silver surfaces with a pale silver belly, crisp white specular "
    "highlights, clean vector-like Japanese mascot illustration.\n"
    "Render on a PURE WHITE background, centred, no text, no logo, no watermark, no shadow, "
    "nothing else in the frame.\n\n"
)

JOBS = [
    (
        STYLE
        + "*** DRAW ONLY A SINGLE EGG. DO NOT DRAW A FISH. DO NOT DRAW A CHARACTER, A FACE, AN EYE, "
        "A MOUTH, FINS OR A TAIL. THE FRAME CONTAINS EXACTLY ONE SPHERE AND NOTHING ELSE. ***\n"
        "Subject: one sturgeon egg - a single smooth glossy dark charcoal-grey sphere, like one "
        "large grain of caviar, with a soft pearlescent sheen and one crisp white highlight near "
        "the upper left. Perfectly round. Centred. Alone.",
        "stage_1_egg.png",
    ),
    (
        STYLE
        + "*** THIS IS A NEWLY HATCHED LARVA, NOT THE ADULT MASCOT. IT MUST LOOK TINY, FRAGILE AND "
        "UNDERDEVELOPED - NOT CUTE AND CHUBBY. NO LONG SNOUT. NO BARBEL WHISKERS. NO SCUTE BUMPS. ***\n"
        "Subject: a just-hatched sturgeon larva - a very small, delicate, semi-translucent pale "
        "silver tadpole-like creature. An oversized rounded head with one large black eye, a "
        "prominent round yolk sac bulging beneath the head, and a thin wispy transparent tail "
        "trailing behind. No proper fins yet, only faint fin buds. The head is blunt and rounded "
        "with no snout at all. It looks newborn and vulnerable.",
        "stage_2_larva.png",
    ),
    (
        STYLE
        + "*** THIS IS A SMALL JUVENILE FRY, CLEARLY YOUNGER AND THINNER THAN THE ADULT MASCOT. ***\n"
        "Subject: a sturgeon fry - a small slim silver fish with a short stubby snout that is only "
        "beginning to form, two tiny barbel whiskers, the first faint soft ridges along the back "
        "where the scutes will grow, small delicate swept-back fins, and one large black eye with a "
        "white catchlight that looks oversized on its small body. Slender and youthful, not chubby. "
        "Swimming level, facing left.\n"
        "FIN RULE: no legs, no feet. Fins only, thin and swept backward along the body.",
        "stage_3_fry.png",
    ),
    (
        STYLE
        + "*** THIS IS AN ADOLESCENT, BETWEEN THE FRY AND THE ADULT MASCOT. ***\n"
        "Subject: a young sturgeon - longer and more developed than a fry but not yet the full "
        "adult. The long flat snout is now clearly formed, four barbel whiskers hang beneath it, a "
        "full row of rounded scute bumps runs along the back, and the swept-back pectoral and "
        "pelvic fins and crescent tail are all well defined. Sleek and streamlined rather than "
        "chubby. Gliding forward, facing left.\n"
        "FIN RULE: no legs, no feet. Fins only, thin and swept backward along the body.",
        "stage_4_young.png",
    ),
]

OUT = "D:/Fuji_Famous/Fujie_Creative/04_campaign/"
for prompt, name in JOBS:
    r = gen(prompt, OUT + name, refs=[M], aspect="1:1")
    ok = not isinstance(r, dict)
    if ok:
        cutout(OUT + name)
    print(json.dumps({"out": name, "ok": ok}, ensure_ascii=False), flush=True)

# adult stage = the master, cut out
import shutil
shutil.copy(M, OUT + "master.png")
cutout(OUT + "master.png")
print("ALL DONE", flush=True)
