"""Put the real Chibi Fujie onto the television bands in the Sturgeon Day picture.

The image model will not draw him correctly at screen size - every attempt came
back as a generic dolphin with no snout, no barbels and no scutes. So the plates
are generated with the lower-third band's left half left empty (see
run_ideas_sturgeonday.py) and the decided artwork from 01_character is composited
in here instead. A television screen is flat and glassy, so a clean paste reads
correctly - unlike a manhole casting, which never did.

Input:  20_new_ideas/sday_a.png  +  01_character/master_v3_wave.png
Output: 20_new_ideas/sday_plate.png

NOT the picture that ships. The owner finished the band by hand on top of this -
adding a photograph of a real sturgeon and the Fujikin mark beside the mascot -
and that hand-finished file is sday_final.png. This script deliberately writes to
sday_plate.png so that re-running it can never overwrite the chosen picture.
"""
import pathlib
from PIL import Image, ImageDraw

ROOT = pathlib.Path("D:/Fuji_Famous/Fujie_Creative")
PLATE = ROOT / "20_new_ideas" / "sday_a.png"
CHIBI = ROOT / "01_character" / "master_v3_wave.png"
OUT = ROOT / "20_new_ideas" / "sday_plate.png"

# Where he goes, measured off the plate. Each entry is the empty cream area of a
# band: (left, top, right, bottom). He is drawn a little taller than the band and
# sits on its baseline, so he breaks above the top edge the way a real broadcast
# mascot does.
SLOTS = [
    (675, 737, 840, 782),   # the big television, bottom right panel
    (247, 282, 351, 302),   # the small television across the room, left panel
]
OVERHANG = 0.42   # how far above the band he rises, as a fraction of band height
INSET = 0.10      # keep him clear of the rounded left end of the band

# The model wrote the day's name into the calendar cell as garbled pseudo-kana, so
# it is painted out and set again in a real Japanese font. The cell is tilted with
# the phone, hence the angle.
DAY = "チョウザメの日"
CELL = (896, 212, 934, 230)     # the garbled text, to be covered
CREAM = (233, 224, 213)         # the cell's own background
ANGLE = 16                      # degrees, text rising to the right
INK = (122, 112, 101)
FONT = "C:/Windows/Fonts/YuGothM.ttc"
SS = 8                          # supersampling, for clean type at this size


def set_calendar_text(plate):
    """Cover the garbled cell label and set the day's name properly.

    The cell is a tilted parallelogram, so a rectangular patch would drag the
    white grid gap in with it. Instead only the warm pixels are repainted: the
    cream cell and the ink on it both run warm (red well above blue), while the
    grid lines around it are neutral.
    """
    from PIL import ImageFont
    l, t, r, b = CELL
    w, h = r - l, b - t
    px = plate.load()
    for y in range(t, b):
        for x in range(l, r):
            pr, pg, pb, pa = px[x, y]
            if pr - pb > 8:                     # inside the cell, or ink on it
                px[x, y] = CREAM + (pa,)

    layer = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    size = int(h * SS * 0.44)
    font = ImageFont.truetype(FONT, size)
    while font.getbbox(DAY)[2] > w * SS * 0.88 and size > 8:
        size -= 2
        font = ImageFont.truetype(FONT, size)
    d = ImageDraw.Draw(layer)
    bx = font.getbbox(DAY)
    d.text(((w * SS - (bx[2] - bx[0])) // 2 - bx[0],
            (h * SS - (bx[3] - bx[1])) // 2 - bx[1]), DAY, font=font, fill=INK + (255,))

    layer = layer.rotate(ANGLE, resample=Image.BICUBIC, expand=False)
    plate.alpha_composite(layer.resize((w, h), Image.LANCZOS), (l, t))
    print(f"  set calendar label at {size // SS}px", flush=True)


def keyed(path):
    """The artwork on a transparent ground, cropped tight.

    The white is flood-filled from the four corners rather than thresholded, so
    the white highlights and sparkles inside the drawing survive.
    """
    im = Image.open(path).convert("RGB")
    w, h = im.size
    flood = im.copy()
    for corner in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)):
        ImageDraw.floodfill(flood, corner, (255, 0, 255), thresh=28)
    rgba = im.convert("RGBA")
    px, fx = rgba.load(), flood.load()
    for y in range(h):
        for x in range(w):
            if fx[x, y] == (255, 0, 255):
                px[x, y] = (255, 255, 255, 0)
    return rgba.crop(rgba.getbbox())


if __name__ == "__main__":
    plate = Image.open(PLATE).convert("RGBA")
    fish = keyed(CHIBI)

    for left, top, right, bottom in SLOTS:
        band = bottom - top
        height = int(round(band * (1 + OVERHANG)))
        width = int(round(fish.width * height / fish.height))
        pad = int(round(band * INSET))
        avail = (right - left) - 2 * pad
        if width > avail:                     # never let him run into the name
            width = avail
            height = int(round(fish.height * width / fish.width))
        stamp = fish.resize((width, height), Image.LANCZOS)
        x = left + pad + (avail - width) // 2
        y = bottom - int(round(band * 0.12)) - height
        plate.alpha_composite(stamp, (x, y))
        print(f"  placed {width}x{height} at {x},{y}", flush=True)

    set_calendar_text(plate)
    plate.convert("RGB").save(OUT)
    print("WROTE", OUT)
