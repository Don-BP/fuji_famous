"""Idea 09 - a Fujie manhole cover in Hitachiota.

One scene, three takes. A colour cast-iron cover set in the paving outside
the station. The centre of the cover is generated EMPTY on purpose - a plain
blue water field - because the official Fujie artwork is composited onto it
afterwards, so its colours are exact.

Output: Fujie_Creative/20_new_ideas/manhole_*.png
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen

OUT = "D:/Fuji_Famous/Fujie_Creative/20_new_ideas/"

RULES = (
    "*** COVER RULE ***\n"
    "The manhole cover is a real Japanese decorative cast-iron cover: a perfect circle set flush "
    "in the paving, a raised outer rim band, a ring of small cast studs, two small round keyholes, "
    "and a large circular CENTRE FIELD filled with coloured resin. "
    "The CENTRE FIELD IS EMPTY of any creature: it shows only a calm deep-blue river-water pattern "
    "of fine concentric ripple lines with a few pale green reed shapes at the lower edge. "
    "There is NO fish, NO animal, NO mascot, NO character, NO logo and NO emblem anywhere on the "
    "cover. Leave the middle of that blue field clear and uninterrupted.\n\n"
    "*** TEXT RULE ***\n"
    "No text anywhere in the picture. No kanji, no kana, no romaji, no numbers, no station signs, "
    "no shop signs, no road markings with letters, no lettering cast into the cover rim. Any "
    "distant signage must be too far away and too soft to read.\n\n"
)

SCENE = (
    "PHOTOREALISTIC editorial photograph on a clean paved forecourt outside a small regional "
    "Japanese railway station in Ibaraki, a bright ordinary weekday. Pale grey paving blocks laid "
    "in a neat pattern, a tactile paving strip, a low kerb, a few bicycles racked to one side, "
    "trees and quiet low buildings soft in the background. "
    "Set flush into the paving is one large colour cast-iron manhole cover, about 60cm across, "
    "clean and newly installed, its coloured resin bright against the grey stone. The iron is dark "
    "grey with the honest texture of cast metal. Natural daylight, crisp and neutral, real ground "
    "shadow around the rim. Sharp focus on the cover. No watermark."
)

TAKES = {
    "manhole_a": SCENE + " Shot from standing height looking almost straight down: the cover large "
                         "and nearly circular in frame, filling most of the picture, paving all "
                         "around, the toes of a pair of trainers at the very bottom edge.",
    "manhole_b": SCENE + " Shot from standing height at a natural walking angle: the cover in the "
                         "lower half of the frame seen as an ellipse, the station forecourt and its "
                         "canopy receding softly behind, a person crouching further back with a "
                         "phone, out of focus.",
    "manhole_c": SCENE + " Low shot close to the ground: the cover fills the foreground as a wide "
                         "ellipse, very sharp, and the paved forecourt and station run away behind "
                         "it with a shallow depth of field.",
}

if __name__ == "__main__":
    for name, prompt in TAKES.items():
        print(name, flush=True)
        gen(RULES + prompt, OUT + name + ".png", aspect="4:3")
