"""The craft line again, this time carrying the OFFICIAL Fujie artwork.

Fujie_Creative/10_merch_wa/ shows what happens when a traditional craft draws a
sturgeon itself. This set keeps the same media - gold leaf, urushi, indigo,
underglaze blue, woven silk - but the fish on the object is the official
illustration, reproduced exactly, the way a workshop would transfer, inlay or
stencil a supplied artwork.

Output: Fujie_Creative/14_merch_wa_official/
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen

OFFICIAL = "D:/Fuji_Famous/Documents_for_dev/05_fujie_絵柄例.png"
OUT = "D:/Fuji_Famous/Fujie_Creative/14_merch_wa_official/"

LOCK = (
    "The attached image is the OFFICIAL illustration of 'Fujie', Fujikin's sturgeon mascot: a "
    "realistic polished chrome-silver sturgeon in profile, long flat pointed snout, four barbels "
    "beneath it, five rows of pale bony scutes, a small dark eye set high and forward, a large "
    "swept tail.\n\n"
    "*** ARTWORK RULE - CRITICAL ***\n"
    "Reproduce this illustration EXACTLY as drawn on the object: same silhouette, same proportions, "
    "same direction, same metallic rendering. Do NOT redraw it as a brush painting, do not "
    "stylise it, do not cartoon it, do not give it a large eye or a smile, do not make it a carp or "
    "a koi. It appears as a transferred, inlaid, stencilled or foil-applied reproduction of this "
    "exact artwork, sitting inside a hand-made traditional object.\n\n"
    "No text anywhere except, at most, one small red seal-shaped stamp.\n\n"
)

JOBS = [
    ("A RINPA GOLD-LEAF FOLDING SCREEN, four panels, seen straight on: gold leaf ground with visible "
     "leaf seams, stylised silver water in flowing parallel lines and whirlpools painted across it, "
     "and the official Fujie applied large across two panels in silver leaf and fine metallic "
     "pigment, swimming through the water lines.",
     "wao_byobu.png", "16:9"),
    ("A BLACK URUSHI LACQUER BOX on dark cloth: deep glossy black lacquer, concentric water rings in "
     "gold maki-e powder radiating across the lid, and the official Fujie inlaid across the centre "
     "in polished silver and mother-of-pearl, a fine gold rim line, the lid slightly offset showing "
     "a vermilion interior.",
     "wao_makie_box.png", "4:3"),
    ("An INDIGO-DYED NOREN hanging in a wooden doorway, split into two panels: deep aizome indigo "
     "with concentric ripple rings reserved in undyed white, and the official Fujie reserved in "
     "white across the upper half by katazome stencil dyeing. Soft daylight from the room beyond.",
     "wao_noren.png", "4:3"),
    ("A SOMETSUKE ARITA PORCELAIN PLATE lying on pale linen beside a small dish: warm white glaze, a "
     "cobalt-blue seigaiha wave border hand-painted around the rim, and the official Fujie applied "
     "across the centre as a fine blue underglaze transfer print, slight bleeding into the glaze.",
     "wao_porcelain.png", "4:3"),
    ("A WOVEN SILK OBI photographed close and flat: deep indigo ground with silver and pale blue "
     "wave arcs woven across it, and the official Fujie woven large in silver and cream thread "
     "swimming diagonally through them. Visible weave structure, thread sheen, raking light.",
     "wao_obi.png", "16:9"),
    ("A HANGING SCROLL (kakejiku) on a plain plaster wall: aged cream paper with two or three bold "
     "wet sumi brushstrokes suggesting a current, and the official Fujie mounted across them, "
     "reproduced exactly, an indigo silk mounting border, a wooden roller at the foot, one small "
     "square red seal, enormous empty space.",
     "wao_scroll.png", "3:4"),
    ("A TEA SETTING on a dark wooden table: a black lacquer tray, a small cast-iron kettle with "
     "concentric ripple rings cast into the iron and the official Fujie inlaid on its side in "
     "silver, two celadon cups, and a folded indigo cloth. Quiet natural side light.",
     "wao_tea_setting.png", "4:3"),
    ("A WOODBLOCK-PRINT POSTER on washi paper: a great breaking wave with clawed foam fingers in "
     "Prussian blue and indigo bokashi gradations, pale dawn sky, visible woodgrain and paper fibre "
     "- and the official Fujie printed across the wave exactly as drawn, in its own metallic greys, "
     "so the modern artwork sits inside the old print.",
     "wao_ukiyoe.png", "4:3"),
]

for prompt, name, aspect in JOBS:
    r = gen(LOCK + prompt, OUT + name, refs=[OFFICIAL], aspect=aspect)
    print(json.dumps({"job": name, "ok": not isinstance(r, dict),
                      "r": r if isinstance(r, dict) else "saved"}, ensure_ascii=False), flush=True)
