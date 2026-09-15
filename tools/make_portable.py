"""Build a single self-contained HTML file with every image inlined as a data URI."""
import base64, io, pathlib, re

SRC = pathlib.Path(r"D:\Fuji_Famous\Fujie_Creative\04_campaign")
OUT = pathlib.Path(r"D:\Fuji_Famous\Fujie_Creative\05_submission\フジィを育てよう.html")

try:
    from PIL import Image
    HAVE_PIL = True
except ImportError:
    HAVE_PIL = False

IMGS = ["stage_1_egg.png", "stage_2_larva.png", "stage_3_fry.png",
        "stage_4_young.png", "master.png", "fujie-official.png"]

MAXPX = 900


def encode(name):
    p = SRC / name
    raw = p.read_bytes()
    if HAVE_PIL:
        im = Image.open(io.BytesIO(raw)).convert("RGBA")
        if max(im.size) > MAXPX:
            ratio = MAXPX / max(im.size)
            im = im.resize((int(im.width * ratio), int(im.height * ratio)), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "PNG", optimize=True)
        raw = buf.getvalue()
    return "data:image/png;base64," + base64.b64encode(raw).decode()


html = (SRC / "raise-fujie.html").read_text(encoding="utf-8")

for name in IMGS:
    uri = encode(name)
    html = html.replace('src="%s"' % name, 'src="%s"' % uri)
    html = html.replace('"%s"' % name, '"%s"' % uri)
    print("inlined", name, "%.1f KB" % (len(uri) / 1024))

# Wrap as a complete standalone document
doc = (
    '<!DOCTYPE html>\n<html lang="ja">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
    '<style>html,body{margin:0;padding:0}img{max-width:100%}</style>\n'
    + html.split("<div id=\"water\">")[0]
    + "\n</head>\n<body>\n<div id=\"water\">"
    + html.split("<div id=\"water\">", 1)[1]
    + "\n</body>\n</html>\n"
)

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(doc, encoding="utf-8")
print("\nWROTE", OUT, "%.2f MB" % (OUT.stat().st_size / 1048576))
