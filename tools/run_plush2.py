"""The plush line, widened - six more of the original, then the Fuji versions.

Every shot is given the existing studio photograph as its first reference, so
the new pieces are the SAME toy rather than a new one: same velboa, same seams,
same embroidered eye. The Fuji set adds the mountain as a companion piece - a
knitted cap, a cushion, a backdrop - and never repaints the fish.

Output: Fujie_Creative/03_plushie/  and  Fujie_Creative/19_fujisan/plush/
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen

PLUSH_REF = "D:/Fuji_Famous/Fujie_Creative/03_plushie/plush_studio_front.png"
LINEUP = "D:/Fuji_Famous/Fujie_Creative/03_plushie/plush_size_lineup.png"
MASTER = "D:/Fuji_Famous/Fujie_Creative/01_character/master_v3_wave.png"
OUT = "D:/Fuji_Famous/Fujie_Creative/03_plushie/"
FOUT = "D:/Fuji_Famous/Fujie_Creative/19_fujisan/plush/"
pathlib.Path(FOUT).mkdir(parents=True, exist_ok=True)

LOCK = (
    "The attached photograph is the EXISTING 'Chibi Fujie' PLUSH TOY. Every shot below shows THIS "
    "SAME manufactured toy - do not redesign it, do not restyle it, do not make a different "
    "mascot.\n"
    "Reproduce it exactly: silver-grey short-pile velboa with a pearlescent sheen, a pale "
    "ivory-silver belly panel, a long flat firmly-stuffed sewn snout, four soft cord barbel "
    "whiskers under the snout, the back scutes as small padded quilted bumps along a raised spine "
    "seam, one large glossy black embroidered eye with a white satin-stitch catchlight, soft sewn "
    "pectoral fins, a dorsal fin and a crescent tail, visible high-quality stitching and seams, a "
    "small woven fabric tag near the tail.\n\n"
    "*** ABSOLUTE RULE: NO LEGS, NO FEET, NO TOES, NO STANDING NUBS. IT IS A FISH. ***\n"
    "It has no limbs beyond those fins and it never stands upright. It rests on its smooth rounded "
    "belly.\n\n"
    "*** COLOUR RULE ***\n"
    "The plush body is ALWAYS silver-grey with a pale ivory-silver belly. Never recolour it blue, "
    "navy, cyan, pink or any other hue.\n\n"
)

CHIBI = (
    "*** CHIBI PROPORTIONS - CRITICAL ***\n"
    "This toy is CHIBI FUJIE, the cute young form, NOT the realistic adult Fujie. The head is HUGE, "
    "roughly one third of the whole length, and deeply rounded; the single glossy black eye is "
    "large, about a quarter the height of the head; the body behind the head is SHORT, plump and "
    "stubby and tapers quickly into the crescent tail; the flat paddle snout sticks well out in "
    "front with four cord whiskers beneath it.\n"
    "Never sew it as a long, slender, realistic sturgeon with a small eye and a stretched-out body. "
    "That is the other character and it must not appear.\n\n"
)

SHOT = (
    "PHOTOREALISTIC photography of a real object - a photograph, not a drawing or a render. The "
    "plush is soft fabric: short pile catching the light, seams and stitch lines visible, a slight "
    "slump where the stuffing gives, a soft contact shadow underneath. No drawn outline anywhere, "
    "no cel shading, no cartoon linework. Real depth of field.\n\n"
    "*** TEXT RULE ***\n"
    "The only words allowed anywhere are Fujie, FUJIKIN and the katakana \u30d5\u30b8\u30a3, small "
    "and discreet on a tag or a box. No other words in any language, no slogans, no shop names, no "
    "invented kanji or kana, no captions, no small print, no price tags.\n\n"
)

FUJI = (
    "*** MOUNT FUJI RULE ***\n"
    "Where Mount Fuji appears it is a LOW, WIDE, CALM cone - the base roughly three times as wide "
    "as the mountain is tall, the slopes long and gently concave, the summit slightly flattened, "
    "the snow cap a soft scalloped band across the top third. Never a tall sharp triangle, never a "
    "mountain range, never a party-hat shape.\n"
    "The mountain is always a SEPARATE object next to or behind the plush - a knitted cap, a sewn "
    "cushion, a printed cloth, a painted backdrop. The fish itself is never repainted blue and "
    "never turned into a mountain.\n\n"
)

# --- six more of the original plush -----------------------------------------

PLAIN = [
    ("plush_detail.png", "1:1", [PLUSH_REF],
     "MACRO DETAIL PHOTOGRAPH of the plush's head and shoulder, filling the frame, on a soft "
     "neutral background. The embroidered eye and its satin-stitch catchlight are razor sharp; the "
     "velboa pile, the topstitched snout seam, the quilted scute bumps and the four cord whiskers "
     "are all readable. The small woven tag is just visible at the edge of the frame, softly out of "
     "focus. Very shallow depth of field, soft directional window light. A shot that proves the "
     "manufacturing quality."),

    ("plush_packaging.png", "4:3", [PLUSH_REF],
     "RETAIL PACKAGING SHOT on a pale surface: the 25cm plush sitting beside its packaging - a "
     "deep navy printed card header with a clear crown-shaped window bag folded open in front of "
     "it, and a small navy-and-silver hang tag on a cord resting against the plush. Clean, "
     "premium Japanese character-goods presentation, soft studio light, generous empty space."),

    ("plush_desk.png", "4:3", [PLUSH_REF],
     "LIFESTYLE PHOTOGRAPH on an office desk: the 25cm plush resting on its belly beside a closed "
     "laptop, a ceramic mug and a notebook, with a softly blurred window behind. Late-afternoon "
     "daylight, warm and quiet. The plush is clearly a desk companion in a working office, not a "
     "studio prop. Shallow depth of field."),

    ("plush_hug_large.png", "3:4", [PLUSH_REF, LINEUP],
     "LIFESTYLE PHOTOGRAPH: the large 50cm plush held in a hug against an adult's chest, arms "
     "wrapped round it, photographed from the front against a softly blurred warm interior. The "
     "person's face is out of frame above; the plush is the subject and its size is obvious. "
     "Natural window light, soft and affectionate, the fabric slightly compressed where it is "
     "squeezed."),

    ("plush_shop_wall.png", "16:9", [PLUSH_REF],
     "RETAIL PHOTOGRAPH taken at a slight angle inside a bright Japanese visitor-centre gift shop: "
     "a pale wood shelving wall stacked with rows of the plush in its three sizes, the keychain "
     "versions hanging from a rail below on ball chains. Warm shop lighting, real depth down the "
     "aisle, the front plush close to the lens and the back rows softening. Tidy, inviting, "
     "abundant."),

    ("plush_cushion.png", "4:3", [PLUSH_REF],
     "PRODUCT PHOTOGRAPH on a pale linen sofa: an oversized round floor-cushion version of the "
     "character, about 60cm across - the same velboa, the same embroidered eye and quilted scute "
     "bumps, but squashed into a soft flattened disc with the snout and tail sewn flat against the "
     "body. The standard 25cm plush rests on top of it for scale. Soft afternoon light, homely "
     "styling."),
]

# --- the Fuji plush set ------------------------------------------------------

FUJIS = [
    ("plush_fuji_cap.png", "1:1", [PLUSH_REF],
     "STUDIO PRODUCT PHOTOGRAPH on a seamless pale background: the 25cm plush lying on its belly "
     "facing the camera, wearing a small KNITTED MOUNT FUJI CAP - a low wide soft-blue knitted cone "
     "with a cream bobbled snow band round its top, sitting between the eye and the dorsal fin. "
     "The knit texture is clearly wool. Soft even lighting, gentle contact shadow."),

    ("plush_fuji_cushion.png", "4:3", [PLUSH_REF],
     "PRODUCT PHOTOGRAPH on a pale linen surface: a sewn MOUNT FUJI CUSHION - a low wide soft-blue "
     "cushion in brushed cotton with a cream fleece snow cap appliqued across its top and visible "
     "piped seams - with the 25cm plush resting against its slope. The cushion is clearly a "
     "separate soft-furnishing product, about the same size as the plush. Warm window light."),

    ("plush_fuji_lineup.png", "16:9", [PLUSH_REF, LINEUP],
     "PRODUCT FAMILY PHOTOGRAPH on a light-grey studio background: the three plush sizes resting on "
     "their bellies in a neat row, smallest to largest - a 10cm keychain with a metal ball chain, a "
     "25cm and a 50cm - each wearing its own knitted Mount Fuji cap sized to fit. Behind them, "
     "standing on the surface, a low wide sewn Mount Fuji cushion as a backdrop. Even lighting, "
     "commercial catalogue arrangement."),

    ("plush_fuji_keychain.png", "3:4", [PLUSH_REF],
     "LIFESTYLE PHOTOGRAPH close up on a Japanese train platform: the 10cm keychain plush clipped "
     "to a commuter's bag strap by a metal ball chain, with a tiny felt MOUNT FUJI charm - a low "
     "wide blue felt cone with a cream felt snow cap, about half the size of the plush - hanging "
     "from the same clip beside it. Soft bokeh background, natural daylight."),

    ("plush_fuji_giftbox.png", "4:3", [PLUSH_REF],
     "GIFT SET PHOTOGRAPH on a pale cloth: a deep navy rigid gift box with the lid tilted behind "
     "it, and inside, nested in cream tissue, the 25cm plush lying beside a small sewn Mount Fuji "
     "cushion and a folded cotton cloth printed with a low wide Fuji. The lid is foil-stamped in "
     "silver with a small Fuji and ripple mark. Premium department-store presentation, soft "
     "directional light."),

    ("plush_fuji_pouch.png", "1:1", [PLUSH_REF],
     "PRODUCT PHOTOGRAPH on a pale wooden surface: the 10cm keychain plush sitting half out of an "
     "indigo cotton DRAWSTRING POUCH printed with a repeating low wide Mount Fuji and wave motif, "
     "the cord loosened. A second closed pouch lies folded beside it. Real dyed cloth with visible "
     "weave and soft creases. Natural side light, quiet composition."),

    ("plush_fuji_shop.png", "16:9", [PLUSH_REF],
     "RETAIL PHOTOGRAPH taken at a slight angle inside a bright gift shop: a pale wood shelving "
     "wall stacked with rows of the plush, many of them wearing knitted Mount Fuji caps, with sewn "
     "Fuji cushions stacked on the lower shelf and a low wide Mount Fuji painted on the wall behind "
     "the display. Warm shop lighting, real depth down the shelves, the front plush close to the "
     "lens. Tidy and inviting."),

    ("plush_fuji_window.png", "4:3", [PLUSH_REF],
     "LIFESTYLE PHOTOGRAPH: the 25cm plush resting on a pale wooden windowsill in its knitted Mount "
     "Fuji cap, with the real Mount Fuji visible far outside the window - low, wide and "
     "snow-capped, softly out of focus in the morning haze. Warm backlight through the glass, a "
     "rim of light along the plush's pile. Quiet and atmospheric."),
]

if __name__ == "__main__":
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for folder, jobs, wrap in [
        (OUT, PLAIN, lambda p: LOCK + CHIBI + SHOT + p),
        (FOUT, FUJIS, lambda p: LOCK + CHIBI + SHOT + FUJI + p),
    ]:
        if only and only not in folder:
            continue
        for name, aspect, refs, prompt in jobs:
            print("-> " + name, flush=True)
            r = gen(wrap(prompt), folder + name, refs, aspect)
            print("   " + ("ok" if isinstance(r, list) else str(r)), flush=True)
