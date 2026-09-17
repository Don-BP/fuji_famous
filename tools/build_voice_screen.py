"""Fill in the phone post in the "give Fujie a voice" picture.

run_ideas_voice.py deliberately leaves the post's caption strip empty and the
account's avatar circle blank, because the model cannot draw Fujie at that size
and invents nonsense Japanese for captions. The real artwork and the real line
from the case copy go on here instead.

The caption is the one in the case text: 今日もごはん。1万匹分 - the feed going in,
in Chibi Fujie's voice, for ten thousand of them.

Input:  20_new_ideas/voice_a.png  +  01_character/master_v3_wave.png
Output: 20_new_ideas/voice_plate.png

Writes to voice_plate.png, never to voice_final.png, so that re-running this can
never overwrite a picture that has been finished by hand afterwards.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from PIL import Image, ImageDraw, ImageFont
from build_sday_screen import keyed

ROOT = pathlib.Path("D:/Fuji_Famous/Fujie_Creative")
CHIBI = ROOT / "01_character" / "master_v3_wave.png"
CAPTION = "今日もごはん。1万匹分"

# Each take frames the phone differently, so the empty strip and the empty avatar
# disc sit in a different place on each one. Measured off the plates.
PLATES = {
    "voice_a": {"strip": (948, 332, 1095, 363), "circle": (947, 336, 975, 360)},
    "voice_b": {"strip": (234, 555, 377, 588), "circle": (235, 560, 262, 585)},
    "voice_d": {"strip": (246, 746, 351, 771), "circle": (247, 751, 265, 768)},
}
GAP = 6                         # breathing room between the avatar and the words
INK = (255, 255, 255)
FONT = "C:/Windows/Fonts/YuGothB.ttc"
SS = 8                          # supersampling, for clean type at this size


def avatar(plate, fish, CIRCLE):
    """Chibi Fujie in the account's profile circle, masked to a disc."""
    l, t, r, b = CIRCLE
    d = min(r - l, b - t)
    cx, cy = (l + r) // 2, (t + b) // 2
    big = d * SS

    # fit the whole silhouette inside the disc rather than cropping it to fill.
    # Filling clipped the long flat snout, which is the one feature that says
    # sturgeon rather than dolphin - the thing this picture cannot afford to lose.
    inner = int(big * 0.84)
    scale = inner / max(fish.width, fish.height)
    im = fish.resize((max(1, int(fish.width * scale)), max(1, int(fish.height * scale))),
                     Image.LANCZOS)

    disc = Image.new("RGBA", (big, big), (247, 246, 242, 255))
    disc.alpha_composite(im, ((big - im.width) // 2, (big - im.height) // 2))
    mask = Image.new("L", (big, big), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, big - 1, big - 1), fill=255)
    disc.putalpha(mask)

    plate.alpha_composite(disc.resize((d, d), Image.LANCZOS), (cx - d // 2, cy - d // 2))
    print(f"  avatar {d}px at {cx},{cy}", flush=True)


def caption(plate, STRIP, CIRCLE):
    """The line from the case copy, set in the empty strip."""
    l, t, r, b = STRIP
    l = CIRCLE[2] + GAP
    w, h = r - l, b - t

    layer = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    size = int(h * SS * 0.54)
    font = ImageFont.truetype(FONT, size)
    while font.getbbox(CAPTION)[2] > w * SS * 0.94 and size > 8:
        size -= 2
        font = ImageFont.truetype(FONT, size)
    bx = font.getbbox(CAPTION)
    ImageDraw.Draw(layer).text(
        (0 - bx[0], (h * SS - (bx[3] - bx[1])) // 2 - bx[1]), CAPTION, font=font, fill=INK + (255,))

    plate.alpha_composite(layer.resize((w, h), Image.LANCZOS), (l, t))
    print(f"  caption at {size // SS}px", flush=True)


if __name__ == "__main__":
    fish = keyed(CHIBI)
    for name in (sys.argv[1:] or list(PLATES)):
        print(name, flush=True)
        STRIP, CIRCLE = PLATES[name]["strip"], PLATES[name]["circle"]
        plate = Image.open(ROOT / "20_new_ideas" / (name + ".png")).convert("RGBA")
        avatar(plate, fish, CIRCLE)
        caption(plate, STRIP, CIRCLE)
        out = ROOT / "20_new_ideas" / (name.replace("voice_", "voice_plate_") + ".png")
        plate.convert("RGB").save(out)
        print("  WROTE", out, flush=True)
