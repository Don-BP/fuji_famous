"""The swimming Chibi Fujie who floats around the hub, as a moving loop.

Until now the floating buddy was one still drawing (chibi_neutral.png) that the
page slid around. This makes him actually swim: the tail sweeps, the flippers
paddle, the body bobs and he blinks once, on a loop of about two seconds.

How the frames were made
------------------------
Not by Gemini. Video comes from the local ComfyUI, using Aitrepreneur's MiniMax
H3 Ultra Turbo V3 workflow (GGUF 12GB), Fast Image to Video section, at the
picture's own resolution:

    D:\\ComfyUI-Easy-Install\\ComfyUI\\user\\default\\workflows\\H3\\
        MINIMAX_H3_ULTRA_TURBO_WORKFLOW-V3 - GGUF 12GB.json

The exact prompt graph that was submitted is kept beside the frames, in
Fujie_Creative/01_character/swim_src/comfyui_prompt.json, together with the
first frame that was fed in and the raw render.

The first frame is the approved master, chibi_neutral.png, trimmed to the
character and dropped onto a square white canvas with a wide margin so he has
room to move without touching an edge. The prompt tells the model, in H3's
image-to-video wording, to keep his identity, colours, outline weight, pose and
size exactly as they are, hold the camera still, keep the background flat white
and empty, and move only the tail, the flippers and a gentle bob.

Two rules from the picture skill still apply and are why the prompt reads the
way it does: no text of any kind, and nothing invented in the scene.

What this script does
---------------------
Takes the raw white-background render and turns it into the file the page uses:

  1. Cuts the white away frame by frame with the same flood-fill as
     tools/cutout.py, so his own pale belly survives and the edge stays soft.
     Then it clears the gaps the flood cannot reach: when he lifts a flipper
     away from his tail, the daylight between them is walled off by his own
     outline, and the fill never gets in. Those are told apart from his belly
     by what surrounds them - a real gap is ringed by the black outline on
     nearly every side, a highlight on his belly is not.
  2. Crops every frame to one shared box, so the cut-out does not wobble.
  3. Ends the loop at the frame that best matches the first one, so it repeats
     without a visible jump.
  4. Writes an animated WebP for the site (real soft transparency) and an
     animated GIF beside it for anywhere that needs one.

Output:
  Fujie_Creative/01_character/chibi_neutral_swim.webp   <- used by the hub
  Fujie_Creative/01_character/chibi_neutral_swim.gif

Run it with:  python tools/run_buddy_swim.py
"""
import pathlib
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = pathlib.Path(r"D:\Fuji_Famous")
CHAR = ROOT / "Fujie_Creative" / "01_character"
SRC = CHAR / "swim_src" / "chibi_swim_raw.mp4"

SENTINEL = (255, 0, 255)
FLOOD_THRESH = 32          # how far from white still counts as background
FEATHER = 1.0              # soft edge, in pixels, before the resize

# walled-off daylight: near-white, big enough to see, and ringed by his outline
GAP_WHITE = 244            # every channel at least this bright
GAP_MIN_AREA = 500         # smaller than this is a speck, not a gap
GAP_RING_DARK = 0.35       # how much of what surrounds it must be black outline
DARK = 120                 # a channel this low is outline, not shading
MARGIN = 0.03              # breathing room kept around the shared crop box
WIDE = 320                 # finished width; he is never drawn wider than 172
FPS = 24                   # what the render came out at
KEEP_EVERY = 2             # drops it to 12 a second, which halves the file


def frames_from(video):
    """Decode the render to a list of RGB frames."""
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="buddyswim_"))
    subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(video), "-start_number", "0",
         str(tmp / "f%04d.png")],
        check=True,
    )
    out = [Image.open(p).convert("RGB") for p in sorted(tmp.glob("*.png"))]
    if not out:
        sys.exit("no frames came out of %s" % video.name)
    return out


def background_mask(im):
    """True where the flat white studio background is, flooding in from the border."""
    w, h = im.size
    work = im.copy()
    seeds = []
    for x in range(0, w, max(1, w // 24)):
        seeds += [(x, 0), (x, h - 1)]
    for y in range(0, h, max(1, h // 24)):
        seeds += [(0, y), (w - 1, y)]
    for s in seeds:
        if work.getpixel(s) != SENTINEL:
            ImageDraw.floodfill(work, s, SENTINEL, thresh=FLOOD_THRESH)
    return np.all(np.array(work) == np.array(SENTINEL), axis=-1)


def walled_off_gaps(im, bg):
    """White the flood could not reach because his own outline shuts it in.

    Everything near-white that the border fill missed is a candidate. The ones
    that are really background - the daylight between a raised flipper and the
    tail - are surrounded by the black outline on nearly every side. The pale
    shine on his belly is surrounded by his own grey, so it stays.
    """
    rgb = np.asarray(im).astype(int)
    candidate = (rgb.min(axis=2) >= GAP_WHITE) & ~bg
    if not candidate.any():
        return np.zeros_like(bg)

    flat = Image.fromarray((candidate * 255).astype(np.uint8))
    # anything that survives being eaten in from all sides is worth looking at;
    # this skips the hundreds of one-pixel specks along the outline
    seeds = np.asarray(flat.filter(ImageFilter.MinFilter(5))) > 127

    found = np.zeros_like(bg)
    taken = np.zeros_like(bg)
    for y, x in np.argwhere(seeds):
        if taken[y, x]:
            continue
        probe = flat.copy()
        ImageDraw.floodfill(probe, (int(x), int(y)), 1)
        blob = candidate & (np.asarray(probe) == 1)
        taken |= blob
        if blob.sum() < GAP_MIN_AREA:
            continue
        grown = np.asarray(
            Image.fromarray((blob * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))
        ) > 127
        ring = grown & ~blob
        if ring.any() and (rgb[ring].min(axis=1) < DARK).mean() >= GAP_RING_DARK:
            found |= blob
    return found


def loop_length(frames, earliest=None):
    """The frame after which the clip is closest to where it started."""
    earliest = earliest or len(frames) // 2
    first = np.asarray(frames[0].convert("L"), dtype=np.float32)
    best, score = len(frames), None
    for i in range(earliest, len(frames)):
        d = np.abs(np.asarray(frames[i].convert("L"), dtype=np.float32) - first).mean()
        if score is None or d < score:
            best, score = i, d
    # the loop runs up to, but not including, the frame that matches the first
    return best, score


def main():
    if not SRC.exists():
        sys.exit("missing render: %s" % SRC)

    raw = frames_from(SRC)
    print("%d frames at %dx%d" % (len(raw), raw[0].width, raw[0].height))

    cut, boxes, gapped = [], [], 0
    for im in raw:
        bg = background_mask(im)
        if bg.mean() < 0.02:
            sys.exit("only %.1f%% of a frame reads as background - "
                     "the character needs more margin" % (bg.mean() * 100))
        gaps = walled_off_gaps(im, bg)
        if gaps.any():
            gapped += 1
            bg = bg | gaps
        alpha = Image.fromarray(np.where(bg, 0, 255).astype(np.uint8))
        if FEATHER:
            alpha = alpha.filter(ImageFilter.GaussianBlur(FEATHER))
        rgba = im.convert("RGBA")
        rgba.putalpha(alpha)
        cut.append(rgba)
        ys, xs = (~bg).nonzero()
        boxes.append((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))

    b = np.array(boxes)
    x0, y0, x1, y1 = b[:, 0].min(), b[:, 1].min(), b[:, 2].max(), b[:, 3].max()
    pad = int(round(max(x1 - x0, y1 - y0) * MARGIN))
    W, H = raw[0].size
    box = (max(0, x0 - pad), max(0, y0 - pad), min(W, x1 + pad), min(H, y1 + pad))
    print("%d of %d frames had walled-off white cleared" % (gapped, len(raw)))
    print("shared crop %dx%d (he drifts %d px across the clip)"
          % (box[2] - box[0], box[3] - box[1], np.ptp(b[:, 0]) + np.ptp(b[:, 1])))

    end, score = loop_length(cut)
    print("loop of %d frames (%.2f s); the seam differs by %.1f of 255" %
          (end, end / FPS, score))

    keep = []
    for im in cut[:end:KEEP_EVERY]:
        im = im.crop(box)
        scale = WIDE / im.width
        keep.append(im.resize((WIDE, round(im.height * scale)), Image.LANCZOS))

    delay = round(1000 * KEEP_EVERY / FPS)
    webp = CHAR / "chibi_neutral_swim.webp"
    keep[0].save(webp, "WEBP", save_all=True, append_images=keep[1:],
                 duration=delay, loop=0, quality=80, method=4, lossless=False)
    print("  %s  %.0f KB" % (webp.name, webp.stat().st_size / 1024))

    gif = CHAR / "chibi_neutral_swim.gif"
    # GIF transparency is all or nothing, so anything half-transparent is thrown
    # to one side or the other before the palette is built.
    flat = []
    for im in keep:
        a = im.getchannel("A").point(lambda v: 255 if v > 128 else 0)
        f = im.copy()
        f.putalpha(a)
        flat.append(f.convert("RGBA"))
    flat[0].save(gif, "GIF", save_all=True, append_images=flat[1:],
                 duration=delay, loop=0, disposal=2, transparency=0)
    print("  %s  %.0f KB" % (gif.name, gif.stat().st_size / 1024))


if __name__ == "__main__":
    main()
