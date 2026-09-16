"""Maison Fujie - the luxury leather-goods line built on the monogram canvas.

The canvas itself is rendered first by tools/run_monogram.py from the official
illustration; it is attached to every shot so the whole line carries one mark.
No existing fashion house is referenced, named or reproduced - the house here is
Fujikin's own.
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen

MONO = "D:/Fuji_Famous/Fujie_Creative/09_merch_maison/monogram_ecru.png"
MONO_D = "D:/Fuji_Famous/Fujie_Creative/09_merch_maison/monogram_midnight.png"
OUT = "D:/Fuji_Famous/Fujie_Creative/09_merch_maison/"

CANVAS = (
    "The attached sheet is the HOUSE MONOGRAM CANVAS: a tan coated canvas printed with a small "
    "repeating dark-brown sturgeon motif, concentric ripple rings and a small ring-and-wave crest. "
    "Reproduce this canvas faithfully on the product - same motif, same scale relative to the bag, "
    "same tan and dark-brown colours, printed flat on the coated canvas with no gloss of its own.\n\n"
)

HOUSE = (
    "PHOTOREALISTIC luxury goods photography for a Japanese maison: hand-finished leather trim in "
    "deep espresso or midnight navy, brushed gold or palladium hardware, saddle stitching in waxed "
    "linen thread, clean edge painting. Studio lighting on a warm stone or marble surface, shallow "
    "depth of field, magazine-quality still life, restrained and expensive.\n\n"
    "*** BRAND RULE - CRITICAL ***\n"
    "This is an original house. Do NOT reproduce, imitate or include the monogram, logo, flower "
    "motif, initials, stripes or hardware stamp of any real fashion brand. No real brand names or "
    "logos anywhere in the image.\n\n"
    "*** TEXT RULE ***\n"
    "The only words allowed anywhere are FUJIE and FUJIKIN, and only if they appear small and "
    "discreet on a leather patch or a stamped plaque. No other words in any language, no slogans, "
    "no invented kanji, no small print.\n\n"
)

JOBS = [
    ("A large soft travel duffle bag in the monogram canvas with espresso leather handles, trim and "
     "a leather base, brushed gold zip pulls and a small leather luggage tag, standing three-quarter "
     "on a pale marble slab against a warm grey wall.",
     "maison_duffle.png", "4:3", MONO),
    ("A structured open-top tote in the monogram canvas with wide espresso leather handles and a "
     "leather-bound rim, photographed three-quarter from above, a small matching zip pouch resting "
     "against it, on a warm limestone surface.",
     "maison_tote.png", "4:3", MONO),
    ("Two stacked hard trunk cases in the monogram canvas, espresso leather corners and edge beading, "
     "brass corner caps, brass latches and a brass lock plate, the smaller trunk on top, lit from the "
     "side in a dim panelled room.",
     "maison_trunks.png", "4:3", MONO),
    ("A flat lay on dark walnut of small leather goods in the monogram canvas: a bifold card holder, "
     "a round luggage tag on a leather loop, a zip coin pouch and a slim passport cover, each edged "
     "in espresso leather with brushed gold hardware, arranged with generous space between them.",
     "maison_small_goods.png", "4:3", MONO),
    ("A large silk twill scarf laid out and softly folded on a pale surface. The silk is ivory with a "
     "deep navy and gold border, a field of fine concentric water ripples, and elegant realistic "
     "sturgeon swimming through it - a printed silk design, not a canvas. A corner is turned to show "
     "the hand-rolled hem.",
     "maison_silk_scarf.png", "1:1", MONO),
    ("A midnight-navy monogram canvas weekend bag with palladium hardware and black leather trim, "
     "photographed on a dark stone floor beside a leather-wrapped umbrella handle, low moody "
     "lighting, one strong highlight along the top seam.",
     "maison_midnight_bag.png", "16:9", MONO_D),
    ("A boutique vitrine: a narrow lit display shelf in warm oak and brass holding three pieces from "
     "the line - the duffle, the tote and a small pouch - evenly spaced on brass risers, a plain "
     "brushed brass plaque on the shelf edge, dark polished floor, warm gallery lighting.",
     "maison_boutique.png", "16:9", MONO),
]

for prompt, name, aspect, ref in JOBS:
    r = gen(CANVAS + HOUSE + prompt, OUT + name, refs=[ref], aspect=aspect)
    print(json.dumps({"job": name, "ok": not isinstance(r, dict),
                      "r": r if isinstance(r, dict) else "saved"}, ensure_ascii=False), flush=True)
