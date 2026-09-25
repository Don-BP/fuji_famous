"""Prepare the pictures for the "From a single egg" film (promo/eggfilm.js).

The film's characters are the pet game's own - egg, hatchling, fry, young fish,
the cheering and waving Chibi - so it is the same creature the judges meet in the
game. Backdrops are the game's painted tanks plus the two painted for the film by
tools/run_egg_film_art.py. This sizes them all for the web and writes them to
promo/eggfilm/ as ef_*.webp; tools/build_site.py copies that folder into
dist/assets/ where the film loads them.

The valve and the handwheel come on white and are cut out here. The wheel's
four gaps between its spokes are walled in by the rim, so the usual cut-out
(which floods in from the border) leaves them white; they are cleared from the
inside as well and the result is checked on the dark page colour.
"""
import pathlib, sys
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from cutout import cutout

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE, CRE = ROOT / "site", ROOT / "Fujie_Creative"
FILM = CRE / "22_egg_film"
OUT = ROOT / "promo" / "eggfilm"
TMP = FILM / "_cut"

BACKDROPS = {
    "bg_title": SITE / "art" / "bg_title_wide.jpg",
    "bg_1987": FILM / "bg_1987_a.png",
    "bg_tank": SITE / "art" / "bg_tank_early_wide.jpg",
    "bg_flow": SITE / "art" / "bg_sheet_wide.jpg",
    "bg_cycle": SITE / "art" / "bg_result_wide.jpg",
    "bg_hall": FILM / "bg_hall_b.png",
    "bg_finale": SITE / "art" / "bg_win_wide.jpg",
}
SPRITES = {  # name: (source, width)
    "egg": (SITE / "stage_1_egg.png", 220),
    "larva": (SITE / "stage_2_larva.png", 300),
    "fry": (SITE / "stage_3_fry.png", 340),
    "young": (SITE / "stage_4_young.png", 560),
    "dash": (SITE / "art" / "fujie_dash.png", 620),
    "cheer": (SITE / "art" / "fujie_cheer.png", 760),
    "wave": (SITE / "art" / "title_fujie.png", 760),
    "burst": (SITE / "art" / "hit_burst.png", 560),
}
CUTS = {  # name: (source, width, interior seeds as fractions of the trimmed picture)
    "valve": (FILM / "prop_valve_a.png", 420, []),
    "wheel": (FILM / "prop_wheel_a.png", 640,
              [(.30, .30), (.70, .30), (.30, .70), (.70, .70)]),
}


def fit(im, width):
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    return im


def clear_walled_in(path, seeds):
    """Flood the white gaps that the outline closes off, from inside them."""
    im = Image.open(path).convert("RGBA")
    rgb = im.convert("RGB")
    mark = (255, 0, 255)
    for fx, fy in seeds:
        s = (int(fx * im.width), int(fy * im.height))
        r, g, b = rgb.getpixel(s)
        if min(r, g, b) < 200:
            print("   ! seed %s is not on white (%d,%d,%d) - skipped" % (s, r, g, b))
            continue
        ImageDraw.floodfill(rgb, s, mark, thresh=40)
    hole = np.all(np.array(rgb) == mark, axis=-1)
    a = np.array(im.getchannel("A")).astype(np.float32)
    soft = np.array(Image.fromarray((hole * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3))
                    .filter(ImageFilter.GaussianBlur(1))).astype(np.float32) / 255
    a = a * (1 - soft)
    im.putalpha(Image.fromarray(a.clip(0, 255).astype(np.uint8)))
    return im, int(hole.sum())


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    total = 0
    for name, src in BACKDROPS.items():
        im = fit(Image.open(src).convert("RGB"), 1600)
        dst = OUT / ("ef_%s.webp" % name)
        im.save(dst, "WEBP", quality=84, method=6)
        total += dst.stat().st_size
        print("%-10s %dx%d  %4d KB" % (name, im.width, im.height, dst.stat().st_size // 1024))
    for name, (src, width) in SPRITES.items():
        im = fit(Image.open(src).convert("RGBA"), width)
        dst = OUT / ("ef_%s.webp" % name)
        im.save(dst, "WEBP", quality=90, method=6)
        total += dst.stat().st_size
        print("%-10s %dx%d  %4d KB" % (name, im.width, im.height, dst.stat().st_size // 1024))
    for name, (src, width, seeds) in CUTS.items():
        tmp = TMP / (name + ".png")
        cutout(src, tmp)
        im, n = clear_walled_in(tmp, seeds) if seeds else (Image.open(tmp).convert("RGBA"), 0)
        # the generator leaves a faint pale halo just outside the navy outline;
        # pull the edge in two pixels - the outline is thicker than that
        im.putalpha(im.getchannel("A").filter(ImageFilter.MinFilter(3)))
        im = im.crop(im.getbbox())
        if name == "wheel":
            # the wheel is a true circle: cut it to one, which removes the halo cleanly
            d = min(im.size)
            big = Image.new("L", (d * 4, d * 4), 0)
            m = int(d * 4 * .016)
            ImageDraw.Draw(big).ellipse((m, m, d * 4 - m, d * 4 - m), fill=255)
            disc = big.resize((d, d), Image.LANCZOS)
            im = im.crop(((im.width - d) // 2, (im.height - d) // 2,
                          (im.width - d) // 2 + d, (im.height - d) // 2 + d))
            im.putalpha(Image.fromarray(np.minimum(np.array(im.getchannel("A")), np.array(disc))))
        im = fit(im, width)
        dst = OUT / ("ef_%s.webp" % name)
        im.save(dst, "WEBP", quality=90, method=6)
        total += dst.stat().st_size
        # proof on the page's dark colour, so trapped white cannot hide
        proof = Image.new("RGBA", im.size, (4, 18, 26, 255))
        proof.alpha_composite(im)
        proof.convert("RGB").save(TMP / (name + "_on_dark.jpg"), quality=85)
        print("%-10s %dx%d  %4d KB  (%d walled-in px cleared)" % (name, im.width, im.height,
              dst.stat().st_size // 1024, n))
    print("\nWROTE %s  (%.1f MB)" % (OUT, total / 1048576))


if __name__ == "__main__":
    main()
