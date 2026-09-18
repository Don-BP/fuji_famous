"""Assemble the public site into dist/.

  dist/            the FUJIE STUDIO hub          (from promo/)
  dist/game/       Raise Fujie, untouched        (from site/)
  dist/timeline/   the scrolling history         (from promo/timeline/)
  dist/assets/     every gallery image, web-sized, plus thumbnails

Run this, then deploy dist/ to gh-pages.
"""
import hashlib, pathlib, re, shutil, sys
from PIL import Image

ROOT = pathlib.Path(r"D:\Fuji_Famous")
SITE = ROOT / "site"
PROMO = ROOT / "promo"
CRE = ROOT / "Fujie_Creative"
DIST = ROOT / "dist"
ASSETS = DIST / "assets"
THUMBS = ASSETS / "t"

BIG, THUMB, Q = 1600, 700, 82

GALLERY_DIRS = ["01_character", "02_stickers", "03_plushie", "07_merch_chibi",
                "08_merch_official", "09_merch_maison", "10_merch_wa", "11_wamon",
                "12_merch_official_2", "13_merch_wamon", "14_merch_wa_official",
                 "17_act2_gallery", "21_manholes",
                # the Fuji collection: one folder per line, flat filenames
                "19_fujisan", "19_fujisan/chibi", "19_fujisan/official",
                "19_fujisan/wa", "19_fujisan/wa_official", "19_fujisan/wamon",
                "19_fujisan/maison", "19_fujisan/plush"]

# art the promo pages need as-is (alpha kept, no re-encoding to JPEG)
VERBATIM = [
    (SITE / "fujie-official.png", "fujie-official.png"),
    (SITE / "stage_1_egg.png", "stage_1_egg.png"),
    (SITE / "stage_2_larva.png", "stage_2_larva.png"),
    (SITE / "stage_3_fry.png", "stage_3_fry.png"),
    (SITE / "stage_4_young.png", "stage_4_young.png"),
    (SITE / "favicon.png", "favicon.png"),
    (SITE / "art" / "fujie_cheer.png", "hero_chibi.png"),
    (CRE / "01_character" / "chibi_neutral.png", "buddy_neutral.png"),
    # the same chibi, actually swimming - the floating buddy on the hub
    (CRE / "01_character" / "chibi_neutral_swim.webp", "buddy_swim.webp"),
    (SITE / "art" / "bg_egg.jpg", "bg_egg.jpg"),
    (SITE / "art" / "bg_tank_early.jpg", "bg_tank_early.jpg"),
    (SITE / "art" / "bg_tank_grown.jpg", "bg_tank_grown.jpg"),
    (SITE / "art" / "bg_win.jpg", "bg_win.jpg"),
    (CRE / "20_new_ideas" / "aquaworld_c_both.png", "idea_aquaworld.png"),
    (CRE / "20_new_ideas" / "letter_final.png", "idea_letter.png"),
    (CRE / "20_new_ideas" / "cover_set_sheet.png", "idea_manhole.png"),
    (CRE / "20_new_ideas" / "openday_final.jpg", "idea_openday.jpg"),
    (CRE / "20_new_ideas" / "sday_final.png", "idea_sday.png"),
    (CRE / "20_new_ideas" / "voice_final.png", "idea_voice.png"),
    (CRE / "20_new_ideas" / "day2027_final.png", "idea_day2027.png"),
]


def jpeg(src, dest, cap):
    im = Image.open(src)
    if im.mode in ("RGBA", "LA", "P"):
        bg = Image.new("RGB", im.size, (250, 249, 245))
        im = im.convert("RGBA")
        bg.paste(im, mask=im.getchannel("A"))
        im = bg
    else:
        im = im.convert("RGB")
    if max(im.size) > cap:
        r = cap / max(im.size)
        im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    im.save(dest, "JPEG", quality=Q, optimize=True, progressive=True)
    return dest.stat().st_size


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    THUMBS.mkdir(parents=True)

    # ---- the game, exactly as it is ----
    shutil.copytree(SITE, DIST / "game",
                    ignore=shutil.ignore_patterns("master.png", "*.md"))
    print("game/      copied")

    # ---- the hub and the timeline ----
    # The script and stylesheet names never change, so a browser that has been
    # to the studio before keeps serving yesterday's gallery list and yesterday's
    # switch from its own cache and there is no way to tell from the outside.
    # Stamping each reference with a hash of the file forces a fresh fetch the
    # moment the file actually changes, and never otherwise.
    for f in ("index.html", "hub.css", "hub.js", "hero.js", "data.js", "buddy.js", "cases.js"):
        shutil.copy2(PROMO / f, DIST / f)
    shutil.copytree(PROMO / "timeline", DIST / "timeline")

    html = (DIST / "index.html").read_text(encoding="utf-8")
    for f in ("hub.css", "hub.js", "hero.js", "data.js", "buddy.js", "cases.js"):
        v = hashlib.sha1((DIST / f).read_bytes()).hexdigest()[:8]
        html = html.replace('"%s"' % f, '"%s?v=%s"' % (f, v))
    (DIST / "index.html").write_text(html, encoding="utf-8")
    print("hub + timeline/ copied (assets version-stamped)")

    # ---- the hero film: 73 stills, already web-sized, copied verbatim ----
    film = PROMO / "film"
    if film.exists():
        shutil.copytree(film, ASSETS / "film")
        n = sum(1 for _ in (ASSETS / "film").rglob("*.webp"))
        print("assets/film %d frames copied" % n)
    else:
        print("  ! no promo/film - the hero film will fall back to the still")

    # ---- gallery images ----
    total = n = 0
    for folder in GALLERY_DIRS:
        d = CRE / folder
        if not d.exists():
            print("  ! missing folder", folder)
            continue
        for p in sorted(d.iterdir()):
            if p.is_dir() or p.suffix.lower() not in (".png", ".jpg", ".jpeg"):
                continue
            total += jpeg(p, ASSETS / (p.stem + ".jpg"), BIG)
            jpeg(p, THUMBS / (p.stem + ".jpg"), THUMB)
            n += 1
    print("assets/    %d images, %.1f MB" % (n, total / 1048576))

    # ---- art used directly by the pages ----
    for src, name in VERBATIM:
        if src.exists():
            shutil.copy2(src, ASSETS / name)
        else:
            print("  ! missing", src.name)

    # ---- the two feature screenshots, if they have been captured ----
    for shot in ("shot_game.jpg", "shot_timeline.jpg"):
        src = PROMO / "shots" / shot
        if src.exists():
            jpeg(src, ASSETS / shot, 1400)
        else:
            fallback = SITE / "art" / ("bg_title.jpg" if "game" in shot else "bg_egg.jpg")
            jpeg(fallback, ASSETS / shot, 1400)
            print("  (placeholder for %s - capture one and rerun)" % shot)

    (DIST / ".nojekyll").write_text("")

    # the copy of the game that lives inside the unlisted studio folder must not
    # be indexed either - the public copy at the site root is the indexable one
    gi = DIST / "game" / "index.html"
    html = gi.read_text(encoding="utf-8")
    if 'name="robots"' not in html:
        html = html.replace('<meta charset="utf-8">',
                            '<meta charset="utf-8">\n'
                            '<meta name="robots" content="noindex,nofollow">', 1)

    # The game's scripts carried a hand-typed "?v=6". Forget to bump it and every
    # returning player keeps yesterday's game from their own cache - exactly the
    # fault that hid two studio fixes. Stamp them with a hash of the file instead,
    # so the number looks after itself.
    for f in ("app.css", "i18n.js", "game.js"):
        v = hashlib.sha1((DIST / "game" / f).read_bytes()).hexdigest()[:8]
        html = re.sub(r'(["\'])%s(\?v=[^"\']*)?\1' % re.escape(f),
                      lambda m: '%s%s?v=%s%s' % (m.group(1), f, v, m.group(1)), html)
    gi.write_text(html, encoding="utf-8")

    # ---- every id in data.js must exist ----
    ids = re.findall(r'\["([\w\-]+)"', (PROMO / "data.js").read_text(encoding="utf-8"))
    missing = [i for i in ids if not (ASSETS / (i + ".jpg")).exists()]
    if missing:
        print("\n!! data.js refers to images that were not built:")
        for m in missing:
            print("   -", m)
        sys.exit(1)
    print("checked     %d gallery ids all present" % len(ids))

    # ---- every picture a page asks for must actually be there ----
    #
    # The check above only proves the gallery's full-size images exist. It says
    # nothing about the thumbnails the tiles use, nor about any picture written
    # straight into the markup, so a tile could point at a file that was never
    # built and the build would still say it was happy. This walks every built
    # page and resolves every local src and href it finds.
    broken = []
    for page in sorted(DIST.rglob("*.html")):
        markup = page.read_text(encoding="utf-8")
        for ref in re.findall(r'(?:src|href)\s*=\s*"([^"]+)"', markup):
            ref = ref.split("?")[0].split("#")[0]
            if not ref or ref.startswith(("http", "//", "data:", "mailto:", "#")):
                continue
            target = (DIST / ref.lstrip("/")) if ref.startswith("/") else (page.parent / ref)
            if not target.exists():
                broken.append("%s -> %s" % (page.relative_to(DIST), ref))
    if broken:
        print("\n!! pages point at files that are not there:")
        for b in broken:
            print("   -", b)
        sys.exit(1)
    print("checked     every picture and link on every page resolves")

    # ---- no contents tile left blank when its idea has a picture ----
    #
    # A tile marked "ph" draws a dashed blank instead of a picture. That is
    # right for an idea with no artwork yet, but three tiles stayed blank long
    # after their pictures had been made and shipped further down the same
    # page, and nothing ever said so. If the section a tile points at has a
    # picture, the tile has no business being blank.
    home = (DIST / "index.html").read_text(encoding="utf-8")
    stranded = []
    for target in re.findall(r'<a href="#([\w-]+)" class="ph[^"]*">', home):
        section = re.search(r'<section id="%s".*?</section>' % re.escape(target),
                            home, re.S)
        if section and "<img" in section.group(0):
            stranded.append(target)
    if stranded:
        print("\n!! these contents tiles are blank but their idea has a picture:")
        for t in stranded:
            print("   -", t)
        sys.exit(1)
    print("checked     no contents tile is blank while its picture exists")

    mb = sum(f.stat().st_size for f in DIST.rglob("*") if f.is_file()) / 1048576
    print("\nWROTE %s  (%.1f MB)" % (DIST, mb))


if __name__ == "__main__":
    main()
