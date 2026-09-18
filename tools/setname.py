import json, io

NAME_FULL = "Vittorio Zumpano（ビットリオ・ズンパーノ）　／　株式会社ブレインパワー　大阪"
NAME_DECK = "株式会社ブレインパワー　大阪　／　Vittorio Zumpano"

# 1) entry sheet fields
p = r"D:\Fuji_Famous\tools\entry_fields.json"
d = json.load(io.open(p, encoding="utf-8"))
d["rep"] = NAME_FULL
io.open(p, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=1))
print("entry_fields.rep =", d["rep"])

# 2) deck
p2 = r"D:\Fuji_Famous\tools\deck.js"
s = io.open(p2, encoding="utf-8").read()
old = "株式会社ブレインパワー　／　〔氏名〕"
n = s.count(old)
s = s.replace(old, NAME_DECK)
io.open(p2, "w", encoding="utf-8").write(s)
print("deck.js: replaced", n, "placeholder(s) ->", NAME_DECK)
