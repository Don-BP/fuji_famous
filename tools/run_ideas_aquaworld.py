"""Idea 07 - a live Fujie tank beside the shark exhibit at an aquarium.

One scene, three takes. The tank is small and real; the shark exhibit behind
it is big and dim; the panel carries Chibi Fujie and the katakana line only.
The fish in the tank is a REAL sturgeon (photograph), not the illustration.

Output: Fujie_Creative/20_new_ideas/aquaworld_*.png
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen

CHIBI = "D:/Fuji_Famous/Fujie_Creative/01_character/master_v3_wave.png"
OUT = "D:/Fuji_Famous/Fujie_Creative/20_new_ideas/"

CHIBI_LOCK = (
    "The attached image is 'Chibi Fujie', the cute second form of Fujikin's sturgeon mascot: a "
    "small chrome-silver sturgeon with a big dark eye, a smile, four little barbels, bony scutes "
    "down the back, fins only (no arms, no legs). Wherever a printed panel or sign shows the "
    "character, reproduce THIS design faithfully - same colours, same proportions, same face.\n\n"
    "*** TEXT RULE ***\n"
    "The only text allowed anywhere in the picture is the katakana line サメじゃないです on the "
    "panel, and optionally the small word FUJIE. No other words, no invented kanji, no signage "
    "blurb, no price boards, no arrows.\n\n"
)

SCENE = (
    "PHOTOREALISTIC editorial photograph inside a large Japanese public aquarium. "
    "Two full-size exhibit tanks side by side, both floor-to-ceiling walls of thick glass. "
    "LEFT: the shark exhibit, huge and dim, several real sharks gliding past, deep blue. "
    "RIGHT: a proper exhibit tank of its own, the same scale, clean and brighter, a wide river-bed "
    "habitat with sand and pale stones, and in it several REAL sturgeon swimming slowly - large "
    "live silver fish, over a metre long, long flat snouts, four barbels, rows of bony scutes, "
    "photographed as real animals, not drawings. The sturgeon tank must look like a permanent "
    "home for big fish, not a display box. "
    "Between the two tanks, on the wall pillar: one clean exhibit panel with Chibi Fujie printed "
    "on it and the katakana line サメじゃないです in large friendly type. "
    "A child of about eight, seen from behind, stands at the panel looking from the sharks to the "
    "sturgeon. Cinematic aquarium light, blue and cool on the left, warmer and clearer on the "
    "right. Shallow depth of field. No watermark."
)

TAKES = {
    "aquaworld_a": SCENE + " Wide shot: both tank walls fully in frame, the panel on the pillar between them, the child small in front.",
    "aquaworld_b": SCENE + " Medium shot centred on the sturgeon tank; one big sturgeon passes close to the "
                            "glass at the child's eye level, the panel readable at the edge, sharks soft at the far left.",
    "aquaworld_c": SCENE + " From the child's eye height, the panel close on the pillar, a sturgeon gliding "
                            "past on the right and a shark silhouette on the left, both tanks towering.",
}

if __name__ == "__main__" and "--both" not in sys.argv:
  for name, prompt in TAKES.items():
    print(name, flush=True)
    gen(CHIBI_LOCK + prompt, OUT + name + ".png", refs=[CHIBI], aspect="4:3")

# ---- variant: the official Fujie on its own nameplate beside the tank ----
OFFICIAL = "D:/Fuji_Famous/Documents_for_dev/05_fujie_絵柄例.png"
OFFICIAL_LOCK = (
    "The SECOND attached image is the OFFICIAL Fujie illustration: a realistic polished chrome-silver "
    "sturgeon in profile, long flat snout, four barbels, rows of pale bony scutes, small dark eye, "
    "large swept tail. It appears ONCE, on a separate rectangular nameplate mounted on the frame of "
    "the sturgeon tank, reproduced EXACTLY as drawn on a plain dark plate with no text over it - only "
    "the small word FUJIE beneath. Do not redraw, restyle, cartoon or recolour it. It must not be "
    "confused with Chibi Fujie on the panel: the panel is the cute one, the nameplate is the chrome one.\n\n"
)
if __name__ == "__main__" and "--both" in sys.argv:
    prompt = CHIBI_LOCK + OFFICIAL_LOCK + TAKES["aquaworld_c"].replace(
        "the panel close on the pillar,", "the panel close on the pillar, the official nameplate visible on the tank frame at the right,")
    gen(prompt, OUT + "aquaworld_c_both.png", refs=[CHIBI, OFFICIAL], aspect="4:3")

