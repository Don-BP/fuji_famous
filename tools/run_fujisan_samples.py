"""Mt. Fuji samples - one test shot per line, to agree the treatment before scaling.

Fujikin is named for Mt. Fuji, so the mountain joins the water as a second house
motif. Each sample below speaks the native language of its own line: the badge
stays flat vector, the craft lines stay hand-made, maison stays leather-and-
monogram, chibi stays cute. Nothing here overwrites existing work - samples land
in Fujie_Creative/19_fujisan/.

Output: Fujie_Creative/19_fujisan/
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen

OFFICIAL = "D:/Fuji_Famous/Documents_for_dev/05_fujie_絵柄例.png"
MASTER = "D:/Fuji_Famous/Fujie_Creative/01_character/master_v3_wave.png"
MONO = "D:/Fuji_Famous/Fujie_Creative/09_merch_maison/monogram_ecru.png"
TILE = "D:/Fuji_Famous/Fujie_Creative/11_wamon/tiles/seigaiha_indigo.png"
OUT = "D:/Fuji_Famous/Fujie_Creative/19_fujisan/"
pathlib.Path(OUT).mkdir(parents=True, exist_ok=True)

# --- shared blocks, lifted from the line scripts so the samples stay in family ---

FUJI = (
    "*** MOUNT FUJI RULE - CRITICAL ***\n"
    "Mount Fuji must be instantly recognisable: a single broad symmetrical cone with gently "
    "concave slopes, a slightly flattened summit with a small crater notch, and a snow cap that "
    "sits as a soft scalloped band across the top third. It is a lone free-standing volcano - no "
    "mountain range behind it, no jagged alpine peaks, no twin peaks, no foothills crowding it. "
    "The silhouette is wide and calm, far wider than it is tall.\n\n"
)

LOCK_OFFICIAL = (
    "The attached image is the OFFICIAL illustration of 'Fujie', Fujikin's sturgeon mascot: a "
    "realistic polished chrome-silver sturgeon in profile, long flat pointed snout, four barbels "
    "beneath it, five rows of pale bony scutes, a small dark eye set high and forward, a large "
    "swept tail.\n\n"
    "*** ARTWORK RULE - CRITICAL ***\n"
    "Reproduce this illustration EXACTLY as drawn wherever it appears: same silhouette, same "
    "proportions, same metallic rendering. Do NOT redraw, restyle, cartoon, recolour or "
    "reproportion it, never give it a big cartoon eye, a smile, arms or legs. On the product it is "
    "a print, a foil stamp, an engraving, an embroidery or an inlay of this exact artwork.\n\n"
)

LOCK_CHIBI = (
    "The attached image is the LOCKED master design of 'Chibi Fujie', the cute young form of "
    "Fujikin's sturgeon mascot. Reproduce this EXACT character: polished chrome-silver body, pale "
    "silver belly, long flat pointed snout, four barbel whiskers under the snout, a row of rounded "
    "scute bumps along the back, one large glossy black eye with a bright white catchlight, "
    "crescent tail fin, bold dark navy outline, flat cel shading.\n\n"
    "*** ABSOLUTE RULE: NO LEGS, NO FEET, NO TOES, NO STANDING NUBS. IT IS A FISH. ***\n"
    "The only appendages are two soft pectoral fins at the sides, a dorsal fin, small pelvic fins "
    "near the tail and the crescent tail. The belly is a smooth continuous curve.\n\n"
)

TEXT_GOODS = (
    "*** TEXT RULE - CRITICAL ***\n"
    "The only words allowed anywhere are FUJIE and FUJIKIN, small and discreet, or a single small "
    "red seal-shaped stamp. No other words in any language, no slogans, no shop names, no invented "
    "kanji or kana, no captions, no small print. Leave surfaces blank rather than filling them "
    "with text.\n\n"
)

JOBS = [

    # ---- 1. the anniversary badge, re-cut with Fuji ---------------------------
    ("badge_40_fuji.png", "1:1", None,
     "A refined circular anniversary emblem for a Japanese corporate campaign, on a pure flat "
     "white background. A thin elegant double-ring roundel in Fujikin corporate cyan blue "
     "(#00A0E9) and deep midnight navy.\n\n"
     "Inside the roundel, filling the lower half, a clean flat-vector MOUNT FUJI: the cone drawn "
     "as a solid deep midnight navy silhouette, its snow cap cut out in white with a soft "
     "scalloped lower edge, sitting on a band of thin concentric cyan water ripples that read as "
     "the lake at its foot. The mountain is calm, wide and perfectly symmetrical.\n\n"
     "Above the mountain, in the clear upper half of the roundel, the numeral 40 set very large in "
     "a confident modern geometric sans-serif, deep midnight navy. Directly beneath the numeral, "
     "much smaller, the years 1987-2027 in clean cyan lettering, sitting just above the summit.\n\n"
     + FUJI +
     "Flat vector logo design. Crisp geometry, perfectly circular, perfectly symmetrical, no "
     "gradients, no shading, no texture. Only those two pieces of lettering appear: the numeral 40 "
     "and the years 1987-2027, both spelled exactly as given. No other words, no Japanese "
     "characters, no company name, no fish, no sun, no clouds, no cherry blossom."),

    # ---- 2. official line, widened: premium corporate gift --------------------
    ("official_fuji_glass.png", "4:3", [OFFICIAL],
     LOCK_OFFICIAL + TEXT_GOODS + FUJI +
     "PHOTOREALISTIC product photography for a premium Japanese corporate gift line. Restrained "
     "palette: deep navy, charcoal, warm off-white washi, brushed silver, one accent of Fujikin "
     "corporate blue. Soft directional studio light, shallow depth of field, generous empty "
     "space.\n\n"
     "THE PRODUCT: a solid optical-crystal paperweight, a clean rectangular block with polished "
     "bevelled edges, standing on a dark brushed-steel plinth on a charcoal surface. Laser-etched "
     "inside the crystal in fine white subsurface dots: Mount Fuji as a calm wide cone with its "
     "snow cap, and the official Fujie swimming across its foot through a few thin concentric "
     "water rings. The etching is delicate and monochrome; the glass catches a cool blue edge "
     "light."),

    # ---- 3. the craft line, drawing the fish itself ---------------------------
    ("wa_fuji_ukiyoe.png", "4:3", [OFFICIAL],
     "The attached image shows the fish this print is based on: a sturgeon with a long flat "
     "pointed snout, four barbels beneath it, five rows of bony scutes along the body, a small eye "
     "set high and forward, a large sweeping upper tail lobe. Keep that silhouette exactly - it "
     "must read as a sturgeon, never a carp, never a koi, never a dolphin, never a shark. Do NOT "
     "copy the chrome rendering: redraw the fish in the woodblock medium described below.\n\n"
     + FUJI +
     "AN ORIGINAL EDO-PERIOD UKIYO-E WOODBLOCK PRINT, newly composed for this project. A great "
     "sturgeon rides the curl of a large breaking wave in the foreground, the wave drawn with the "
     "clawed foam fingers of classical Japanese prints in Prussian blue and indigo gradations. "
     "Far beyond the water, small and serene, Mount Fuji stands snow-capped against a pale dawn "
     "sky with soft bokashi shading. Flat areas of colour with fine keyblock outlines, visible "
     "woodgrain, the soft fibre of aged washi paper.\n\n"
     "Authentic traditional Japanese craft, no modern graphic-design gloss, no cartoon styling, no "
     "big shiny cartoon eye. No text anywhere except, at most, one small red seal-shaped stamp."),

    # ---- 4. the craft line carrying the official artwork ----------------------
    ("wao_fuji_byobu.png", "16:9", [OFFICIAL],
     LOCK_OFFICIAL + FUJI +
     "A RINPA GOLD-LEAF BYOBU FOLDING SCREEN, four panels, photographed straight on. Gold leaf "
     "ground with visible leaf seams. Across the two right panels, Mount Fuji painted large in "
     "soft malachite green and indigo with a thick snow cap in raised white gofun pigment, wrapped "
     "at the base by stylised gold cloud bands. Across the two left panels, stylised silver water "
     "in flowing parallel lines and whirlpools, and the official Fujie applied in silver leaf and "
     "fine metallic pigment, swimming through the water toward the mountain.\n\n"
     "Authentic hand-made screen: a black lacquer frame, fabric hinges, the faint texture of the "
     "leaf. No modern graphic-design gloss. No text anywhere except, at most, one small red "
     "seal-shaped stamp."),

    # ---- 5. wamon goods: the pattern collection on a real object --------------
    ("wamon_fuji_furoshiki.png", "1:1", [OFFICIAL, TILE],
     "TWO images are attached.\n"
     "IMAGE 1 is the OFFICIAL illustration of 'Fujie', Fujikin's sturgeon mascot - a realistic "
     "polished chrome-silver sturgeon in profile. Reproduce it EXACTLY as drawn; on the cloth it "
     "is a printed reproduction of this exact artwork in a single flat colour. Never redraw, "
     "cartoon or reproportion it.\n"
     "IMAGE 2 is the PATTERN: a traditional indigo seigaiha wave pattern drawn for this project. "
     "Reproduce that exact pattern - same motif, same geometry, same two colours - as the dyed "
     "ground of the cloth.\n\n"
     + FUJI + TEXT_GOODS +
     "PHOTOREALISTIC product photography of finely made Japanese goods. THE PRODUCT: a large "
     "indigo-dyed cotton FUROSHIKI wrapping cloth laid out flat and slightly rumpled on a pale "
     "wooden table. The seigaiha pattern covers the whole cloth. Rising out of the pattern in the "
     "centre, resist-dyed in undyed white cloth, a calm wide MOUNT FUJI with its snow cap - the "
     "wave scales of the pattern forming the sea at its foot. The official Fujie is printed in "
     "white across the water in front of the mountain. Natural side light, quiet composition, "
     "wabi-sabi restraint, nothing plasticky."),

    # ---- 6. maison: the luxury line ------------------------------------------
    ("maison_fuji_scarf.png", "1:1", [MONO],
     "The attached sheet is the HOUSE MONOGRAM CANVAS: a repeating small dark-brown sturgeon "
     "motif, concentric ripple rings and a small ring-and-wave crest. Reproduce this monogram "
     "faithfully - same motif, same scale, same drawing.\n\n"
     + FUJI +
     "PHOTOREALISTIC luxury goods photography for an original Japanese maison. THE PRODUCT: a "
     "large square SILK TWILL SCARF, loosely folded and draped on a warm stone surface so the "
     "centre and one corner are readable. The scarf's border is a dense band of the house "
     "monogram in espresso brown on ecru. The centre medallion is a serene MOUNT FUJI rendered in "
     "fine engraved-line hatching - midnight navy, espresso and a single pale gold - rising above "
     "a lake of concentric ripple rings drawn from the same monogram vocabulary. Rolled hand-"
     "stitched hem, soft silk sheen, shallow depth of field, magazine still life.\n\n"
     "*** BRAND RULE - CRITICAL ***\n"
     "This is an original house. Do NOT reproduce, imitate or include the monogram, logo, flower "
     "motif, initials, stripes or hardware stamp of any real fashion brand. No real brand names "
     "or logos anywhere.\n\n"
     + TEXT_GOODS),

    # ---- 7. chibi: the playful line ------------------------------------------
    ("chibi_fuji_acrylic.png", "4:3", [MASTER],
     LOCK_CHIBI + FUJI + TEXT_GOODS +
     "PHOTOREALISTIC commercial product photography, Japanese character-goods quality, crisp "
     "focus, soft even studio lighting, gentle contact shadows, clean uncluttered composition.\n\n"
     "THE PRODUCT: a set of three clear ACRYLIC STANDS on a pale grey shelf, each a printed acrylic "
     "figure slotted into a small clear base. The tallest is a layered diorama stand: a flat "
     "acrylic cut-out of a cute pastel MOUNT FUJI - soft blue cone, rounded white snow cap - sits "
     "behind, and Chibi Fujie floats in front of it on a little curl of cartoon wave, one pectoral "
     "fin raised in a cheerful wave. The two smaller stands are Chibi Fujie alone, one napping "
     "curled up, one peeking out from behind a tiny Mount Fuji. Bright, clean, kawaii shop-shelf "
     "styling."),
]

if __name__ == "__main__":
    for name, aspect, refs, prompt in JOBS:
        print(f"-> {name}", flush=True)
        r = gen(prompt, OUT + name, refs, aspect)
        print(f"   {r}", flush=True)
