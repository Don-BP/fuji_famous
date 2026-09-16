"""A painted UI kit: illustrated banners for each mini-game row, plate art for the
buttons, a framed panel for the modal sheets, and a steel gauge track.

Plates are built to be stretched (buttons, gauges) or 9-sliced (the panel frame),
so they scale without the artwork distorting.
"""
import json, pathlib, shutil, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen
from cutout import cutout
from PIL import Image

M = "D:/Fuji_Famous/Fujie_Creative/01_character/master_v3_wave.png"
OUT = pathlib.Path("D:/Fuji_Famous/Fujie_Creative/06_game/")
SITE = pathlib.Path("D:/Fuji_Famous/site/art/")

BANNER = (
    "A wide painterly banner tile for a Japanese mobile game menu row. Deep underwater palette "
    "locked to #04121A, #07202B, #103544, #1D5566 with cool cyan #3FB6EE accents and pale silver "
    "#BFCFD6 highlights. Cinematic and atmospheric, with a soft dark vignette down the LEFT half "
    "of the frame so white caption text stays readable there.\n"
    "ABSOLUTE RULES: NO text, letters, numbers, logos or watermarks. NO user interface elements. "
    "The subject sits in the RIGHT half of the frame; the LEFT half is quiet dark water.\n\n"
)

PLATE = (
    "A single clean mobile-game UI element, drawn flat-on and perfectly symmetrical, filling the "
    "whole frame edge to edge with no margin around it. Crisp vector game-UI art with a bold dark "
    "navy outline and polished surfaces.\n"
    "ABSOLUTE RULES: NO text, letters, numbers, icons, logos or watermarks anywhere. The middle "
    "of the shape is completely EMPTY and UNDECORATED so a caption can be printed over it. "
    "Nothing else in the frame, no background scenery, no shadow outside the shape.\n\n"
)

JOBS = [
    # ---------- one illustrated banner per mini-game row ----------
    (BANNER + "Subject, on the right: a cluster of glossy dark sturgeon eggs with warm amber-gold "
     "sheen tumbling down through dim water into an open pearl-white scallop shell waiting below, "
     "with a few bubbles and a soft golden glow around the eggs.",
     "row_egg.png", "16:9"),
    (BANNER + "Subject, on the right: two dark round burrow holes in a murky rocky riverbed, with "
     "the pale grey dorsal fin and snout of a small cartoon shark just rising out of one of them, "
     "a ring of water splash around it, lit from above in cold cyan.",
     "row_shark.png", "16:9"),
    (BANNER + "Subject, on the right: a narrow river gorge of dark craggy rock pillars with fast "
     "white-cyan current streaks and trails of bubbles rushing between them from right to left, "
     "giving a strong sense of speed.",
     "row_race.png", "16:9"),
    (BANNER + "Subject, on the right: three closed pearl-white scallop shells resting in a row on "
     "pale rippled sand, with a warm golden glow leaking out from beneath the middle one and soft "
     "cyan caustic light playing across the sand.",
     "row_shell.png", "16:9"),

    # ---------- button and panel plates ----------
    (PLATE + "Subject: a wide horizontal PILL-SHAPED BUTTON with fully rounded ends, filling the "
     "frame from edge to edge. Bright cyan #3FB6EE face with a smooth glossy highlight sweeping "
     "across the upper half, a thin polished chrome-silver rim, and a soft cyan glow beneath it. "
     "Premium, tactile, like a physical button. Its centre is a clean empty cyan surface.",
     "ui_btn.png", "16:9"),
    (PLATE + "Subject: a wide horizontal PILL-SHAPED BUTTON with fully rounded ends, filling the "
     "frame from edge to edge. Dark slate blue-black face like brushed gunmetal, a thin brushed "
     "stainless steel rim catching a faint cool highlight along the top edge, understated and "
     "secondary. Its centre is a clean empty dark surface.",
     "ui_btn_ghost.png", "16:9"),
    (PLATE + "Subject: a horizontal ROUNDED RECTANGULAR CARD filling the frame edge to edge - a "
     "dark slate blue-green face with a faint watery sheen, framed by a thin brushed stainless "
     "steel bevel with a tiny rivet in each of the four corners. Industrial, precise and premium, "
     "like a piece of Japanese instrument housing. Its centre is a clean empty dark surface.",
     "ui_row.png", "16:9"),
    (PLATE + "Subject: a tall ROUNDED RECTANGULAR PANEL FRAME filling the frame edge to edge - a "
     "deep dark blue-black face, framed all the way around by a brushed stainless steel bevelled "
     "border of even thickness on all four sides, with a small rivet in each corner and a thin "
     "inner cyan pinstripe just inside the steel. The entire middle is flat, empty and "
     "undecorated. The border is exactly the same width top, bottom, left and right.",
     "ui_panel.png", "3:4"),
    (PLATE + "Subject: a long, thin, horizontal empty GAUGE TRACK filling the width of the frame - "
     "a shallow rounded capsule groove in dark slate, recessed with a soft inner shadow along its "
     "top edge and a thin brushed steel rim around it, like an empty instrument gauge waiting to "
     "be filled. Completely empty inside, no fill, no markings.",
     "ui_gauge.png", "16:9"),
]

for prompt, name, aspect in JOBS:
    dest = str(OUT / name)
    r = gen(prompt, dest, refs=[M], aspect=aspect)
    ok = not isinstance(r, dict)
    if ok:
        im = Image.open(dest)
        if name.startswith("ui_"):
            cutout(dest)                      # plates keep transparent corners
            im = Image.open(dest)
            cap = 520
            if max(im.size) > cap:
                s = cap / max(im.size)
                im = im.resize((round(im.width*s), round(im.height*s)), Image.LANCZOS)
            im.convert("RGBA").quantize(colors=200, method=Image.FASTOCTREE).save(
                dest, "PNG", optimize=True)
            shutil.copy(dest, SITE / name)
        else:
            if max(im.size) > 900:
                s = 900 / max(im.size)
                im = im.resize((round(im.width*s), round(im.height*s)), Image.LANCZOS)
            im.convert("RGB").save(str(SITE / name.replace(".png", ".jpg")),
                                   "JPEG", quality=80, optimize=True, progressive=True)
    print(json.dumps({"out": name, "ok": ok}), flush=True)
print("DONE", flush=True)
