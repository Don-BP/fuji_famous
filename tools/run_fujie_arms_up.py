"""Chibi Fujie throws both flippers up - a short clip for the egg film's finale.

The film used to swap the cheering drawing for the waving drawing in one frame,
which read as a jump. This makes the real movement instead: he starts from the
approved master pose (chibi_neutral.png) and lifts both flippers high in a happy
cheer, then waves them.

Made the same way as the hub's swimming Chibi (tools/run_buddy_swim.py): the
owner's local ComfyUI, MiniMax H3 Ultra Turbo image-to-video, using the exact
prompt graph that worked for the swim clip (Fujie_Creative/01_character/
swim_src/comfyui_prompt.json) with a new first frame, new motion prompt and a
longer duration. Plain white background, so it can be cut out afterwards by
tools/build_egg_film_arms.py.

  python tools/run_fujie_arms_up.py [takes]

Raw renders go to Fujie_Creative/22_egg_film/arms_src/arms_<n>.mp4, never
overwritten (an existing file moves to old/).
"""
import json, pathlib, shutil, sys, time, urllib.parse, urllib.request, uuid
from datetime import datetime
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHAR = ROOT / "Fujie_Creative" / "01_character"
OUT = ROOT / "Fujie_Creative" / "22_egg_film" / "arms_src"
COMFY = "http://127.0.0.1:8188"
COMFY_INPUT = pathlib.Path(r"D:\ComfyUI-Easy-Install\ComfyUI\input\minimax_h3")
IN_NAME = "fujie_arms_in.png"
SECONDS = 3.0

PROMPT = """For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] A flat two-dimensional cartoon illustration on a plain, empty, pure white background. <Picture 1> shows a chubby chibi sturgeon mascot drawn in a clean, thick dark outline style with flat cel shading in grey and pale silver-white: a long flat pointed snout, four small barbels hanging beneath the snout, one large round black eye with a white highlight, a small smiling mouth, a row of small bony scutes along its back, two side flippers, small belly fins and a single upswept tail fin. Its identity, colours, outline weight, body proportions, size in frame and flat cartoon style remain exactly the same for the entire video, identical to <Picture 1>. It has exactly one tail and exactly two flippers, and no teeth. The camera is a completely static shot and never moves, zooms or pans. The background stays flat, empty and pure white for the whole video, with no water, no bubbles, no ripples, no shadow, no scenery, no sparkles and no text of any kind. The mascot stays centred with clear empty margin on all four sides and never leaves the frame. It is overjoyed: in the first second it happily lifts both of its side flippers up high above its head in a big cheer, as if saying hooray, and its mouth opens in a wide joyful smile. Then it keeps both flippers raised and gives them two small cheerful waves while its whole body bounces gently once and its single tail fin swishes. The motion is smooth, springy, bouncy and cartoon-like, like a cheerful hand-drawn animation.

overall_soundscape: Silence.

non_diegetic_music: N/A"""


def first_frame():
    """The master pose, trimmed, on a white square with room above for the flippers."""
    im = Image.open(CHAR / "chibi_neutral.png").convert("RGBA")
    im = im.crop(im.getbbox())
    side = 672
    s = (side * .56) / max(im.size)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    canvas = Image.new("RGBA", (side, side), (255, 255, 255, 255))
    canvas.alpha_composite(im, ((side - im.width) // 2, int(side * .60 - im.height / 2)))
    COMFY_INPUT.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(COMFY_INPUT / IN_NAME)
    OUT.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(OUT / "first_frame.png")


def graph(seed):
    g = json.load(open(CHAR / "swim_src" / "comfyui_prompt.json", encoding="utf-8"))
    for k in ("4098", "4099", "4100", "4101", "3987"):   # alpha cut is done by our own script
        g.pop(k, None)
    g["4011"]["inputs"]["value"] = PROMPT
    g["3998"]["inputs"]["value"] = SECONDS
    g["3991"]["inputs"]["noise_seed"] = seed
    g["3967"]["inputs"]["filename_prefix"] = "FUJIE-ARMS"
    g["3993"]["inputs"]["media_state"] = json.dumps([{
        "kind": "picture", "file": "minimax_h3/%s [input]" % IN_NAME, "name": IN_NAME,
        "duration": None, "width": 672, "height": 672, "has_audio": False,
        "audio_mode": "off", "uid": "fujiearms%d" % seed}])
    return g


def run(g):
    body = json.dumps({"prompt": g, "client_id": uuid.uuid4().hex}).encode()
    try:
        pid = json.load(urllib.request.urlopen(urllib.request.Request(
            COMFY + "/prompt", body, {"Content-Type": "application/json"})))["prompt_id"]
    except urllib.error.HTTPError as e:
        sys.exit(e.read().decode("utf-8", "replace")[:3000])
    while True:
        h = json.load(urllib.request.urlopen(f"{COMFY}/history/{pid}"))
        if pid in h:
            st = h[pid].get("status", {})
            if st.get("status_str") == "error":
                sys.exit(json.dumps(st)[:3000])
            vids = [v for o in h[pid]["outputs"].values() for v in o.get("gifs", []) + o.get("videos", [])]
            if vids or st.get("completed"):
                return vids
        time.sleep(5)


def main(takes, first=1):
    first_frame()
    urllib.request.urlopen(urllib.request.Request(COMFY + "/free", json.dumps(
        {"unload_models": True, "free_memory": True}).encode(), {"Content-Type": "application/json"}))
    for n in range(first - 1, first - 1 + takes):
        seed = 2027 + n * 101
        vids = run(graph(seed))
        v = [x for x in vids if x["filename"].lower().endswith(".mp4")][0]
        dst = OUT / ("arms_%d.mp4" % (n + 1))
        if dst.exists():
            (OUT / "old").mkdir(exist_ok=True)
            shutil.move(dst, OUT / "old" / ("%s_%s.mp4" % (dst.stem, datetime.now().strftime("%Y%m%d_%H%M%S"))))
        q = urllib.parse.urlencode({"filename": v["filename"], "subfolder": v.get("subfolder", ""), "type": v.get("type", "output")})
        with urllib.request.urlopen(f"{COMFY}/view?{q}") as r, open(dst, "wb") as f:
            f.write(r.read())
        print("wrote", dst.relative_to(ROOT), flush=True)


if __name__ == "__main__":
    # python tools/run_fujie_arms_up.py [takes] [first take number]
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 3, int(sys.argv[2]) if len(sys.argv) > 2 else 1)
