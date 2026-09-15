import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen

M = "D:/Fuji_Famous/Fujie_Creative/01_character/master_v2_float.png"

STYLE = (
    "The attached image is the locked master design of 'Chibi Fujie', a cute chrome-silver sturgeon "
    "mascot. Match its exact art style: bold dark navy outline, flat cel shading, polished "
    "chrome-silver body with a pale silver belly, crisp white specular highlights, one large glossy "
    "black eye with a bright white catchlight.\n\n"
    "ABSOLUTE RULE: no legs, no feet, no toes. Fins only - two pectoral fins at the sides, a dorsal "
    "fin, and a tail fin.\n\n"
    "Render on a PURE WHITE background, centred, full body, no text, no logo, no watermark, no "
    "shadow. Simple and clean so it can be cut out.\n\n"
)

JOBS = [
    (STYLE + "Draw a single sturgeon EGG: a small glossy dark-grey sphere with a soft pearlescent "
     "sheen and a faint pale highlight, like a single grain of caviar. Simple, round, no face.",
     "stage_1_egg.png"),
    (STYLE + "Draw a newly hatched sturgeon LARVA in the chibi style: a tiny, delicate, almost "
     "translucent silver tadpole-like creature with an oversized head, a large round black eye with "
     "a white catchlight, a visible rounded yolk sac under its belly, and a thin wispy tail. Very "
     "small and fragile-looking, no snout yet, no scutes yet.",
     "stage_2_larva.png"),
    (STYLE + "Draw a juvenile sturgeon FRY in the chibi style: a small slender silver fish with the "
     "snout just beginning to form into a short point, tiny soft barbel whiskers, the first faint "
     "row of soft scute bumps along the back, small pectoral fins, and one large black eye with a "
     "white catchlight. Clearly a younger, thinner, less developed version of the master character.",
     "stage_3_fry.png"),
    (STYLE + "Draw a YOUNG ADULT version of the master character: the same chibi Fujie but noticeably "
     "longer and sleeker, with a fully formed long flat snout, four clear barbel whiskers, a complete "
     "row of scute bumps along the back, well-defined pectoral fins and a strong crescent tail. "
     "Confident forward-swimming pose. Halfway between the cute chibi and a real adult sturgeon.",
     "stage_4_young.png"),
    (STYLE + "Draw the master character celebrating: floating joyfully with both pectoral fins raised "
     "high, eye squeezed shut in a huge happy smile, surrounded by small white sparkle marks. "
     "Triumphant and delighted.",
     "stage_5_celebrate.png"),
]

OUT = "D:/Fuji_Famous/Fujie_Creative/04_campaign/"
for prompt, name in JOBS:
    r = gen(prompt, OUT + name, refs=[M], aspect="1:1")
    print(json.dumps({"out": name, "ok": not isinstance(r, dict)}, ensure_ascii=False), flush=True)
