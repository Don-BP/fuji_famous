"""Two English-caption sticker sheets (40 stickers) for overseas messaging apps.

Sheet EN-01 is everyday chat - the replies people actually send.
Sheet EN-02 is mood and motion, leaning on the flow idea Fujikin already owns.
Japanese sheets 01-03 are not touched.
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

COLOUR = (
    "*** COLOUR RULE ***\n"
    "The body is ALWAYS chrome-silver with a pale silver belly. Never recolour it orange, red or "
    "any other hue, not even to show heat, cold or emotion. Show those with effects around the "
    "character instead.\n\n"
)

ENGLISH = (
    "*** LANGUAGE RULE - CRITICAL ***\n"
    "Every caption is in ENGLISH. No Japanese characters anywhere on this sheet. Set the captions "
    "in a chunky rounded bold sans-serif with a thick white outline and a dark navy fill, spelled "
    "EXACTLY as written, correctly and legibly, one caption per sticker. Check the spelling of "
    "every word before finishing.\n\n"
)

SHEET = (
    "Create a LINE / WhatsApp STICKER SHEET: 4 columns by 5 rows of 20 separate die-cut stickers "
    "on a pure white background, each sticker with a thick white die-cut border, bright bold "
    "expressive sticker art with clean flat colour.\n"
    "CRITICAL: every caption below appears exactly once, on its own sticker, and no sticker is "
    "left without a caption. Every pose is different - vary the body angle, camera and expression "
    "on every panel, always showing the whole body including the tail. Count carefully before "
    "finishing.\n\n"
    "The 20 stickers in order (caption in quotes):\n"
)

EN1 = [
    '1. Waving one pectoral fin brightly, body tilted forward in greeting - "Morning!"',
    '2. Both fins thrown up in celebration, eye squeezed shut with joy, confetti - "Yay!"',
    '3. Bowing deeply, body folded forward, small sparkle above - "Thank you!"',
    '4. Making a big round OK sign with a curled fin, confident smile - "OK!"',
    '5. Bowing low with the snout almost touching the ground, apologetic sweat drop - "Sorry!"',
    '6. Leaning eagerly toward the viewer, fin raised like a pupil answering - "On it!"',
    '7. Giving a big thumbs-up style fin, wide grin, sparkle - "Nice!"',
    '8. Curled up asleep in a little ball, single Z floating above - "So sleepy"',
    '9. Belly up, tongue out, tiny fork and empty plate beside it - "Hungry..."',
    '10. Rearing back in shock, eye huge, jagged surprise lines behind - "No way!"',
    '11. Head tilted, one fin on the chin, question mark floating above - "Really?"',
    '12. Popping out of a party popper with streamers everywhere - "Congrats!"',
    '13. Tucked under a tiny blanket, crescent moon and stars behind - "Good night"',
    '14. Hugging a big glossy heart with both fins, blushing - "Love it"',
    '15. Half sunk with only the snout and one waving fin above the waterline - "Help!"',
    '16. Peeking around the edge of the sticker with one bright eye - "I am here"',
    '17. Swimming away over the shoulder, one fin waving back at the viewer - "See you!"',
    '18. Cheering with both fins up and a small flag held in the tail - "Go team!"',
    '19. Turning away with fins crossed, eye shut, firmly refusing - "Nope"',
    '20. Tipping a tiny cup of tea, relaxed and content, steam curling up - "Take a break"',
]

EN2 = [
    '1. Exploding up out of the water in a huge arched leap, crown of spray - "Let us go!"',
    '2. Riding down the face of a curling wave, leaning hard into the turn - "Making waves"',
    '3. Diving straight down into the dark, bubble trail streaming upward - "Deep dive"',
    '4. Belly-flopping into water, enormous splash ring, eye squeezed shut - "Splash!"',
    '5. Cruising level and serene through smooth flowing current lines - "Creating the flow"',
    '6. Powering forward against strong current arrows, determined frown - "Upstream"',
    '7. Floating on its back with fins behind the head, totally relaxed - "Chill"',
    '8. Staring dead ahead with narrowed eye, focus lines converging - "Focus"',
    '9. Two identical Fujies bumping fins together in mid-water - "Teamwork"',
    '10. Bursting through a paper finish banner, arms of spray behind - "Big win"',
    '11. Both pectoral fins raised in a strong-arm flex, body braced and puffed up, energy sparks behind it - it is still entirely a fish, no human arms, no shoulders, no muscles - "Power up"',
    '12. Shivering inside a ring of ice crystals, tiny scarf, teeth chattering - "Brrr"',
    '13. Fanning itself with a fin under a blazing sun, sweat beads flying, body still chrome-silver - "Too hot"',
    '14. Wearing tiny round glasses over a stack of books, pencil in fin - "Study time"',
    '15. Slumped flat and melted over the bottom edge of the panel - "So tired"',
    '16. Spinning in a tight corkscrew like a drill, spiral motion lines - "Spin!"',
    '17. Lit by a huge lightning bolt of inspiration, reeling backward - "Got it!"',
    '18. Skidding to a violent side-on stop, dust and spray trail - "Stop!"',
    '19. Flying at the viewer with a fin thrown forward for a high five - "High five"',
    '20. Landing in a heroic crouch on a rock, seaweed streaming like a cape - "Hero"',
]


def run(name, items):
    prompt = LOCK + COLOUR + ENGLISH + SHEET + "\n".join(items)
    r = gen(prompt, OUT + name, refs=[M, SMP, PREV], aspect="4:5")
    print(json.dumps({"sheet": name, "ok": not isinstance(r, dict),
                      "r": r if isinstance(r, dict) else "saved"},
                     ensure_ascii=False), flush=True)


only = sys.argv[1] if len(sys.argv) > 1 else None
if only in (None, "1"):
    run("sticker_sheet_EN_01_chat.png", EN1)
if only in (None, "2"):
    run("sticker_sheet_EN_02_action.png", EN2)
