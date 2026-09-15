import os, sys, json, base64, mimetypes, urllib.request, pathlib, re, shutil, datetime

ROOT = pathlib.Path(r"D:\Fuji_Famous")
KEY = None
for line in (ROOT/"SECRET"/"Gemini.txt").read_text(encoding="utf-8").splitlines():
    if "GEMINI_API_KEY" in line:
        KEY = line.split("=",1)[1].strip().strip('"').strip("'")
KEY = KEY or os.environ.get("GEMINI_API_KEY")
MODEL = os.environ.get("GEN_MODEL", "gemini-3.1-flash-image")
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

def archive(path):
    """Never overwrite. Move an existing file into ./old/ with a timestamp suffix."""
    p = pathlib.Path(path)
    if not p.exists():
        return None
    old = p.parent / "old"
    old.mkdir(parents=True, exist_ok=True)
    stamp = datetime.datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y%m%d-%H%M%S")
    dest = old / f"{p.stem}__{stamp}{p.suffix}"
    n = 2
    while dest.exists():
        dest = old / f"{p.stem}__{stamp}-{n}{p.suffix}"
        n += 1
    shutil.move(str(p), str(dest))
    print(f"  archived -> {dest}", flush=True)
    return dest


def gen(prompt, out_path, refs=None, aspect=None, tries=3):
    parts = [{"text": prompt}]
    for r in (refs or []):
        p = pathlib.Path(r)
        mt = mimetypes.guess_type(str(p))[0] or "image/png"
        parts.insert(0, {"inline_data": {"mime_type": mt,
                        "data": base64.b64encode(p.read_bytes()).decode()}})
    body = {"contents": [{"parts": parts}]}
    if aspect:
        body["generationConfig"] = {"imageConfig": {"aspectRatio": aspect}}
    data = json.dumps(body).encode()
    last = ""
    for attempt in range(tries):
        try:
            req = urllib.request.Request(URL, data=data, headers={
                "x-goog-api-key": KEY, "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=240) as resp:
                j = json.load(resp)
            saved = []
            for c in j.get("candidates", []):
                for i, part in enumerate(c.get("content", {}).get("parts", [])):
                    blob = part.get("inlineData") or part.get("inline_data")
                    if blob:
                        op = pathlib.Path(out_path)
                        if saved:
                            op = op.with_name(f"{op.stem}_{len(saved)+1}{op.suffix}")
                        op.parent.mkdir(parents=True, exist_ok=True)
                        archive(op)
                        op.write_bytes(base64.b64decode(blob["data"]))
                        saved.append(str(op))
            if saved:
                return saved
            last = json.dumps(j)[:400]
        except Exception as e:
            last = f"{type(e).__name__}: {e}"
            try: last += " | " + e.read().decode()[:400]
            except Exception: pass
    return {"error": last}

if __name__ == "__main__":
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    for job in spec:
        r = gen(job["prompt"], job["out"], job.get("refs"), job.get("aspect"))
        print(json.dumps({"out": job["out"], "result": r}, ensure_ascii=False))
