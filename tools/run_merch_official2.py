"""The official line, widened - real goods carrying the OFFICIAL Fujie artwork.

Every shot is given the official illustration as its first reference and is told
to reproduce it exactly as drawn. Nothing is restyled, recoloured or redrawn:
the fish appears on each product the way a printer, an engraver or an embroidery
machine would put it there.

Output: Fujie_Creative/12_merch_official_2/
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen

OFFICIAL = "D:/Fuji_Famous/Documents_for_dev/05_fujie_絵柄例.png"
OUT = "D:/Fuji_Famous/Fujie_Creative/12_merch_official_2/"

LOCK = (
    "The attached image is the OFFICIAL illustration of 'Fujie', Fujikin's sturgeon mascot. "
    "Reproduce it EXACTLY as drawn wherever it appears on the product: a realistic polished "
    "chrome-silver sturgeon in profile, long flat pointed snout, four barbels hanging beneath the "
    "snout, five rows of pale bony scutes along the body, a small dark eye set high and forward, "
    "large swept tail, smooth metallic gradients and crisp white specular highlights.\n\n"
    "*** ARTWORK RULE - CRITICAL ***\n"
    "Do NOT redraw, restyle, simplify, cartoon, recolour, flip the anatomy or change the "
    "proportions of this illustration. Do not give it a big cartoon eye, a smile, arms or legs. It "
    "is reproduced on the goods as a print, an engraving, an embossing, a foil stamp or an "
    "embroidery of this exact artwork, at whatever single flat colour the process implies.\n\n"
)

HOUSE = (
    "PHOTOREALISTIC product photography for a premium Japanese corporate gift line. Restrained "
    "palette: deep navy, charcoal, warm off-white washi, brushed silver and a single accent of "
    "Fujikin corporate blue. Fine concentric water-ripple line work is the house graphic device and "
    "may appear around the fish. Soft directional studio light, shallow depth of field, generous "
    "empty space, nothing cluttered.\n\n"
    "*** TEXT RULE ***\n"
    "The only words permitted anywhere are FUJIE, FUJIKIN and the katakana フジィ, and only small "
    "and discreet. No other words in any language, no slogans, no invented kanji or kana, no small "
    "print, no price tags, no packaging blurb.\n\n"
)

JOBS = [
    ("A structured leather briefcase-style tote in deep navy full-grain leather standing on a pale "
     "stone surface, the official Fujie blind-debossed large and low on the front panel so it reads "
     "only as a change in the leather, brushed silver hardware, a single ripple line tooled beneath "
     "it.",
     "official_leather_tote.png", "4:3"),
    ("A heavyweight natural canvas tote bag hanging against a plaster wall, the official Fujie "
     "screen-printed large across the front in a single deep navy ink with fine ripple rings behind "
     "it, navy webbing handles.",
     "official_canvas_tote.png", "4:3"),
    ("A presentation card of metal lapel pins on deep navy board, photographed slightly from above: "
     "one polished silver pin of the official Fujie in full profile, one small round pin of three "
     "ripple rings, and a slim silver tie bar with the fish etched along it. Hard enamel and "
     "polished plating, soft specular highlights.",
     "official_pin_set.png", "4:3"),
    ("Three hardcover notebooks fanned on a walnut desk - navy, charcoal and off-white washi - each "
     "with the official Fujie stamped in silver foil on the cover above a single fine ripple line, "
     "a slim silver pen resting alongside.",
     "official_notebooks.png", "4:3"),
    ("A set of three folded cotton handkerchiefs on a linen cloth, photographed from above: one "
     "off-white with the official Fujie printed small in the corner, one pale grey with the fish "
     "printed large across the diagonal, one navy with the fish woven in tone-on-tone. Crisp hemmed "
     "edges, soft daylight.",
     "official_handkerchiefs.png", "4:3"),
    ("A long-handled umbrella leaning open against a grey wall, deep navy canopy with the official "
     "Fujie printed once, large, across two panels in pale silver-grey, a wooden handle and a "
     "polished metal ferrule.",
     "official_umbrella.png", "4:3"),
    ("Two heavy crystal rocks glasses on a dark bar surface, the official Fujie sand-etched into the "
     "side of the nearer glass with concentric ripple rings etched into the thick base, warm low "
     "light raking through the glass.",
     "official_glassware.png", "4:3"),
    ("A desk set photographed from above on charcoal felt: a silver business-card holder with the "
     "official Fujie engraved on the lid, a solid metal paperweight with the fish in relief, and a "
     "navy leather card wallet blind-embossed with the same artwork.",
     "official_desk_set.png", "4:3"),
    ("A rigid navy gift box with its lid lifted, the official Fujie foil-stamped in silver on the "
     "lid, inside a folded off-white handkerchief, a small pin card and a notebook nested in dark "
     "grey tissue, a narrow silver-grey ribbon beside it.",
     "official_gift_set.png", "4:3"),
    ("A corporate reception wall in brushed stainless steel and dark stone: the official Fujie "
     "mounted large as a polished metal relief with fine engraved ripple rings radiating out behind "
     "it, soft architectural lighting, a low bench in the foreground.",
     "official_wall_relief.png", "16:9"),
]

for prompt, name, aspect in JOBS:
    r = gen(LOCK + HOUSE + prompt, OUT + name, refs=[OFFICIAL], aspect=aspect)
    print(json.dumps({"job": name, "ok": not isinstance(r, dict),
                      "r": r if isinstance(r, dict) else "saved"}, ensure_ascii=False), flush=True)
