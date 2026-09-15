import json, io

p = r"D:\Fuji_Famous\tools\entry_fields.json"
d = json.load(io.open(p, encoding="utf-8"))
d["src"] = "D:/Fuji_Famous/Documents_for_dev/03_エントリーシート.doc"
d["dest"] = "D:/Fuji_Famous/Fujie_Creative/05_submission/エントリーシート_記入済.docx"
io.open(p, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=1))

d2 = json.load(io.open(p, encoding="utf-8"))
import os
print("src :", d2["src"], "| exists:", os.path.exists(d2["src"]))
print("dest:", d2["dest"])
