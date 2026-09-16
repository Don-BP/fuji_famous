"""A calm swimming Chibi Fujie for the roaming buddy on the site.

The happy, star-covered pose already exists (site/art/fujie_cheer.png) and is
used only for the moment the cursor touches him. This is the face he wears the
rest of the time.
"""
import json, pathlib, subprocess, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen

M = "D:/Fuji_Famous/Fujie_Creative/01_character/master_v3_wave.png"
CHEER = "D:/Fuji_Famous/site/art/fujie_cheer.png"
OUT = "D:/Fuji_Famous/Fujie_Creative/01_character/chibi_neutral.png"

PROMPT = (
    "TWO images are attached. IMAGE 1 is the LOCKED master design of 'Chibi Fujie'. IMAGE 2 is the "
    "same character in a happy pose - match IMAGE 2's drawing style, line weight, colour and "
    "FACING DIRECTION exactly.\n\n"
    "Draw the SAME character in a CALM NEUTRAL swimming pose: body held level and relaxed in a "
    "gentle three-quarter view, pectoral fins out to the sides as if gliding, tail relaxed, mouth "
    "closed in a small soft neutral line - not grinning, not frowning, not open - one large glossy "
    "black eye open normally with its white catchlight. Calm and content, doing nothing in "
    "particular.\n\n"
    "*** DO NOT INCLUDE ***\n"
    "No stars, no sparkles, no blush, no motion lines, no bubbles, no shadow, no props, no text.\n\n"
    "*** CHARACTER RULES ***\n"
    "Polished chrome-silver body, pale silver belly, long flat pointed snout, four barbel whiskers "
    "under the snout, a row of rounded scute bumps along the back, crescent tail, bold dark navy "
    "outline, flat cel shading with crisp white highlights.\n"
    "NO legs, NO feet, NO toes. Only fins: two pectoral fins at the sides, small pelvic fins near "
    "the tail, a dorsal fin and the crescent tail. Every fin is thin and swept backward. The belly "
    "line stays smooth and continuous.\n\n"
    "Centre the character on a PURE FLAT WHITE background with clear white margin all around it, "
    "nothing else in the frame."
)

r = gen(PROMPT, OUT, refs=[M, CHEER], aspect="1:1")
print(json.dumps({"ok": not isinstance(r, dict)}, ensure_ascii=False), flush=True)
if not isinstance(r, dict):
    subprocess.run([sys.executable, "D:/Fuji_Famous/tools/cutout.py", OUT], check=False)
