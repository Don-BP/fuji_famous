"""Idea 09 - the set of Fujie manhole covers for Hitachiota.

Five covers, seen straight down and filling the frame. Each is generated as a
BLANK - a real cast-iron cover with an empty coloured field - because the
Fujie artwork is composited on afterwards, so the official fish keeps the
exact colours of the original and Chibi stays on model.

Output: Fujie_Creative/20_new_ideas/cover_blank_*.png
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen

OUT = "D:/Fuji_Famous/Fujie_Creative/20_new_ideas/"

RULES = (
    "*** COVER RULE ***\n"
    "A real Japanese decorative cast-iron manhole cover, photographed STRAIGHT DOWN from directly "
    "above so it is a PERFECT CIRCLE, not an ellipse. The cover fills almost the whole frame with "
    "only a narrow band of grey paving stone visible at the corners. Dark grey cast iron with "
    "honest casting texture, a raised outer rim band, a ring of small cast studs, two small round "
    "keyholes at the sides, and a large circular CENTRE FIELD filled with coloured resin. "
    "The CENTRE FIELD IS COMPLETELY EMPTY of any creature: no fish, no animal, no mascot, no "
    "character, no logo, no emblem, no crest. The very middle of the field must be clear and "
    "uninterrupted - keep all pattern to the outer part of the field.\n\n"
    "*** TEXT RULE ***\n"
    "No text anywhere: no kanji, no kana, no romaji, no numbers, no lettering cast into the rim.\n\n"
    "Bright even daylight, no harsh shadow, sharp and clean, photographed as a real object in the "
    "ground. No watermark.\n\n"
)

FIELDS = {
    "cover_blank_river": "The coloured field is a deep river blue with fine concentric ripple rings, "
                         "and a clump of pale green reeds rising from the lower left edge.",
    "cover_blank_reeds": "The coloured field is a soft teal green, with pale water-plant leaves "
                         "around the lower half and a scatter of small grey pebbles along the bottom edge.",
    "cover_blank_bubbles": "The coloured field is a pale sky blue, lightest at the top, with a "
                           "scatter of small round bubbles rising up the left and right edges.",
    "cover_blank_hills": "The coloured field is a deep indigo below and a pale dawn sky band across "
                         "the top, with a low silhouette of green wooded hills along the upper edge "
                         "and calm water beneath.",
    "cover_blank_wave": "The coloured field is a mid blue with a bold traditional Japanese seigaiha "
                        "wave pattern in white and pale blue confined to a band around the outer "
                        "edge of the field, the centre left plain.",
}

if __name__ == "__main__":
    for name, field in FIELDS.items():
        print(name, flush=True)
        gen(RULES + field, OUT + name + ".png", aspect="1:1")
