"""Render still frames of the egg film from the built site, for checking.

Needs the dist server running (preview "fujie-dist", port 8779). Draws the
film at chosen moments via window.__eggFilm.frame(t) and saves full-size PNGs,
plus one contact sheet, into Fujie_Creative/22_egg_film/_frames/.

  python tools/egg_film_frames.py 3.9 8.5 14        # these moments
  python tools/egg_film_frames.py --every 2         # one every 2 seconds
  python tools/egg_film_frames.py --lang en ...     # English captions
"""
import base64, pathlib, sys
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "Fujie_Creative" / "22_egg_film" / "_frames"
URL = "http://localhost:8779/"


def main(args):
    lang = "ja"
    if "--lang" in args:
        i = args.index("--lang"); lang = args[i + 1]; del args[i:i + 2]
    if "--every" in args:
        step = float(args[args.index("--every") + 1])
        times = [round(x * step, 2) for x in range(int(59 / step) + 1)]
    else:
        times = [float(a) for a in args] or [3.9]
    OUT.mkdir(parents=True, exist_ok=True)
    shots = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1280, "height": 900}, locale="ja-JP" if lang == "ja" else "en-US")
        pg.goto(URL, wait_until="networkidle")
        pg.wait_for_timeout(800)
        pg.evaluate("document.getElementById('story').scrollIntoView()")
        pg.evaluate("window.__eggFilm.ready().then(() => 1)")
        pg.evaluate("""() => { var h=document.getElementById('eggFilm'); h.style.cssText='position:fixed;left:0;top:0;width:1280px;z-index:99999'; }""")
        for t in times:
            data = pg.evaluate("""(t) => { window.__eggFilm.frame(t);
                return document.querySelector('#eggFilm canvas').toDataURL('image/png'); }""", t)
            f = OUT / ("%s_%05.1f.png" % (lang, t))
            f.write_bytes(base64.b64decode(data.split(",", 1)[1]))
            shots.append(f)
        b.close()
    cols = 3 if len(shots) > 4 else len(shots)
    tw, th = 640, 360
    rows = (len(shots) + cols - 1) // cols
    sheet = Image.new("RGB", (tw * cols, th * rows))
    for i, f in enumerate(shots):
        sheet.paste(Image.open(f).convert("RGB").resize((tw, th)), ((i % cols) * tw, (i // cols) * th))
    sheet.save(OUT / "sheet.jpg", quality=86)
    print("wrote %d frames + sheet.jpg" % len(shots))


if __name__ == "__main__":
    main(sys.argv[1:])
