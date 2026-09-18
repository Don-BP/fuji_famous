"""Chapter 01 - the fish, and how few are left. A replacement.

The picture that opens the whole proposal. It has to say two things at once:
this is a REAL sturgeon, and there are hardly any left.

The one it replaces said only the second thing. It was a vast dark sea with the
fish a speck in the middle of it - the emptiness read perfectly and the animal
did not read at all. At tile size you could not tell it was a sturgeon, which is
the one fact chapter 01 exists to establish.

So the emptiness stays and the fish comes forward. It fills enough of the frame
that the flat snout, the four barbels and the rows of bony scutes are all
legible at thumbnail size, while the water around it stays empty and unpeopled
so that nothing suggests a shoal.

No people, no mascot, no text - this is the one picture on the page that is
meant to be taken for a real photograph of a real animal.

Output: Fujie_Creative/20_new_ideas/endangered_*.png
Once one is chosen, copy it over Fujie_Creative/17_act2_gallery/endangered_water.png
(gen.py archives the old one, so this is reversible) and rebuild.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen

OUT = "D:/Fuji_Famous/Fujie_Creative/20_new_ideas/"

RULES = (
    "*** MASCOT RULE ***\n"
    "Do NOT draw any mascot, cartoon character, logo or illustration anywhere in this picture. "
    "This is a straight underwater photograph of a real animal and nothing else.\n\n"
    "*** TEXT RULE ***\n"
    "There must be NO text anywhere in the picture at all: no words, no kanji, no kana, no Latin "
    "letters, no numbers, no captions, no watermark, no photographer credit, no border.\n\n"
    "*** FISH RULE ***\n"
    "The sturgeon is a REAL photographed fish, not a drawing and not a cartoon: silver-grey going "
    "to olive along the back and pale on the belly, a LONG FLAT POINTED SNOUT, FOUR BARBELS "
    "hanging under the snout in front of the mouth, rows of BONY SCUTES ridged along the back and "
    "down each flank, small eye set well back, and a shark-like UPSWEPT tail with the upper lobe "
    "much longer than the lower. It is an ancient, armoured, heavy-bodied fish. "
    "Do NOT draw a shark. Do NOT draw a dolphin. Do NOT draw a generic fish, a salmon or a carp.\n\n"
    "*** ONE FISH RULE ***\n"
    "There is exactly ONE sturgeon in the picture. No second fish, no shoal, no small fish in the "
    "distance, no other animals of any kind. The water around it is empty. That emptiness is the "
    "point of the photograph and must be preserved.\n\n"
    "*** SIZE RULE ***\n"
    "The fish is LARGE in the frame and unmistakable. A viewer seeing this picture the size of a "
    "postage stamp must still be able to tell it is a sturgeon: the snout, the barbels and the "
    "scutes all clearly readable. The previous version had the fish tiny and far away and was "
    "thrown away for exactly that reason. Do not place the fish small or distant.\n\n"
    "*** NO PEOPLE RULE ***\n"
    "No people, no divers, no boats, no nets, no tanks, no glass, no aquarium walls, no buildings "
    "and no man-made objects of any kind. Open natural water only.\n\n"
)

WATER = (
    "PHOTOREALISTIC underwater wildlife photograph. Deep, cold, still natural fresh water, dark "
    "green-black in the distance and fading to nothing - no visible bottom, no plants, no rocks, "
    "no debris. Pale daylight comes down from the surface far above in long soft shafts, catching "
    "the fish and leaving everything around it dark. Fine suspended particles hang in the beams. "
    "Quiet, cold, solemn, elegiac. Natural colour, no colour cast, sharp on the fish and soft "
    "everywhere else, shot on a full-frame camera with a wide aperture. No watermark. "
)

TAKES = {
    # Side-on and close: the most legible reading of the animal.
    "endangered_a": WATER + (
        "ONE large sturgeon fills the middle of the frame, seen from the side and slightly below, "
        "swimming slowly from right to left. It spans most of the width of the picture. A single "
        "shaft of light from above falls along its back and lights the rows of bony scutes and the "
        "long flat snout; the four barbels are clearly visible hanging beneath it. Its eye catches "
        "a small highlight. The water behind it drops away into empty darkness."),

    # Rising to the light: the fish large, the emptiness still enormous.
    "endangered_b": WATER + (
        "ONE large sturgeon rises slowly towards the bright surface, seen from below and to one "
        "side, its pale belly and the underside of the flat snout lit from above and the four "
        "barbels hanging clear. It is big in the frame and close to the camera, its tail towards "
        "the lower corner, the bright surface far above it and the whole rest of the picture empty "
        "dark water. A silhouette of scutes along the raised back."),

    # The original composition, corrected: the emptiness kept, the fish brought forward.
    "endangered_c": WATER + (
        "A wide, quiet, almost empty picture of deep open water crossed by pale shafts of light - "
        "and ONE sturgeon, alone, swimming unhurried across the lower middle of the frame, close "
        "enough to the camera to be read completely: flat snout, four barbels, armoured rows of "
        "scutes, upswept tail. Around and above it there is nothing at all but water and light. "
        "The animal is the subject and the emptiness is the story."),

    # The head alone: the most certain way to prove it is a sturgeon.
    "endangered_d": WATER + (
        "A close portrait of ONE sturgeon's head and shoulders filling the frame, angled slightly "
        "towards the camera: the long flat pointed snout leading, the FOUR BARBELS hanging clearly "
        "beneath it in front of the low mouth, the small dark eye set far back, the first bony "
        "scutes rising along the back behind the head. Soft light from above, the body fading into "
        "darkness behind. Intimate, ancient and a little sad."),
}


if __name__ == "__main__":
    wanted = sys.argv[1:] or list(TAKES)
    for name in wanted:
        print(name, flush=True)
        gen(RULES + TAKES[name], OUT + name + ".png", aspect="4:3")
