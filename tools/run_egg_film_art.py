"""Artwork for the "From a single egg" film (idea 04 on the hub).

The film reuses the pet game's own characters and backdrops, so it matches the
game and the stickers. This script only makes what the game never needed:

  bg_1987   - storybook dusk in the Satomi valley: a small valve works beside a
              river, the evening the idea was spoken. No people, no mascot, the
              upper-left sky left open for a speech bubble.
  bg_hall   - the farm hall at Satomi, rows of deep round fibreglass tanks, for
              the "more than ten thousand" pull-back. Fish are added in the film.
  prop_valve- one big cartoon valve in the sticker line style, on white, to be
              cut out and turned by the film during the flow-control scene.

Runs on the owner's local ComfyUI with Qwen Image 2.1 in edit mode: each take
is given a game backdrop or game sprite as its style reference, so the paint
handling and palette carry over. Output goes to Fujie_Creative/22_egg_film/.
Nothing is overwritten; an existing file moves to old/ first.
"""
import json, os, shutil, sys, time, urllib.request, uuid, random
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "Fujie_Creative", "22_egg_film")
COMFY = "http://127.0.0.1:8188"
COMFY_INPUT = r"D:\ComfyUI-Easy-Install\ComfyUI\input"

TEXT_RULE = ("Absolutely no words, kanji, kana, letters, numbers, captions, signage, "
             "logos or watermark anywhere in the picture.")
MASCOT_RULE = "Draw no mascot, no cartoon character, no animal character anywhere."
PEOPLE_RULE = "No people at all."
FARM_RULE = ("The farm is an indoor recirculating hall with deep round fibreglass tanks - "
             "never an open-air pond, never a public aquarium.")
NEG = ("text, letters, words, kanji, watermark, logo, signature, people, person, "
       "character, mascot, cartoon animal, blurry, low quality, distorted, photo")

TAKES = {
    "bg_1987": dict(ref="site/art/bg_title_wide.jpg", seed=11987, prompt=(
        "Create a brand-new wide storybook illustration. Use <image1> only for its painting "
        "style: soft painterly brushwork, deep teal and blue palette, gentle glow. "
        "Scene: dusk in a quiet mountain valley in rural Ibaraki, Japan. A small modest "
        "Japanese factory building with a pitched roof, warm yellow light in its windows, "
        "silver pipes and one round wheel valve on its outer wall, sits beside a clear shallow "
        "river that runs toward the viewer. Forested hills, the first stars in a deep blue "
        "sky, a thin crescent moon. Cozy, hopeful, whimsical, like a picture book. "
        "Keep the upper-left third of the sky open and uncluttered. "
        f"{PEOPLE_RULE} {MASCOT_RULE} {TEXT_RULE}")),
    "bg_hall": dict(ref="site/art/bg_tank_early_wide.jpg", seed=12002, prompt=(
        "Create a brand-new wide illustration. Use <image1> only for its painting style, "
        "palette and lighting: painterly, deep teal, soft pools of light. "
        "Scene: a large, calm indoor fish-farm hall seen from a high angle. Many deep round "
        "fibreglass tanks in neat rows fill the floor into the distance, each glowing softly "
        "teal from within, the water dark and still. Silver pipes run along the tank rims, "
        "hanging lamps make warm circles of light, a wide gentle walkway between rows. "
        "Empty water: no fish visible. Peaceful, a little magical. "
        f"{FARM_RULE} {PEOPLE_RULE} {MASCOT_RULE} {TEXT_RULE}")),
    "prop_valve": dict(ref="site/stage_3_fry.png", seed=13998, prompt=(
        "Create a brand-new picture. Use <image1> only for its drawing style: glossy cute "
        "cartoon sticker art, thick dark navy outline, soft cel shading, sparkle highlights. "
        "Subject: one single industrial valve seen from the front: a polished silver valve "
        "body joined to a short silver pipe on the left and right, with a big round blue "
        "handwheel with four spokes on top facing the viewer. Chunky, friendly, toy-like "
        "proportions. Centered, with wide empty margins on every side, on a plain pure white "
        "background. " f"{MASCOT_RULE} {TEXT_RULE}")),
    # The film spins this one, so it must be a perfect face-on circle.
    "prop_wheel": dict(ref="site/stage_3_fry.png", seed=14040, prompt=(
        "Create a brand-new picture. Use <image1> only for its drawing style: glossy cute "
        "cartoon sticker art, thick dark navy outline, soft cel shading, sparkle highlights. "
        "Subject: one single round blue valve handwheel seen perfectly face-on, a flat "
        "perfect circle: a thick blue rim, four straight spokes meeting at a silver round hub "
        "with a bolt in the center, radially symmetric. No valve body, no pipe, nothing else. "
        "Centered, with wide empty margins on every side, on a plain pure white background. "
        f"{MASCOT_RULE} {TEXT_RULE}")),
}


def node(cls, **inputs):
    return {"class_type": cls, "inputs": inputs}


def graph(prompt, ref_name, seed, prefix):
    g = {
        "40": node("UNETLoader", unet_name="qwen_image_2.1_int8_convrot.safetensors", weight_dtype="default"),
        "41": node("CLIPLoader", clip_name="qwen3vl_8b_int8_convrot.safetensors", type="qwen_image", device="default"),
        "42": node("VAELoader", vae_name="qwen_image_2.1_vae_bf16.safetensors"),
        "46": node("LoraLoaderModelOnly", lora_name="qwen-image-2.1-fix-1.0-comfy.safetensors", strength_model=1, model=["40", 0]),
        "47": node("APG", eta=1, norm_threshold=10, momentum=0.3, model=["46", 0]),
        "48": node("FreSca", scale_low=1, scale_high=2, freq_cutoff=8, model=["47", 0]),
        "49": node("KSamplerSelect", sampler_name="seeds_2"),
        "50": node("BasicScheduler", scheduler="sgm_uniform", steps=20, denoise=1, model=["48", 0]),
        "3": node("RandomNoise", noise_seed=seed),
        "20": node("LoadImage", image=ref_name),
        "62": node("TextEncodeQwenImage21", resolution=1024, clip=["41", 0], prompt=prompt,
                   negative_prompt=NEG, vae=["42", 0], **{"images.image_1": ["20", 0]}),
        "115": node("CFGGuider", cfg=3, model=["48", 0], positive=["62", 0], negative=["62", 1]),
        "116": node("SamplerCustomAdvanced", noise=["3", 0], guider=["115", 0], sampler=["49", 0],
                    sigmas=["50", 0], latent_image=["62", 2]),
        "117": node("VAEDecode", samples=["116", 0], vae=["42", 0]),
        "91": node("SaveImage", filename_prefix=prefix, images=["117", 0]),
    }
    return g


def post(g):
    body = json.dumps({"prompt": g, "client_id": uuid.uuid4().hex}).encode()
    req = urllib.request.Request(COMFY + "/prompt", body, {"Content-Type": "application/json"})
    try:
        return json.load(urllib.request.urlopen(req))["prompt_id"]
    except urllib.error.HTTPError as e:
        sys.exit(e.read().decode("utf-8", "replace")[:3000])


def wait(pid):
    while True:
        h = json.load(urllib.request.urlopen(f"{COMFY}/history/{pid}"))
        if pid in h:
            st = h[pid].get("status", {})
            if st.get("status_str") == "error":
                sys.exit(json.dumps(st)[:3000])
            imgs = [i for o in h[pid]["outputs"].values() for i in o.get("images", [])]
            if imgs:
                return imgs
        time.sleep(3)


def keep(path):
    if os.path.exists(path):
        old = os.path.join(os.path.dirname(path), "old")
        os.makedirs(old, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        b, e = os.path.splitext(os.path.basename(path))
        shutil.move(path, os.path.join(old, f"{b}_{stamp}{e}"))


def main(names, variants):
    os.makedirs(OUT, exist_ok=True)
    for name in names:
        t = TAKES[name]
        ref = os.path.join(ROOT, t["ref"])
        ref_name = "eggfilm_" + os.path.basename(ref)
        shutil.copy(ref, os.path.join(COMFY_INPUT, ref_name))
        for v in range(variants):
            seed = t["seed"] + v * 7919
            pid = post(graph(t["prompt"], ref_name, seed, f"egg_film/{name}"))
            img = wait(pid)[0]
            q = urllib.parse.urlencode({"filename": img["filename"], "subfolder": img["subfolder"], "type": img["type"]})
            dst = os.path.join(OUT, f"{name}_{chr(97 + v)}.png")
            keep(dst)
            with urllib.request.urlopen(f"{COMFY}/view?{q}") as r, open(dst, "wb") as f:
                f.write(r.read())
            print("wrote", os.path.relpath(dst, ROOT), flush=True)


if __name__ == "__main__":
    import urllib.parse
    args = sys.argv[1:]
    n = int(args.pop(0)) if args and args[0].isdigit() else 2
    main(args or list(TAKES), n)
