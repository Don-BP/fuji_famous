"""Lay the six Hitachiota covers out as one sheet for the hub.

Three carry the official Fujie, three carry Chibi; three carry Mount Fuji.
Output: Fujie_Creative/20_new_ideas/cover_set_sheet.png
"""
import pathlib
from PIL import Image

OUT = pathlib.Path("D:/Fuji_Famous/Fujie_Creative/20_new_ideas")

SET = [
    "whole_fuji_official_2",  # Mount Fuji, the official fish, seigaiha
    "whole_official_1",       # seigaiha waves, the official fish
    "whole_official_3",       # ripples and reeds, the official fish
    "whole_fuji_chibi_1",     # Mount Fuji and Chibi in the waves
    "whole_chibi_1",          # river blue and reeds, Chibi
    "whole_chibi_3",          # the lotus pond, Chibi
]

W, H, BG = 1200, 896, (243, 242, 237)
T, GAP = 380, 20

if __name__ == "__main__":
    sheet = Image.new("RGB", (W, H), BG)
    cols, rows = 3, 2
    x0 = (W - (cols * T + (cols - 1) * GAP)) // 2
    y0 = (H - (rows * T + (rows - 1) * GAP)) // 2
    for i, name in enumerate(SET):
        im = Image.open(OUT / (name + ".png")).convert("RGB")
        sheet.paste(im.resize((T, T), Image.LANCZOS),
                    (x0 + (i % cols) * (T + GAP), y0 + (i // cols) * (T + GAP)))
    sheet.save(OUT / "cover_set_sheet.png")
    print("sheet ok")
