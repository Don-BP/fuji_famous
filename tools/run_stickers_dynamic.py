"""Generate a third LINE sticker sheet of genuinely dynamic action poses.

The existing two sheets are all mild upright three-quarter variations. This sheet
is deliberately all movement: leaps, spins, impacts, extreme angles. It is written
as an ADDITION - sheets 01 and 02 are not touched.
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen

M = "D:/Fuji_Famous/Fujie_Creative/01_character/master_v3_wave.png"
SMP = "D:/Fuji_Famous/Documents_for_dev/sticker sheets/Sticker sheet sample 1.png"
PREV = "D:/Fuji_Famous/Fujie_Creative/02_stickers/sticker_sheet_01.png"
OUT = "D:/Fuji_Famous/Fujie_Creative/02_stickers/"

LOCK = (
    "The first attached image is the LOCKED master design of 'Chibi Fujie', a cute chrome-silver "
    "sturgeon mascot. Reproduce this EXACT character in every panel with total consistency: "
    "polished chrome-silver body, pale silver belly, long flat pointed snout, four barbel whiskers "
    "under the snout, a row of rounded scute bumps along the back, one large glossy black eye with "
    "a bright white catchlight, crescent tail fin, bold dark navy outline, flat cel shading with "
    "crisp white specular highlights.\n\n"
    "*** FIN RULE - CRITICAL ***\n"
    "NO legs, NO feet, NO toes, NO stumps. The character has only fins: two pectoral fins at the "
    "sides used expressively like little arms, a pair of small PELVIC FINS near the tail, a dorsal "
    "fin, and the crescent tail. Every fin is thin, flat and leaf-shaped, lying close to the body "
    "and SWEPT BACKWARD toward the tail. No fin ever points straight down, supports the body's "
    "weight, or touches the ground. The belly line stays smooth and continuous.\n\n"
)

POSE = (
    "*** POSE RULE - THE WHOLE POINT OF THIS SHEET ***\n"
    "Every single sticker must be a BIG DYNAMIC ACTION POSE. The previous sheets were too static "
    "- almost every panel was the same calm upright three-quarter view. Do NOT repeat that here.\n"
    "In this sheet:\n"
    "  * Show the WHOLE BODY in motion, tail included, never just a floating head-and-shoulders.\n"
    "  * Tilt the body on a strong diagonal. Twist it. Throw it off balance. Use foreshortening "
    "so a fin or the snout comes straight at the viewer.\n"
    "  * Vary the camera every panel: worm's-eye, bird's-eye, far, extreme close-up, upside down, "
    "coming toward the viewer, flying out of the panel.\n"
    "  * Push the expression to the extreme - wide open mouth, squeezed-shut eye, shouting.\n"
    "  * Lean on manga action effects: speed lines, motion blur streaks, impact starbursts, "
    "sweat beads flying off, water spray, dust puffs, radiating focus lines.\n"
    "  * No two panels may share the same body angle.\n\n"
)

STK = (
    LOCK + POSE
    + "Create a JAPANESE LINE STICKER SHEET: 4 columns by 5 rows of 20 separate die-cut stickers on "
    "a pure white background, each with a thick white sticker border, bright bold expressive "
    "Japanese sticker art.\n"
    "CRITICAL: every caption must be DIFFERENT - each caption below appears exactly once, on its "
    "own sticker, and no sticker is left without a caption. Captions in a chunky rounded bold "
    "Japanese font with a white outline, placed above or beside the character, accurate and "
    "legible. Count carefully before finishing.\n\n"
    "The 20 stickers in order (caption in quotes):\n"
)

S3 = [
    '1. Exploding up out of the water in a huge leap, whole body arched, crown of spray - "とんだー！"',
    '2. Mid-air somersault, body curled into a spinning circle, swirling motion lines - "くるくる"',
    '3. Rocketing straight at the viewer head-on, snout hugely foreshortened, radiating speed lines - "いそげー"',
    '4. Swinging its tail hard and knocking a small cartoon shark out of frame, impact starburst - "サメじゃない！"',
    '5. Plunging head-first straight down, tail high above, bubble trail streaming up - "いくぞー"',
    '6. Carving down the face of a huge curling wave, body leaning hard into the turn - "ながれにのれ"',
    '7. Bursting up through the water surface from below, water crown ring around it - "とうじょう！"',
    '8. Punching a fin high in the air at the top of a jump, body twisted, eye squeezed shut - "よっしゃ！"',
    '9. Corkscrewing forward like a drill, body spiralling, tight spiral motion lines - "きりもみ"',
    '10. Blasting away from the viewer into the distance, only its tail and a dust cloud left - "しゅっぱつ"',
    '11. Slamming down into the bottom of the panel, impact cracks radiating out - "ドーン"',
    '12. Balanced upside down on the very tip of its snout, tail waving, wobble lines - "みて！"',
    '13. Reeling back mid-air, struck by a sudden idea, huge lightning bolt behind it - "ひらめいた"',
    '14. Flexing both pectoral fins hard like a bodybuilder, body low and braced, sparks - "パワー！"',
    '15. Skidding to a violent stop side-on, body leaning back, skid trail and dust - "ストップ！"',
    '16. Flying at the viewer with a fin thrown forward for a high-five, impact flash - "ハイタッチ"',
    '17. Curled into a tight ball and shooting upward like a rocket, flame trail below - "ロケット"',
    '18. Hanging upside down from the top edge of the sticker, peeking down sneakily - "こっそり"',
    '19. Flipped completely over on its back mid-laugh, tail kicking, laughter marks - "わらう"',
    '20. Landing in a heroic crouch on a rock, seaweed streaming behind like a cape - "ヒーロー"',
]

r = gen(STK + "\n".join(S3), OUT + "sticker_sheet_03_action.png", refs=[M, SMP, PREV], aspect="4:5")
print(json.dumps({"ok": not isinstance(r, dict), "r": r if isinstance(r, dict) else "saved"},
                 ensure_ascii=False), flush=True)
