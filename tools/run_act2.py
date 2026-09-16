"""Art for the second act: conservation, the shark joke, and the 2027 anniversary.

Three deck plates plus six hero stickers that carry the "I'm not a shark" line.
Everything lands in Fujie_Creative/15_act2/. Re-runnable; gen.py archives on write.
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen

M = "D:/Fuji_Famous/Fujie_Creative/01_character/master_v3_wave.png"
PREV = "D:/Fuji_Famous/Fujie_Creative/02_stickers/sticker_sheet_01.png"
OUT = "D:/Fuji_Famous/Fujie_Creative/15_act2/"
pathlib.Path(OUT).mkdir(parents=True, exist_ok=True)

LOCK = (
    "The first attached image is the LOCKED master design of 'Chibi Fujie', a cute chrome-silver "
    "sturgeon mascot. Reproduce this EXACT character with total consistency: polished chrome-silver "
    "body, pale silver belly, long flat pointed snout, four barbel whiskers under the snout, a row "
    "of rounded scute bumps along the back, one large glossy black eye with a bright white "
    "catchlight, crescent tail fin, bold dark navy outline, flat cel shading with crisp white "
    "specular highlights.\n\n"
    "*** FIN RULE - CRITICAL ***\n"
    "NO legs, NO feet, NO toes, NO stumps. The character has only fins: two pectoral fins at the "
    "sides used expressively like little arms, a pair of small PELVIC FINS near the tail, a dorsal "
    "fin, and the crescent tail. Every fin is thin, flat and leaf-shaped, lying close to the body "
    "and SWEPT BACKWARD toward the tail. No fin ever points straight down, supports the body's "
    "weight, or touches the ground. The belly line stays smooth and continuous.\n\n"
    "*** COLOUR RULE ***\n"
    "The body is ALWAYS chrome-silver with a pale silver belly. Never recolour it orange, red or "
    "any other hue, not even to show heat, cold or emotion.\n\n"
)

STICKER = (
    "Create ONE single die-cut messaging sticker, centred on a pure flat WHITE background with "
    "generous empty white margin on all four sides. Bright bold expressive sticker art, clean flat "
    "colour, thick dark navy outline. Do NOT draw a white die-cut border or any frame around the "
    "art. Do NOT draw a grid, a sheet, or multiple panels - exactly one character illustration on "
    "an empty white field. The whole body including the tail is visible.\n\n"
)


def jp(cap):
    return (
        "*** LANGUAGE RULE - CRITICAL ***\n"
        "The caption is JAPANESE and reads EXACTLY: " + cap + "\n"
        "Set it in a chunky rounded bold Japanese gothic face with a thick white outline and a "
        "dark navy fill. Every kana must be correct and legible. No English anywhere.\n\n"
    )


def en(cap):
    return (
        "*** LANGUAGE RULE - CRITICAL ***\n"
        'The caption is ENGLISH and reads EXACTLY: "' + cap + '"\n'
        "Set it in a chunky rounded bold sans-serif with a thick white outline and a dark navy "
        "fill, spelled exactly as written. No Japanese characters anywhere.\n\n"
    )


PLATES = [
    # ---- the shark joke, as a deck comparison plate --------------------------
    ("shark_vs_sturgeon.png", "16:9", [M, PREV], LOCK +
     "Create a clean editorial COMPARISON illustration on a pure flat white background, split into "
     "two clearly separated halves with a generous empty gap down the middle.\n\n"
     "LEFT HALF: a plain grey SHARK drawn in the same cute flat cel-shaded style - blunt rounded "
     "snout, a visible mouth of small triangular teeth, a tall straight triangular dorsal fin, a "
     "stiff upright crescent tail, plain smooth skin with no bumps along its back, a small round "
     "eye. It is an ordinary shark, NOT the silver mascot: matte blue-grey, no chrome, no whiskers, "
     "no scutes.\n\n"
     "RIGHT HALF: Chibi Fujie the chrome-silver sturgeon exactly as locked above, smiling "
     "confidently, one pectoral fin raised as if presenting himself, four barbel whiskers clearly "
     "visible, the row of rounded scute bumps clearly visible along his back, no teeth at all, a "
     "long flat pointed snout.\n\n"
     "The two animals face each other across the gap. They are the same size in frame. They never "
     "overlap or touch. Do not merge them into one creature. No text, no captions, no labels, no "
     "arrows, no lettering of any kind anywhere in the image - the difference is shown purely by "
     "how the two animals are drawn."),

    # ---- conservation: rarity, no mascot -------------------------------------
    ("endangered_water.png", "16:9", None,
     "A still, solemn, painterly illustration of deep dark river water seen from below the surface. "
     "Cold teal-black depths at the bottom of the frame, a faint pale glow from the distant surface "
     "at the top, thin god rays falling through suspended silt. Far away and small in the frame, "
     "ONE lone wild sturgeon in silhouette - a long armoured prehistoric fish with a pointed snout, "
     "a ridge of bony plates along its back, and a shark-like upswept tail - drifting away from the "
     "viewer into the gloom. It is a realistic wild animal, not a cartoon and not a mascot: muted "
     "grey-brown, no chrome, no big cartoon eye, no outline.\n\n"
     "The composition is mostly empty water. The fish is tiny against all that emptiness - the "
     "picture is about how few of them are left. Quiet, beautiful, elegiac. Muted desaturated "
     "palette. Cinematic wide shot. Absolutely no text, no lettering, no captions, no logos, no "
     "watermark, no frame, no border."),

    # ---- 40th anniversary emblem --------------------------------------------
    ("badge_40.png", "1:1", None,
     "A refined circular anniversary emblem for a Japanese corporate campaign, on a pure flat white "
     "background. A thin elegant double-ring roundel in Fujikin corporate cyan blue (#00A0E9) and "
     "deep midnight navy. At the centre, the numeral 40 set very large in a confident modern "
     "geometric sans-serif, deep navy. Directly beneath the numeral, smaller, the years "
     "1987-2027 in clean cyan lettering. Around the lower inside curve of the ring, small and "
     "restrained, a single flowing line of stylised water - a simple minimal wave motif inspired by "
     "Japanese dry-garden sand ripples, thin concentric arcs, no foam and no spray.\n\n"
     "Flat vector logo design. Crisp geometry, perfectly circular, perfectly symmetrical. Only "
     "those two pieces of lettering appear: the numeral 40 and the years 1987-2027, both spelled "
     "exactly as given. No other words, no Japanese characters, no company name, no fish."),
]

STICKERS = [
    ("notshark_jp_01.png", jp("サメじゃないです"), LOCK + STICKER +
     "Chibi Fujie facing the viewer with both pectoral fins held up flat in a polite, slightly "
     "flustered 'no no' gesture, head tilted, a small embarrassed sweat drop at his temple, one "
     "eyebrow raised in mild protest. A tiny grey shark silhouette floats in the air beside his "
     "head with a thin red diagonal line struck through it, small and cartoonish."),

    ("notshark_jp_02.png", jp("サメじゃないってば"), LOCK + STICKER +
     "Chibi Fujie exasperated - eye squeezed shut, mouth open mid-protest, both pectoral fins "
     "thrown out wide in frustration, small jagged annoyance lines and a tiny cross-popping anger "
     "mark above his head. Comic, not angry. He is clearly insisting for the second time."),

    ("notshark_jp_03.png", jp("チョウザメです"), LOCK + STICKER +
     "Chibi Fujie sitting proudly upright and puffed up with quiet dignity, chin lifted, one "
     "pectoral fin laid across his chest as if introducing himself formally. The four barbel "
     "whiskers under his snout and the row of rounded scute bumps along his back are exaggerated "
     "and clearly visible - these are the features that prove what he is. A soft sparkle behind "
     "him."),

    ("notshark_en_01.png", en("Not a shark!"), LOCK + STICKER +
     "Chibi Fujie facing the viewer with both pectoral fins held up flat in a polite, slightly "
     "flustered 'no no' gesture, head tilted, a small embarrassed sweat drop at his temple. A tiny "
     "grey shark silhouette floats in the air beside his head with a thin red diagonal line struck "
     "through it, small and cartoonish."),

    ("notshark_en_02.png", en("I am a sturgeon"), LOCK + STICKER +
     "Chibi Fujie sitting proudly upright and puffed up with quiet dignity, chin lifted, one "
     "pectoral fin laid across his chest as if introducing himself formally. The four barbel "
     "whiskers under his snout and the row of rounded scute bumps along his back are exaggerated "
     "and clearly visible. A soft sparkle behind him."),

    ("notshark_jp_04.png", jp("２億年このまま"), LOCK + STICKER +
     "Chibi Fujie drifting serenely with his eye closed and a small contented smile, completely "
     "unbothered, fins relaxed at his sides. Behind him, drawn small and simple like a doodle, a "
     "tiny cartoon dinosaur waves goodbye as it walks away into the distance. He has outlasted it "
     "and he knows it. Calm, dry, quietly smug."),

    ("notshark_en_04.png", en("200 million years"), LOCK + STICKER +
     "Chibi Fujie drifting serenely with his eye closed and a small contented smile, completely "
     "unbothered, fins relaxed at his sides. Behind him, drawn small and simple like a doodle, a "
     "tiny cartoon dinosaur waves goodbye as it walks away into the distance. He has outlasted it "
     "and he knows it. Calm, dry, quietly smug."),

    # Sheet 02 rendered this caption as the meaningless "アイ" and gave him clenched
    # fists instead of fins. Redrawn on its own; the sheet itself is not touched.
    ("fight_fixed.png", jp("ファイト"), LOCK + STICKER +
     "Chibi Fujie cheering someone on with fierce encouragement. He is braced and leaning "
     "forward, both PECTORAL FINS raised in front of his chest in a spirited 'you can do it' "
     "gesture - they are flat leaf-shaped fins, NOT hands, NOT fists, NOT arms: no fingers, no "
     "knuckles, no thumbs anywhere. One eyebrow is set determinedly and his mouth is open in a "
     "shout. Small motion lines and a warm burst of energy behind him.",),

    ("rocket_straight.png", jp("ロケット"), LOCK + STICKER +
     "Chibi Fujie flying straight upward like a launched rocket. His whole body is RIGID and "
     "PERFECTLY STRAIGHT along a single vertical line - snout pointing dead upward at the top of "
     "the frame, tail pointing dead downward at the bottom, spine absolutely rigid with no bend, "
     "no curve, no arch and no S-shape anywhere. Every fin is pinned tight against his sides and "
     "swept backward toward the tail, streamlined like a missile. Eye squeezed shut with "
     "determination, mouth set in a confident grin. A bright orange and white flame plume blasts "
     "straight down from behind his tail, with sharp vertical speed lines and small puffs of "
     "smoke on either side. Seen side-on, the full body visible from snout to tail.",),

    ("notshark_en_03.png", en("Still not a shark"), LOCK + STICKER +
     "Chibi Fujie deadpan and unimpressed, staring flatly at the viewer with a half-lidded eye, "
     "one pectoral fin resting on his cheek, utterly resigned. A tiny grey shark silhouette drifts "
     "past behind him. Dry comic timing - he has given up correcting people."),
]


def run_plates():
    for name, aspect, refs, prompt in PLATES:
        r = gen(prompt, OUT + name, refs=refs, aspect=aspect)
        print(json.dumps({"plate": name, "ok": not isinstance(r, dict)}, ensure_ascii=False), flush=True)


def run_stickers(pick=None):
    for name, lang, prompt in STICKERS:
        if pick and name not in pick:
            continue
        r = gen(prompt + lang, OUT + name, refs=[M, PREV], aspect="1:1")
        print(json.dumps({"sticker": name, "ok": not isinstance(r, dict)}, ensure_ascii=False), flush=True)


only = sys.argv[1] if len(sys.argv) > 1 else None
if only in (None, "plates"):
    run_plates()
if only in (None, "stickers"):
    run_stickers()
elif only == "pick":
    run_stickers(set(sys.argv[2:]))
print("ACT2 DONE", flush=True)
