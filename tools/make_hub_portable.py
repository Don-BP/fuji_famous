"""Build one self-contained HTML file of the WHOLE studio for offline handover.

tools/make_portable.py makes the game on its own. This makes everything: the hub,
the 40-year timeline and the game, in a single file that opens from a USB stick
with no network and no sibling files. The judges get the same thing the live site
gives them, as a backup for the link.

Everything is inlined - every picture, the hero film, the stylesheets, the
scripts, the fonts. Pictures are re-encoded smaller than the live site's, because
a single file has to stay small enough to send.

The hub builds some picture paths at run time ("assets/t/" + id + ".jpg"), so
rather than rewriting the site source this installs the same shim the game copy
uses: any known path is swapped for its inlined copy at the moment it is used.
That keeps working when the site code changes.

"Play the game" and "read the timeline" are separate pages on the real site. Here
they are carried inside the file and open over the hub in a panel, with a close
button back to where you were.

Run tools/build_site.py first - this reads dist/, not the sources.

Output:
  Fujie_Creative/05_submission/フジィスタジオ_オフライン版.html
"""
import base64
import io
import json
import pathlib
import re
import sys
import urllib.request

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
GAME = ROOT / "Fujie_Creative" / "05_submission" / "フジィを育てよう.html"
OUT = ROOT / "Fujie_Creative" / "05_submission" / "フジィスタジオ_オフライン版.html"
CACHE = ROOT / "tools" / "_fontcache"

# how far the pictures come down for the offline copy
LARGE, LARGE_Q = 900, 74      # what the lightbox opens
THUMB, THUMB_Q = 440, 72      # the contact-sheet tiles
ART, ART_Q = 900, 80          # the page's own art, transparency kept

# the film ships in four cuts for four screen shapes; offline keeps the two that
# a laptop or a phone will actually ask for, and hero.js is pointed at them
FILM_WIDE, FILM_TALL = "w720", "m480"

GH = "https://raw.githubusercontent.com/google/fonts/main/"
FONTS = [
    ("Dela Gothic One", 400, "ofl/delagothicone/DelaGothicOne-Regular.ttf"),
    ("Zen Maru Gothic", 400, "ofl/zenmarugothic/ZenMaruGothic-Regular.ttf"),
    ("Zen Maru Gothic", 500, "ofl/zenmarugothic/ZenMaruGothic-Medium.ttf"),
    ("Zen Maru Gothic", 700, "ofl/zenmarugothic/ZenMaruGothic-Bold.ttf"),
    ("Shippori Mincho", 400, "ofl/shipporimincho/ShipporiMincho-Regular.ttf"),
    ("Shippori Mincho", 600, "ofl/shipporimincho/ShipporiMincho-SemiBold.ttf"),
]


def uri(raw, mime):
    return "data:%s;base64,%s" % (mime, base64.b64encode(raw).decode())


def as_js(value):
    """JSON for dropping inside a <script>.

    The panel carries whole HTML pages, and an unescaped </script> inside one of
    them would close the block it is sitting in and take the rest of the file
    with it.
    """
    return json.dumps(value).replace("</", "<\\/")


def sub_literal(pattern, replacement, text):
    """re.sub, but the replacement goes in exactly as written.

    A plain replacement string is scanned for backslash escapes, which quietly
    halves the backslashes in the scripts and stylesheets being inlined and
    leaves behind regular expressions that no longer parse.
    """
    return re.sub(pattern, lambda m: replacement, text, count=1)


def webp(path, cap, quality):
    """Re-encode a picture small, keeping transparency where there is any."""
    im = Image.open(path)
    alpha = im.mode in ("RGBA", "LA", "P") and "transparency" in im.info or im.mode in ("RGBA", "LA")
    im = im.convert("RGBA" if alpha else "RGB")
    if max(im.size) > cap:
        r = cap / max(im.size)
        im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=quality, method=4)
    return buf.getvalue()


# ---------------------------------------------------------------- the pages
def read(*parts):
    p = DIST.joinpath(*parts)
    if not p.exists():
        sys.exit("missing %s - run tools/build_site.py first" % p)
    return p.read_text(encoding="utf-8")


hub_html = read("index.html")
hub_css = read("hub.css")
hub_js = {n: read(n) for n in ("data.js", "hub.js", "hero.js", "buddy.js", "cases.js")}

tl_html = read("timeline", "index.html")
tl_css = read("timeline", "timeline.css")
tl_js = read("timeline", "timeline.js")
# the timeline sits one folder down on the real site; flatten its paths so they
# match the hub's, and one table of pictures serves both
tl_html = tl_html.replace("../assets/", "assets/")
tl_css = tl_css.replace("../assets/", "assets/")
tl_js = tl_js.replace("../assets/", "assets/")

if not GAME.exists():
    sys.exit("missing %s - run tools/make_portable.py first" % GAME)
game_html = GAME.read_text(encoding="utf-8")

# ---------------------------------------------------------------- pictures
assets = {}
A = DIST / "assets"
kept = dropped = 0
for p in sorted(A.iterdir()):
    if p.is_dir() or p.suffix.lower() not in (".png", ".jpg", ".jpeg", ".webp"):
        continue
    key = "assets/" + p.name
    if p.suffix.lower() == ".webp":
        assets[key] = uri(p.read_bytes(), "image/webp")   # already small, may be animated
    elif p.suffix.lower() == ".png":
        assets[key] = uri(webp(p, ART, ART_Q), "image/webp")
    else:
        assets[key] = uri(webp(p, LARGE, LARGE_Q), "image/webp")
    kept += 1
for p in sorted((A / "t").iterdir()):
    if p.suffix.lower() in (".jpg", ".jpeg", ".png"):
        assets["assets/t/" + p.name] = uri(webp(p, THUMB, THUMB_Q), "image/webp")
        kept += 1
for folder in (FILM_WIDE, FILM_TALL):
    d = A / "film" / folder
    for p in sorted(d.glob("*.webp")):
        assets["assets/film/%s/%s" % (folder, p.name)] = uri(p.read_bytes(), "image/webp")
        kept += 1
for name in ("poster.jpg", "poster_m.jpg"):
    p = A / "film" / name
    if p.exists():
        assets["assets/film/" + name] = uri(webp(p, LARGE, LARGE_Q), "image/webp")
        kept += 1
print("inlined %d pictures" % kept)

# point the film loader at the two cuts that are actually in the file
hub_js["hero.js"] = re.sub(r'"(w1280|w720)/"', '"%s/"' % FILM_WIDE, hub_js["hero.js"])
hub_js["hero.js"] = re.sub(r'\(retina \? "m720/" : "m480/"\)', '"%s/"' % FILM_TALL, hub_js["hero.js"])

# ---------------------------------------------------------------- fonts
CHARS = set(hub_html + hub_css + tl_html + tl_css + tl_js)
for s in hub_js.values():
    CHARS |= set(s)
CHARS |= set("0123456789%.,:;!?'\"()[]-–—…、。「」『』・％／＋×〜 ")
CHARS = "".join(sorted(c for c in CHARS if c.isprintable()))


def font_face(family, weight, repo_path):
    CACHE.mkdir(parents=True, exist_ok=True)
    src = CACHE / repo_path.rsplit("/", 1)[1]
    if not src.exists():
        print("  downloading", src.name)
        src.write_bytes(urllib.request.urlopen(GH + repo_path, timeout=300).read())
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

# ---------------------------------------------------------------- swaps
missing = []


def swap_css(text):
    def one(m):
        key = m.group(1).split("?")[0].replace("../", "")
        if key not in assets:
            missing.append(key)
            return m.group(0)
        return 'url("%s")' % assets[key]
    return re.sub(r'url\("([^"]+\.(?:png|jpg|jpeg|webp)[^"]*)"\)', one, text)


def strip_network(text):
    text = re.sub(r'\s*<link rel="preconnect"[^>]*>', "", text)
    text = re.sub(r'\s*<link rel="stylesheet" href="https://fonts\.googleapis[^>]*>', "", text)
    return text


def swap_img_src(text):
    def one(m):
        key = m.group(1).replace("../", "")
        if key not in assets:
            missing.append(key)
            return m.group(0)
        return 'src="%s"' % assets[key]
    return re.sub(r'src="((?:\.\./)?assets/[^"]+\.(?:png|jpg|jpeg|webp))"', one, text)


hub_css = swap_css(hub_css)
tl_css = swap_css(tl_css)
hub_html = swap_img_src(strip_network(hub_html))
tl_html = swap_img_src(strip_network(tl_html))

for text in (hub_html, tl_html):
    m = re.search(r'<link rel="icon"[^>]*>', text)
    if m:
        break
icon = '<link rel="icon" type="image/webp" href="%s">' % assets.get("assets/favicon.png", "")
hub_html = sub_literal(r'<link rel="icon"[^>]*>', icon, hub_html)
tl_html = sub_literal(r'<link rel="icon"[^>]*>', icon, tl_html)

# ---------------------------------------------------------------- the shim
SHIM = r"""
(function(){
  var A = __ASSETS__;
  window.__ART = A;
  if (!A || !Object.keys(A).length) return;
  var keys = Object.keys(A).sort(function(a,b){ return b.length - a.length; });
  var RE = new RegExp("(?:\\.\\./)?(?:" + keys.map(function(k){
    return k.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }).join("|") + ")", "g");
  function fix(v){
    return (typeof v === "string" && v.indexOf("assets/") >= 0)
      ? v.replace(RE, function(m){ return A[m.replace("../","")] || m; }) : v;
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
      configurable:true, enumerable:styleDesc.enumerable,
      get:function(){
        var real = styleDesc.get.call(this);
        if (seen.has(real)) return seen.get(real);
        var p = new Proxy(real, {
          get:function(t,k){ var v = t[k];
            return typeof v === "function" ? v.bind(t) : v; },
          set:function(t,k,v){ t[k] = fix(v); return true; }
        });
        seen.set(real, p);
        return p;
      }
    });
  }
  /* new Image().src = "..." goes through the same setter as any other image */
  var img = new Image();
  if (!Object.getOwnPropertyDescriptor(HTMLImageElement.prototype, "src")) {
    /* nothing to do - wrap() above already covered it */
  }
})();
"""

# ---------------------------------------------------------------- the panel
# the game and the timeline are separate pages on the live site; here they live
# inside the file and open over the hub
PANEL_CSS = """
#offx{position:fixed;inset:0;z-index:9000;background:#061620;display:none}
#offx.on{display:block}
#offx iframe{position:absolute;inset:0;width:100%;height:100%;border:0;background:#061620}
#offxBack{position:absolute;right:14px;top:14px;z-index:2;font:700 14px/1 system-ui,sans-serif;
  color:#06222e;background:#7fd9f5;border:0;border-radius:999px;padding:11px 18px;cursor:pointer;
  box-shadow:0 6px 20px rgba(0,0,0,.45)}
#offxBack:hover{background:#a5e6ff}
@media (max-width:600px){#offxBack{right:10px;top:10px;padding:10px 15px}}
"""

PANEL_JS = r"""
(function(){
  var DOCS = __DOCS__;
  var box = document.createElement("div");
  box.id = "offx";
  box.innerHTML = '<button id="offxBack" type="button"></button><iframe id="offxF" title=""></iframe>';
  document.body.appendChild(box);
  var frame = box.querySelector("#offxF");
  var back  = box.querySelector("#offxBack");
  var en    = function(){ return document.documentElement.lang === "en"; };

  function open(which){
    if (!DOCS[which]) return;
    back.textContent = en() ? "← Back to the hub" : "← 目次にもどる";
    frame.srcdoc = DOCS[which];
    box.classList.add("on");
    document.body.style.overflow = "hidden";
  }
  function close(){
    box.classList.remove("on");
    frame.srcdoc = "";
    document.body.style.overflow = "";
  }
  /* a page inside the panel still has its own links back to the hub and across
     to the other page; it calls in here rather than trying to walk to a file */
  window.__panel = function(which){ which === "close" ? close() : open(which); };

  /* the panel page picks its own language from the browser, same as the hub did,
     so they agree unless the reader has switched the hub over since */
  frame.addEventListener("load", function(){
    try {
      var d = frame.contentDocument;
      var btn = d && d.getElementById("langBtn");
      if (btn && (d.documentElement.lang === "en") !== en()) btn.click();
    } catch (err) {}
  });

  back.addEventListener("click", close);
  addEventListener("keydown", function(e){ if (e.key === "Escape") close(); });

  /* every link that would have walked to another page on the real site */
  document.addEventListener("click", function(e){
    var a = e.target.closest && e.target.closest("a[href]");
    if (!a) return;
    var h = a.getAttribute("href") || "";
    var which = /^\.?\/?game\/?$/.test(h) ? "game"
              : /^\.?\/?timeline\/?$/.test(h) ? "timeline" : null;
    if (!which) return;
    e.preventDefault();
    open(which);
  }, true);
})();
"""

# an embedded page gets no origin of its own, so anything it saved on the real
# site has nowhere to go; hand it a pocket that lasts as long as the panel is open
STORAGE_GUARD = """<script>
try { localStorage.getItem("x"); } catch (e) {
  var __m = {};
  Object.defineProperty(window, "localStorage", { value: {
    getItem: function(k){ return Object.prototype.hasOwnProperty.call(__m,k) ? __m[k] : null; },
    setItem: function(k,v){ __m[k] = String(v); },
    removeItem: function(k){ delete __m[k]; },
    clear: function(){ __m = {}; }
  }});
}
</script>"""


# a page in the panel keeps its own "back to the hub" and "play the game" links;
# they would try to walk to a folder that is not there, so they call the hub instead
PANEL_NAV = """<script>
addEventListener("click", function (e) {
  var a = e.target.closest && e.target.closest("a[href]");
  if (!a) return;
  var h = (a.getAttribute("href") || "").replace(/^\\.\\//, "");
  var to = /^\\.\\.\\/?$/.test(h) ? "close"
         : /^(\\.\\.\\/)?game\\/?$/.test(h) ? "game"
         : /^(\\.\\.\\/)?timeline\\/?$/.test(h) ? "timeline" : null;
  if (!to || !window.parent || !window.parent.__panel) return;
  e.preventDefault();
  window.parent.__panel(to);
}, true);
</script>"""


def guard(doc):
    return re.sub(r"<head[^>]*>",
                  lambda m: m.group(0) + STORAGE_GUARD + PANEL_NAV, doc, count=1)


# ---------------------------------------------------------------- timeline doc
tl_doc = tl_html
tl_doc = sub_literal(r'<link rel="stylesheet" href="timeline\.css[^"]*">',
                     "<style>%s%s</style>" % (fontcss, tl_css), tl_doc)
# the panel shares the hub's table of pictures rather than carrying a second copy;
# a panel page is served from inside the hub, so it can read straight off it
tl_doc = sub_literal(r'<script src="timeline\.js[^"]*"></script>',
                     "<script>%s</script>\n<script>%s</script>"
                     % (SHIM.replace("__ASSETS__",
                                     "(window.parent && window.parent.__ART) || {}"),
                        tl_js), tl_doc)
tl_doc = guard(tl_doc)

docs = {"timeline": tl_doc, "game": guard(game_html)}

# ---------------------------------------------------------------- hub doc
out = hub_html
out = sub_literal(r'<link rel="stylesheet" href="hub\.css[^"]*">',
                  "<style>%s%s%s</style>" % (fontcss, hub_css, PANEL_CSS), out)

shim_js = SHIM.replace("__ASSETS__", as_js(assets))
first = True
for name in ("data.js", "hub.js", "hero.js", "buddy.js", "cases.js"):
    body = hub_js[name]
    block = "<script>%s</script>" % body
    if first:
        block = "<script>%s</script>\n%s" % (shim_js, block)
        first = False
    out = re.sub(r'<script src="%s[^"]*"></script>' % re.escape(name), lambda m, b=block: b, out)

out = out.replace("</body>", "<script>%s</script>\n</body>"
                  % PANEL_JS.replace("__DOCS__", as_js(docs)))

if missing:
    print("  ! %d references had no inlined file:" % len(missing), sorted(set(missing))[:6])

# the scripts being inlined are full of backslashes, and anything that quietly
# eats one leaves a regular expression the browser refuses to parse - long after
# this script has said it finished. Check the shim came out whole, in the hub,
# in the panel page and in the copy of the game that was inlined whole.
fingerprint = r"""k.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")"""
for where, text in (("the hub", out), ("the timeline panel", tl_doc),
                    ("the game panel", docs["game"])):
    if fingerprint not in text:
        sys.exit("a script was mangled on the way into %s - every replacement "
                 "has to go through sub_literal" % where)
if "<script src=" in out or "<link rel=\"stylesheet\" href=\"" in out:
    left = re.findall(r'<script src="[^"]+"|<link rel="stylesheet" href="[^"]+"', out)
    sys.exit("something is still loaded from outside the file: %s" % left[:4])

OUT.write_bytes(out.encode("utf-8"))
print("\nWROTE %s  %.1f MB" % (OUT.name, OUT.stat().st_size / 1048576))
