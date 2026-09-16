"""Fujie 和 - the sturgeon as a motif in traditional Japanese craft.

These are not the official mascot illustration. They are the real fish drawn the
way Japanese craft has always drawn carp, cranes and waves: woodblock, rinpa
gold leaf, maki-e lacquer, sometsuke porcelain, indigo dye. On a finished
product the official artwork would be used unmodified; this line shows the
craft language it would sit in.
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen

REF = "D:/Fuji_Famous/Documents_for_dev/05_fujie_絵柄例.png"
OUT = "D:/Fuji_Famous/Fujie_Creative/10_merch_wa/"

FISH = (
    "The attached image shows the fish this motif is based on: a sturgeon (Acipenser) with a long "
    "flat pointed snout, four barbels hanging beneath it, five rows of bony scutes along the body, a "
    "small eye set high and forward, a large sweeping upper tail lobe. Keep that silhouette and "
    "those features exactly - it must always read as a sturgeon, never a carp, never a koi, never a "
    "dolphin, never a shark. Do NOT copy the chrome rendering: redraw the fish in the traditional "
    "medium described below.\n\n"
)

CRAFT = (
    "Authentic traditional Japanese craft, photographed or reproduced faithfully, no modern "
    "graphic-design gloss, no cartoon styling, no big shiny cartoon eye.\n\n"
    "*** TEXT RULE ***\n"
    "No text anywhere unless it is a small red seal-shaped stamp. No words in any language, no "
    "invented kanji, no signature lines, no captions.\n\n"
)

JOBS = [
    ("An EDO-PERIOD UKIYO-E WOODBLOCK PRINT: a single great sturgeon riding the curl of a huge "
     "breaking wave, the wave drawn with the clawed foam fingers of classical Japanese prints, "
     "Prussian blue and indigo gradations, a pale dawn sky with bokashi shading, visible woodgrain "
     "and the soft fibre of aged washi paper, flat areas of colour with fine keyblock outlines.",
     "wa_ukiyoe_wave.png", "4:3"),
    ("A RINPA GOLD-LEAF BYOBU FOLDING SCREEN, four panels, seen straight on: gold leaf ground with "
     "visible leaf seams, stylised silver water in flowing parallel lines and swirling whirlpools, "
     "two sturgeon swimming among them in ink and soft mineral pigment, a few malachite-green "
     "water plants at the lower edge.",
     "wa_byobu_screen.png", "16:9"),
    ("A MAKI-E LACQUER BOX on a dark cloth: deep black urushi lacquer, a sturgeon and concentric "
     "water rings rendered in gold and silver powder with raised takamaki-e detail, a fine gold rim "
     "line, the lid slightly offset to show the vermilion lacquer interior. Museum-quality close "
     "product photography with soft reflections.",
     "wa_makie_box.png", "4:3"),
    ("SOMETSUKE ARITA PORCELAIN: a set of three pieces on a pale linen cloth - a large shallow plate, "
     "a small dish and a sake cup - each painted in cobalt blue underglaze with a sturgeon swimming "
     "among seigaiha wave scales, fine brushwork, slight bleeding of the blue into the glaze, a "
     "warm white body with a glassy surface.",
     "wa_arita_porcelain.png", "4:3"),
    ("A KIMONO OBI TEXTILE photographed close and flat: woven silk in deep indigo with a field of "
     "seigaiha wave arcs in silver and pale blue thread, and sturgeon woven in gold and cream thread "
     "swimming diagonally across it. Visible weave structure and thread sheen, raking light.",
     "wa_obi_textile.png", "16:9"),
    ("An INDIGO-DYED NOREN curtain hanging in a wooden doorway, split into two panels: traditional "
     "aizome deep indigo with the sturgeon and concentric ripples reserved in undyed white by "
     "katazome stencil dyeing, slight irregularity in the dye, soft daylight from the room beyond, "
     "the linen gently moving.",
     "wa_noren_indigo.png", "4:3"),
    ("A SUMI-E HANGING SCROLL (kakejiku) on a plain plaster wall: a single sturgeon in fluid black "
     "ink on aged cream paper, one or two bold wet brushstrokes suggesting the current beneath it, "
     "enormous empty space, a narrow indigo silk mounting border, a wooden roller at the bottom, one "
     "small square red seal.",
     "wa_sumie_scroll.png", "3:4"),
    ("A TEA SETTING on a dark wooden table: a black lacquer tray bearing a small cast-iron kettle "
     "with a sturgeon and ripple relief in the iron, two celadon cups, and a folded indigo cloth "
     "with a small white sturgeon stencil. Quiet natural side light, wabi-sabi restraint.",
     "wa_tea_setting.png", "4:3"),
]

for prompt, name, aspect in JOBS:
    r = gen(FISH + CRAFT + prompt, OUT + name, refs=[REF], aspect=aspect)
    print(json.dumps({"job": name, "ok": not isinstance(r, dict),
                      "r": r if isinstance(r, dict) else "saved"}, ensure_ascii=False), flush=True)
