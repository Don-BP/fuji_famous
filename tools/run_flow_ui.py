"""Art for the reworked flow control: an instrument bezel and a valve handwheel.

The dial's moving parts (ticks, safe-zone arc, needle) are drawn in SVG at run
time so they can animate; these two pieces are the fixed housing around them.
Both are cut out to transparent afterwards.
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen

KIT = "D:/Fuji_Famous/site/art/ui_panel.png"
OUT = "D:/Fuji_Famous/site/art/"

STYLE = (
    "Match this exact game UI art style: brushed chrome and polished steel housing with small "
    "round rivets, a deep midnight-teal interior, a thin bright cyan inner light line, soft "
    "specular highlights, clean flat game-art rendering with crisp edges. Industrial instrument "
    "panel from a precision engineering company. Centred on a pure flat WHITE background with "
    "generous white margin all round. No text, no numbers, no lettering, no logos anywhere.\n\n"
)

ITEMS = [
    ("ui_dial.png", "1:1", STYLE +
     "A round industrial pressure-gauge HOUSING seen perfectly face-on, dead centre, perfectly "
     "circular and perfectly symmetrical. A thick brushed-chrome bezel ring with eight small "
     "rivets spaced evenly around it, a thin bright cyan light line just inside the ring, and "
     "inside that a smooth EMPTY dial face of deep midnight-teal shading slightly darker toward "
     "the bottom, with a faint glass reflection arc across the upper left. The dial face must be "
     "completely EMPTY - absolutely no needle, no pointer, no tick marks, no scale, no numbers, "
     "no markings of any kind. Only the ring and the empty face."),

    ("ui_valvewheel.png", "1:1", STYLE +
     "A valve handwheel seen perfectly face-on, dead centre, perfectly circular and symmetrical. "
     "A polished chrome outer rim with five evenly spaced spokes radiating from a raised hexagonal "
     "hub at the centre, like the handwheel on an industrial gate valve. Bright metal highlights "
     "on the upper edges of the rim and spokes, a thin cyan glow tracing the inside of the rim. "
     "Compact and chunky so it reads clearly at small size. No text or numbers."),
]


def main():
    for name, aspect, prompt in ITEMS:
        r = gen(prompt, OUT + name, refs=[KIT], aspect=aspect)
        print(json.dumps({"art": name, "ok": not isinstance(r, dict)}), flush=True)
    print("FLOW UI DONE", flush=True)


if __name__ == "__main__":
    main()
