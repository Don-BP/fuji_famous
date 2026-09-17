"""Idea 09 - the covers drawn as whole designs.

Instead of laying artwork onto a blank, the cover and the fish are drawn
together as one casting, with the character supplied as a reference. Takes
are written to Fujie_Creative/20_new_ideas/whole_*.png for picking.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen

OUT = "D:/Fuji_Famous/Fujie_Creative/20_new_ideas/"
CHIBI = "D:/Fuji_Famous/Fujie_Creative/01_character/chibi_neutral.png"
OFFICIAL = "D:/Fuji_Famous/Documents_for_dev/05_fujie_\u7d75\u67c4\u4f8b.png"

COVER = (
    "PHOTOREALISTIC photograph of a real Japanese decorative colour manhole cover, the kind towns "
    "make for their own mascot and collectors travel to photograph. Shot STRAIGHT DOWN from "
    "directly above so the cover is a PERFECT CIRCLE filling almost the whole frame, with only a "
    "narrow band of grey paving at the corners. "
    "It is a genuine casting: dark grey iron with real casting texture, a raised outer rim band, a "
    "ring of small cast studs and two small keyholes. Inside, the design is made of RAISED IRON "
    "LINES with flat opaque coloured resin poured into the cells between them - hard edges, few "
    "colours, bold simple shapes, the look of a woodblock print. No photograph inside the cover, "
    "no gradients, no airbrushing, no gloss, no glow, no drop shadows, nothing transparent. "
    "Slightly worn and dusty in the real way, bright even daylight, sharp. No watermark.\n\n"
    "*** TEXT RULE ***\n"
    "No text anywhere: no kanji, no kana, no romaji, no numbers, no lettering on the rim.\n\n"
)

CHIBI_REF = (
    "The attached image is 'Chibi Fujie', a cute chrome-silver STURGEON: long flat snout, four "
    "barbels under it, a big dark eye, a smile, a row of bony scutes down the back, fins only - no "
    "arms, no legs. Cast HIM into the middle of the cover, redrawn as flat cast-and-resin artwork "
    "in his own silver-grey and white, keeping his shape, his face and his proportions exactly. He "
    "is a sturgeon: never a dolphin, a shark or a whale.\n\n"
)

OFFICIAL_REF = (
    "The attached image is the official Fujie: a realistic silver sturgeon in side profile, long "
    "flat snout, four barbels, rows of pale bony scutes along the body, small dark eye, large swept "
    "tail. Cast HIM across the middle of the cover in side profile, redrawn as flat cast-and-resin "
    "artwork in silver-grey, white and shadow grey, keeping his outline and proportions exactly.\n\n"
)

TAKES = {
    "whole_chibi_1": (CHIBI, CHIBI_REF + COVER + "The field around him is deep river blue with a "
                      "band of stylised wave lines around the edge and a few flat reeds at the bottom."),
    "whole_chibi_2": (CHIBI, CHIBI_REF + COVER + "The field around him is pale blue with flat round "
                      "bubbles and a ring of stylised water ripples near the rim."),
    "whole_official_1": (OFFICIAL, OFFICIAL_REF + COVER + "The field around him is mid blue with a "
                         "bold seigaiha wave pattern in white confined to a ring around the outer edge."),
    "whole_official_2": (OFFICIAL, OFFICIAL_REF + COVER + "The field around him is deep indigo water "
                         "with flat green hills in silhouette across the top and flat reeds at the bottom."),
    "whole_chibi_3": (CHIBI, CHIBI_REF + COVER + "The field around him is a flat green and blue "
                      "lotus pond: simple lily pads, two flat lotus flowers and a few curling "
                      "current lines, all in a handful of solid colours."),
    "whole_official_3": (OFFICIAL, OFFICIAL_REF + COVER + "The field around him is teal water with "
                         "flat concentric ripple rings behind him and a clump of flat reeds rising "
                         "from the bottom left."),
}

if __name__ == "__main__":
    only = sys.argv[1:]
    for name, (ref, prompt) in TAKES.items():
        if only and not any(o in name for o in only):
            continue
        print(name, flush=True)
        gen(prompt, OUT + name + ".png", refs=[ref], aspect="1:1")
