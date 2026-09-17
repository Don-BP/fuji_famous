"""Lay the five Hitachiota covers out as one sheet for the hub.

Three carry the official Fujie, two carry Chibi.
Output: Fujie_Creative/20_new_ideas/cover_set_sheet.png
"""
import pathlib
from PIL import Image

OUT = pathlib.Path("D:/Fuji_Famous/Fujie_Creative/20_new_ideas")

SET = [
    "whole_fuji_both_2",     # the station - Mount Fuji, both Fujies, seigaiha waves
    "whole_fuji_official_1",  # city hall - Mount Fuji and the official fish
    "whole_fuji_chibi_1",     # the farm gate - Mount Fuji and Chibi
    "whole_official_1",       # a main street - seigaiha, the official fish
    "whole_chibi_3",          # a park - Chibi in the lotus pond
]

W, H, BG = 1200, 896, (243, 242, 237)
T, GAP = 356, 22

if __name__ == "__main__":
    sheet = Image.new("RGB", (W, H), BG)
    top_y, bot_y = 40, 40 + T + GAP
    xs = [(W - (3 * T + 2 * GAP)) // 2 + i * (T + GAP) for i in range(3)]
    xs += [(W - (2 * T + GAP)) // 2 + i * (T + GAP) for i in range(2)]
    ys = [top_y] * 3 + [bot_y] * 2
    for name, x, y in zip(SET, xs, ys):
        im = Image.open(OUT / (name + ".png")).convert("RGB")
        sheet.paste(im.resize((T, T), Image.LANCZOS), (x, y))
    sheet.save(OUT / "cover_set_sheet.png")
    print("sheet ok")
