"""Build one self-contained HTML file of the game for offline handover.

Everything the game needs is inlined - art, the stylesheet, both scripts, the
favicon, and subsetted copies of the two Google fonts - so the file plays from a
USB stick with no network and no sibling files.

game.js builds some art paths at run time ("art/" + name + ".png"), so rather
than rewriting the game source this installs a small shim that maps any known
asset path through the inlined table at the moment it is used. That keeps
working when the game code changes.
"""
import base64, io, json, pathlib, re, urllib.request

from PIL import Image

ROOT  = pathlib.Path(__file__).resolve().parent.parent
SRC   = ROOT / "site"
OUT   = ROOT / "Fujie_Creative" / "05_submission" / "フジィを育てよう.html"
CACHE = ROOT / "tools" / "_fontcache"

MAXPX = 620          # the stage art ships bigger than it is ever drawn

GH = "https://raw.githubusercontent.com/google/fonts/main/"
FONTS = [
    ("Dela Gothic One", 400, "ofl/delagothicone/DelaGothicOne-Regular.ttf"),
    ("Zen Maru Gothic", 400, "ofl/zenmarugothic/ZenMaruGothic-Regular.ttf"),
    ("Zen Maru Gothic", 700, "ofl/zenmarugothic/ZenMaruGothic-Bold.ttf"),
]

ROOT_ART = ["stage_1_egg.png", "stage_2_larva.png", "stage_3_fry.png",
            "stage_4_young.png", "fujie-official.png"]


def uri(raw, mime):
    return "data:%s;base64,%s" % (mime, base64.b64encode(raw).decode())


def shrink(path):
    """Resize and quantise a PNG, keeping whichever version comes out smaller."""
    im = Image.open(path).convert("RGBA")
    if max(im.size) > MAXPX:
        r = MAXPX / max(im.size)
        im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    out = None
    for candidate in (im.quantize(colors=200, method=Image.FASTOCTREE), im):
        buf = io.BytesIO()
        candidate.save(buf, "PNG", optimize=True)
        if out is None or buf.tell() < len(out):
            out = buf.getvalue()
    return out


# ---------------------------------------------------------------- source files
html = (SRC / "index.html").read_text(encoding="utf-8")
css  = (SRC / "app.css").read_text(encoding="utf-8")
i18n = (SRC / "i18n.js").read_text(encoding="utf-8")
game = (SRC / "game.js").read_text(encoding="utf-8")

# ---------------------------------------------------------------- art
assets, missing = {}, []
for p in sorted((SRC / "art").iterdir()):
    if p.suffix.lower() not in (".png", ".jpg", ".jpeg"):
        continue
    mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
    assets["art/" + p.name] = uri(p.read_bytes(), mime)   # already web-optimised
for name in ROOT_ART:
    assets[name] = uri(shrink(SRC / name), "image/png")
print("inlined %d images" % len(assets))

# ---------------------------------------------------------------- fonts
# every character the game can put on screen, plus the usual furniture
CHARS = set(html + css + i18n + game)
CHARS |= set("0123456789%.,:;!?'\"()[]-–—…"
             "、。「」『』・％／＋×〜 ")
CHARS = "".join(sorted(CHARS))


def font_face(family, weight, repo_path):
    CACHE.mkdir(parents=True, exist_ok=True)
    src = CACHE / repo_path.rsplit("/", 1)[1]
    if not src.exists():
        print("  downloading", src.name)
        src.write_bytes(urllib.request.urlopen(GH + repo_path, timeout=180).read())
    from fontTools import subset
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.desubroutinize = True
    opts.drop_tables += ["DSIG"]
    font = subset.load_font(str(src), opts)
    sub = subset.Subsetter(options=opts)
    sub.populate(text=CHARS)
    sub.subset(font)
    buf = io.BytesIO()
    subset.save_font(font, buf, opts)
    raw = buf.getvalue()
    print("  %-18s %d  %6.1f KB" % (family, weight, len(raw) / 1024))
    return ("@font-face{font-family:'%s';font-style:normal;font-weight:%d;"
            "font-display:swap;src:url(%s) format('woff2')}"
            % (family, weight, uri(raw, "font/woff2")))


print("subsetting fonts to %d characters" % len(CHARS))
fontcss = "".join(font_face(*f) for f in FONTS)

# ---------------------------------------------------------------- stylesheet
def swap_url(m):
    key = m.group(1).split("?")[0]
    if key not in assets:
        missing.append(key)
        return m.group(0)
    return 'url("%s")' % assets[key]


css = re.sub(r'url\("([^"]+\.(?:png|jpg|jpeg)[^"]*)"\)', swap_url, css)

# ---------------------------------------------------------------- page
# strip the things a single offline file cannot use
html = re.sub(r'\s*<link rel="preconnect"[^>]*>', "", html)
html = re.sub(r'\s*<link rel="stylesheet" href="https://fonts\.googleapis[^>]*>', "", html)
html = re.sub(r'\s*<link rel="stylesheet" href="app\.css[^"]*">', "", html)
html = re.sub(r'\s*<link rel="apple-touch-icon"[^>]*>', "", html)
html = re.sub(r'<link rel="icon"[^>]*>',
              '<link rel="icon" type="image/png" href="%s">'
              % uri((SRC / "favicon.png").read_bytes(), "image/png"), html)


# img sources become data-a, filled in once the shim is live
def hide_src(m):
    key = m.group(1)
    if key not in assets:
        missing.append(key)
        return m.group(0)
    return 'data-a="%s"' % key


html = re.sub(r'src="((?:art/)?[\w\-]+\.(?:png|jpg|jpeg))"', hide_src, html)

SHIM = r"""
(function(){
  var A = __ASSETS__;
  window.__ART = A;
  var keys = Object.keys(A).sort(function(a,b){ return b.length - a.length; });
  var RE = new RegExp(keys.map(function(k){
    return k.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }).join("|"), "g");
  function fix(v){
    return (typeof v === "string" && v.indexOf(".") >= 0)
      ? v.replace(RE, function(m){ return A[m]; }) : v;
  }
  function owner(obj, prop){
    while (obj){ if (Object.getOwnPropertyDescriptor(obj, prop)) return obj;
                 obj = Object.getPrototypeOf(obj); }
    return null;
  }
  function wrap(proto, prop){
    if (!proto) return;
    var d = Object.getOwnPropertyDescriptor(proto, prop);
    if (!d || !d.set) return;
    Object.defineProperty(proto, prop, { configurable:true, enumerable:d.enumerable,
      get:d.get, set:function(v){ d.set.call(this, fix(v)); } });
  }
  wrap(owner(HTMLImageElement.prototype, "src"), "src");
  wrap(owner(Element.prototype, "innerHTML"), "innerHTML");
  wrap(owner(document.documentElement.style, "backgroundImage"), "backgroundImage");
  var setAttr = Element.prototype.setAttribute;
  Element.prototype.setAttribute = function(n, v){
    return setAttr.call(this, n, (n === "src" || n === "href") ? fix(v) : v);
  };
  var setProp = CSSStyleDeclaration.prototype.setProperty;
  CSSStyleDeclaration.prototype.setProperty = function(n, v, p){
    return setProp.call(this, n, fix(v), p);
  };
  /* Chrome keeps camel-cased style properties on the instance rather than on a
     prototype, so el.style.backgroundImage = "..." cannot be wrapped directly.
     Hand out a proxy of the style object instead, which catches the write
     before the browser goes looking for the file. */
  var styleOwner = owner(document.documentElement, "style");
  var styleDesc = styleOwner && Object.getOwnPropertyDescriptor(styleOwner, "style");
  if (styleDesc && styleDesc.get && typeof Proxy === "function"){
    var seen = new WeakMap();
    Object.defineProperty(styleOwner, "style", {
      configurable:true, enumerable:styleDesc.enumerable, set:styleDesc.set,
      get:function(){
        var real = styleDesc.get.call(this), p = seen.get(real);
        if (!p){
          p = new Proxy(real, {
            get:function(t, k){ var v = t[k]; return typeof v === "function" ? v.bind(t) : v; },
            set:function(t, k, v){ t[k] = fix(v); return true; }
          });
          seen.set(real, p);
        }
        return p;
      }
    });
  }
  /* last resort, and a net for anything added later: if an art path still
     reaches an inline style, swap it as soon as the attribute changes */
  new MutationObserver(function(recs){
    for (var i = 0; i < recs.length; i++){
      var el = recs[i].target, s = el.getAttribute && el.getAttribute("style");
      if (s && s.indexOf("art/") >= 0) setAttr.call(el, "style", fix(s));
    }
  }).observe(document.documentElement,
             { attributes:true, subtree:true, attributeFilter:["style"] });
})();
"""

FILL = r"""
(function(){
  var list = document.querySelectorAll("[data-a]");
  for (var i = 0; i < list.length; i++){
    var v = window.__ART[list[i].getAttribute("data-a")];
    if (v) list[i].setAttribute("src", v);
  }
})();
"""

head = ("<script>" + SHIM.replace("__ASSETS__", json.dumps(assets)) + "</script>\n"
        "<style>" + fontcss + "\n" + css + "</style>\n</head>")
html = html.replace("</head>", head, 1)

# the page version-stamps these (game.js?v=3), so match with or without a query
html = re.sub(r'<script src="i18n\.js[^"]*"></script>',
              lambda m: "<script>" + FILL + "</script>\n<script>" + i18n + "</script>",
              html, count=1)
html = re.sub(r'<script src="game\.js[^"]*"></script>',
              lambda m: "<script>" + game + "</script>", html, count=1)

# ---------------------------------------------------------------- checks
if missing:
    print("  !! not found in site/:", sorted(set(missing)))
for tag in ("app.css", "i18n.js", "game.js", "fonts.googleapis"):
    if re.search(r'(?:href|src)="[^"]*' + re.escape(tag), html):
        print("  !! still linked:", tag)

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(html, encoding="utf-8")
print("\nWROTE %s  (%.2f MB)" % (OUT, OUT.stat().st_size / 1048576))
