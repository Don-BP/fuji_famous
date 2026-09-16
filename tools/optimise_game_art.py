"""Shrink site/art for the web: backgrounds become JPEG, sprites stay transparent PNG."""
import pathlib
from PIL import Image

ART = pathlib.Path("D:/Fuji_Famous/site/art")
total_before = total_after = 0

for p in sorted(ART.glob("*.png")):
    before = p.stat().st_size
    im = Image.open(p)
    if p.name.startswith("bg_"):
        out = p.with_suffix(".jpg")
        im.convert("RGB").save(out, "JPEG", quality=82, optimize=True, progressive=True)
        p.unlink()
        after = out.stat().st_size
        name = out.name
    else:
        # sprites: hold alpha, but drop to 8-bit+alpha where it is safe
        q = im.convert("RGBA").quantize(colors=200, method=Image.FASTOCTREE)
        q.save(p, "PNG", optimize=True)
        after = p.stat().st_size
        if after > before:            # quantising made it worse - put the original back
            im.save(p, "PNG", optimize=True)
            after = p.stat().st_size
        name = p.name
    total_before += before
    total_after += after
    print(f"  {name:<20} {before/1024:7.0f}K -> {after/1024:7.0f}K")

print(f"TOTAL {total_before/1024:.0f}K -> {total_after/1024:.0f}K")
