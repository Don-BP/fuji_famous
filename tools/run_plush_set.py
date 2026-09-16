"""The six-pose keychain assortment, built one pose at a time.

Asking for "six toys in six different poses" in a single picture has failed
twice: the model quietly repeats itself and one figure drifts back to the adult
fish. So each pose is photographed on its own - one toy, one instruction, a
flat grey sweep behind it - and the six are then cut out and laid onto a single
pale studio surface here. The model never gets to choose how many poses there
are, because it only ever sees one.

  python tools/run_plush_set.py            both sets, generate then compose
  python tools/run_plush_set.py water      just the water set
  python tools/run_plush_set.py fuji       just the Mount Fuji set
  python tools/run_plush_set.py --compose  re-lay the grid from what exists

Writes:
  Fujie_Creative/03_plushie/plush_mascot_set.png
  Fujie_Creative/19_fujisan/plush/plush_fuji_mascot_set.png
with the single poses kept beside them in poses/ (not published - build_site
only walks the top level of a gallery folder).
"""
import pathlib, shutil, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen, archive
from PIL import Image, ImageDraw
import numpy as np

SENTINEL = (255, 0, 255)
PAPER = (250, 249, 245)

REF = "D:/Fuji_Famous/Fujie_Creative/03_plushie/plush_keychain_lifestyle.png"
WATER_DIR = pathlib.Path("D:/Fuji_Famous/Fujie_Creative/03_plushie")
FUJI_DIR = pathlib.Path("D:/Fuji_Famous/Fujie_Creative/19_fujisan/plush")

LOCK = (
    "The attached photograph is the EXISTING 'Chibi Fujie' MASCOT KEYCHAIN - a small Japanese plush "
    "charm about 10cm long. This shot is THAT SAME manufactured toy. Do not redesign it, do not "
    "restyle it, do not invent a different mascot.\n"
    "Reproduce it exactly: satin-finish silver-grey plush with a soft pearlescent sheen, a pale "
    "ivory belly, a firmly-stuffed sewn snout, four fine cord barbel whiskers hanging under the "
    "snout, a row of small padded scute bumps along the back, ONE large glossy black embroidered "
    "eye with a single white catchlight, soft sewn pectoral fins, a dorsal fin and a crescent "
    "tail, neat visible seams, a small woven fabric tag near the tail, and a silver split ring "
    "and short chain at the top of the head.\n\n"
    "*** ABSOLUTE RULE: NO LEGS, NO FEET, NO TOES, NO STANDING NUBS. IT IS A FISH. ***\n"
    "*** COLOUR RULE: the body is ALWAYS silver-grey with a pale ivory belly. Never blue, navy, "
    "cyan, pink or any other hue. ***\n\n"
)

CHIBI = (
    "*** CHIBI PROPORTIONS - CRITICAL ***\n"
    "This is CHIBI FUJIE, the cute young form, and NOT the realistic adult Fujie.\n"
    "The head is HUGE - roughly one third of the whole length - and rounded. The single glossy "
    "black eye is large, about a quarter the height of the head. The body behind the head is "
    "SHORT, plump and stubby, tapering quickly into a small crescent tail. The snout is a short "
    "blunt paddle, not a long spike.\n"
    "NEVER render a long, slender, realistic sturgeon with a small eye, a long pointed snout and "
    "a stretched-out body. That is the other character and it does not belong here.\n\n"
)

SHOT = (
    "*** THE ONE THING THAT RUINS THIS SHOT ***\n"
    "Every previous attempt came back as the same polite toy sitting upright on its belly at a "
    "three-quarter angle with its head held high. That picture already exists six times over and "
    "is useless. Whatever the pose below says, COMMIT TO IT COMPLETELY and push it to the "
    "extreme - tip the toy right over, turn it upside down, lay it flat, take the camera "
    "overhead or round the back. If the result could be mistaken for a toy sitting calmly "
    "upright, it is wrong.\n\n"
    "PHOTOREALISTIC photography of a real object - a photograph, not a drawing or a render. The "
    "plush is soft fabric: satin pile catching the light, seams and stitch lines visible, a "
    "slight give where it is stuffed. No drawn outline, no cel shading, no cartoon linework.\n\n"
    "*** FRAMING RULE - READ TWICE ***\n"
    "EXACTLY ONE toy is in this picture. One. Not two, not a row, not a set, not a grid, not a "
    "contact sheet. The single toy is centred and fills most of the frame.\n"
    "The background is ONE FLAT EVEN MID-GREY - a plain neutral grey studio sweep of a single "
    "uniform tone, clearly darker than the silver plush. No gradient, no pattern, no horizon "
    "line, no table edge, no cast shadow falling on the background, no vignette.\n"
    "Nothing else is in the frame: no props, no hands, no packaging, no second charm, no "
    "furniture. Soft even studio light from the front left, gentle and shadowless.\n\n"
    "*** TEXT RULE ***\n"
    "NO WRITING OF ANY KIND anywhere in the picture - no captions, no labels, no numbers, no "
    "pose names, no slogans, no logos beyond the tiny woven tag already on the toy.\n\n"
    "*** TAIL RULE ***\n"
    "The CRESCENT TAIL FIN at the rear is clearly visible - two soft swept lobes sewn as one "
    "piece. The body never simply ends in a stump, and the dorsal fin on the back is never "
    "mistaken for the tail.\n\n"
)

CAP = (
    "*** THE CAP ***\n"
    "This one wears a small KNITTED MOUNT FUJI CAP pulled onto the top of its head: a LOW, WIDE, "
    "soft-blue knitted cone - the base about three times as wide as the cap is tall, slopes long "
    "and gently concave - finished with a cream bobbled snow band around the summit. Never a "
    "tall sharp triangle, never a party hat. The cap stays firmly on whatever the toy is doing, "
    "and the fish underneath is still silver-grey, never repainted blue.\n\n"
)

POSES = [
    ("headstand",
     "POSE - UPSIDE DOWN, BALANCED ON THE TIP OF ITS SNOUT: the toy is completely INVERTED, "
     "standing on its head. The tip of the flat snout is the only thing touching the ground; the "
     "whole plump body rises straight up above it like a skittle and the crescent tail waves at "
     "the very top of the frame. The single eye is near the bottom, upside down, looking pleased "
     "with itself. The pectoral fins are flung out sideways for balance and the chain hangs "
     "downward from the ring. A tall vertical upside-down silhouette."),

    ("sleep",
     "POSE - CURLED ASLEEP, SEEN FROM DIRECTLY ABOVE: a top-down shot looking straight down at "
     "the toy, which is curled into a CLOSED RING - the snout tucked right against the crescent "
     "tail so the plump body makes a complete letter O with an open hole through the middle. The "
     "single eye is a stitched closed curve, fast asleep. The row of padded scute bumps runs "
     "around the outside of the ring. A doughnut, not a fish lying straight."),

    ("bellyup",
     "POSE - FLAT ON ITS BACK, SEEN FROM DIRECTLY ABOVE: the camera looks straight down at the "
     "toy lying on its back on the floor, fast asleep and fully relaxed. The pale ivory BELLY "
     "fills the middle of the frame facing the lens, both pectoral fins flop out wide to the "
     "sides like a starfish, the head is tipped back with the snout pointing up at the camera and "
     "the crescent tail is spread flat at the bottom. A wide, flat, spread-out silhouette - "
     "nothing is upright and nothing is in profile."),

    ("dive",
     "POSE - DIVING NOSE-DOWN: the toy is caught head-first, the snout pointed steeply down at "
     "the ground and nearly touching it, the plump body rising diagonally behind, and the "
     "crescent tail lifted high and straight up at the top of the frame. The pectoral fins are "
     "swept back close along the body. A steep upright diagonal."),

    ("somersault",
     "POSE - MID-AIR SOMERSAULT, TUMBLING: the toy is well clear of the ground, caught halfway "
     "through a forward roll - the body TWISTED AND TIPPED OVER onto its side and rotated so the "
     "head is DOWN at the lower left and the tail is UP at the upper right, the whole toy lying "
     "along a steep diagonal and clearly not the right way up. The chain flies loose away from "
     "the head. A wide open gap of plain background under the whole body - nothing touches it, no "
     "stand, no hand, no wire. It reads instantly as tumbling through the air."),

    ("back",
     "POSE - SEEN FROM BEHIND, LOOKING BACK OVER ITS SHOULDER: the camera is behind the toy. What "
     "faces the lens is its BACK - the row of small padded scute bumps running away down the "
     "spine and the crescent tail nearest the camera, foreshortened. The head is turned sharply "
     "back over one shoulder so the single eye and the snout come into view in three-quarter "
     "profile. The pale ivory belly is hidden on the far side. The only shot taken from behind "
     "the toy, and it must read that way at a glance."),
]

MATCH = (
    "Edit the attached photograph. Return the SAME photograph with ONE thing added.\n\n"
    "ADD: a small knitted Mount Fuji cap on top of the plush toy's head - a LOW, WIDE, soft-blue "
    "knitted cone, the base about three times as wide as the cap is tall, slopes long and gently "
    "concave, finished with a cream bobbled snow band around the summit. Never a tall sharp "
    "triangle, never a party hat. It sits naturally on the plush, squashing the pile a little, "
    "following whatever tilt the head already has, lit by the same light as the rest of the "
    "picture.\n\n"
    "CHANGE NOTHING ELSE. Same toy, same pose, same camera angle, same crop and size in frame, "
    "same grey background, same shadow, same colours. Do not re-pose it, do not turn it toward "
    "the camera, do not straighten or lift the head, do not move the chain. If the toy is "
    "diving, curled up, seen from behind, lying on its side or in mid-air, it stays exactly that "
    "way. The fish stays silver-grey - only the cap is blue. No words anywhere.\n"
)

CHARM = (
    "\nA small flat FELT MOUNT FUJI CHARM - a low wide blue cone with a cream snow cap, about the "
    "size of the toy's head - hangs from the same split ring on a short chain and rests against "
    "the toy."
)

HOLD = (
    "CHANGE NOTHING ELSE. Same toy, same pose, same camera angle, same crop and size in the "
    "frame, same grey background, same shadow, same light, same big glossy black eye with its "
    "white catchlight, same cord whiskers, same chain. Do not re-pose it, do not turn it toward "
    "the camera, do not straighten or lift the head. If the toy is upside down, curled up, on "
    "its back, diving, tumbling or seen from behind, it stays exactly that way. No words "
    "anywhere in the picture.\n"
)

# --- the water line: six editions, one per pose ----------------------------
# Six silver fish on six grey squares read as one toy photographed six times,
# however hard the poses work. What tells a collection apart at a glance is
# that the toys themselves are different, so each pose is also its own edition.
TINTS = {
    "water": {
        "headstand": None,          # the standard edition, left as shot

        "sleep":
        "RECOLOUR the plush body: it is now DEEP INDIGO BLUE satin with the same pearlescent "
        "sheen, and a fine WHITE SEIGAIHA WAVE PATTERN - the traditional Japanese repeating "
        "fan-shaped wave - is printed across its back and flanks. The belly stays pale ivory, the "
        "fins and tail are indigo.\n",

        "bellyup":
        "RECOLOUR the plush body: it is now soft pale BLUSH PINK satin with the same pearlescent "
        "sheen, with a light scatter of small deeper-pink SAKURA PETALS printed over it. The "
        "belly stays cream.\n",

        "dive":
        "RECOLOUR the plush body: it is now soft MATCHA GREEN satin with the same pearlescent "
        "sheen - a calm, slightly dusty tea green, never bright or neon. The belly stays cream.\n",

        "somersault":
        "RECOLOUR the plush body: it is now CHAMPAGNE GOLD satin with a warm metallic sheen - the "
        "40th anniversary edition. The belly stays pale ivory and the little woven tag by the "
        "tail is gold rather than natural linen.\n",

        "back":
        "RECOLOUR the plush body: it is now deep glossy near-BLACK satin with a faint charcoal "
        "pearl sheen - the caviar edition. The belly stays pale pearl ivory so the shape still "
        "reads clearly.\n",
    },
    # the Fuji line keeps the silver fish; the knitted cap is what changes
    "fuji": {
        "headstand": "SOFT SKY BLUE with a cream bobbled snow band - the standard edition",
        "sleep": "DEEP VERMILION RED with a cream bobbled snow band - the aka-fuji, the mountain "
                 "lit red at sunrise",
        "bellyup": "SOFT DAWN PINK with a cream bobbled snow band - the sunrise edition",
        "dive": "FRESH SUMMER GREEN with a cream bobbled snow band - the summer edition, the "
                "mountain with its snow nearly gone",
        "somersault": "CHAMPAGNE GOLD with a cream bobbled snow band - the anniversary edition",
        "back": "DARK INDIGO NAVY with a cream bobbled snow band - the night edition",
    },
}

SETS = {
    "water": dict(dir=WATER_DIR, out="plush_mascot_set.png", extra="", charmed=()),
    "fuji": dict(dir=FUJI_DIR, out="plush_fuji_mascot_set.png", extra=CAP,
                 charmed=("back", "somersault"), after="water"),
}


def editions(which, keys=None):
    """Turn each pose photograph into its own edition of the keychain."""
    cfg = SETS[which]
    pdir = cfg["dir"] / "poses"
    edir = pdir / "ed"
    edir.mkdir(parents=True, exist_ok=True)
    for key, _ in POSES:
        if keys and key not in keys:
            continue
        src = pdir / ("%s_%s.png" % (which, key))
        if not src.exists():
            print("  ! shoot the poses first - missing " + src.name)
            continue
        dest = edir / src.name
        change = TINTS[which][key]
        print("-> ed/%s" % dest.name, flush=True)
        if change is None:
            archive(dest)
            shutil.copy2(src, dest)
            print("   ok (standard edition)", flush=True)
            continue
        if which == "fuji":
            change = ("RECOLOUR the knitted Mount Fuji cap on the toy's head. THE CAP IS NOW "
                      + change + ". The fish underneath stays silver-grey - only the cap "
                      "changes.\n")
        r = gen("Edit the attached photograph. Return the SAME photograph with ONE thing "
                "changed.\n\n" + change + "\n" + HOLD, str(dest), [str(src)], "1:1")
        print("   " + ("ok" if isinstance(r, list) else str(r)), flush=True)


def shots(which, keys=None):
    """Photograph the six poses one at a time. Name poses to re-roll just those."""
    cfg = SETS[which]
    pdir = cfg["dir"] / "poses"
    pdir.mkdir(parents=True, exist_ok=True)
    for key, pose in POSES:
        if keys and key not in keys:
            continue
        body = pose + (CHARM if key in cfg["charmed"] else "")
        refs = [REF]
        if cfg.get("after"):
            # Described in words, the cap drags every pose back to the same
            # head-up sit. Handed the finished water shot and asked only to knit
            # a cap onto it, the model keeps the pose it is given.
            done = SETS[cfg["after"]]["dir"] / "poses" / ("%s_%s.png" % (cfg["after"], key))
            if not done.exists():
                print("  ! shoot the %s set first - missing %s" % (cfg["after"], done.name))
                continue
            prompt = MATCH + (CHARM if key in cfg["charmed"] else "")
            refs = [str(done)]
        else:
            prompt = LOCK + CHIBI + cfg["extra"] + SHOT + body
        dest = pdir / ("%s_%s.png" % (which, key))
        print("-> %s" % dest.name, flush=True)
        r = gen(prompt, str(dest), refs, "1:1")
        print("   " + ("ok" if isinstance(r, list) else str(r)), flush=True)


def subject_box(im, thresh=40):
    """Where the toy actually sits in its frame, so the crop can centre on it.

    Flood-fills the studio sweep inward from the border; whatever survives is the
    toy. Used only for framing - nothing is cut out, so a ragged fill costs
    nothing. Falls back to the whole frame if the sweep is not flat enough."""
    work = im.convert("RGB")
    w, h = work.size
    seeds = []
    for x in range(0, w, max(1, w // 24)):
        seeds += [(x, 0), (x, h - 1)]
    for y in range(0, h, max(1, h // 24)):
        seeds += [(0, y), (w - 1, y)]
    for s in seeds:
        if work.getpixel(s) != SENTINEL:
            ImageDraw.floodfill(work, s, SENTINEL, thresh=thresh)
    a = np.array(work)
    bg = np.all(a == np.array(SENTINEL), axis=-1)
    if bg.mean() < 0.15:
        return (0, 0, w, h)
    ys, xs = np.where(~bg)
    return (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)


def compose(which, w=2400, h=1350, cols=3, rows=2, gap=14, edge=14):
    """Lay the six single-pose photographs out as one clean product sheet.

    Each shot keeps its own frame, lighting and contact shadow - they are cropped
    to the cell and butted together with a thin paper-coloured gutter, the way a
    real product sheet is made up. Nothing is masked out, so there are no cut
    edges to go ragged."""
    cfg = SETS[which]
    pdir = cfg["dir"] / "poses"

    cw = (w - 2 * edge - (cols - 1) * gap) / cols
    ch = (h - 2 * edge - (rows - 1) * gap) / rows
    sheet = Image.new("RGB", (w, h), PAPER)

    for i, (key, _) in enumerate(POSES):
        src = pdir / "ed" / ("%s_%s.png" % (which, key))
        if not src.exists():
            src = pdir / ("%s_%s.png" % (which, key))
        if not src.exists():
            print("  ! missing pose " + src.name)
            return None
        im = Image.open(src).convert("RGB")

        # widest crop of the cell's shape that still fits, slid onto the toy
        want = cw / ch
        if im.width / im.height > want:
            bw, bh = round(im.height * want), im.height
        else:
            bw, bh = im.width, round(im.width / want)
        x0, y0, x1, y1 = subject_box(im)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        left = min(max(round(cx - bw / 2), 0), im.width - bw)
        top = min(max(round(cy - bh / 2), 0), im.height - bh)
        tile = im.crop((left, top, left + bw, top + bh)).resize(
            (round(cw), round(ch)), Image.LANCZOS)

        sheet.paste(tile, (round(edge + (i % cols) * (cw + gap)),
                           round(edge + (i // cols) * (ch + gap))))

    out = cfg["dir"] / cfg["out"]
    archive(out)
    sheet.save(out, "PNG", optimize=True)
    print("WROTE %s  %dx%d" % (out, w, h))
    return out


if __name__ == "__main__":
    args = sys.argv[1:]
    only_compose = "--compose" in args
    picked = [a for a in args if a in SETS] or list(SETS)
    names = [k for k, _ in POSES]
    keys = [a for a in args if a in names] or None
    for which in picked:
        if "--tint" in args:
            editions(which, keys)
        elif not only_compose:
            shots(which, keys)
            editions(which, keys)
        compose(which)
