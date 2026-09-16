"""和紋 goods - the pattern collection put on real objects, with the OFFICIAL Fujie.

Each shot gets two references: the official illustration, reproduced exactly, and
one pattern tile from the collection, reproduced as the cloth or the print. The
patterns were drawn for this fish in tools/run_wamon.py and run_wamon2.py, so the
goods and the swatches stay in step.

Output: Fujie_Creative/13_merch_wamon/
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen

OFFICIAL = "D:/Fuji_Famous/Documents_for_dev/05_fujie_絵柄例.png"
T = "D:/Fuji_Famous/Fujie_Creative/11_wamon/tiles/"
T2 = "D:/Fuji_Famous/Fujie_Creative/11_wamon/tiles2/"
OUT = "D:/Fuji_Famous/Fujie_Creative/13_merch_wamon/"

LOCK = (
    "TWO images are attached.\n"
    "IMAGE 1 is the OFFICIAL illustration of 'Fujie', Fujikin's sturgeon mascot: a realistic "
    "polished chrome-silver sturgeon in profile, long flat pointed snout, four barbels beneath it, "
    "five rows of pale bony scutes, a small dark eye set high and forward, a large swept tail. "
    "Reproduce it EXACTLY as drawn wherever it appears. Do NOT redraw, restyle, cartoon, recolour "
    "or reproportion it, and never give it a big cartoon eye or a smile. On the product it is a "
    "print, a foil stamp, an embroidery, an inlay or an engraving of this exact artwork.\n"
    "IMAGE 2 is the PATTERN: a traditional Japanese wamon drawn for this project. Reproduce that "
    "exact pattern - same motif, same geometry, same two colours - as the cloth, paper or printed "
    "surface of the product. Do not substitute a different Japanese pattern.\n\n"
)

CRAFT = (
    "PHOTOREALISTIC product photography of finely made Japanese goods. Real materials: dyed cotton "
    "and silk, indigo, washi, lacquer, brass, leather, wood. Natural side light, quiet composition, "
    "a lot of empty space, wabi-sabi restraint. Nothing plasticky, no modern graphic-design gloss.\n\n"
    "*** TEXT RULE ***\n"
    "The only words permitted anywhere are FUJIE, FUJIKIN and the katakana フジィ, small and "
    "discreet, or a single small red seal stamp. No other words in any language, no invented kanji "
    "or kana, no captions, no small print.\n\n"
)

JOBS = [
    ("A SENSU FOLDING FAN opened on a dark wooden table. The silk leaf carries the pattern across "
     "the whole fan and the official Fujie is printed large across the centre in silver, swimming "
     "with the wave arcs. Polished bamboo ribs, a silk tassel at the rivet.",
     "wamon_sensu.png", "4:3", T2 + "seigaiha_fujie_vermilion.png"),
    ("A LONG WALLET (nagasaifu) in indigo-dyed cloth over leather, lying closed on a linen surface "
     "with a second one opened beside it. The cloth carries the pattern; the official Fujie is "
     "foil-stamped small in gold at the lower right of the closed wallet. Brass snap, neat stitching.",
     "wamon_long_wallet.png", "4:3", T2 + "kikko_valve_gold.png"),
    ("A BOSTON-STYLE WEEKEND BAG in heavy indigo sashiko-stitched cotton with tan leather handles "
     "and base, standing on a wooden floor. The body carries the pattern; the official Fujie is "
     "embroidered large in off-white thread across the side panel.",
     "wamon_weekend_bag.png", "4:3", T + "asanoha_indigo.png"),
    ("A KINCHAKU DRAWSTRING POUCH and a small zip pouch on a pale linen cloth, both in cotton "
     "printed with the pattern, the official Fujie printed once on the face of each in a single "
     "dark ink, cotton drawstring cords.",
     "wamon_pouches.png", "4:3", T + "uroko_indigo.png"),
    ("A SET OF THREE HANDKERCHIEFS folded and stacked on a wooden tray, each in a different "
     "colourway of the pattern, the top one opened to show the official Fujie printed large in the "
     "centre in a single flat ink. Hand-rolled hems, soft daylight.",
     "wamon_handkerchiefs.png", "4:3", T + "seigaiha_vermilion.png"),
    ("A STACK OF NOTEPADS AND MEMO BLOCKS on a dark desk, their covers papered in the pattern like "
     "chiyogami, the top pad open to a blank page with the official Fujie printed small at the head "
     "of the sheet, a brass pencil resting across it.",
     "wamon_notepads.png", "4:3", T2 + "roe_komon_indigo.png"),
    ("A FUROSHIKI cloth printed with the pattern, tied around a square box in the classic knot on a "
     "tatami surface, the official Fujie printed large on the visible face of the cloth, the knot "
     "casting a soft shadow.",
     "wamon_furoshiki_wrapped.png", "4:3", T + "shippo_indigo.png"),
    ("A MEISHI CARD CASE in black urushi lacquer on a dark cloth, its lid decorated in maki-e: the "
     "pattern in fine gold powder across the surface and the official Fujie inlaid in silver across "
     "the centre, a fine gold rim line, the lid slightly offset.",
     "wamon_makie_card_case.png", "4:3", T2 + "karakusa_nagare_gold.png"),
    ("A TENUGUI cloth hanging from a wooden rail against a plaster wall, printed with the pattern "
     "over its whole length with the official Fujie printed large near the lower end, the cloth "
     "moving slightly in the light.",
     "wamon_tenugui.png", "3:4", T + "tatewaku_indigo.png"),
    ("A SAKE SET on a black lacquer tray: a porcelain tokkuri flask and two cups, each glazed white "
     "and decorated in cobalt blue with the pattern, and the official Fujie printed on the flask in "
     "a single blue underglaze transfer. Quiet natural light.",
     "wamon_sake_set.png", "4:3", T + "kanoko_vermilion.png"),
    ("A LONG UMBRELLA open and leaning against a wall, the canopy printed with the pattern across "
     "every panel and the official Fujie printed once, large, spanning two panels in silver-grey. "
     "Bamboo handle, dark metal ferrule.",
     "wamon_umbrella.png", "4:3", T2 + "yagasuri_nagare_indigo.png"),
    ("A DISPLAY TABLE in a craft shop, photographed from slightly above: the fan, the long wallet, "
     "the folded handkerchiefs, the pouches and the notepads laid out together on a dark wooden "
     "surface, all sharing the same pattern family, with a small brass stand holding a card "
     "showing the official Fujie. Warm shop light, tidy and inviting.",
     "wamon_shop_table.png", "16:9", T2 + "ichimatsu_fujie_indigo.png"),
]

for prompt, name, aspect, tile in JOBS:
    r = gen(LOCK + CRAFT + prompt, OUT + name, refs=[OFFICIAL, tile], aspect=aspect)
    print(json.dumps({"job": name, "ok": not isinstance(r, dict),
                      "r": r if isinstance(r, dict) else "saved"}, ensure_ascii=False), flush=True)
