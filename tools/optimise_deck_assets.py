"""Build compressed copies of every image the deck uses, preserving aspect ratios.

Photographs and sticker sheets become JPEG; artwork that needs a transparent
background stays PNG. Layout is unaffected because proportions are unchanged.
"""
import pathlib, shutil
from PIL import Image

SRC = pathlib.Path(r"D:\Fuji_Famous\Fujie_Creative")
DST = SRC / "deck_assets"

# (relative path, keep alpha?, max pixels on the long edge)
FILES = [
    ("01_character/master_v3_wave.png",        False, 900),
    ("01_character/master_expressions.png",    False, 1700),
    ("02_stickers/sticker_sheet_01.png",       False, 1500),
    ("02_stickers/sticker_sheet_02.png",       False, 1500),
    ("03_plushie/plush_studio_front.png",      False, 1200),
    ("03_plushie/plush_size_lineup.png",       False, 1600),
    ("03_plushie/plush_keychain_lifestyle.png", False, 1000),
    ("04_campaign/fujie-official.png",         True,  1600),
    ("04_campaign/stage_1_egg.png",            True,  700),
    ("04_campaign/stage_2_larva.png",          True,  700),
    ("04_campaign/stage_3_fry.png",            True,  900),
    ("04_campaign/stage_4_young.png",          True,  900),
    # the goods slides - one hero per line, then the Fuji collection
    ("07_merch_chibi/gacha_capsule_set.png",   False, 1400),
    ("12_merch_official_2/official_gift_set.png", False, 1400),
    ("09_merch_maison/maison_tote.png",        False, 1400),
    ("13_merch_wamon/wamon_shop_table.png",    False, 1600),
    ("10_merch_wa/wa_ukiyoe_wave.png",         False, 1600),
    ("11_wamon/wamon_collection_board.png",    False, 1600),
    ("13_merch_wamon/wamon_sensu.png",         False, 1200),
    ("19_fujisan/badge_40_fuji.png",           False,  900),
    ("19_fujisan/wa/wa_fuji_ukiyoe.png",       False, 1600),
    ("19_fujisan/wa_official/wao_fuji_byobu.png", False, 1600),
    ("19_fujisan/wamon/wamon_fuji_furoshiki.png", False, 1200),
    ("19_fujisan/maison/maison_fuji_scarf.png", False, 1200),
    ("19_fujisan/chibi/chibi_fuji_gacha.png",  False, 1200),
    ("19_fujisan/official/official_fuji_glass.png", False, 1200),
    # the mascot keychain slide
    ("03_plushie/plush_mascot_set.png",         False, 1600),
    ("03_plushie/plush_mascot_rail.png",        False, 1400),
    ("03_plushie/plush_mascot_blindbag.png",    False, 1400),
    # one picture per new idea, sitting in the corner of its own slide - the
    # box is under five inches wide, so 1100px is already more than the
    # slide can show
    ("20_new_ideas/aquaworld_c_both.png",       False, 1100),
    ("20_new_ideas/letter_final.png",           False, 1100),
    ("20_new_ideas/cover_set_sheet.png",        False, 1100),
    ("20_new_ideas/openday_final.jpg",          False, 1100),
    ("20_new_ideas/sday_final.png",             False, 1100),
]

total_before = total_after = 0
for rel, keep_alpha, maxpx in FILES:
    src = SRC / rel
    if not src.exists():
        print("  ! missing", rel)
        continue
    before = src.stat().st_size
    im = Image.open(src)
    if max(im.size) > maxpx:
        r = maxpx / max(im.size)
        im = im.resize((max(1, int(im.width * r)), max(1, int(im.height * r))), Image.LANCZOS)

    out = DST / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    if keep_alpha:
        im.convert("RGBA").save(out, "PNG", optimize=True)
    else:
        # flatten onto white, then JPEG
        flat = Image.new("RGB", im.size, (255, 255, 255))
        im = im.convert("RGBA")
        flat.paste(im, mask=im.split()[3])
        out = out.with_suffix(".jpg")
        flat.save(out, "JPEG", quality=84, optimize=True, progressive=True)

    after = out.stat().st_size
    total_before += before
    total_after += after
    print("%-42s %7.0fKB -> %6.0fKB  %s" % (rel, before / 1024, after / 1024, out.suffix))

print("\ntotal  %.1f MB -> %.1f MB" % (total_before / 1048576, total_after / 1048576))
