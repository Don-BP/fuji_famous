"""Re-paint the wide plates that came back tiled instead of widened.

Asked to "extend the scene left and right", the model repeated the portrait
composition: bg_tank_early and bg_tank_grown grew extra tank walls standing in
the middle of the frame, and bg_shell came back as three panels with visible
seams. This run says plainly that the centre must be one unbroken span of open
water and that nothing may be repeated or mirrored.
"""
import json, pathlib, sys
from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen

SITE = pathlib.Path(r"D:\Fuji_Famous\site\art")
MASTER = pathlib.Path(r"D:\Fuji_Famous\Fujie_Creative\06_game")
WIDE = MASTER / "wide"
OUT_W, Q = 1600, 80

BASE = (
    "The attached image is an existing painted background plate from a Japanese mobile game, "
    "drawn in a tall portrait frame.\n\n"
    "Re-paint the SAME SCENE as a single WIDESCREEN 16:9 plate. Same place, same subject, same "
    "palette, same light sources, same mood, same painterly brushwork.\n\n"
    "*** COMPOSITION RULE - THIS IS THE WHOLE POINT ***\n"
    "This must be ONE continuous scene painted for a wide frame, as though the artist had always "
    "worked at this shape. Do NOT repeat, mirror, tile or duplicate any part of the original. "
    "There must be no vertical seam, no panel join, and no second copy of any wall, pillar or "
    "structure. Widen the space itself - the room simply gets wider - rather than adding more "
    "objects to fill the extra width.\n\n"
    "*** THE CENTRE MUST STAY EMPTY ***\n"
    "The middle 60% of the frame is unbroken open water. No wall, no pillar, no column, no panel "
    "edge, no structural line and no machinery anywhere in it. Walls, pipes and fittings belong "
    "only at the far left and right edges, angled away from the viewer. A character and body text "
    "are drawn on top of the middle, so it must read as calm, dark, empty water.\n\n"
    "Palette locked to dark teal and navy - #04121A, #07202B, #103544, #1D5566 - with cool cyan "
    "#3FB6EE light accents and pale silver #BFCFD6 highlights, and a gentle vignette at the edges.\n"
    "ABSOLUTE RULES: NO characters. NO fish. NO creatures. NO people. NO text, letters, numbers, "
    "logos, watermarks or UI elements. Empty scenery only.\n"
)

EXTRA = {
    "bg_tank_early": "\nThe scene is the inside of ONE small dim hatchery tank: a single smooth "
                     "pale concrete wall sweeping away at the far left and another at the far "
                     "right, one soft overhead lamp, one slender steel inlet pipe high at one "
                     "side with fine bubbles rising. Everything between those two side walls is "
                     "open water.",
    "bg_tank_grown": "\nThe scene is the inside of ONE large deep rearing tank: a single broad "
                     "concrete wall falling away at the far left and another at the far right, a "
                     "row of cool light panels across the ceiling casting rippling caustics, and "
                     "a bank of polished steel pipes and valve fittings confined to the upper "
                     "right corner only. Everything between the two side walls is one wide span "
                     "of open blue-green water.",
    "bg_shell": "\nThe scene is one continuous stretch of rippled pale sea floor seen from just "
                "above it, lit softly from above, fading into darker water toward the top of the "
                "frame. A smooth unbroken sand bed - no seams, no panels, no dividing lines.",
}


def publish(src, name):
    im = Image.open(src).convert("RGB")
    if im.width > OUT_W:
        im = im.resize((OUT_W, round(im.height * OUT_W / im.width)), Image.LANCZOS)
    dest = SITE / (name + "_wide.jpg")
    im.save(dest, "JPEG", quality=Q, optimize=True, progressive=True)
    print("   -> %-24s %dx%d  %.0f KB" % (dest.name, im.width, im.height,
                                          dest.stat().st_size / 1024))


for name in ("bg_tank_early", "bg_tank_grown", "bg_shell"):
    ref = MASTER / (name + ".png")
    if not ref.exists():
        ref = SITE / (name + ".jpg")
    target = WIDE / (name + ".png")
    r = gen(BASE + EXTRA[name], str(target), refs=[str(ref)], aspect="16:9")
    ok = not isinstance(r, dict)
    print(json.dumps({"plate": name, "ok": ok}, ensure_ascii=False), flush=True)
    if ok and target.exists():
        publish(target, name)
