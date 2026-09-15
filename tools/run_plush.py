import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen

M = "D:/Fuji_Famous/Fujie_Creative/01_character/master_v2_float.png"

LOCK = (
    "The attached image is the LOCKED master design of 'Chibi Fujie' (chibi Fujie), the cute young "
    "form of Fujikin's sturgeon mascot. Reproduce this EXACT character: polished chrome-silver body, "
    "pale silver belly, long flat pointed snout, four barbel whiskers under the snout, a row of "
    "rounded scute bumps along the back, one large glossy black eye with a bright white catchlight, "
    "crescent tail fin.\n\n"
    "*** ABSOLUTE RULE: NO LEGS, NO FEET, NO TOES, NO STANDING NUBS. IT IS A FISH. ***\n"
    "The only appendages are two soft pectoral fins on the sides, one dorsal fin on the back, and "
    "the crescent tail fin. The underside is a smooth continuous rounded belly with nothing "
    "protruding downward. It never stands upright on anything. It rests on its belly.\n\n"
)

PLUSH = (
    LOCK
    + "Create a PHOTOREALISTIC PRODUCT PHOTOGRAPH of this character manufactured as a real Japanese "
    "plush toy. Silver-grey short-pile velboa plush with a pearlescent sheen, pale ivory-silver "
    "belly panel, the long flat snout firmly stuffed and sewn, four soft cord barbel whiskers, the "
    "back scutes as small padded quilted bumps along a raised spine seam, one large glossy black "
    "embroidered eye with a white satin-stitch catchlight, soft sewn pectoral fins, a dorsal fin and "
    "a crescent tail, visible high-quality stitching and seams, a small woven fabric tag near the "
    "tail. The plush has NO legs and NO feet whatsoever - it lies on its smooth rounded belly like a "
    "fish. Premium Japanese character-goods quality. No text or logo on the plush.\n\n"
)

JOBS = [
    (
        LOCK + "Produce a CHARACTER TURNAROUND MODEL SHEET on a clean white background: the same "
        "character five times in one horizontal row, evenly spaced, identical size and eye level - "
        "front view, three-quarter front, full side profile facing right, three-quarter rear, and "
        "back view. Neutral friendly floating pose in every view, fins relaxed. Thin light-grey "
        "horizontal guide lines at the top of the head, the eye line, and the base of the body. "
        "No text, no labels, no watermark.",
        "D:/Fuji_Famous/Fujie_Creative/01_character/master_turnaround.png", "16:9",
    ),
    (
        PLUSH + "Studio product photograph on a seamless pure white background, soft even three-point "
        "lighting, gentle contact shadow. The plush lies on its belly facing the camera at a slight "
        "three-quarter angle with its head lifted cheerfully, centred, filling the frame. Crisp "
        "commercial e-commerce product shot.",
        "D:/Fuji_Famous/Fujie_Creative/03_plushie/plush_studio_front.png", "1:1",
    ),
    (
        PLUSH + "Photograph of the plush cradled in an adult's two open hands against a softly "
        "blurred warm neutral background, natural window light. Shows it is about 25cm long, "
        "palm-sized and huggable. Shallow depth of field, warm inviting lifestyle photography.",
        "D:/Fuji_Famous/Fujie_Creative/03_plushie/plush_in_hands.png", "4:3",
    ),
    (
        PLUSH + "Product family photograph on a clean light-grey studio background: three sizes of "
        "the same plush resting on their bellies in a neat row, smallest to largest - a 10cm keychain "
        "version with a metal ball-chain clip, a 25cm version, and a 50cm huggable version. Even "
        "lighting, commercial catalogue arrangement.",
        "D:/Fuji_Famous/Fujie_Creative/03_plushie/plush_size_lineup.png", "16:9",
    ),
    (
        PLUSH + "Lifestyle photograph: the 10cm keychain version clipped to the strap of a commuter's "
        "bag, photographed close up on a Japanese train platform, soft bokeh background, natural "
        "daylight. Warm everyday Japanese character-goods photography.",
        "D:/Fuji_Famous/Fujie_Creative/03_plushie/plush_keychain_lifestyle.png", "3:4",
    ),
]

for prompt, out, aspect in JOBS:
    r = gen(prompt, out, refs=[M], aspect=aspect)
    print(json.dumps({"out": out, "ok": not isinstance(r, dict)}, ensure_ascii=False), flush=True)
