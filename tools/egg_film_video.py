"""Record the egg film to an MP4, sound and all - a copy to watch and to check.

The film itself lives on the hub and is drawn live in the browser. This drives
the built site headlessly (preview "fujie-dist" on port 8779 must be running),
draws every frame at 30 fps, renders the soundtrack offline, prints a loudness
reading for every two seconds so silence or clipping shows up, and joins it all
with ffmpeg.

  python tools/egg_film_video.py            # Japanese
  python tools/egg_film_video.py en         # English captions

Output: Fujie_Creative/22_egg_film/一粒の卵から_<lang>.mp4
"""
import base64, io, pathlib, shutil, subprocess, sys, wave
import numpy as np
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIR = ROOT / "Fujie_Creative" / "22_egg_film"
TMP = DIR / "_video"
FPS = 30


def main(lang):
    if TMP.exists():
        shutil.rmtree(TMP)
    TMP.mkdir(parents=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1280, "height": 900},
                        locale="ja-JP" if lang == "ja" else "en-US")
        pg.goto("http://localhost:8779/", wait_until="networkidle")
        pg.wait_for_timeout(800)
        pg.evaluate("document.getElementById('story').scrollIntoView()")
        pg.evaluate("window.__eggFilm.ready().then(() => 1)")
        pg.evaluate("""() => { var h=document.getElementById('eggFilm');
            h.style.cssText='position:fixed;left:0;top:0;width:1280px;z-index:99999'; }""")
        end = pg.evaluate("window.__eggFilm.END")
        wav = base64.b64decode(pg.evaluate("window.__eggFilm.renderAudio()"))
        (TMP / "sound.wav").write_bytes(wav)
        n = int(end * FPS)
        for i in range(n):
            data = pg.evaluate("""(t) => { window.__eggFilm.frame(t);
                return document.querySelector('#eggFilm canvas').toDataURL('image/jpeg', .93); }""", i / FPS)
            (TMP / ("f%05d.jpg" % i)).write_bytes(base64.b64decode(data.split(",", 1)[1]))
            if i % 300 == 0:
                print("  frame %d / %d" % (i, n), flush=True)
        b.close()

    with wave.open(io.BytesIO(wav)) as w:
        rate = w.getframerate()
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    a = a.reshape(-1, 2).mean(axis=1)
    print("\nsound, every 2 s (peak / loudness in dB):")
    for s in range(0, int(len(a) / rate), 2):
        c = a[s * rate:(s + 2) * rate]
        rms = 20 * np.log10(np.sqrt(np.mean(c ** 2)) + 1e-9)
        peak = 20 * np.log10(np.max(np.abs(c)) + 1e-9)
        print("  %2d-%2ds  peak %6.1f  loud %6.1f %s" % (s, s + 2, peak, rms, "#" * max(0, int((rms + 50) / 2))))
    clip = int(np.sum(np.abs(a) > .99))
    print("  samples at the ceiling:", clip)

    out = DIR / ("一粒の卵から_%s.mp4" % lang)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(TMP / "f%05d.jpg"),
                    "-i", str(TMP / "sound.wav"), "-c:v", "libx264", "-preset", "slow", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest",
                    "-movflags", "+faststart", str(out)], check=True)
    print("\nWROTE", out.relative_to(ROOT), "%.1f MB" % (out.stat().st_size / 1048576))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "ja")
