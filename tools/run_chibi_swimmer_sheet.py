"""A character sheet for the swimming Chibi Fujie that turned up on the
Mount Fuji manhole cover - a flatter, more fish-like version of him than the
standing chibi. Curiosity piece, not part of the entry.

Output: Fujie_Creative/20_new_ideas/chibi_swimmer_sheet.png
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen

OUT = "D:/Fuji_Famous/Fujie_Creative/20_new_ideas/"
REF = OUT + "chibi_swimmer_ref.png"

PROMPT = (
    "The attached image is a mascot design photographed on a cast metal manhole cover: a cute "
    "swimming sturgeon seen from the side. Study him carefully. He has a long flat snout with four "
    "small barbels hanging under it, one big round dark eye with a white catchlight, a simple "
    "smiling mouth, a large white belly patch that sweeps back along his body, a row of small "
    "triangular bony scutes along his back AND a second row along his flank, small rounded fins and "
    "a swept tail. His body is soft silver-grey, his belly is white, and everything is drawn with a "
    "bold dark outline and FLAT colour - no shading, no gradients, no gloss.\n\n"
    "Draw a CHARACTER SHEET of this same character as clean flat vector artwork on a plain white "
    "background. Keep his proportions, his face and his markings exactly as in the reference; only "
    "the pose and angle change. Do NOT copy the metal, the rivets, the blue field or any part of "
    "the manhole cover - just the character.\n\n"
    "Lay it out as two rows.\n"
    "TOP ROW - a turnaround of him swimming level, all the same size, evenly spaced: seen from his "
    "left side, from three-quarters front, head-on from the front, and from three-quarters behind.\n"
    "BOTTOM ROW - four expressions, each drawn as his whole head and the front part of his body, "
    "complete and unclipped, at the same size and evenly spaced: happy, "
    "surprised with wide eyes, sleepy with the eye closed, and proud with the chin lifted.\n\n"
    "*** TEXT RULE ***\n"
    "No text anywhere: no labels, no kanji, no kana, no romaji, no numbers, no arrows, no "
    "measurement lines. White background, nothing else in the picture.\n"
)

if __name__ == "__main__":
    gen(PROMPT, OUT + "chibi_swimmer_sheet.png", refs=[REF], aspect="16:9")
