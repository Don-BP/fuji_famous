"""Generate all game art: title screen, four mini-game backgrounds, every sprite,
and a refreshed character turnaround based on master_v3_wave.

Sprites are generated on white, cut out to transparent PNG, then downscaled.
Backgrounds are generated portrait (the game is a phone column) and left opaque.
"""
import json, pathlib, shutil, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen
from cutout import cutout
from PIL import Image

CHAR = "D:/Fuji_Famous/Fujie_Creative/01_character/"
M = CHAR + "master_v3_wave.png"
OUT = pathlib.Path("D:/Fuji_Famous/Fujie_Creative/06_game/")
SITE = pathlib.Path("D:/Fuji_Famous/site/art/")
OUT.mkdir(parents=True, exist_ok=True)
SITE.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- style blocks

CHAR_STYLE = (
    "Match the art style of the attached reference character EXACTLY: the same chibi sturgeon "
    "mascot, bold dark navy outline, flat cel shading, polished chrome-silver body with a pale "
    "silver belly, crisp white specular highlights and small white sparkle stars, clean "
    "vector-like Japanese mascot illustration.\n"
    "CHARACTER RULES - these are absolute:\n"
    "  * Long flat paddle-shaped snout (rostrum) extending well past the mouth.\n"
    "  * Four thin barbel whiskers hanging under the snout.\n"
    "  * A row of rounded scute bumps running along the back.\n"
    "  * FINS ONLY. No legs, no feet, no hands, no arms. The pectoral fins are thin and "
    "swept backward along the body.\n"
    "  * One large round black eye with a white catchlight. Friendly closed smile.\n"
    "Render on a PURE WHITE background, no text, no logo, no watermark, no cast shadow, "
    "nothing else in the frame.\n\n"
)

PROP_STYLE = (
    "Match the art style of the attached reference image: bold dark navy outline, flat cel "
    "shading, polished chrome-silver surfaces, crisp white specular highlights, clean "
    "vector-like Japanese mobile-game asset.\n"
    "Render on a PURE WHITE background, centred, no text, no logo, no watermark, no cast "
    "shadow, nothing else in the frame.\n\n"
)

BG_STYLE = (
    "A painterly vertical background plate for a Japanese mobile game. Deep underwater river "
    "scene. Palette locked to dark teal and navy: #04121A, #07202B, #103544, #1D5566, with "
    "cool cyan #3FB6EE light accents and pale silver #BFCFD6 highlights. Soft, atmospheric, "
    "slightly hazy, gentle vignette toward the edges so bright UI text stays readable on top.\n"
    "ABSOLUTE RULES: NO characters. NO fish. NO creatures. NO people. NO text, letters, "
    "numbers, logos, watermarks or UI elements. Empty scenery only. The centre of the frame "
    "must stay visually calm and uncluttered.\n\n"
)

# ------------------------------------------------------------------- the jobs
# (prompt, filename, refs, aspect, is_sprite)

JOBS = [
    # ---------- character sheet ----------
    (
        CHAR_STYLE
        + "Subject: a five-view MODEL SHEET TURNAROUND of this exact character, drawn at the "
        "SAME height and the SAME scale across the whole row, evenly spaced, standing upright "
        "in a neutral pose with fins relaxed at the sides.\n"
        "Left to right the five views are: 1) FRONT view facing the viewer, the flat snout "
        "pointing straight at the camera and foreshortened, barbels hanging down. 2) THREE-"
        "QUARTER FRONT view turned to the left. 3) FULL SIDE PROFILE facing left, showing the "
        "complete snout length and the full row of back scutes. 4) THREE-QUARTER REAR view. "
        "5) BACK view from directly behind, showing the row of scutes running down the spine "
        "and the tail.\n"
        "Thin pale grey horizontal guide lines run across the sheet at the top of the head, "
        "the eye line and the base of the body. All five drawings sit on the same guide lines.",
        "master_turnaround.png", [M], "16:9", False,
    ),

    # ---------- title screen ----------
    (
        CHAR_STYLE
        + "Subject: a HERO TITLE-SCREEN POSE of this character. He is bursting joyfully up out "
        "of the water toward the viewer, body angled diagonally, head turned slightly toward "
        "the camera, one pectoral fin raised in a big cheerful wave. Bright confident smile, "
        "eye sparkling. A ring of water droplets and a few white sparkle stars burst around "
        "him. Dynamic, energetic, poster-worthy. Slightly larger and more detailed than a "
        "normal pose.",
        "title_fujie.png", [M], "1:1", True,
    ),
    (
        BG_STYLE
        + "Scene: looking up from just below the surface of a clear deep river at dawn. Broad "
        "shafts of pale cyan light spear down from a rippling silver surface at the top of the "
        "frame into darkness at the bottom. Fine bubbles drift upward. A soft cloud of tiny "
        "out-of-focus light motes. Majestic and hopeful.",
        "bg_title.png", None, "3:4", False,
    ),

    # ---------- 1. egg catch ----------
    (
        CHAR_STYLE
        + "Subject: this character seen FROM THE FRONT, facing the viewer, holding up a large "
        "open scallop shell in front of his chest like a bowl or a basket, ready to catch "
        "something falling from above. The shell is held level, its open hollow side facing "
        "straight up at the camera so you can see into it. He grips the shell's edges with "
        "both pectoral fins - fins pressed against the shell, NOT hands, NOT arms, NOT "
        "fingers. He is looking up and slightly toward the viewer with a bright eager "
        "expression, mouth open in a happy grin.\n"
        "The scallop shell is a chunky ribbed fan-shaped shell in pale pearl white and soft "
        "silver with a dark navy outline matching the character.\n"
        "Full body, upright, centred.",
        "fujie_shell.png", [M], "1:1", True,
    ),
    (
        PROP_STYLE
        + "*** DRAW ONLY A SINGLE EGG. NO FISH. NO FACE. NO CHARACTER. ONE SPHERE ALONE. ***\n"
        "Subject: one single grain of sturgeon caviar - a perfectly round glossy sphere in "
        "deep charcoal grey with a warm amber-gold pearlescent sheen across the lower half and "
        "one crisp white specular highlight at the upper left. It glows very faintly, as if "
        "precious. Bold dark navy outline. Centred and alone.",
        "roe_egg.png", [M], "1:1", True,
    ),
    (
        BG_STYLE
        + "Scene: a calm dim hatchery pool seen from the side. A smooth dark silt floor runs "
        "across the bottom third of the frame. Above it, open dark water with a few thin pale "
        "cyan light beams falling from above and a scatter of drifting bubbles. The upper two "
        "thirds of the frame are almost empty open water.",
        "bg_egg.png", None, "3:4", False,
    ),

    # ---------- 2. whack-a-shark ----------
    (
        PROP_STYLE
        + "Subject: a cartoon SHARK bursting straight up out of the water toward the viewer, "
        "seen from the front and slightly above - head, gaping toothy mouth and both pectoral "
        "fins visible, body cut off at the bottom of the frame as if still emerging. Comic and "
        "goofy rather than frightening: oversized round eyes, a big silly grin full of blunt "
        "white triangular teeth, a tall dorsal fin. Body is slate grey-blue with a white "
        "belly, bold dark navy outline, flat cel shading, white specular highlights.\n"
        "It is clearly a SHARK, not a sturgeon: short blunt pointed snout, NO long flat "
        "paddle snout, NO barbel whiskers, NO scute bumps along the back.",
        "shark_pop.png", [M], "1:1", True,
    ),
    (
        CHAR_STYLE
        + "Subject: this character in a comic ANNOYED, FIRED-UP pose, seen in three-quarter "
        "view facing right. One pectoral fin is raised high above his head, cocked back ready "
        "to swing down and give something a good smack. Eyebrows furrowed into a determined "
        "scowl, mouth open in a shout, one puff of comic steam by his head. Playful and funny, "
        "not genuinely angry. Full body, upright.",
        "fujie_whack.png", [M], "1:1", True,
    ),
    (
        BG_STYLE
        + "Scene: a murky rocky riverbed floor filling the whole frame, seen from above at a "
        "slight angle. Dark craggy stones, patches of silt and a few strands of dark river "
        "weed around the outer edges. Low green-teal ambient light. The centre of the frame is "
        "a broad flat open patch of silt with nothing on it.",
        "bg_shark.png", None, "3:4", False,
    ),

    # ---------- 3. upstream dash ----------
    (
        CHAR_STYLE
        + "Subject: this character swimming HARD and FAST to the RIGHT, seen in full side "
        "profile with his snout pointing to the right edge of the frame. Body stretched out "
        "long and streamlined, tail mid-beat and slightly blurred with speed, pectoral fins "
        "swept tight back against the body. Eye narrowed in fierce determination, mouth set in "
        "a grim line, pushing against a current. A few white speed streaks and bubbles trail "
        "behind him to the left. Athletic and powerful.",
        "fujie_dash.png", [M], "1:1", True,
    ),
    (
        PROP_STYLE
        + "*** DRAW ONE ROCK PILLAR ONLY. NO FISH, NO CREATURE, NO FACE. ***\n"
        "Subject: a single tall narrow vertical column of craggy river rock, filling the full "
        "height of a tall thin frame from the very top edge to the very bottom edge. Dark "
        "slate blue-grey stone with sharp chiselled facets, pale cyan highlights along the "
        "left edges, and a little dark green river weed clinging to it. Bold dark navy "
        "outline. Flat cel shading. The rock touches both the top and bottom edges of the "
        "frame so it reads as a full-height pillar.",
        "rock_pillar.png", [M], "9:16", True,
    ),
    (
        BG_STYLE
        + "Scene: a fast river channel seen from the side. Sheer dark rock walls run along the "
        "far left and far right edges of the frame only. Between them, open rushing water "
        "filled with long soft horizontal streaks of pale cyan current and trails of small "
        "bubbles, giving a strong sense of sideways speed. The whole middle of the frame is "
        "open water.",
        "bg_race.png", None, "3:4", False,
    ),

    # ---------- 4. which shell ----------
    (
        PROP_STYLE
        + "*** DRAW ONE CLOSED SHELL ONLY. NO FISH, NO CREATURE, NO FACE, NO EYES. ***\n"
        "Subject: a single chunky CLOSED scallop shell resting on the ground, seen from the "
        "front and slightly above, like an upturned bowl. Fan shaped with bold deep ribs "
        "radiating out from a small hinge at the bottom. Pale pearl white and soft chrome "
        "silver with an iridescent sheen, a bold dark navy outline and a crisp white highlight "
        "sweeping across the upper left. Solid, heavy and hiding something. Centred and alone.",
        "shell_closed.png", [M], "1:1", True,
    ),
    (
        PROP_STYLE
        + "*** DRAW ONE PEARL ONLY. NO FISH, NO SHELL, NO FACE. ONE SPHERE ALONE. ***\n"
        "Subject: one perfectly round glowing pearl in warm cream and pale gold, with a soft "
        "golden halo of light around it, a crisp white specular highlight at the upper left "
        "and a faint rainbow iridescence across its surface. Bold dark navy outline. Precious "
        "and radiant. Centred and alone.",
        "pearl.png", [M], "1:1", True,
    ),
    (
        BG_STYLE
        + "Scene: a pale sandy riverbed seen from just above, filling the frame. Fine rippled "
        "sand in muted grey-taupe under cool cyan water light, with soft caustic light "
        "patterns playing across it and a few small pebbles and shell fragments scattered "
        "around the outer edges only. The wide centre band of the frame is clean empty "
        "rippled sand.",
        "bg_shell.png", None, "3:4", False,
    ),
]

# ------------------------------------------------------------------- run them

SPRITE_MAX = 700
BG_MAX = 1100


def shrink(path, cap):
    im = Image.open(path)
    if max(im.size) > cap:
        s = cap / max(im.size)
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    im.save(path, "PNG", optimize=True)
    return im.size


only = set(a for a in sys.argv[1:])
results = []
for prompt, name, refs, aspect, sprite in JOBS:
    if only and name not in only:
        continue
    dest = CHAR + name if name == "master_turnaround.png" else str(OUT / name)
    r = gen(prompt, dest, refs=refs, aspect=aspect)
    ok = not isinstance(r, dict)
    if ok:
        if sprite:
            cutout(dest)
        if name != "master_turnaround.png":
            shrink(dest, SPRITE_MAX if sprite else BG_MAX)
            shutil.copy(dest, SITE / name)
    results.append({"out": name, "ok": ok, "err": r.get("error", "")[:160] if not ok else ""})
    print(json.dumps(results[-1], ensure_ascii=False), flush=True)

print("DONE " + json.dumps({"ok": sum(1 for r in results if r["ok"]),
                            "fail": [r["out"] for r in results if not r["ok"]]}), flush=True)
