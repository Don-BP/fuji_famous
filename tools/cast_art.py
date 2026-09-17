"""Turn a piece of Fujie artwork into something a foundry could actually cast.

A Japanese colour manhole cover is raised iron outlines with flat opaque
resin poured into the cells between them. So the artwork has to lose its
gloss, its gradients and any soft edge: every part becomes one flat colour,
every colour is walled by a raised iron line, and nothing is see-through.
The flat colours are taken FROM the original artwork, so nothing is invented.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

IRON = (46, 48, 52)


def _near_white(rgb, thr=232):
    return (rgb.min(axis=2) > thr)


def solid_cutout(path):
    """Opaque silhouette + RGB. Background is only what the border can reach,
    so white bellies and white highlights stay part of the character."""
    im = Image.open(path)
    if im.mode == "RGBA":
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.getchannel("A"))
        rgb = bg
    else:
        rgb = im.convert("RGB")
    a = np.asarray(rgb).astype(int)
    nw = np.ascontiguousarray((_near_white(a).astype(np.uint8)) * 255)
    flood = Image.fromarray(nw).copy()   # fromarray shares a read-only buffer
    w, h = flood.size
    seeds = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1),
             (w // 2, 0), (w // 2, h - 1), (0, h // 2), (w - 1, h // 2)]
    for s in seeds:
        if flood.getpixel(s) == 255:
            ImageDraw.floodfill(flood, s, 128, thresh=0)
    outside = np.array(flood) == 128
    mask = (~outside).astype(np.uint8) * 255
    mask = Image.fromarray(mask).filter(ImageFilter.MedianFilter(5))
    bb = mask.point(lambda p: 255 if p > 127 else 0).getbbox()
    return rgb.crop(bb), mask.crop(bb)


def cast(path, colours=4, line=3.0, bevel=True, scale=1, simplify=9):
    """Flatten the artwork to `colours` flat cells and wall each one in iron."""
    rgb, mask = solid_cutout(path)
    if scale != 1:
        sz = (int(rgb.width * scale), int(rgb.height * scale))
        rgb = rgb.resize(sz, Image.LANCZOS)
        mask = mask.resize(sz, Image.LANCZOS)
    m = np.asarray(mask) > 127

    # flat cells, using colours sampled from the artwork itself
    pre = rgb.filter(ImageFilter.MedianFilter(simplify | 1))
    q = pre.quantize(colors=colours, method=Image.MEDIANCUT)
    lab = np.asarray(q).astype(np.int16)
    pal = np.asarray(q.getpalette()[: colours * 3]).reshape(-1, 3)
    lab = np.asarray(Image.fromarray(lab.astype(np.uint8))
                     .filter(ImageFilter.MedianFilter((simplify + 2) | 1))
                     .filter(ImageFilter.MedianFilter((simplify + 2) | 1)))
    flat = pal[np.clip(lab, 0, colours - 1)].astype(np.uint8)

    # raised iron walls between cells and around the outside
    edge = np.zeros(lab.shape, bool)
    edge[:, 1:] |= lab[:, 1:] != lab[:, :-1]
    edge[1:, :] |= lab[1:, :] != lab[:-1, :]
    edge &= m
    inner = Image.fromarray((edge * 255).astype(np.uint8))
    inner = inner.filter(ImageFilter.MaxFilter(int(max(1, line)) | 1))

    solid = Image.fromarray((m * 255).astype(np.uint8))
    shrunk = solid.filter(ImageFilter.MinFilter(int(max(3, line * 2)) | 1))
    contour = ImageChops.subtract(solid, shrunk)

    out = Image.fromarray(flat).convert("RGBA")
    ink = Image.new("RGBA", out.size, IRON + (0,))
    ink.putalpha(ImageChops.lighter(inner, contour).filter(ImageFilter.GaussianBlur(0.6)))
    out.alpha_composite(ink)

    if bevel:
        hgt = solid.filter(ImageFilter.GaussianBlur(max(1.5, line)))
        hn = np.asarray(hgt).astype(np.float32) / 255.0
        gy, gx = np.gradient(hn)
        lit = np.clip((-gx - gy) * 2.6, -1, 1)
        o = np.asarray(out).astype(np.float32)
        o[..., :3] = np.clip(o[..., :3] + lit[..., None] * 42.0, 0, 255)
        out = Image.fromarray(o.astype(np.uint8))

    a = np.asarray(out).astype(np.uint8).copy()
    a[..., 3] = (m * 255).astype(np.uint8)          # hard edge: nothing see-through
    return Image.fromarray(a, "RGBA")
