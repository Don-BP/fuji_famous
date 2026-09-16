"""Product shots for the Chibi Fujie goods line - the playful, mass-market half.

These are the pieces a visitor centre shop, a gacha corner and a LINE store would
actually carry. The elegant grown-up line is rendered separately by
tools/run_elegant_line.py from the official artwork.
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen

M = "D:/Fuji_Famous/Fujie_Creative/01_character/master_v3_wave.png"
OUT = "D:/Fuji_Famous/Fujie_Creative/07_merch_chibi/"

LOCK = (
    "The attached image is the LOCKED master design of 'Chibi Fujie', the cute young form of "
    "Fujikin's sturgeon mascot. Reproduce this EXACT character on every product: polished "
    "chrome-silver body, pale silver belly, long flat pointed snout, four barbel whiskers under the "
    "snout, a row of rounded scute bumps along the back, one large glossy black eye with a bright "
    "white catchlight, crescent tail fin, bold dark navy outline, flat cel shading.\n\n"
    "*** ABSOLUTE RULE: NO LEGS, NO FEET, NO TOES, NO STANDING NUBS. IT IS A FISH. ***\n"
    "The only appendages are two soft pectoral fins at the sides, a dorsal fin, small pelvic fins "
    "near the tail and the crescent tail. The underside is a smooth continuous rounded belly with "
    "nothing protruding downward. It rests on its belly.\n\n"
)

SHOT = (
    "PHOTOREALISTIC commercial product photography, Japanese character-goods quality, crisp focus, "
    "soft even studio lighting, gentle contact shadows, clean uncluttered composition. "
    "Do not invent a different mascot - every character shown is the attached one.\n\n"
    "*** TEXT RULE - CRITICAL ***\n"
    "The ONLY words allowed anywhere in the image are: Fujie, FUJIKIN and the katakana フジィ. "
    "Do not write any other words in any language - no product names, no slogans, no shop names, "
    "no captions, no invented kanji or kana, no small print. Leave surfaces blank rather than "
    "filling them with text. Any of the three allowed words that does appear must be spelled "
    "exactly as written here.\n\n"
)

JOBS = [
    (
        "GACHAPON CAPSULE TOY SET. Six small collectible PVC figures of the character in six "
        "different poses - leaping, curled asleep, waving, diving, sitting upright, tail-flicking - "
        "arranged in a neat row on a seamless white background, each about 5cm, glossy chrome-silver "
        "paint with a pearl finish. Two clear plastic capsule halves, one open with a figure inside, "
        "sit at the front. Behind them a small printed card shows the six figures as a line-up.",
        "gacha_capsule_set.png", "16:9",
    ),
    (
        "ACRYLIC STAND AND CHARM LINE-UP. Four die-cut clear acrylic character stands of different "
        "poses on small clear bases, standing in a row on a pale grey surface, each about 10cm tall, "
        "the printed character crisp with a thick white border and the clear acrylic visible around "
        "it. In front of them two small acrylic keychain charms with silver ball chains.",
        "acrylic_stands.png", "16:9",
    ),
    (
        "HARD ENAMEL PIN SET on a presentation card. Five small metal pins on a navy backing card: "
        "the character's head, a full-body swimming pose, a single ripple ring, a caviar tin, and a "
        "tiny valve wheel. Polished silver metal plating; the enamel fills are deep navy, white and "
        "cyan.\n"
        "*** COLOUR RULE - CRITICAL ***\n"
        "Wherever the character's BODY appears on a pin - head pin and full-body pin alike - it is "
        "filled in PALE CHROME-SILVER and white enamel with a paler silver belly, exactly as in the "
        "attached master. Never fill the body with navy, blue, cyan or any other colour. Navy is "
        "only for the backing card and for outlines; cyan is only for water and the tin band. If a "
        "pin shows a blue fish, that is WRONG.\n"
        "The card lies flat on a warm neutral surface, photographed slightly from above, with soft "
        "specular highlights on the metal.\n"
        "The ONLY words anywhere in the image are Fujie, FUJIKIN and the katakana フジィ, printed "
        "on the backing card. Do NOT add PIN SET, SET, COLLECTION, セット or any other word, "
        "label, number or small print.",
        "enamel_pins.png", "4:3",
    ),
    (
        "APPAREL FLAT LAY on a pale oak table, shot straight down: a folded heather-grey t-shirt "
        "with a small chest print of the character, a natural canvas tote bag with a large print of "
        "the character riding a wave, a navy cap with the character embroidered on the front, and a "
        "pair of folded socks with a small repeating character pattern. Neat editorial arrangement "
        "with generous empty space.",
        "apparel_flatlay.png", "4:3",
    ),
    (
        "LUNCH SET on a light wooden table: a two-tier bento box with the character printed on the "
        "lid, a slim stainless water bottle with a wrap-around print of the character swimming "
        "through ripple lines, a chopstick case, and a small folded lunch cloth with a repeating "
        "character pattern. Warm natural window light, homely styling.",
        "lunch_set.png", "4:3",
    ),
    (
        "STATIONERY SET photographed from above on a white desk: three rolls of washi tape with "
        "repeating character and ripple patterns, a spiral memo pad with the character on the cover, "
        "two clear plastic document files with large character prints, a set of four die-cut sticky "
        "notes, and a silver ballpoint pen with a small character charm. Clean flat-lay layout.",
        "stationery_set.png", "4:3",
    ),
    (
        "JAPANESE SOUVENIR CONFECTIONERY BOX, the kind sold at a factory visitor centre. A rigid "
        "gift box in deep navy and silver with the character on the lid swimming through fine "
        "engraved ripple lines, the lid lifted to show individually wrapped silver-foil biscuits "
        "inside, each small wrapper printed with the character. A single unwrapped biscuit with the "
        "character embossed on it sits beside the box. Premium department-store styling.",
        "sweets_box.png", "4:3",
    ),
    (
        "RETAIL SHOP DISPLAY photograph inside a bright Japanese visitor-centre gift shop: a wooden "
        "shelving unit holding the plush toys, acrylic stands, capsule toys and the confectionery "
        "boxes, with a large printed header sign above showing the character and clean ripple "
        "graphics. Warm shop lighting, shallow depth of field, inviting and busy but tidy.",
        "shop_display.png", "16:9",
    ),
]

only = sys.argv[1] if len(sys.argv) > 1 else None
for prompt, name, aspect in JOBS:
    if only and only not in name:
        continue
    r = gen(LOCK + SHOT + prompt, OUT + name, refs=[M], aspect=aspect)
    print(json.dumps({"job": name, "ok": not isinstance(r, dict),
                      "r": r if isinstance(r, dict) else "saved"}, ensure_ascii=False), flush=True)
