import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen

M = "D:/Fuji_Famous/Fujie_Creative/01_character/master_v2_float.png"
ORIG = "D:/Fuji_Famous/Documents_for_dev/05_fujie_絵柄例.png"

BASE = (
    "The first attached image is the official Fujikin sturgeon mascot (anatomy reference). The second "
    "is the chibi version. Redraw the chibi version with ONE correction to the fins.\n\n"
    "KEEP IDENTICAL: polished chrome-silver body, pale silver belly, long flat pointed snout, four "
    "barbel whiskers under the snout, a row of rounded scute bumps along the back, one large glossy "
    "black eye with a bright white catchlight, crescent tail fin, bold dark navy outline, flat cel "
    "shading with crisp white specular highlights, cheerful friendly smile.\n\n"
    "*** FIN CORRECTION - THIS IS THE WHOLE POINT OF THE REDRAW ***\n"
    "The character has a pair of small PELVIC FINS on the underside toward the rear, as a real "
    "sturgeon does. They must be unmistakably FINS, never legs or feet:\n"
    "- thin and flat, leaf-shaped, tapering to a soft point\n"
    "- lying close against the lower flank of the body\n"
    "- SWEPT BACKWARD toward the tail at a shallow angle, trailing as if gliding through water\n"
    "- NEVER pointing downward, NEVER stubby or rounded, NEVER stumpy nubs, NEVER touching any "
    "ground, NEVER supporting the body's weight\n"
    "The same applies to the two pectoral fins at the front: thin, flat and fin-shaped, swept back "
    "along the sides. Nothing on this character may read as a leg, a foot, a toe or a stump. "
    "The belly line stays smooth and continuous.\n\n"
    "Pure white background, full body, centred, no text, no logo, no shadow.\n\n"
)

JOBS = [
    (BASE + "POSE: gliding forward through water, body level and streamlined, head slightly raised, "
     "pectoral fins swept back along the sides, pelvic fins trailing behind them near the tail. "
     "Serene and elegant.",
     "master_v3_glide.png"),
    (BASE + "POSE: floating cheerfully with the body angled slightly upward and the tail curving "
     "behind, one pectoral fin lifted in a friendly wave while the other rests along the flank, "
     "pelvic fins trailing back near the tail. Warm and welcoming.",
     "master_v3_wave.png"),
]

OUT = "D:/Fuji_Famous/Fujie_Creative/01_character/"
for prompt, name in JOBS:
    r = gen(prompt, OUT + name, refs=[ORIG, M], aspect="1:1")
    print(json.dumps({"out": name, "ok": not isinstance(r, dict)}, ensure_ascii=False), flush=True)
