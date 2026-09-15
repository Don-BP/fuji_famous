import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen

M = "D:/Fuji_Famous/Fujie_Creative/01_character/master_v3_wave.png"

STYLE = (
    "The attached image is the locked master design of 'Chibi Fujie', a cute chrome-silver sturgeon "
    "mascot. Match its exact art style: bold dark navy outline, flat cel shading, polished "
    "chrome-silver body with a pale silver belly, crisp white specular highlights, one large glossy "
    "black eye with a bright white catchlight.\n\n"
    "FIN RULE: no legs, no feet, no toes, no stumps. Fins only - pectoral fins at the sides and "
    "pelvic fins near the tail, all thin, flat, leaf-shaped and SWEPT BACKWARD along the body, "
    "never pointing downward and never supporting weight.\n\n"
    "Render on a PURE WHITE background, centred, full body, facing left, no text, no logo, "
    "no watermark, no shadow.\n\n"
)

JOBS = [
    (STYLE + "Draw a juvenile sturgeon FRY: a small slender silver fish, clearly a younger and "
     "thinner version of the master character. The snout is only partly formed into a short point, "
     "the barbel whiskers are tiny, the scute bumps along the back are just beginning to appear as "
     "faint soft ridges, the fins are small and delicate. Big eye relative to the small body. "
     "Fragile and endearing.",
     "stage_3_fry.png"),
    (STYLE + "Draw a YOUNG ADULT version of the master character: noticeably longer and sleeker than "
     "the chibi, with a fully formed long flat snout, four clear barbel whiskers, a complete row of "
     "scute bumps along the back, well-defined swept-back fins and a strong crescent tail. "
     "Confident forward-gliding pose. Halfway between the cute chibi and a real adult sturgeon.",
     "stage_4_young.png"),
]

OUT = "D:/Fuji_Famous/Fujie_Creative/04_campaign/"
for prompt, name in JOBS:
    r = gen(prompt, OUT + name, refs=[M], aspect="1:1")
    print(json.dumps({"out": name, "ok": not isinstance(r, dict)}, ensure_ascii=False), flush=True)
