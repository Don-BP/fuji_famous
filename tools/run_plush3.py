"""More Chibi Fujie plush, led by the mascot keychain.

The 10cm keychain is the piece that carries: it is cheap, it hangs where people
see it, and it puts the fish on a bag rather than on a shelf. These shots build
that out into a proper mascot line - an assortment, a shop rail, blind bags,
and the places one actually ends up - plus two sewn poses for the shelf.

Every shot is given the existing keychain photograph first, so it is the SAME
toy: satin-finish silver, one embroidered eye, cord whiskers, woven tag.

Output: Fujie_Creative/03_plushie/  and  Fujie_Creative/19_fujisan/plush/
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen

KEY = "D:/Fuji_Famous/Fujie_Creative/03_plushie/plush_keychain_lifestyle.png"
STUDIO = "D:/Fuji_Famous/Fujie_Creative/03_plushie/plush_studio_front.png"
OUT = "D:/Fuji_Famous/Fujie_Creative/03_plushie/"
FOUT = "D:/Fuji_Famous/Fujie_Creative/19_fujisan/plush/"

LOCK = (
    "The attached photograph is the EXISTING 'Chibi Fujie' MASCOT KEYCHAIN - a small Japanese plush "
    "charm about 10cm long. Every shot below shows THIS SAME manufactured toy. Do not redesign it, "
    "do not restyle it, do not invent a different mascot.\n"
    "Reproduce it exactly: satin-finish silver-grey plush with a soft pearlescent sheen, a pale "
    "ivory belly, a long flat firmly-stuffed sewn snout, four fine cord barbel whiskers hanging "
    "under the snout, a row of small padded scute bumps along the back, ONE large glossy black "
    "embroidered eye with a single white catchlight, soft sewn pectoral fins, a dorsal fin and a "
    "crescent tail, neat visible seams, a small woven fabric tag near the tail, and a silver split "
    "ring and chain at the top of the head.\n\n"
    "*** ABSOLUTE RULE: NO LEGS, NO FEET, NO TOES, NO STANDING NUBS. IT IS A FISH. ***\n"
    "*** COLOUR RULE: the body is ALWAYS silver-grey with a pale ivory belly. Never blue, navy, "
    "cyan, pink or any other hue. ***\n\n"
)

CHIBI = (
    "*** CHIBI PROPORTIONS - CRITICAL ***\n"
    "This is CHIBI FUJIE, the cute young form. It is NOT the realistic adult Fujie, and the two must "
    "never be mixed inside one picture.\n"
    "The head is HUGE - roughly one third of the whole length - and rounded. The single glossy black "
    "eye is large, about a quarter the height of the head. The body behind the head is SHORT, plump "
    "and stubby, tapering quickly into a small crescent tail. The snout is a short blunt paddle, not "
    "a long spike.\n"
    "NEVER render any of them as a long, slender, realistic sturgeon with a small eye, a long snout "
    "and a stretched-out body. That is the other character. Every one of the six has the same big "
    "head, the same big eye and the same stubby body as the attached toy.\n\n"
)

TAIL = (
    "*** TAIL RULE ***\n"
    "EVERY figure clearly shows its CRESCENT TAIL FIN at the rear - two soft swept lobes sewn as one "
    "piece. The body never simply ends in a stump, and the dorsal fin on the back is never mistaken "
    "for the tail.\n\n"
)

SHOT = (
    "PHOTOREALISTIC photography of a real object - a photograph, not a drawing or a render. The "
    "plush is soft fabric: satin pile catching the light, seams and stitch lines visible, a slight "
    "give where it is stuffed, real shadows. No drawn outline anywhere, no cel shading, no cartoon "
    "linework. Real lens, real depth of field.\n\n"
    "*** TEXT RULE ***\n"
    "The only words allowed anywhere are Fujie, FUJIKIN and the katakana \u30d5\u30b8\u30a3, small "
    "and discreet on a tag or a header card. No other words in any language, no slogans, no shop "
    "names, no invented kanji or kana, no captions, no small print, no prices.\n"
    "Never write the pose names or any part of these instructions into the picture. No labels under "
    "or beside any figure, no numbers, no grid captions.\n\n"
)

FUJI = (
    "*** MOUNT FUJI RULE ***\n"
    "Mount Fuji is a LOW, WIDE, CALM cone - the base roughly three times as wide as it is tall, "
    "slopes long and gently concave, summit slightly flattened, snow cap a soft scalloped band "
    "across the top third. Never a tall sharp triangle. It is always a SEPARATE object - a knitted "
    "cap, a felt charm, a sewn cushion - and the fish is never repainted blue.\n\n"
)

PLAIN = [
    ("plush_mascot_set.png", "16:9", [KEY, STUDIO],
     "PRODUCT ASSORTMENT PHOTOGRAPH on a pale grey surface: six mascot keychains laid out in two "
     "rows of three, each with its own silver split ring and short chain.\n"
     + CHIBI + TAIL +
     "This is ONE photograph of six soft toys arranged in two rows of three on a single continuous "
     "pale grey surface. It is NOT a contact sheet and NOT a catalogue page: no panel borders, no "
     "dividing lines between the toys, no white gutters, and NO CAPTIONS, NO LABELS AND NO WRITING "
     "OF ANY KIND anywhere in the picture. Never write these pose descriptions into the image.\n"
     "The six are sewn in six genuinely different shapes so the set reads as a collection. No two "
     "repeat a pose and no two face the same way; in every one both the face and the crescent tail "
     "are visible. Left to right along the top row and then the bottom:\n"
     "one propped on its belly at a three-quarter angle turned toward the camera, a pectoral fin "
     "lifted in a cheerful wave, head tilted;\n"
     "one curled into a closed ring with its snout tucked against its tail, seen from above, its "
     "eye a single stitched closed curve;\n"
     "one resting on its belly in full side view facing right, head up, the short round body and "
     "the crescent tail both clearly in profile;\n"
     "one diving, head angled steeply down toward the surface and tail lifted high behind it;\n"
     "one lounging on its side with the pale belly toward the camera, head propped up and one "
     "pectoral fin raised behind its head;\n"
     "one caught mid-leap facing left, its body curved into a deep C with the head and the crescent "
     "tail both lifted clear of the surface.\n"
     "Even soft studio light, gentle contact shadows, a quiet unfussy arrangement."),

    ("plush_mascot_rail.png", "4:3", [KEY],
     "RETAIL PHOTOGRAPH inside a bright Japanese gift shop: a chrome display rail hung with four "
     "rows of the mascot keychains on their chains, dozens of them, receding slightly to the right. "
     "The nearest one is sharp and close to the lens, the rows behind softening. A small navy "
     "header card sits above the rail. Warm shop lighting, real depth."),

    ("plush_mascot_backpack.png", "3:4", [KEY],
     "LIFESTYLE PHOTOGRAPH outdoors: the mascot keychain clipped to the zip pull of a student's "
     "canvas backpack, photographed close up from the side as the person walks, tree-lined street "
     "softly blurred behind. The charm swings slightly, catching afternoon sun along its satin "
     "pile. Candid and warm, shallow depth of field."),

    ("plush_mascot_hand.png", "1:1", [KEY],
     "PHOTOGRAPH of the mascot keychain held up in one open adult hand against a softly blurred "
     "cafe interior, natural window light. The hand gives the scale immediately - the charm sits "
     "comfortably across the palm. Warm, inviting, shallow depth of field."),

    ("plush_mascot_cafe.png", "4:3", [KEY],
     "LIFESTYLE PHOTOGRAPH on a pale wooden cafe table: the mascot keychain propped against a "
     "ceramic latte cup, its chain pooled beside it, a notebook and a pair of sunglasses just out "
     "of focus behind. Soft morning window light from the left, quiet and everyday."),

    ("plush_mascot_blindbag.png", "4:3", [KEY],
     "PRODUCT PHOTOGRAPH on a pale surface: a row of four sealed BLIND BAGS in matte navy foil, "
     "each printed with a small silver fish silhouette, and in front of them one torn open with a "
     "mascot keychain half out of the bag and a second charm sitting beside it. Crisp studio light, "
     "the foil catching a soft highlight, clean uncluttered composition."),

    ("plush_mascot_pair.png", "1:1", [KEY],
     "CLOSE LIFESTYLE PHOTOGRAPH: two mascot keychains clipped side by side to the handle of a "
     "leather handbag, one facing forward and one turned away, their chains tangled together. Shot "
     "tight, the bag leather and the satin plush both readable, a softly blurred street behind. "
     "Natural daylight."),

    ("plush_mascot_luggage.png", "4:3", [KEY],
     "TRAVEL PHOTOGRAPH: the mascot keychain clipped by a small carabiner to the handle of a hard "
     "shell suitcase standing in an airport departure hall, the terminal softly blurred behind with "
     "warm bokeh from the ceiling lights. Shot low and close, the charm sharp against the blur."),
]

FUJIS = [
    ("plush_fuji_mascot_set.png", "16:9", [KEY],
     "PRODUCT ASSORTMENT PHOTOGRAPH on a pale grey surface: six mascot keychains laid out in two "
     "rows of three, each with its own silver split ring and short chain, and each wearing a small "
     "KNITTED MOUNT FUJI CAP - a low wide soft-blue knitted cone with a cream bobbled snow band. "
     "Small felt Mount Fuji charms hang beside two of them on the same chains.\n"
     + CHIBI + TAIL +
     "This is ONE photograph of six soft toys arranged in two rows of three on a single continuous "
     "pale grey surface. It is NOT a contact sheet and NOT a catalogue page: no panel borders, no "
     "dividing lines between the toys, no white gutters, and NO CAPTIONS, NO LABELS AND NO WRITING "
     "OF ANY KIND anywhere in the picture. Never write these pose descriptions into the image.\n"
     "The six are sewn in six genuinely different shapes so the set reads as a collection. No two "
     "repeat a pose and no two face the same way; in every one both the face and the crescent tail "
     "are visible. Left to right along the top row and then the bottom:\n"
     "one propped on its belly at a three-quarter angle turned toward the camera, a pectoral fin "
     "lifted in a cheerful wave, head tilted;\n"
     "one curled into a closed ring with its snout tucked against its tail, seen from above, its "
     "eye a single stitched closed curve and its cap tipped forward;\n"
     "one resting on its belly in full side view facing right, head up, the short round body and "
     "the crescent tail both clearly in profile;\n"
     "one diving, head angled steeply down and tail lifted high behind it;\n"
     "one lounging on its side with the pale belly toward the camera, head propped up and one "
     "pectoral fin raised behind its head;\n"
     "one caught mid-leap facing left, its body curved into a deep C with the head and the crescent "
     "tail both lifted clear of the surface.\n"
     "Every one still wears its knitted Mount Fuji cap. Even soft studio light, a quiet "
     "arrangement."),

    ("plush_fuji_mascot_rail.png", "4:3", [KEY],
     "RETAIL PHOTOGRAPH inside a bright Japanese gift shop: a chrome display rail hung with rows of "
     "the mascot keychains in knitted Mount Fuji caps, alternating with small felt Mount Fuji "
     "charms on their own chains. The nearest charm is sharp and close to the lens, the rows behind "
     "softening, a low wide Mount Fuji painted on the wall beyond. Warm shop lighting, real depth."),
]

if __name__ == "__main__":
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for folder, jobs, wrap in [
        (OUT, PLAIN, lambda p: LOCK + CHIBI + SHOT + p),
        (FOUT, FUJIS, lambda p: LOCK + CHIBI + SHOT + FUJI + p),
    ]:
        for name, aspect, refs, prompt in jobs:
            if only and only not in name:
                continue
            print("-> " + name, flush=True)
            r = gen(wrap(prompt), folder + name, refs, aspect)
            print("   " + ("ok" if isinstance(r, list) else str(r)), flush=True)
