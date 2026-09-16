import io, re, pathlib

p = r"D:\Fuji_Famous\tools\deck.js"
s = io.open(p, encoding="utf-8").read()
base = pathlib.Path(r"D:\Fuji_Famous\Fujie_Creative\deck_assets")

refs = sorted(set(re.findall(r'IMG \+ "([^"]+\.png)"', s)))
n = 0
for r in refs:
    jpg_rel = pathlib.Path(r).with_suffix(".jpg").as_posix()
    if (base / jpg_rel).exists():
        new = "deck_assets/" + jpg_rel
    elif (base / r).exists():
        new = "deck_assets/" + r
    else:
        print("  ! no optimised copy for", r)
        continue
    s = s.replace('IMG + "%s"' % r, 'IMG + "%s"' % new)
    n += 1
    print("%-44s -> %s" % (r, new))

# the stage strip builds its path dynamically
old_dyn = 'IMG + "04_campaign/" + st[1]'
if old_dyn in s:
    s = s.replace(old_dyn, 'IMG + "deck_assets/04_campaign/" + st[1]')
    print("dynamic stage-strip path repointed")

io.open(p, "w", encoding="utf-8").write(s)
print("\npatched", n, "static refs")
