"""Ask Gemini to watch and listen to the recorded egg film and critique it.

A second opinion on picture AND sound, since the sound cannot be checked by eye.
Uploads Fujie_Creative/22_egg_film/一粒の卵から_ja.mp4 (tools/egg_film_video.py
makes it) through the Files API and prints the review.
"""
import json, pathlib, sys, time, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
KEY = [l.split("=", 1)[1].strip().strip("'\"") for l in
       (ROOT / "SECRET" / "Gemini.txt").read_text(encoding="utf-8").splitlines() if "GEMINI_API_KEY" in l][0]
MODEL = "gemini-pro-latest"
API = "https://generativelanguage.googleapis.com"

PROMPT = """You are a senior animation director and sound designer reviewing a ~59 second
whimsical cartoon short, "一粒の卵から / From a single egg", for a Japanese corporate mascot
contest (Fujikin's sturgeon mascot Fujie). It is animated live in a browser with synthesised
music-box score and sound effects. Story beats: title egg; 1987 a scientist's remark at a valve
works; 1992 first hatch, 5 of 100 survive; flow control (temperature, flow, oxygen) lifts survival
to 60%; 1998 world-first full life cycle; 2002 first caviar, 10,000+ fish at Satomi; 2027 an egg
hatches into Chibi Fujie, end card.

Watch AND listen closely. Give a frank, specific critique with timestamps:
1. Anything broken, glitchy, cut off, overlapping, unreadable or off-model.
2. Pacing: any beat too fast to read or too slow.
3. Sound: is the music pleasant and in tune, does it fit the mood of each beat, are any
   effects harsh, too loud, too quiet, mistimed, or missing where the picture needs one?
   Any hiss, clicks, muddiness or silence that feels wrong?
4. The 5 most valuable concrete improvements, most important first.
Be concise. No praise padding."""


def req(url, data=None, headers=None, method=None):
    r = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    return urllib.request.urlopen(r, timeout=600)


def main(path):
    raw = path.read_bytes()
    start = req(f"{API}/upload/v1beta/files?key={KEY}", json.dumps({"file": {"display_name": "eggfilm"}}).encode(), {
        "X-Goog-Upload-Protocol": "resumable", "X-Goog-Upload-Command": "start",
        "X-Goog-Upload-Header-Content-Length": str(len(raw)), "X-Goog-Upload-Header-Content-Type": "video/mp4",
        "Content-Type": "application/json"})
    up = start.headers["X-Goog-Upload-URL"]
    f = json.load(req(up, raw, {"X-Goog-Upload-Command": "upload, finalize", "X-Goog-Upload-Offset": "0",
                                "Content-Length": str(len(raw))}))["file"]
    while f.get("state") == "PROCESSING":
        time.sleep(5)
        f = json.load(req(f"{API}/v1beta/{f['name']}?key={KEY}"))
    body = {"contents": [{"parts": [{"file_data": {"mime_type": "video/mp4", "file_uri": f["uri"]}}, {"text": PROMPT}]}]}
    out = json.load(req(f"{API}/v1beta/models/{MODEL}:generateContent?key={KEY}", json.dumps(body).encode(),
                        {"Content-Type": "application/json"}))
    print("".join(p.get("text", "") for p in out["candidates"][0]["content"]["parts"]))
    req(f"{API}/v1beta/{f['name']}?key={KEY}", method="DELETE")


if __name__ == "__main__":
    main(pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "Fujie_Creative" / "22_egg_film" / "一粒の卵から_ja.mp4")
