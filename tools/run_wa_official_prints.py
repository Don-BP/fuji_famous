"""Redo the three paper pieces where the official Fujie looked stuck on.

The craft line reproduces the official illustration exactly - that is the
whole point of the "official" shelf, and Article 7 of the character manual
requires it. On gold leaf, lacquer, silver thread and underglaze that works:
those media carry a supplied artwork as a bright applied inlay, so a crisp
metallic fish is what a real workshop would hand back.

On paper it did not. The first prompts asked for the fish "metallic and
precise against the flat woodblock colour", "as though a modern plate had
been printed over an old block" - and got exactly that: a glossy 3D fish
floating above a flat print, with its own lighting and a cut-out edge.

So these three ask for the opposite relationship. The fish is cut as one of
the blocks and pulled in the same run as the rest: same inks, same paper,
same registration, same ageing. Nothing about the fish itself changes -
silhouette, proportions, direction, scutes, barbels, eye and tail are all
held exactly as the official artwork draws them. What changes is that the
sheet is printing it rather than carrying it.

Candidates land in a cand/ folder beside each target so the originals stay
put until one is chosen.

Output: Fujie_Creative/14_merch_wa_official/cand/
        Fujie_Creative/19_fujisan/wa_official/cand/
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen

OFFICIAL = "D:/Fuji_Famous/Documents_for_dev/05_fujie_絵柄例.png"
WAO = "D:/Fuji_Famous/Fujie_Creative/14_merch_wa_official/cand/"
FUJI = "D:/Fuji_Famous/Fujie_Creative/19_fujisan/wa_official/cand/"

TAKES = 3          # candidates per piece, picked by eye afterwards

LOCK = (
    "The attached image is the OFFICIAL illustration of 'Fujie', Fujikin's sturgeon mascot: a "
    "polished silver sturgeon in profile, long flat pointed snout, four barbels beneath it, five "
    "rows of pale bony scutes along the body, a small dark eye set high and forward, a large "
    "swept tail.\n\n"
    "*** SHAPE RULE - CRITICAL ***\n"
    "Keep this exact fish: same silhouette, same proportions, same snout length, the same four "
    "barbels, the same five rows of scutes, the same small high eye, the same tail. Do NOT "
    "restyle it as a carp or a koi, do not give it a big cartoon eye, do not add or remove fins.\n"
    "IT FACES RIGHT. The snout and barbels are at the RIGHT-HAND side of the fish and the tail is "
    "at the LEFT, exactly as in the attached artwork. Never mirror it.\n\n"
    "*** MEDIUM RULE - EVEN MORE CRITICAL ***\n"
    "The fish is NOT a modern picture placed on top of an old one. It was cut as one of the "
    "blocks and pulled in the same run as everything else on the sheet. That means it obeys the "
    "sheet completely:\n"
    "- the same ink and the same limited palette as the rest of the print, in its own cool "
    "silver-greys - flat printed colour, no photographic gloss, no chrome highlights, no "
    "airbrushed gradients, no 3D shading\n"
    "- the same keyblock outline weight as every other shape in the image, with the small breaks "
    "and thick-thin variation a cut line has\n"
    "- the same slight off-register colour edges, the same ink absorption, the same bokashi "
    "gradation where the printer would have wiped one\n"
    "- the paper grain and washi fibre show THROUGH it exactly as they show through the rest\n"
    "- the same age, the same foxing, the same soft paper light. No drop shadow, no cut-out "
    "edge, no glow, nothing that lifts the fish off the sheet.\n"
    "If the fish looks shinier, smoother, sharper or newer than the water around it, it is "
    "WRONG. It must look printed, not pasted.\n\n"
    "*** NO SIGNATURE, NO QUOTATION ***\n"
    "One small red seal-shaped stamp is allowed. NOTHING else: no signature "
    "cartouche, no black brushed characters, no title slip, no publisher mark, no writing of any "
    "kind. A signature would read as the work of a real historical artist, which this is not.\n"
    "Compose the scene fresh. NO BOATS, no rowers, no people, no buildings. Do not reproduce the "
    "framing or the arrangement of any famous existing print.\n\n"
)

JOBS = [
    (WAO + "wao_ukiyoe.png", "4:3",
     "AN EDO-PERIOD UKIYO-E WOODBLOCK PRINT on washi, composed freshly for this project: a great "
     "breaking wave with clawed foam fingers in Prussian blue and indigo bokashi gradations, a "
     "pale dawn sky, reeds at the left bank - and Fujie swimming through the trough of the wave, "
     "cut and printed in cool silver-greys as part of the same block set. Visible woodgrain and "
     "paper fibre across the whole sheet, the fish included. Do not copy the framing of any "
     "existing famous print."),

    (WAO + "wao_scroll.png", "3:4",
     "A HANGING SCROLL (kakejiku) on a plain plaster wall: aged cream paper, an indigo silk "
     "mounting border, a wooden roller at the foot, one small square red seal, enormous empty "
     "space. On the paper, two or three bold wet sumi brushstrokes suggest a current, and Fujie "
     "swims along them - painted by the same hand, in the same session, in sumi ink and a little "
     "silver pigment: the ink pools and drags at the edges of the fish exactly as it does in the "
     "brushstrokes, the paper drinks it the same way, the dry-brush breaks match. The fish is "
     "part of the painting, not mounted on it."),

    (FUJI + "wao_fuji_ukiyoe.png", "4:3",
     "AN EDO-PERIOD UKIYO-E WOODBLOCK PRINT on washi, composed freshly for this project: a large "
     "breaking wave in Prussian blue and indigo gradations with clawed foam fingers, and beyond "
     "the water a LOW, WIDE, snow-capped Mount Fuji, small and serene under a pale bokashi sky. "
     "Mount Fuji is a low wide calm cone - the base roughly three times as wide as the mountain "
     "is tall, long shallow concave slopes, a slightly flattened summit, the snow a soft "
     "scalloped band across the top third. Never a tall sharp triangle. Fujie swims in the "
     "foreground water, cut and printed in cool silver-greys as part of the same block set, the "
     "paper fibre showing through. Do not copy the framing of any existing famous print."),
]

only = sys.argv[1] if len(sys.argv) > 1 else None

for out, aspect, prompt in JOBS:
    if only and only not in out:
        continue
    for take in range(1, TAKES + 1):
        p = pathlib.Path(out)
        dest = p.with_name("%s_take%d%s" % (p.stem, take, p.suffix))
        r = gen(LOCK + prompt, str(dest), refs=[OFFICIAL], aspect=aspect)
        print(json.dumps({"job": dest.name, "ok": not isinstance(r, dict),
                          "r": r if isinstance(r, dict) else "saved"},
                         ensure_ascii=False), flush=True)
