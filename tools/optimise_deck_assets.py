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
