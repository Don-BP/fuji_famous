import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen

M = "D:/Fuji_Famous/Fujie_Creative/01_character/master_v3_wave.png"
SMP = "D:/Fuji_Famous/Documents_for_dev/sticker sheets/Sticker sheet sample 1.png"
PREV = "D:/Fuji_Famous/Fujie_Creative/02_stickers/sticker_sheet_01.png"

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

STK = (
    LOCK
    + "Create a JAPANESE LINE STICKER SHEET: 4 columns by 5 rows of 20 separate die-cut stickers on "
    "a pure white background, each with a thick white sticker border, bright bold expressive "
    "Japanese sticker art with small cartoon effect marks (sparkles, sweat drops, motion lines).\n"
    "CRITICAL: every caption must be DIFFERENT - each caption below appears exactly once, on its "
    "own sticker, and no sticker is left without a caption. Captions in a chunky rounded bold "
    "Japanese font with a white outline, placed above or beside the character, accurate and "
    "legible. Count carefully before finishing.\n\n"
    "The 20 stickers in order (caption in quotes):\n"
)

S1 = [
    '1. Waving a pectoral fin cheerfully - "おはよう"',
    '2. Bowing politely, sparkles - "ありがとう"',
    '3. Balancing a steaming teacup on a fin - "おつかれさま"',
    '4. Fin curled into an OK sign, winking - "OK"',
    '5. Fin raised to the brow in a salute - "りょうかい"',
    '6. Head dipped, sweat drop, apologetic - "ごめんね"',
    '7. Deep polite bow - "よろしく"',
    '8. Fin held up in a thumbs-up gesture, big grin - "いいね"',
    '9. Eye sparkling with stars, amazed - "すごい"',
    '10. Fin clenched, fired up, flame behind - "がんばって"',
    '11. Confident, fin patting own chest - "まかせて"',
    '12. Spinning with joy, confetti - "うれしい"',
    '13. Shocked, eye huge, body recoiling - "えっ"',
    '14. Drowsy half-closed eye, floating Z marks - "ねむい"',
    '15. Drooping over an empty plate - "おなかすいた"',
    '16. Both fins flailing in panic, tears - "たすけて"',
    '17. Curled asleep under a crescent moon - "おやすみ"',
    '18. Darting off with a briefcase, motion lines - "いってきます"',
    '19. Crying with big teardrops - "かなしい"',
    '20. Leaning in with a concerned look - "だいじょうぶ"',
]

S2 = [
    '1. Surfing a curling blue wave on a board - "ながれにのれ"',
    '2. Climbing a cliff face, determined - "きわみへ"',
    '3. Delighted beside an open tin of black caviar - "キャビア"',
    '4. Nodding knowingly, eye closed - "なるほど"',
    '5. Applauding with both fins, impressed - "さすが"',
    '6. One fin held out flat to stop - "ちょっとまって"',
    '7. Doubtful, one brow raised, question mark - "ほんと"',
    '8. Cheering with both fins up, confetti - "やったー"',
    '9. Melted into a puddle, exhausted - "つかれた"',
    '10. Sweating under a hot sun, fanning itself - "あつい"',
    '11. Shivering wrapped in a scarf, snowflakes - "さむい"',
    '12. Firing a party popper, streamers - "おめでとう"',
    '13. Punching the air with a fin, energetic - "ファイト"',
    '14. Both fins together, satisfied after a meal - "ごちそうさま"',
    '15. Happy reunion wave - "ひさしぶり"',
    '16. Balancing a glass on a fin in a toast - "かんぱい"',
    '17. Frozen solid inside a block of ice - "がーん"',
    '18. Freshly polished, gleaming, sparkles - "ぴかぴか"',
    '19. Blowing a kiss, red heart - "だいすき"',
    '20. Waving goodbye gently - "またね"',
]

PLUSH = (
    LOCK
    + "Create a PHOTOREALISTIC PRODUCT PHOTOGRAPH of this character manufactured as a real Japanese "
    "plush toy. Silver-grey short-pile velboa plush with a pearlescent sheen, pale ivory-silver "
    "belly panel, the long flat snout firmly stuffed and sewn, four soft cord barbel whiskers, the "
    "back scutes as small padded quilted bumps along a raised spine seam, one large glossy black "
    "embroidered eye with a white satin-stitch catchlight, soft sewn pectoral and pelvic fins lying "
    "swept back against the body, a dorsal fin and a crescent tail, visible high-quality stitching, "
    "a small woven fabric tag near the tail. The plush has NO legs and NO feet - it lies on its "
    "smooth rounded belly like a fish. Premium Japanese character-goods quality. No text or logo on "
    "the plush itself.\n\n"
)

JOBS = [
    (STK + "\n".join(S1), "02_stickers/sticker_sheet_01.png", "4:5", [M, SMP, PREV]),
    (STK + "\n".join(S2), "02_stickers/sticker_sheet_02.png", "4:5", [M, SMP, PREV]),
    (PLUSH + "Studio product photograph on a seamless pure white background, soft even three-point "
     "lighting, gentle contact shadow. The plush lies on its belly facing the camera at a slight "
     "three-quarter angle with its head lifted cheerfully, centred, filling the frame. Crisp "
     "commercial e-commerce product shot.",
     "03_plushie/plush_studio_front.png", "1:1", [M]),
    (PLUSH + "Photograph of the plush cradled in an adult's two open hands against a softly blurred "
     "warm neutral background, natural window light. Shows it is about 25cm long, palm-sized and "
     "huggable. Shallow depth of field, warm inviting lifestyle photography.",
     "03_plushie/plush_in_hands.png", "4:3", [M]),
    (PLUSH + "Product family photograph on a clean light-grey studio background: three sizes of the "
     "same plush resting on their bellies in a neat row, smallest to largest - a 10cm keychain "
     "version with a metal ball-chain clip, a 25cm version, and a 50cm huggable version. Even "
     "lighting, commercial catalogue arrangement.",
     "03_plushie/plush_size_lineup.png", "16:9", [M]),
    (PLUSH + "Lifestyle photograph: the 10cm keychain version clipped to the strap of a commuter's "
     "bag, photographed close up on a Japanese train platform, soft bokeh background, natural "
     "daylight. Warm everyday Japanese character-goods photography.",
     "03_plushie/plush_keychain_lifestyle.png", "3:4", [M]),
]

BASE = "D:/Fuji_Famous/Fujie_Creative/"
for prompt, rel, aspect, refs in JOBS:
    r = gen(prompt, BASE + rel, refs=refs, aspect=aspect)
    print(json.dumps({"out": rel, "ok": not isinstance(r, dict)}, ensure_ascii=False), flush=True)
print("ALL DONE", flush=True)
