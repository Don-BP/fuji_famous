"""Idea 08 - the hundred-year letter, written to the fish your own age.

One scene, three takes. Open day INSIDE the Satomi farm: a recirculating
aquaculture hall with deep tanks, a letter-writing table set up for the day,
and a large permanent sealed box on a stand that will not be opened until
2030. Chibi Fujie is printed centred on the box lid. The fish are REAL
sturgeon (photograph), in water deep enough for them.

Output: Fujie_Creative/20_new_ideas/letter_*.png
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen

CHIBI = "D:/Fuji_Famous/Fujie_Creative/01_character/master_v3_wave.png"
OUT = "D:/Fuji_Famous/Fujie_Creative/20_new_ideas/"

CHIBI_LOCK = (
    "The attached image is 'Chibi Fujie', the cute second form of Fujikin's sturgeon mascot: a "
    "small chrome-silver STURGEON with a big dark eye, a smile, four little barbels hanging under a "
    "long flat snout, a row of bony scutes along the back, fins only (no arms, no legs). Where he "
    "is printed on the box lid, reproduce THIS design faithfully - same chrome-silver colour, same "
    "proportions, same face, same four barbels, same snout, same scutes. He is a printed mark on "
    "the wood, not a character standing in the scene. He must be a sturgeon: do NOT draw a dolphin, "
    "a shark, a whale or a generic cartoon fish.\n\n"
    "*** PLACEMENT RULE ***\n"
    "Chibi Fujie is printed on the FLAT TOP of the box lid, CENTRED - equal space to left and "
    "right, equal space front and back, squarely in the middle of the lid panel. Not off to one "
    "side, not near an edge, not tilted.\n\n"
    "*** TEXT RULE ***\n"
    "The only text allowed anywhere in the picture is the year on the front of the box, stencilled "
    "as exactly four separate digits in a straight row: 2, then 0, then 3, then 0. Space them "
    "evenly with a clear gap between each one. Each digit must be complete, upright and separate - "
    "no overlapping digits, no doubled digits, no extra digits, no merged shapes. Nothing else: no "
    "other words, no invented kanji, no hand-written text readable on the letter paper, no signage, "
    "no banners, no labels, no equipment markings.\n\n"
)

SCENE = (
    "PHOTOREALISTIC editorial photograph INSIDE a modern Japanese land-based sturgeon farm - a "
    "large clean indoor aquaculture hall, not an aquarium and not an outdoor pond. High steel roof "
    "structure, bright even daylight coming through roof panels, pale walls. Rows of LARGE DEEP "
    "circular rearing tanks: dark grey-green fibreglass tanks about four metres across and "
    "chest-high, filled to the brim with deep clear water, so the fish have real depth beneath "
    "them. Grey pipework, feed lines and a filtration plant run neatly along the wall; the wet "
    "concrete floor has drainage channels. The place is clean, working and orderly. "
    "In the nearest tank several REAL sturgeon move slowly through deep water: large live silver "
    "fish over a metre long, long flat snouts, four barbels, rows of bony scutes, photographed as "
    "real animals, never drawings. One rises near the surface; the others are further down in the "
    "dark water. "
    "A letter-writing area is set up for open day on the wide walkway between the tanks: a long "
    "plain wooden table with sheets of writing paper and pencils, a few simple chairs. "
    "A Japanese schoolchild of about eight sits writing a letter in pencil, calm and concentrating. "
    "Next to the table stands a LARGE PERMANENT SEALED BOX - a heavy chest of pale wood with steel "
    "corner brackets and a strong lock, roughly the size of a tea chest, mounted solidly on a low "
    "steel stand so it stands at waist height and clearly never moves. There is a narrow posting "
    "slot cut in the lid. The four digits of the year are stencilled large on its front panel, and "
    "Chibi Fujie is printed centred on the flat top of the lid. "
    "A few other local families are further down the hall at the tanks. Natural documentary light, "
    "clear and slightly cool, shallow depth of field, no watermark."
)

TAKES = {
    "letter_a": SCENE + " Wide shot down the length of the hall: the round tanks receding on both "
                        "sides, the writing table and the big sealed box in the middle of the "
                        "walkway, the child small at the table, families beyond.",
    "letter_b": SCENE + " Medium shot at the table: the child writing in the left of frame, the "
                        "large sealed box standing beside them on the right with the year stencilled "
                        "clearly on its front and Chibi Fujie centred on the lid, the rim of a tank "
                        "and a sturgeon in the deep water just behind them.",
    "letter_c": SCENE + " From beside the tank rim: a big sturgeon in the deep water fills the "
                        "foreground, and beyond the rim the child at the table and the large sealed "
                        "box stand on the walkway, both in focus.",
}

if __name__ == "__main__":
    for name, prompt in TAKES.items():
        print(name, flush=True)
        gen(CHIBI_LOCK + prompt, OUT + name + ".png", refs=[CHIBI], aspect="4:3")
