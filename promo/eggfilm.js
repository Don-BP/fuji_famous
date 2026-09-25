/* FUJIE STUDIO - "From a single egg", the short film in idea 04.

   Everything here is drawn and heard live in the browser: the pictures are the
   pet game's own characters and backdrops plus three painted for the film, and
   every note and sound effect is synthesised with Web Audio, so there is no
   video file and no audio file to fetch.

   The film is a pure function of time: frame(t) draws the moment t seconds in,
   from nothing but t. That is what lets the poster be any frame, and lets the
   picture stay locked to the sound - the clock IS the audio clock.            */
(function () {
  "use strict";
  var host = document.getElementById("eggFilm");
  if (!host) return;

  /* the title card holds INTRO seconds longer than the story was first cut for;
     every scene and sound after it is pushed back by that much */
  var INTRO = 2.5;
  var W = 1280, H = 720, END = 60.5 + INTRO;
  var POSTER = 2.1;   /* the still before play: the egg in the light, no lettering under the button */
  var canvas = host.querySelector("canvas");
  var g = canvas.getContext("2d");
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ================================================================ art === */
  var ART = {
    bgTitle: "ef_bg_title.webp", bg1987: "ef_bg_1987.webp", bgTank: "ef_bg_tank.webp",
    bgFlow: "ef_bg_flow.webp", bgCycle: "ef_bg_cycle.webp", bgHall: "ef_bg_hall.webp",
    bgFinale: "ef_bg_finale.webp",
    egg: "ef_egg.webp", larva: "ef_larva.webp", fry: "ef_fry.webp", young: "ef_young.webp",
    dash: "ef_dash.webp", cheer: "ef_cheer.webp", wave: "ef_wave.webp",
    burst: "ef_burst.webp", valve: "ef_valve.webp", wheel: "ef_wheel.webp",
    arms: "ef_arms.webp"
  };
  var ARMS = { n: 37, cols: 8, w: 380, h: 400, fps: 12 };   /* written by tools/build_egg_film_arms.py */
  var IMG = {}, loading = null;
  function loadArt() {
    if (loading) return loading;
    /* Web fonts arrive in slices by character, and a canvas never asks for a
       slice on its own - so ask for every character the film will draw, read
       straight out of the scene code itself. */
    var src = SCENES.map(function (s) { return s.draw.toString(); }).join("");
    var glyphs = Array.from(new Set(src.replace(/[\u0000-\u007f]/g, "") + "0123456789,%+—–")).join("") + "AZaz";
    var fonts = document.fonts && document.fonts.load ? Promise.all([
      document.fonts.load("700 34px 'Zen Maru Gothic'", glyphs),
      document.fonts.load("40px 'Dela Gothic One'", glyphs),
      document.fonts.load("600 56px 'Shippori Mincho'", glyphs)
    ]).catch(function () {}) : Promise.resolve();
    loading = Promise.all(Object.keys(ART).map(function (k) {
      return new Promise(function (ok) {
        var im = new Image();
        im.onload = function () { IMG[k] = im; ok(); };
        im.onerror = function () { ok(); };
        im.src = "assets/" + ART[k];
      });
    }).concat([fonts]));
    return loading;
  }

  /* ============================================================ helpers === */
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
  function lerp(a, b, k) { return a + (b - a) * k; }
  function seg(t, a, b) { return clamp((t - a) / (b - a), 0, 1); }
  function inOut(k) { return k < .5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2; }
  function outCubic(k) { return 1 - Math.pow(1 - k, 3); }
  function outBack(k) { var c = 1.9; return 1 + (c + 1) * Math.pow(k - 1, 3) + c * Math.pow(k - 1, 2); }
  function outElastic(k) {
    if (k <= 0) return 0; if (k >= 1) return 1;
    return Math.pow(2, -10 * k) * Math.sin((k * 10 - .75) * (2 * Math.PI / 3)) + 1;
  }
  /* fade in over fi, hold, fade out over fo */
  function env(t, a, b, fi, fo) { return Math.min(seg(t, a, a + fi), 1 - seg(t, b - fo, b)); }
  function rng(seed) {
    return function () {
      seed |= 0; seed = seed + 0x6D2B79F5 | 0;
      var r = Math.imul(seed ^ seed >>> 15, 1 | seed);
      r = r + Math.imul(r ^ r >>> 7, 61 | r) ^ r;
      return ((r ^ r >>> 14) >>> 0) / 4294967296;
    };
  }
  function lang() { return document.documentElement.lang === "en" ? "en" : "ja"; }

  /* a backdrop, covering the frame, slowly pushing in or drifting */
  function bg(img, zoom, px, py, alpha) {
    if (!img) return;
    var s = Math.max(W / img.width, H / img.height) * zoom;
    var w = img.width * s, h = img.height * s;
    var ox = (W - w) / 2 + px * (w - W) / 2, oy = (H - h) / 2 + py * (h - H) / 2;
    g.globalAlpha = alpha == null ? 1 : alpha;
    g.drawImage(img, ox, oy, w, h);
    g.globalAlpha = 1;
    return { x: ox, y: oy, s: w / img.width };   /* to place things on the painting */
  }
  /* a sprite by its centre and width, with rotation, squash and stretch */
  function spr(img, x, y, w, o) {
    if (!img) return;
    o = o || {};
    var a = o.alpha == null ? 1 : o.alpha;
    if (a <= 0.002) return;
    var h = w * img.height / img.width;
    g.save();
    g.globalAlpha = a;
    g.translate(x, y);
    if (o.rot) g.rotate(o.rot);
    g.scale((o.flip ? -1 : 1) * (o.sx || 1), o.sy || 1);
    if (o.glow) { g.shadowColor = o.glow; g.shadowBlur = o.glowSize || 30; }
    g.drawImage(img, -w / 2, -h / 2, w, h);
    g.restore();
  }
  /* one drawing out of a sprite sheet, placed like spr() */
  function drawCell(img, m, i, x, y, w, o) {
    var h = w * m.h / m.w, sx = (i % m.cols) * m.w, sy = Math.floor(i / m.cols) * m.h;
    g.save();
    g.globalAlpha = o.alpha == null ? 1 : o.alpha;
    g.translate(x, y);
    if (o.rot) g.rotate(o.rot);
    g.scale(o.sx || 1, o.sy || 1);
    g.drawImage(img, sx, sy, m.w, m.h, -w / 2, -h / 2, w, h);
    g.restore();
  }
  function glowDot(x, y, r, color, a) {
    if (a <= 0) return;
    var gr = g.createRadialGradient(x, y, 0, x, y, r);
    gr.addColorStop(0, color.replace("A", a));
    gr.addColorStop(1, color.replace("A", 0));
    g.fillStyle = gr;
    g.fillRect(x - r, y - r, r * 2, r * 2);
  }
  /* a four-point cartoon sparkle, like the ones on the stickers */
  function star(x, y, r, a, rot) {
    if (a <= 0 || r <= 0) return;
    g.save();
    g.translate(x, y); g.rotate(rot || 0);
    g.globalAlpha = a;
    g.fillStyle = "#fff";
    g.shadowColor = "rgba(160,235,255,.9)"; g.shadowBlur = r * 1.4;
    g.beginPath();
    g.moveTo(0, -r);
    g.quadraticCurveTo(r * .12, -r * .12, r, 0);
    g.quadraticCurveTo(r * .12, r * .12, 0, r);
    g.quadraticCurveTo(-r * .12, r * .12, -r, 0);
    g.quadraticCurveTo(-r * .12, -r * .12, 0, -r);
    g.fill();
    g.restore();
  }
  function burstStars(t, t0, x, y, n, spread, seed) {
    var k = seg(t, t0, t0 + .9);
    if (k <= 0 || k >= 1) return;
    var r = rng(seed);
    for (var i = 0; i < n; i++) {
      var ang = r() * Math.PI * 2, d = spread * (.45 + r() * .7) * outCubic(k);
      star(x + Math.cos(ang) * d, y + Math.sin(ang) * d, (8 + r() * 12) * (1 - k * .6), 1 - k, k * 2);
    }
  }

  /* ----------------------------------------------- the water all around -- */
  var MOTES = [], BUBS = [];
  (function () {
    var r = rng(7);
    for (var i = 0; i < 70; i++) MOTES.push({ x: r() * W, y: r() * H, s: .5 + r() * 2, v: 4 + r() * 10, p: r() * 6.3 });
    for (i = 0; i < 26; i++) BUBS.push({ x: r() * W, y: r() * H, s: 3 + r() * 9, v: 30 + r() * 60, p: r() * 6.3 });
  })();
  function motes(t, a) {
    g.fillStyle = "#cfefff";
    for (var i = 0; i < MOTES.length; i++) {
      var m = MOTES[i];
      var y = ((m.y - t * m.v) % H + H) % H, x = m.x + Math.sin(t * .4 + m.p) * 14;
      g.globalAlpha = a * (.25 + .35 * Math.sin(t * 1.3 + m.p) * Math.sin(t * 1.3 + m.p));
      g.beginPath(); g.arc(x, y, m.s, 0, 6.283); g.fill();
    }
    g.globalAlpha = 1;
  }
  function bubbles(t, a, n) {
    g.lineWidth = 1.6;
    for (var i = 0; i < (n || BUBS.length); i++) {
      var b = BUBS[i];
      var y = ((b.y - t * b.v) % (H + 40) + H + 40) % (H + 40) - 20;
      var x = b.x + Math.sin(t * 1.7 + b.p) * 8;
      g.globalAlpha = a * .55;
      g.strokeStyle = "#dff6ff";
      g.beginPath(); g.arc(x, y, b.s, 0, 6.283); g.stroke();
      g.globalAlpha = a * .8;
      g.fillStyle = "#fff";
      g.beginPath(); g.arc(x - b.s * .35, y - b.s * .35, b.s * .22, 0, 6.283); g.fill();
    }
    g.globalAlpha = 1;
  }
  /* soft moving pools of light, the sun through the surface */
  function caustics(t, a, tint) {
    g.save();
    g.globalCompositeOperation = "lighter";
    for (var i = 0; i < 5; i++) {
      var x = W * (.15 + .18 * i) + Math.sin(t * .31 + i * 2.1) * 90;
      var y = H * .2 + Math.cos(t * .23 + i) * 60;
      glowDot(x, y, 260, tint || "rgba(90,200,230,A)", .07 * a);
    }
    g.restore();
  }
  function rays(t, a, cx) {
    g.save();
    g.globalCompositeOperation = "lighter";
    for (var i = 0; i < 5; i++) {
      var sway = Math.sin(t * .35 + i * 1.7) * .08;
      var x0 = (cx || W / 2) + (i - 2) * 120;
      var gr = g.createLinearGradient(0, 0, 0, H);
      gr.addColorStop(0, "rgba(190,240,255," + (.10 * a) + ")");
      gr.addColorStop(1, "rgba(190,240,255,0)");
      g.fillStyle = gr;
      g.beginPath();
      g.moveTo(x0 - 30, -10); g.lineTo(x0 + 30, -10);
      g.lineTo(x0 + 220 * (sway + (i - 2) * .25) + 90, H); g.lineTo(x0 + 220 * (sway + (i - 2) * .25) - 90, H);
      g.fill();
    }
    g.restore();
  }
  var VIG = null, GRAIN = null;
  function finish(t) {
    if (!VIG) {
      VIG = document.createElement("canvas"); VIG.width = W; VIG.height = H;
      var v = VIG.getContext("2d");
      var gr = v.createRadialGradient(W / 2, H / 2, H * .35, W / 2, H / 2, H * .95);
      gr.addColorStop(0, "rgba(2,10,16,0)"); gr.addColorStop(1, "rgba(2,10,16,.62)");
      v.fillStyle = gr; v.fillRect(0, 0, W, H);
      GRAIN = document.createElement("canvas"); GRAIN.width = 256; GRAIN.height = 256;
      var q = GRAIN.getContext("2d"), d = q.createImageData(256, 256), r = rng(3);
      for (var i = 0; i < d.data.length; i += 4) {
        var c = r() * 255; d.data[i] = d.data[i + 1] = d.data[i + 2] = c; d.data[i + 3] = 14;
      }
      q.putImageData(d, 0, 0);
    }
    g.drawImage(VIG, 0, 0);
    var f = Math.floor(t * 24);
    g.save();
    g.globalCompositeOperation = "overlay";
    g.fillStyle = g.createPattern(GRAIN, "repeat");
    g.translate((f * 71) % 256, (f * 37) % 256);
    g.fillRect(-256, -256, W + 512, H + 512);
    g.restore();
  }

  /* --------------------------------------------------------- lettering -- */
  var SANS = "'Zen Maru Gothic','Hiragino Maru Gothic ProN','Noto Sans JP',sans-serif";
  var DISPLAY = "'Dela Gothic One','Hiragino Sans',sans-serif";
  var SERIF = "'Shippori Mincho','Hiragino Mincho ProN','Yu Mincho',serif";

  function textShadowed(s, x, y, a) {
    g.globalAlpha = a;
    g.shadowColor = "rgba(0,10,20,.85)"; g.shadowBlur = 14; g.shadowOffsetY = 2;
    g.fillText(s, x, y);
    g.shadowColor = "transparent"; g.shadowBlur = 0; g.shadowOffsetY = 0;
    g.globalAlpha = 1;
  }
  /* the subtitle strip: one line or two, rising in and fading out */
  function caption(t, a, b, ja, en) {
    var k = env(t, a, b, .4, .35);
    if (k <= 0) return;
    var lines = lang() === "en" ? en : ja;
    /* on a phone the frame is small, so the words grow */
    var size = (lang() === "en" ? 30 : 33) * (host.clientWidth < 560 ? 1.35 : 1);
    g.save();
    var band = g.createLinearGradient(0, H - 190, 0, H);
    band.addColorStop(0, "rgba(2,12,20,0)"); band.addColorStop(1, "rgba(2,12,20," + (.7 * k) + ")");
    g.fillStyle = band; g.fillRect(0, H - 190, W, 190);
    g.font = "700 " + size + "px " + SANS;
    g.textAlign = "center"; g.textBaseline = "middle";
    g.fillStyle = "#f4fbff";
    var rise = (1 - outCubic(seg(t, a, a + .5))) * 12;
    var y0 = H - 62 - (lines.length - 1) * (size + 12);
    for (var i = 0; i < lines.length; i++) {
      var ki = env(t, a + i * .18, b, .4, .35);
      textShadowed(lines[i], W / 2, y0 + i * (size + 14) + rise, ki);
    }
    g.restore();
  }
  /* the year, in a round badge that pops in top-left */
  function yearBadge(t, a, b, year, sub) {
    var k = seg(t, a, a + .55), out = seg(t, b - .4, b);
    if (k <= 0 || out >= 1) return;
    var s = outBack(k) * (1 - out * .3), al = 1 - out;
    g.save();
    g.translate(118, 112); g.scale(s, s);
    g.globalAlpha = al;
    g.fillStyle = "rgba(6,28,46,.9)";
    g.beginPath(); g.arc(0, 0, 66, 0, 6.283); g.fill();
    g.lineWidth = 5; g.strokeStyle = "#00a0e9";
    g.beginPath(); g.arc(0, 0, 60, -Math.PI / 2, -Math.PI / 2 + 6.283 * outCubic(seg(t, a + .1, a + .9))); g.stroke();
    g.lineWidth = 2; g.strokeStyle = "rgba(255,255,255,.35)";
    g.beginPath(); g.arc(0, 0, 70, 0, 6.283); g.stroke();
    g.fillStyle = "#fff"; g.textAlign = "center"; g.textBaseline = "middle";
    g.font = "32px " + DISPLAY;
    g.fillText(year, 0, sub ? -6 : 2);
    if (sub) { g.font = "700 13px " + SANS; g.fillStyle = "#8fdcff"; g.fillText(sub, 0, 24); }
    g.restore();
  }
  /* a tilted "world first" style stamp */
  function stamp(t, a, b, x, y, big, small) {
    var k = seg(t, a, a + .45), out = seg(t, b - .35, b);
    if (k <= 0 || out >= 1) return;
    var s = lerp(1.9, 1, outCubic(k)) * (1 - out * .2);
    g.save();
    g.translate(x, y); g.rotate(-.12); g.scale(s, s);
    g.globalAlpha = Math.min(1, k * 2.5) * (1 - out);
    g.fillStyle = "#ffd75e";
    g.strokeStyle = "#0b2740"; g.lineWidth = 6; g.lineJoin = "round";
    g.beginPath();
    for (var i = 0; i < 28; i++) {
      var ang = i / 28 * 6.283, r = i % 2 ? 84 : 100;
      g[i ? "lineTo" : "moveTo"](Math.cos(ang) * r * 1.25, Math.sin(ang) * r * .78);
    }
    g.closePath(); g.stroke(); g.fill();
    g.fillStyle = "#0b2740"; g.textAlign = "center"; g.textBaseline = "middle";
    g.font = (lang() === "en" ? "21px " : "38px ") + DISPLAY;
    g.fillText(lang() === "en" ? small : big, 0, lang() === "en" ? 0 : -4);
    g.restore();
  }
  /* a little open tin of caviar, drawn in the sticker line: navy outline, silver, glossy roe */
  function caviarTin(t, a, b, x, y) {
    var k = outBack(seg(t, a, a + .5)), out = seg(t, b - .35, b);
    if (k <= 0 || out >= 1) return;
    g.save();
    g.translate(x, y + Math.sin(t * 2) * 3); g.scale(k * (1 - out * .2), k * (1 - out * .2));
    g.globalAlpha = 1 - out;
    g.lineWidth = 6; g.strokeStyle = "#0b2740"; g.lineJoin = "round";
    /* lid, tipped open behind */
    g.fillStyle = "#c9d3db";
    g.beginPath(); g.ellipse(18, -58, 92, 30, -.18, 0, 6.283); g.fill(); g.stroke();
    g.fillStyle = "#e8eef2"; g.beginPath(); g.ellipse(18, -60, 70, 20, -.18, 0, 6.283); g.fill();
    /* body */
    var grd = g.createLinearGradient(-90, 0, 90, 0);
    grd.addColorStop(0, "#9aa7b2"); grd.addColorStop(.45, "#eef3f6"); grd.addColorStop(1, "#8795a1");
    g.fillStyle = grd;
    g.beginPath(); g.moveTo(-90, 0); g.lineTo(-90, 34); g.ellipse(0, 34, 90, 26, 0, Math.PI, 0, true); g.lineTo(90, 0); g.closePath(); g.fill(); g.stroke();
    /* the roe */
    g.fillStyle = "#1c2630"; g.beginPath(); g.ellipse(0, 0, 90, 26, 0, 0, 6.283); g.fill(); g.stroke();
    var r = rng(202);
    for (var i = 0; i < 46; i++) {
      var ang = r() * 6.283, d = Math.sqrt(r());
      var ex = Math.cos(ang) * d * 78, ey = Math.sin(ang) * d * 19;
      g.fillStyle = "#2c3a46"; g.beginPath(); g.arc(ex, ey, 6, 0, 6.283); g.fill();
      g.fillStyle = "rgba(255,255,255,.75)"; g.beginPath(); g.arc(ex - 2, ey - 2, 1.8, 0, 6.283); g.fill();
    }
    star(-40, -18, 12 * Math.abs(Math.sin(t * 2.2)), 1, t);
    g.restore();
  }
  /* a big counting number */
  function counter(t, x, y, value, label, a, size) {
    if (a <= 0) return;
    g.save();
    g.textAlign = "center"; g.textBaseline = "alphabetic";
    g.font = (size || 88) + "px " + DISPLAY;
    g.fillStyle = "#fff";
    g.shadowColor = "rgba(0,160,233,.8)"; g.shadowBlur = 24;
    g.globalAlpha = a;
    g.fillText(value, x, y);
    g.shadowBlur = 0;
    g.font = "700 20px " + SANS; g.fillStyle = "#9fe3ff";
    g.fillText(label, x, y + 34);
    g.restore();
  }
  /* a cartoon speech bubble with a tail */
  function speech(x, y, w, h, tx, ty, s, a) {
    g.save();
    g.globalAlpha = a;
    g.translate(tx, ty); g.scale(s, s); g.translate(-tx, -ty);
    g.lineWidth = 6; g.strokeStyle = "#0b2740"; g.fillStyle = "#fff"; g.lineJoin = "round";
    var r = 34;
    g.beginPath();
    g.moveTo(x + r, y); g.lineTo(x + w - r, y); g.quadraticCurveTo(x + w, y, x + w, y + r);
    g.lineTo(x + w, y + h - r); g.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
    var mx = clamp(tx, x + r + 30, x + w - r - 30);
    g.lineTo(mx + 26, y + h); g.lineTo(tx, ty); g.lineTo(mx - 14, y + h);
    g.lineTo(x + r, y + h); g.quadraticCurveTo(x, y + h, x, y + h - r);
    g.lineTo(x, y + r); g.quadraticCurveTo(x, y, x + r, y);
    g.closePath();
    g.shadowColor = "rgba(0,0,0,.35)"; g.shadowBlur = 18; g.shadowOffsetY = 6;
    g.fill(); g.shadowColor = "transparent"; g.stroke();
    g.restore();
  }

  /* ============================================================ scenes === */
  var SCENES = [];
  var shift = 0;
  function scene(a, b, draw, iris) {
    var sh = shift;
    SCENES.push({ a: a + sh, b: b + sh, draw: sh ? function (t) { draw(t - sh); } : draw, iris: iris });
  }

  /* ---- A. title: one egg drifts down through the light (0 - 5) ---- */
  scene(0, 5.2 + INTRO, function (t) {
    g.fillStyle = "#03101a"; g.fillRect(0, 0, W, H);
    bg(IMG.bgTitle, 1.12 - t * .015, 0, -.3, seg(t, 0, 1.4));
    rays(t, seg(t, .3, 2), W / 2);
    caustics(t, 1);
    motes(t, seg(t, 0, 1.5));
    var k = seg(t, .6, 3.3);
    var ey = lerp(-60, 300, outCubic(k)), ex = W / 2 + Math.sin(t * 1.6) * 26 * (1 - k);
    glowDot(ex, ey, 120, "rgba(140,230,255,A)", .5 * seg(t, 1.5, 3));
    spr(IMG.egg, ex, ey, 70, { rot: Math.sin(t * 1.9) * .18 * (1 - k * .7) });
    star(ex - 16, ey - 18, 16 * Math.sin(Math.PI * seg(t, 2.2, 2.9)), 1, t);
    /* the title, letter by letter */
    var title = lang() === "en" ? "From a single egg" : "一粒の卵から";
    g.save();
    g.textAlign = "center"; g.textBaseline = "middle";
    g.font = (lang() === "en" ? "600 58px " : "600 72px ") + SERIF;
    var total = g.measureText(title).width, x = W / 2 - total / 2;
    for (var i = 0; i < title.length; i++) {
      var ch = title[i], cw = g.measureText(ch).width;
      var kk = seg(t, 2.4 + i * .09, 3.0 + i * .09);
      g.globalAlpha = kk * (1 - seg(t, 4.5 + INTRO, 5.2 + INTRO));
      g.fillStyle = "#fff";
      g.shadowColor = "rgba(120,220,255,.8)"; g.shadowBlur = 22;
      g.fillText(ch, x + cw / 2, 440 + (1 - outCubic(kk)) * 18);
      x += cw;
    }
    g.shadowBlur = 0;
    g.font = "700 18px " + SANS; g.fillStyle = "#8fdcff";
    g.globalAlpha = seg(t, 3.2, 3.8) * (1 - seg(t, 4.5 + INTRO, 5.2 + INTRO));
    g.fillText(lang() === "en" ? "FUJIKIN STURGEON · 1987 — 2027" : "フジキン チョウザメ事業　1987 — 2027", W / 2, 505);
    g.restore();
    bubbles(t, .7, 12);
  });

  /* ---- B. 1987: an evening, a remark (5 - 12.5) ---- */
  shift = INTRO;
  scene(4.6, 12.9, function (t) {
    var lt = t - 5;
    bg(IMG.bg1987, 1.08 - lt * .006, lerp(.25, -.1, inOut(seg(lt, 0, 7.5))), .2);
    /* stars twinkling over the painted ones */
    var r = rng(19);
    for (var i = 0; i < 22; i++) {
      var sx = r() * W, sy = r() * 300, ph = r() * 6;
      star(sx, sy, 3 + 4 * Math.pow(Math.max(0, Math.sin(lt * 2 + ph)), 6), .9, 0);
    }
    /* the windows breathe */
    glowDot(900, 470, 150, "rgba(255,200,110,A)", .22 + .06 * Math.sin(lt * 3.1));
    /* the river glints */
    g.save(); g.globalCompositeOperation = "lighter";
    for (i = 0; i < 16; i++) {
      var gx = 120 + i * 60 + Math.sin(lt * .8 + i) * 20, gy = 600 + (i % 4) * 22;
      g.globalAlpha = .35 * Math.pow(Math.max(0, Math.sin(lt * 2.4 + i * 1.3)), 4);
      g.fillStyle = "#bff3ff"; g.fillRect(gx, gy, 26, 2);
    }
    g.restore();
    yearBadge(lt, .3, 7.4, "1987");
    /* the idea pops up out of the window */
    var kb = seg(lt, 1.1, 1.7);
    if (kb > 0) {
      var s = outBack(kb) * (1 - seg(lt, 7.0, 7.4));
      var bx = 250, by = 110, bw = 470, bh = 200;
      speech(bx, by, bw, bh, 905, 452, s, 1);
      g.save();
      g.translate(905, 452); g.scale(s, s); g.translate(-905, -452);
      var p1 = outBack(seg(lt, 1.6, 2.1)), p2 = outBack(seg(lt, 2.0, 2.5)), p3 = outBack(seg(lt, 2.4, 2.9));
      spr(IMG.valve, bx + 100, by + 102, 130 * p1, { rot: Math.sin(lt * 3) * .05 });
      g.fillStyle = "#0b2740"; g.font = "54px " + DISPLAY; g.textAlign = "center"; g.textBaseline = "middle";
      g.globalAlpha = p2; g.fillText("+", bx + 200, by + 104); g.globalAlpha = 1;
      spr(IMG.young, bx + 330, by + 100 + Math.sin(lt * 4) * 5, 220 * p3, { flip: false });
      g.globalAlpha = seg(lt, 3.0, 3.3);
      g.fillStyle = "#00a0e9"; g.font = "60px " + DISPLAY;
      g.save(); g.translate(bx + bw - 34, by + 46); g.rotate(.2 + Math.sin(lt * 5) * .08);
      g.fillText("?", 0, 0); g.restore();
      g.restore();
      burstStars(lt, 3.0, bx + bw - 34, by + 46, 7, 70, 5);
    }
    caption(lt, .7, 7.4,
      ["「フジキンのバルブを使って、", "チョウザメの養殖を始めてみては」── 西堀栄三郎"],
      ["“Why not use Fujikin's valves", "to try farming sturgeon?” — Eizaburo Nishibori"]);
  }, { x: 900, y: 470 });

  /* ---- C. 1992: a hundred eggs, and only five (12.5 - 20) ---- */
  var EGGS = [];
  (function () {
    /* a soft round cloud, laid out like seeds in a sunflower */
    var r = rng(92), keep = [23, 47, 58, 71, 36];
    for (var i = 0; i < 100; i++) {
      var rad = Math.sqrt((i + .5) / 100), ang = i * 2.39996;
      EGGS.push({
        x: 640 + Math.cos(ang) * rad * 330 + (r() - .5) * 14,
        y: 340 + Math.sin(ang) * rad * 175 + (r() - .5) * 10,
        d: r(), p: r() * 6.3, keep: keep.indexOf(i)
      });
    }
  })();
  scene(12.1, 20.4, function (t) {
    var lt = t - 12.5;
    bg(IMG.bgTank, 1.06 + lt * .006, 0, 0);
    caustics(lt + 12, .8);
    motes(t, .8);
    yearBadge(lt, .2, 7.3, "1992");
    var fadeStart = 4.3;
    var left = 100;
    for (var i = 0; i < EGGS.length; i++) {
      var e = EGGS[i];
      var appear = seg(lt, .1 + e.d * 1.4, .45 + e.d * 1.4);
      if (appear <= 0) continue;
      var hatch = lt > 2.2 + e.d * 1.3;
      var bob = Math.sin(lt * 2 + e.p) * 4;
      var x = e.x, y = e.y + bob;
      if (e.keep < 0) {
        /* the ones that did not make it drift up as little lights */
        var go = seg(lt, fadeStart + e.d * 2, fadeStart + .9 + e.d * 2);
        if (go >= 1) { left--; continue; }
        if (go > 0) {
          left -= go > .3 ? 1 : 0;
          glowDot(x, y - go * 90, 26, "rgba(170,235,255,A)", .7 * (1 - go));
          spr(IMG.larva, x, y - go * 90, 40 * (1 - go * .8), { alpha: 1 - go });
          continue;
        }
      } else if (lt > fadeStart) {
        /* the five that lived gather in the middle and glow */
        var m = inOut(seg(lt, fadeStart + 1.2, fadeStart + 2.6));
        x = lerp(x, 470 + e.keep * 85, m); y = lerp(y, 290 + (e.keep % 2) * 40, m) + bob;
        glowDot(x, y, 70, "rgba(120,220,255,A)", .55 * seg(lt, fadeStart + .5, fadeStart + 1.5));
      }
      if (!hatch) {
        spr(IMG.egg, x, y, 30 * outBack(appear), { rot: Math.sin(lt * 5 + e.p) * .08 });
      } else {
        var hk = seg(lt, 2.2 + e.d * 1.3, 2.5 + e.d * 1.3);
        var big = e.keep >= 0 && lt > fadeStart ? lerp(44, 64, seg(lt, fadeStart + 1.2, fadeStart + 2.6)) : 44;
        spr(IMG.larva, x, y, big * outBack(hk),
            { rot: Math.sin(lt * 7 + e.p) * .14, flip: e.p > 3 });
        if (hk < 1) star(x, y, 14 * (1 - hk), 1 - hk, hk);
      }
    }
    if (lt > fadeStart - .2) {
      counter(lt, 1110, 200, String(left), lang() === "en" ? "OF 100 FISH" : "／100 尾",
        seg(lt, fadeStart - .2, fadeStart + .3) * (1 - seg(lt, 7.2, 7.6)));
    }
    caption(lt, .5, 3.6,
      ["1992年、日本の民間で初めての人工ふ化。"],
      ["1992: the first artificial hatch by a private company in Japan."]);
    caption(lt, 3.7, 7.2,
      ["でも最初の年、育ったのは", "100尾のうち、わずか5尾でした。"],
      ["But in that first year,", "only 5 fish in 100 lived."]);
  }, { x: 640, y: 300 });

  /* ---- D. the fix: a valve maker's flow control (20 - 30) ---- */
  var SCHOOL = [];
  (function () {
    var r = rng(41);
    for (var i = 0; i < 14; i++) SCHOOL.push({ r: 90 + (i % 5) * 34 + r() * 20, p: i * 2.39 + r() * .6, v: .45 + r() * .35, y: ((i * 7) % 14 / 13 - .5) * 250, d: r() });
  })();
  function gauge(t, a, x, y, label, icon, okAt) {
    var k = outBack(seg(t, a, a + .45));
    if (k <= 0) return;
    g.save();
    g.translate(x, y); g.scale(k, k);
    g.fillStyle = "rgba(6,28,46,.88)"; g.strokeStyle = "rgba(143,220,255,.55)"; g.lineWidth = 2;
    g.beginPath(); g.roundRect ? g.roundRect(-120, -40, 240, 80, 40) : g.rect(-120, -40, 240, 80); g.fill(); g.stroke();
    /* the dial */
    g.lineWidth = 7; g.lineCap = "round";
    g.strokeStyle = "#e0564a"; g.beginPath(); g.arc(-72, 8, 26, Math.PI, Math.PI * 1.45); g.stroke();
    g.strokeStyle = "#f1c24b"; g.beginPath(); g.arc(-72, 8, 26, Math.PI * 1.5, Math.PI * 1.62); g.stroke();
    g.strokeStyle = "#39d49a"; g.beginPath(); g.arc(-72, 8, 26, Math.PI * 1.68, Math.PI * 2); g.stroke();
    var settle = outElastic(seg(t, okAt, okAt + 1.1));
    var ang = lerp(Math.PI * 1.1, Math.PI * 1.84, settle) + Math.sin(t * 9) * .03 * (1 - settle);
    g.strokeStyle = "#fff"; g.lineWidth = 4;
    g.beginPath(); g.moveTo(-72, 8); g.lineTo(-72 + Math.cos(ang) * 24, 8 + Math.sin(ang) * 24); g.stroke();
    g.fillStyle = "#fff"; g.beginPath(); g.arc(-72, 8, 5, 0, 6.283); g.fill();
    g.font = "700 26px " + SANS; g.textAlign = "left"; g.textBaseline = "middle";
    g.fillStyle = "#f4fbff"; g.fillText(label, -30, 2);
    if (t > okAt + .6) {
      var ck = outBack(seg(t, okAt + .6, okAt + 1));
      g.fillStyle = "#39d49a"; g.beginPath(); g.arc(92, 0, 16 * ck, 0, 6.283); g.fill();
      g.strokeStyle = "#062"; g.lineWidth = 4;
      g.beginPath(); g.moveTo(84, 0); g.lineTo(90, 7); g.lineTo(101, -7); g.stroke();
    }
    g.restore();
  }
  function flowRibbons(t, a) {
    if (a <= 0) return;
    g.save();
    g.globalCompositeOperation = "lighter";
    g.lineCap = "round";
    for (var i = 0; i < 6; i++) {
      var y0 = 170 + i * 80, ph = t * (1.6 + i * .15) + i;
      var gr = g.createLinearGradient(0, 0, W, 0);
      gr.addColorStop(0, "rgba(120,230,255,0)");
      gr.addColorStop(.5, "rgba(120,230,255," + (.22 * a) + ")");
      gr.addColorStop(1, "rgba(120,230,255,0)");
      g.strokeStyle = gr; g.lineWidth = 6 + (i % 3) * 5;
      g.beginPath();
      for (var x = 0; x <= W; x += 20) {
        var y = y0 + Math.sin(x * .006 + ph) * 28 + Math.sin(x * .013 - ph * .7) * 10;
        g[x ? "lineTo" : "moveTo"](x, y);
      }
      g.stroke();
      /* dashes riding the current */
      g.strokeStyle = "rgba(230,250,255," + (.5 * a) + ")"; g.lineWidth = 3;
      for (var j = 0; j < 3; j++) {
        var dx = ((t * 260 + j * 430 + i * 170) % (W + 200)) - 100;
        var dy = y0 + Math.sin(dx * .006 + ph) * 28 + Math.sin(dx * .013 - ph * .7) * 10;
        g.beginPath(); g.moveTo(dx, dy); g.lineTo(dx + 40, dy + Math.cos(dx * .006 + ph) * 6); g.stroke();
      }
    }
    g.restore();
  }
  scene(19.6, 30.4, function (t) {
    var lt = t - 20;
    bg(IMG.bgFlow, 1.1 - lt * .006, 0, 0);
    caustics(t, .8);
    var flowOn = seg(lt, 1.6, 3.2);
    flowRibbons(t, flowOn);
    motes(t * (1 + flowOn * 2), .7);
    /* the handwheel rolls in and turns */
    var wk = outBack(seg(lt, .15, .8));
    var turn = inOut(seg(lt, .9, 2.8)) * Math.PI * 3.5 + Math.max(0, lt - 2.8) * .8;
    spr(IMG.wheel, lerp(-160, 230, wk), 400, 330, { rot: turn - (1 - wk) * 2 });
    if (lt > .9 && lt < 2.8) {
      g.save(); g.strokeStyle = "rgba(255,255,255,.6)"; g.lineWidth = 5; g.lineCap = "round";
      for (var i = 0; i < 3; i++) {
        var a0 = turn * .2 + i * 2.1;
        g.beginPath(); g.arc(230, 400, 200, a0, a0 + .5); g.stroke();
      }
      g.restore();
    }
    /* temperature, flow, oxygen */
    var J = lang() !== "en";
    var gOut = 1 - seg(lt, 5.1, 5.5);
    if (gOut > 0) {
      g.save(); g.globalAlpha = gOut;
      gauge(lt, 1.0, 1030, 190, J ? "水温" : "Temp", 0, 2.9);
      gauge(lt, 1.35, 1030, 290, J ? "水流" : "Flow", 1, 3.3);
      gauge(lt, 1.7, 1030, 390, J ? "溶存酸素" : "Oxygen", 2, 3.7);
      g.restore();
    }
    /* the five little ones, then more and more, growing into fry */
    var grow = seg(lt, 4.4, 5.4);
    var n = Math.round(lerp(5, SCHOOL.length, seg(lt, 5, 8)));
    for (i = 0; i < n; i++) {
      var f = SCHOOL[i];
      var fin = i < 5 ? 1 : seg(lt, 5 + (i - 5) * .33, 5.6 + (i - 5) * .33);
      var ang = lt * f.v + f.p;
      var cx = 600 + Math.cos(ang) * f.r * 1.15, cy = 350 + f.y + Math.sin(ang * 2) * 18;
      var facing = -Math.sin(ang) < 0;
      if (i < 5 && lt < 4.4) {
        cx = lerp(470 + i * 85, cx, inOut(seg(lt, 0, 1.4)));
        cy = lerp(290 + (i % 2) * 40, cy, inOut(seg(lt, 0, 1.4)));
      }
      var popK = seg(lt, 4.4 + i * .12, 4.7 + i * .12);
      if (i < 5 && popK < 1) {
        spr(IMG.larva, cx, cy, 62, { rot: Math.sin(lt * 7 + f.p) * .14, flip: !facing });
        if (popK > 0) star(cx, cy, 30 * Math.sin(popK * Math.PI), 1, popK);
      } else {
        var size = 82 + f.d * 20;
        spr(IMG.fry, cx, cy + Math.sin(lt * 5 + f.p) * 4, size * outBack(i < 5 ? popK : fin),
            { rot: Math.sin(lt * 3 + f.p) * .08, flip: !facing });
      }
    }
    /* survival 5% -> 60% */
    var sk = seg(lt, 5.6, 7.9);
    if (lt > 5.4) {
      var pct = Math.round(lerp(5, 60, inOut(sk)));
      counter(lt, 1040, 250, pct + "%", J ? "生残率" : "SURVIVAL RATE",
        seg(lt, 5.4, 5.8) * (1 - seg(lt, 9.6, 10)), 110);
      if (sk >= 1) burstStars(lt, 7.9, 1040, 210, 9, 120, 11);
    }
    caption(lt, .9, 4.6,
      ["水温、水流、溶存酸素。"],
      ["Water temperature. Flow. Dissolved oxygen."]);
    caption(lt, 4.8, 9.9,
      ["決め手は、フジキンが本業で磨いた", "超精密な流体制御でした。"],
      ["What settled it was the ultra-precise", "fluid control Fujikin had perfected."]);
  }, { x: 230, y: 400 });

  /* ---- E. 1998: the circle closes (30 - 37.5) ---- */
  var RING = { x: 640, y: 320, r: 190 };
  function ringPos(i) { var a = -Math.PI / 2 + i * Math.PI / 2; return [RING.x + Math.cos(a) * RING.r * 1.25, RING.y + Math.sin(a) * RING.r]; }
  function arrowArc(i, k, a) {
    if (k <= 0) return;
    var a0 = -Math.PI / 2 + i * Math.PI / 2 + .42, a1 = a0 + (Math.PI / 2 - .84) * k;
    g.save();
    g.globalAlpha = a;
    g.strokeStyle = "#7fe0ff"; g.lineWidth = 7; g.lineCap = "round";
    g.shadowColor = "rgba(0,160,233,.9)"; g.shadowBlur = 16;
    g.beginPath();
    for (var s = 0; s <= 24; s++) {
      var ang = lerp(a0, a1, s / 24);
      g[s ? "lineTo" : "moveTo"](RING.x + Math.cos(ang) * RING.r * 1.25, RING.y + Math.sin(ang) * RING.r);
    }
    g.stroke();
    if (k > .15) {
      var ex = RING.x + Math.cos(a1) * RING.r * 1.25, ey = RING.y + Math.sin(a1) * RING.r;
      var tx = -Math.sin(a1) * RING.r * 1.25, ty = Math.cos(a1) * RING.r;
      var d = Math.atan2(ty, tx);
      g.fillStyle = "#7fe0ff";
      g.beginPath();
      g.moveTo(ex + Math.cos(d) * 16, ey + Math.sin(d) * 16);
      g.lineTo(ex + Math.cos(d + 2.4) * 16, ey + Math.sin(d + 2.4) * 16);
      g.lineTo(ex + Math.cos(d - 2.4) * 16, ey + Math.sin(d - 2.4) * 16);
      g.fill();
    }
    g.restore();
  }
  scene(29.6, 37.9, function (t) {
    var lt = t - 30;
    bg(IMG.bgCycle, 1.08 + lt * .008, 0, 0);
    caustics(t, 1, "rgba(120,220,255,A)");
    motes(t, .8);
    yearBadge(lt, .2, 7.3, "1998");
    var closed = seg(lt, 3.6, 4.0);
    /* glow in the middle when the circle closes */
    glowDot(RING.x, RING.y, 300, "rgba(120,230,255,A)", .45 * closed * (.8 + .2 * Math.sin(lt * 3)));
    var spin = Math.max(0, lt - 4) * .0;
    var stages = [IMG.egg, IMG.larva, IMG.fry, IMG.young], sizes = [74, 120, 132, 250];
    for (var i = 0; i < 4; i++) {
      var p = ringPos(i), at = 1.5 + i * .55;
      if (i === 3) {
        /* the grown fish swims in from the left and takes its place */
        var sw = inOut(seg(lt, 0, 1.6));
        var x = lerp(-200, p[0], sw), y = lerp(430, p[1], sw) + Math.sin(lt * 3) * 6;
        if (lt < 1.7) spr(IMG.dash, x, y, 300, {});
        else spr(IMG.young, p[0], p[1] + Math.sin(lt * 3) * 6, sizes[3] * lerp(1.15, 1, seg(lt, 1.7, 2)), {});
        continue;
      }
      var k = outBack(seg(lt, at, at + .45));
      var pulse = 1 + closed * .06 * Math.sin(lt * 4 + i);
      spr(stages[i], p[0], p[1] + Math.sin(lt * 2.5 + i) * 5, sizes[i] * k * pulse,
          { rot: i === 1 ? Math.sin(lt * 6) * .1 : 0 });
      if (k > 0) burstStars(lt, at, p[0], p[1], 5, 60, 30 + i);
    }
    for (i = 0; i < 4; i++) arrowArc(i, seg(lt, 1.8 + i * .55, 2.3 + i * .55), 1);
    /* the new eggs: one fish's eggs, the circle starting again */
    if (closed > 0) {
      var r = rng(98);
      for (i = 0; i < 12; i++) {
        var a = r() * 6.283, d = 30 + r() * 60, k2 = seg(lt, 3.8 + i * .05, 4.6 + i * .05);
        var p0 = ringPos(0);
        spr(IMG.egg, p0[0] + Math.cos(a) * d * outCubic(k2), p0[1] + Math.sin(a) * d * .7 * outCubic(k2),
            26 * k2, { alpha: k2 });
      }
      burstStars(lt, 3.6, RING.x, RING.y, 14, 260, 77);
    }
    stamp(lt, 4.1, 7.4, 1060, 170, "世界初", "WORLD FIRST");
    caption(lt, 1.0, 7.4,
      ["1998年、世界初の完全養殖。", "卵から育てた魚が、また卵を産みました。"],
      ["1998: a world first.", "Fish raised from eggs laid eggs of their own."]);
  }, { x: 640, y: 320 });

  /* ---- F. 2002 and today: ten thousand at Satomi (37.5 - 45) ---- */
  /* the glass tanks in the hall painting, back to front, in the painting's own
     pixels: rim centre, rim radii, and where the tank meets the floor */
  var TANKS = [
    [590, 285, 65, 20, 330], [1015, 265, 70, 20, 310], [215, 285, 88, 25, 340],
    [1180, 320, 90, 32, 380], [60, 340, 125, 40, 430], [1310, 345, 85, 35, 450],
    [485, 355, 125, 35, 500], [890, 355, 118, 35, 480],
    [405, 440, 150, 50, 660], [1005, 440, 165, 50, 650],
    [1200, 530, 215, 60, 768], [200, 575, 195, 70, 768]
  ];
  var HALL = [];
  (function () {
    var r = rng(2002);
    TANKS.forEach(function (k, i) {
      for (var j = 0; j < (i >= 8 ? 2 : 3); j++) HALL.push({ tank: i, v: .35 + r() * .35, p: r() * 6.3, d: .25 + r() * .6 });
    });
  })();
  scene(37.1, 45.4, function (t) {
    var lt = t - 37.5;
    var z = lerp(1.32, 1.02, inOut(seg(lt, 0, 7.5)));
    var m = bg(IMG.bgHall, z, 0, lerp(.5, 0, inOut(seg(lt, 0, 7.5))));
    /* the warm lamps breathe */
    caustics(t, .6, "rgba(255,210,140,A)");
    var fishA = seg(lt, .4, 2);
    if (m) {
      for (var ti = 0; ti < TANKS.length; ti++) {
        var k = TANKS[ti];
        var cx = m.x + k[0] * m.s, rimY = m.y + k[1] * m.s, rx = k[2] * m.s, ry = k[3] * m.s, bot = m.y + k[4] * m.s;
        g.save();
        /* only inside this tank: the water under the rim, down to the floor */
        g.beginPath();
        g.ellipse(cx, rimY, rx * .97, ry * .9, 0, 0, Math.PI);
        g.lineTo(cx - rx * .97, bot - ry * .6);
        g.ellipse(cx, bot - ry * .6, rx * .97, ry * .9, 0, Math.PI, 0, true);
        g.closePath();
        g.clip();
        for (var i = 0; i < HALL.length; i++) {
          var f = HALL[i];
          if (f.tank !== ti) continue;
          var ph = lt * f.v + f.p;
          /* round and round the tank: coming towards us it grows and brightens */
          var near = (Math.cos(ph) + 1) / 2;
          var fx = cx + Math.sin(ph) * rx * .6;
          var fy = rimY + ry + (bot - rimY - ry * 1.6) * f.d + near * ry * .35;
          spr(IMG.young, fx, fy, rx * lerp(.5, .72, near),
              { flip: Math.cos(ph) > 0, alpha: fishA * lerp(.4, .9, near), rot: Math.sin(ph) * .05 });
        }
        g.restore();
        /* the surface catches the lamp light */
        g.save(); g.globalCompositeOperation = "lighter";
        g.globalAlpha = fishA * (.12 + .08 * Math.sin(lt * 2 + ti));
        g.strokeStyle = "#bff6ff"; g.lineWidth = 2;
        g.beginPath(); g.ellipse(cx, rimY + 2, rx * (.5 + .3 * ((lt * .5 + ti * .37) % 1)), ry * .5, 0, 0, 6.283); g.stroke();
        g.restore();
      }
    }
    yearBadge(lt, .2, 3.8, "2002");
    stamp(lt, .8, 3.8, 1060, 170, "日本初", "JAPAN'S FIRST");
    caviarTin(lt, 1.2, 3.8, 1060, 330);
    yearBadge(lt, 3.9, 7.5, lang() === "en" ? "NOW" : "いま");
    var ck = seg(lt, 4.0, 5.6);
    if (lt > 3.9) {
      var n = Math.round(lerp(0, 10000, 1 - Math.pow(1 - ck, 3)));
      counter(lt, W / 2, 190, n.toLocaleString("en-US") + (ck >= 1 ? "+" : ""),
        lang() === "en" ? "STURGEON" : "尾のチョウザメ", seg(lt, 3.9, 4.3) * (1 - seg(lt, 7.1, 7.5)), 104);
      if (ck >= 1) burstStars(lt, 5.6, W / 2, 150, 10, 200, 13);
    }
    caption(lt, .6, 3.7,
      ["2002年、日本初の国産キャビアを出荷。"],
      ["2002: Japan's first home-grown caviar is shipped."]);
    caption(lt, 4.0, 7.4,
      ["茨城県・里美養魚場。", "いまも1万尾を超えるチョウザメが泳いでいます。"],
      ["Satomi Fish Farm, Ibaraki.", "More than ten thousand sturgeon still swim there."]);
  }, { x: 640, y: 380 });

  /* ---- G. 2027: a new egg, and it is Fujie (45 - 59) ---- */
  scene(45, END - INTRO, function (t) {
    var lt = t - 45;
    bg(IMG.bgFinale, 1.1 - lt * .005, 0, -.2);
    rays(t, 1, 640);
    caustics(t, 1, "rgba(255,230,160,A)");
    motes(t, 1);
    bubbles(t, .8);
    var cx = 640, cy = 360;
    /* the egg arrives */
    var dk = seg(lt, .2, 2.0);
    var hatchAt = 3.1;
    if (lt < hatchAt) {
      var ey = lerp(-60, cy, outCubic(dk)), ex = cx + Math.sin(lt * 1.7) * 30 * (1 - dk);
      var wob = lt > 2.2 ? Math.sin(lt * 38) * .16 * seg(lt, 2.2, 2.5) : Math.sin(lt * 1.9) * .15;
      glowDot(ex, ey, 150, "rgba(255,240,190,A)", .5 * seg(lt, 1.2, 2.2));
      spr(IMG.egg, ex, ey, 96, { rot: wob, sx: 1 + seg(lt, 2.8, 3.1) * .12, sy: 1 - seg(lt, 2.8, 3.1) * .1 });
      /* cracks */
      var ck = seg(lt, 2.3, 3.0);
      if (ck > 0) {
        g.save(); g.translate(ex, ey); g.rotate(wob);
        g.strokeStyle = "#e8fbff"; g.lineWidth = 3; g.lineJoin = "round";
        g.beginPath();
        var pts = [[-40, -6], [-24, 4], [-12, -8], [0, 6], [12, -6], [26, 5], [40, -4]];
        var m = Math.ceil(pts.length * ck);
        for (var i = 0; i < m; i++) g[i ? "lineTo" : "moveTo"](pts[i][0], pts[i][1]);
        g.stroke(); g.restore();
      }
      star(ex + 20, ey - 26, 18 * Math.sin(Math.PI * seg(lt, 1.8, 2.4)), 1, lt);
    }
    /* POP */
    var pk = seg(lt, hatchAt, hatchAt + .5);
    if (pk > 0 && pk < 1) spr(IMG.burst, cx, cy, 520 * outCubic(pk), { alpha: 1 - pk, rot: pk });
    if (lt > hatchAt) {
      g.save(); g.globalCompositeOperation = "lighter";
      glowDot(cx, cy, 700, "rgba(255,250,230,A)", .55 * (1 - seg(lt, hatchAt, hatchAt + .6)));
      g.restore();
    }
    burstStars(lt, hatchAt, cx, cy, 18, 330, 2027);
    /* Fujie springs out, then settles to the left for the end card */
    if (lt > hatchAt) {
      var sk = seg(lt, hatchAt, hatchAt + .7);
      var squash = 1 + Math.sin(sk * Math.PI * 2.5) * .18 * (1 - sk);
      var move = inOut(seg(lt, 6.5, 7.6));
      var fx = lerp(cx, 350, move), fy = lerp(cy, 380, move) + Math.sin(lt * 2.2) * 8;
      var size = lerp(360, 380, move) * outBack(sk);
      var o = { sx: 1 / squash, sy: squash, rot: Math.sin(lt * 1.7) * .03 };
      if (IMG.arms && ARMS.n) {
        /* the hand-animated clip: out of the egg, both flippers up, then
           he keeps waving by rocking back and forth through the last drawings */
        var i = Math.floor((lt - hatchAt) * ARMS.fps), last = ARMS.n - 1;
        if (i > last) {
          var span = Math.min(10, last), pp = (i - last) % (2 * span);
          i = last - (pp < span ? pp : 2 * span - pp);
        }
        drawCell(IMG.arms, ARMS, i, fx, fy, size * 1.05, o);
      } else {
        spr(lt > 7.0 ? IMG.wave : IMG.cheer, fx, fy, size, o);
      }
      if (lt > 9) burstStars(lt, 9 + Math.floor((lt - 9) / 1.6) * 1.6, fx + 60, fy - 80, 4, 90, Math.floor(lt / 1.6));
      /* Fujie says hello */
      var hk = outBack(seg(lt, 3.9, 4.3)) * (1 - seg(lt, 6.4, 6.8));
      if (hk > 0) {
        speech(900, 100, 360, 140, 860, 250, hk, 1);
        g.save();
        g.translate(860, 250); g.scale(hk, hk); g.translate(-860, -250);
        g.fillStyle = "#0b2740"; g.textAlign = "center"; g.textBaseline = "middle";
        if (lang() === "en") {
          g.font = "34px " + DISPLAY; g.fillText("Hi! I'm Fujie!", 1080, 170);
        } else {
          g.font = "700 26px " + SANS; g.fillText("はじめまして！", 1080, 146);
          g.font = "40px " + DISPLAY; g.fillText("フジィです", 1080, 194);
        }
        g.restore();
      }
    }
    /* the end card */
    var ek = seg(lt, 6.0, 7.0);
    if (ek > 0) {
      g.save();
      g.textAlign = "left"; g.textBaseline = "alphabetic";
      var X = 700, J = lang() !== "en";
      g.globalAlpha = seg(lt, 7.2, 7.8);
      g.font = "30px " + DISPLAY; g.fillStyle = "#8fdcff";
      g.fillText("1987 — 2027", X, 250 + (1 - outCubic(seg(lt, 7.2, 7.8))) * 14);
      g.fillStyle = "#fff";
      g.shadowColor = "rgba(0,40,70,.8)"; g.shadowBlur = 20;
      g.font = (J ? "600 60px " : "600 50px ") + SERIF;
      var l1 = J ? "一粒の卵から、" : "Forty years,", l2 = J ? "40年。" : "from a single egg.";
      g.globalAlpha = seg(lt, 7.6, 8.3);
      g.fillText(l1, X, 330 + (1 - outCubic(seg(lt, 7.6, 8.3))) * 16);
      g.globalAlpha = seg(lt, 8.0, 8.7);
      g.fillText(l2, X, 404 + (1 - outCubic(seg(lt, 8.0, 8.7))) * 16);
      g.shadowBlur = 0;
      /* the line under it draws itself */
      g.globalAlpha = 1;
      g.strokeStyle = "#00a0e9"; g.lineWidth = 4; g.lineCap = "round";
      g.beginPath(); g.moveTo(X, 462); g.lineTo(X + 380 * outCubic(seg(lt, 8.6, 9.6)), 462); g.stroke();
      g.globalAlpha = seg(lt, 10.3, 11);
      g.font = "500 20px " + SANS; g.fillStyle = "#bfe6f7";
      g.fillText(J ? "ながれを創る、世界へ" : "Creating the Flow for Sustainability", X, 520);
      g.restore();
    }
    /* last breath: settle to a slightly darker frame */
    var fade = seg(lt, 13.5, 15.5);
    if (fade > 0) { g.fillStyle = "rgba(2,10,16," + fade * .35 + ")"; g.fillRect(0, 0, W, H); }
  }, { x: 640, y: 360 });

  /* draw moment t: the scene, and the next one opening through an iris */
  function frame(t) {
    g.setTransform(canvas.width / W, 0, 0, canvas.width / W, 0, 0);
    var cur = null, nxt = null;
    for (var i = 0; i < SCENES.length; i++) {
      var s = SCENES[i];
      if (t >= s.a && t < s.b) { if (!cur) cur = s; else nxt = s; }
    }
    if (!cur) cur = SCENES[SCENES.length - 1];
    cur.draw(t);
    if (nxt && nxt.iris) {
      var k = inOut(seg(t, nxt.a, cur.b));
      var R = k * 1500;
      g.save();
      g.beginPath(); g.arc(nxt.iris.x, nxt.iris.y, Math.max(R, .1), 0, 6.283); g.clip();
      nxt.draw(t);
      g.restore();
      if (k > 0 && k < 1) {
        g.save();
        g.strokeStyle = "rgba(230,250,255," + (1 - k) + ")"; g.lineWidth = 10;
        g.beginPath(); g.arc(nxt.iris.x, nxt.iris.y, R, 0, 6.283); g.stroke();
        /* a ring of bubbles riding the edge */
        var r = rng(Math.floor(nxt.a * 10));
        for (var j = 0; j < 22; j++) {
          var a = r() * 6.283, rr = R + (r() - .3) * 40;
          g.lineWidth = 2; g.strokeStyle = "rgba(230,250,255," + (.8 * (1 - k)) + ")";
          g.beginPath(); g.arc(nxt.iris.x + Math.cos(a) * rr, nxt.iris.y + Math.sin(a) * rr, 4 + r() * 10, 0, 6.283); g.stroke();
        }
        g.restore();
      }
    }
    finish(t);
    /* fade up from black at the very start */
    if (t < .8) { g.fillStyle = "rgba(3,16,26," + (1 - t / .8) + ")"; g.fillRect(0, 0, W, H); }
  }

  /* ============================================================= sound === */
  var BPM = 96, BEAT = 60 / BPM, BAR = BEAT * 4;
  function mtof(m) { return 440 * Math.pow(2, (m - 69) / 12); }
  var EVENTS = null;
  function buildEvents() {
    var E = [];
    /* everything from the 1987 scene on starts INTRO seconds later */
    function at(time, fn) { E.push({ t: time >= 4.9 ? time + INTRO : time, fn: fn }); }
    /* the extra bar under the held title: Dm7 to G, the music box still wondering */
    [[0, 77, 1, .6], [1, 76, 1, .55], [2, 74, 1.5, .55], [3.5, 79, .5, .5]].forEach(function (n) {
      E.push({ t: 5 + n[0] * BEAT, fn: function (c, w) { musicBox(c, w, n[1], n[2] * BEAT, n[3]); } });
    });
    E.push({ t: 5, fn: function (c, w) { pad(c, w, [53, 57, 60, 64], BAR / 2, .7); } });
    E.push({ t: 5 + BAR / 2, fn: function (c, w) { pad(c, w, [55, 59, 62, 65], BAR / 2, .7); } });
    function bar(n, beat) { return n * BAR + (beat || 0) * BEAT; }
    /* ---- the score: [bar, beat, note, length in beats, velocity] ---- */
    var MEL = [
      /* A title - a music box, wondering */
      [0, 0, 76, 1, .7], [0, 1, 79, 1, .6], [0, 2, 83, 1, .65], [0, 3, 84, 1, .7],
      [1, 0, 81, 1, .7], [1, 1, 79, 1, .6], [1, 2, 76, 1.5, .6], [1, 3.5, 74, .5, .5],
      /* B 1987 - a spring in its step */
      [2, 0, 77, .5, .7], [2, .5, 76, .5, .5], [2, 1, 74, .5, .55], [2, 1.5, 72, .5, .5], [2, 2, 69, 1, .6], [2, 3, 72, 1, .6],
      [3, 0, 74, .5, .7], [3, .5, 76, .5, .55], [3, 1, 77, .5, .6], [3, 1.5, 79, .5, .6], [3, 2, 81, 1, .7], [3, 3, 79, 1, .6],
      [4, 0, 84, 1, .75], [4, 1, 79, 1, .6], [4, 2, 76, .5, .6], [4, 2.5, 79, .5, .6], [4, 3, 84, 1, .7],
      /* C 1992 - hopeful, then the turn */
      [5, 0, 69, .5, .5], [5, .5, 72, .5, .5], [5, 1, 76, .5, .55], [5, 1.5, 81, .5, .6], [5, 2, 76, .5, .5], [5, 2.5, 72, .5, .5], [5, 3, 76, .5, .5], [5, 3.5, 81, .5, .55],
      [6, 0, 77, .5, .6], [6, .5, 81, .5, .6], [6, 1, 84, .5, .65], [6, 1.5, 81, .5, .55], [6, 2, 77, 1, .6], [6, 3, 72, 1, .5],
      [7, 0, 80, 1, .6], [7, 1, 79, 1, .55], [7, 2, 77, 1, .5], [7, 3, 72, 1, .45],
      /* D flow - rising */
      [10, 0, 72, 1, .6], [10, 1, 74, 1, .6], [10, 2, 76, 1, .65], [10, 3, 79, 1, .7],
      [11, 0, 79, 1, .7], [11, 1, 81, 1, .7], [11, 2, 83, 1, .75], [11, 3, 86, 1, .8],
      /* E 1998 - arrival */
      [12, 0, 84, 1.5, .85], [12, 1.5, 83, .5, .6], [12, 2, 84, 1, .7], [12, 3, 88, 1, .8],
      [13, 0, 89, 1, .8], [13, 1, 88, 1, .7], [13, 2, 84, 1, .7], [13, 3, 81, 1, .65],
      [14, 0, 83, 1, .7], [14, 1, 86, 1, .75], [14, 2, 91, 1, .8], [14, 3, 88, 1, .75],
      /* F 2002 - wide and warm */
      [15, 0, 77, 2, .6], [15, 2, 76, 2, .55], [16, 0, 79, 1.5, .6], [16, 1.5, 76, .5, .5], [16, 2, 72, 2, .55],
      [17, 0, 74, 1, .6], [17, 1, 77, 1, .6], [17, 2, 81, 1, .65], [17, 3, 79, 1, .6],
      /* G finale - the title tune, grown up */
      [19, 0, 76, 1, .7], [19, 1, 79, 1, .7], [19, 2, 83, 1, .75], [19, 3, 84, 1, .8],
      [20, 0, 88, 1, .8], [20, 1, 86, 1, .7], [20, 2, 84, 1, .7], [20, 3, 81, 1, .65],
      [21, 0, 84, 1.5, .75], [21, 1.5, 81, .5, .6], [21, 2, 77, 1, .65], [21, 3, 81, 1, .7],
      [22, 0, 84, 2, .85], [22, 2, 79, 1, .55], [22, 3, 76, 1, .5], [23, 0, 72, 3, .6]
    ];
    MEL.forEach(function (n) { at(bar(n[0], n[1]), function (c, w) { musicBox(c, w, n[2], n[3] * BEAT, n[4]); }); });
    /* chords under it: [bar, notes, bars long, kind] */
    var CH = [
      [0, [48, 55, 64, 71], 1], [1, [45, 52, 60, 67], 1],
      [2, [41, 53, 57, 60], 1], [3, [43, 55, 59, 62], 1], [4, [36, 52, 55, 60], 1],
      [5, [45, 57, 60, 64], 1], [6, [41, 57, 60, 65], 1], [7, [41, 56, 60, 65], 1],
      [8, [45, 57, 60, 64], 1], [9, [41, 57, 60, 65], 1], [10, [36, 55, 60, 64], 1], [11, [43, 55, 59, 62], 1],
      [12, [36, 55, 60, 64, 67], 1], [13, [41, 57, 60, 65], 1], [14, [43, 55, 59, 62], .5], [14.5, [45, 57, 60, 64], .5],
      [15, [41, 57, 60, 65, 69], 1], [16, [40, 55, 60, 64], 1], [17, [38, 57, 60, 65], .5], [17.5, [43, 55, 59, 62], .5],
      [18, [36, 55, 60, 64], 1], [19, [36, 55, 60, 64], 1], [20, [47, 55, 62, 67], .5], [20.5, [45, 57, 60, 64], .5],
      [21, [41, 57, 60, 65], .5], [21.5, [43, 55, 59, 62], .5], [22, [36, 55, 60, 64, 67, 72], 1.4]
    ];
    CH.forEach(function (c) {
      at(bar(c[0]), function (ctx, w) { pad(ctx, w, c[1].slice(1), c[2] * BAR, c[0] >= 18 ? 1.35 : c[0] >= 15 ? 1.15 : c[0] >= 12 ? .9 : .7); });
      if (c[0] >= 2) at(bar(c[0]), function (ctx, w) { bass(ctx, w, c[1][0], BEAT * 1.6, .8); });
      if (c[0] >= 2 && c[0] < 5 || c[0] >= 12 && c[0] < 15 || c[0] >= 18 && c[0] < 22) {
        at(bar(c[0], 2), function (ctx, w) { bass(ctx, w, c[1][0] + 7, BEAT * 1.2, .55); });
      }
    });
    /* flow scene: marimba eighths that thicken as the fish come back */
    for (var b = 8; b < 12; b++) {
      var chord = [[57, 60, 64, 69], [53, 57, 60, 65], [55, 60, 64, 67], [55, 59, 62, 67]][b - 8];
      for (var e = 0; e < 8; e++) {
        (function (b, e, chord) {
          at(bar(b, e / 2), function (c, w) { marimba(c, w, chord[e % 4] + (e >= 4 ? 12 : 0), .5 + (b - 8) * .1); });
        })(b, e, chord);
      }
      (function (b) { at(bar(b), function (c, w) { bass(c, w, [45, 41, 36, 43][b - 8], BEAT * .8, .8); }); })(b);
      (function (b) { at(bar(b, 2), function (c, w) { bass(c, w, [45, 41, 36, 43][b - 8], BEAT * .8, .6); }); })(b);
    }
    /* a harp-like run into 1998 and one at the very end */
    [[29.3, 55], [54.0, 55]].forEach(function (r) {
      for (var i = 0; i < 12; i++) (function (i) {
        at(r[0] + i * .055, function (c, w) { musicBox(c, w, r[1] + [12, 16, 19, 24, 28, 31, 36, 40, 43, 48, 52, 55][i], .6, .3); });
      })(i);
    });

    /* ---- sound effects, placed on the picture ---- */
    at(.7, function (c, w) { shimmer(c, w, 2.4, .25); });
    at(2.25, function (c, w) { sparkle(c, w, 3, .5); });
    at(3.2, function (c, w) { plip(c, w, .6); });
    /* 1987 */
    at(5.1, function (c, w) { crickets(c, w, 7.2, .12); });
    at(6.1, function (c, w) { pop(c, w, .7); });
    at(6.6, function (c, w) { bubble(c, w, 500, .5); });
    at(7.0, function (c, w) { bubble(c, w, 620, .5); });
    at(7.4, function (c, w) { bubble(c, w, 760, .5); });
    at(8.0, function (c, w) { ding(c, w, .6); sparkle(c, w, 4, .4); });
    at(12.2, function (c, w) { whoosh(c, w, .8, .35, true); });
    /* 1992: eggs appear, hatch, and most drift away */
    for (var i = 0; i < 16; i++) (function (i) {
      at(12.6 + i * .09, function (c, w) { musicBox(c, w, [84, 86, 88, 91, 93, 96][i % 6] - 12, .3, .1); });
      at(14.7 + i * .085, function (c, w) { bubble(c, w, mtof([72, 76, 79, 84, 88][i % 5]) / 2, .09); });
    })(i);
    at(16.8, function (c, w) { shimmer(c, w, 3.2, .12, true); });
    [96, 92, 89, 84, 80, 77].forEach(function (m, i) {
      at(17.1 + i * .38, function (c, w) { musicBox(c, w, m, .8, .22 - i * .02); });
    });
    /* the flow: clank, ratchet, whoosh, gauges settle, the counter climbs */
    at(20.2, function (c, w) { clunk(c, w, .8); });
    at(21.0, function (c, w) { clunk(c, w, .45); });
    at(21.8, function (c, w) { clunk(c, w, .35); });
    at(20.9, function (c, w) { rush(c, w, 2.4, 1.1); });
    for (i = 0; i < 6; i++) (function (i) { at(21.0 + i * .3, function (c, w) { musicBox(c, w, [72, 76, 79, 84, 88, 91][i], .5, .35); }); })(i);
    at(21.4, function (c, w) { stream(c, w, 8.3, .18); });
    for (i = 0; i < 9; i++) (function (i) { at(22 + i * .85, function (c, w) { bubble(c, w, mtof([60, 64, 67, 72, 67, 64, 72, 76, 72][i]), .1); }); })(i);
    [21.0, 21.35, 21.7].forEach(function (x, i) { at(x, function (c, w) { bubble(c, w, mtof([72, 76, 79][i]) / 2, .35); }); });
    [22.9, 23.3, 23.7].forEach(function (x, i) { at(x + .7, function (c, w) { ding(c, w, .35, 88 + i * 3); }); });
    for (i = 0; i < 5; i++) (function (i) { at(24.4 + i * .12, function (c, w) { bubble(c, w, mtof([76, 79, 81, 84, 88][i]) / 2, .3); sparkle(c, w, 1, .2); }); })(i);
    var PENTA = [60, 62, 64, 67, 69, 72, 74, 76, 79, 81, 84];
    for (i = 0; i < 11; i++) (function (i) { at(25.7 + i * .2, function (c, w) { musicBox(c, w, PENTA[i], .4, .26); }); })(i);
    at(27.9, function (c, w) { ding(c, w, .55, 84); sparkle(c, w, 5, .4); });
    /* 1998 */
    at(30.0, function (c, w) { whoosh(c, w, 1.3, .5); });
    [31.5, 32.05, 32.6].forEach(function (x, i) { at(x, function (c, w) { bubble(c, w, mtof([79, 84, 88][i]) / 2, .45); sparkle(c, w, 2, .3); }); });
    at(33.6, function (c, w) { bells(c, w, [72, 79, 84, 88], .5); sparkle(c, w, 8, .5); });
    at(34.1, function (c, w) { stampHit(c, w, .9); });
    /* 2002 */
    at(37.4, function (c, w) { whoosh(c, w, 1.0, .35, true); });
    at(37.8, function (c, w) { stream(c, w, 7, .12); });
    at(38.3, function (c, w) { stampHit(c, w, .9); });
    for (i = 0; i < 11; i++) (function (i) { at(41.55 + i * .14, function (c, w) { musicBox(c, w, PENTA[i], .4, .26); }); })(i);
    at(43.1, function (c, w) { ding(c, w, .55, 84); sparkle(c, w, 5, .35); });

    /* 2027 */
    at(45.1, function (c, w) { shimmer(c, w, 2.2, .3); });
    at(46.9, function (c, w) { sparkle(c, w, 3, .45); });
    at(47.3, function (c, w) { crack(c, w, .45); });
    at(47.65, function (c, w) { crack(c, w, .5); });
    at(47.9, function (c, w) { crack(c, w, .55); });
    at(47.4, function (c, w) { riser(c, w, .7, .35); });
    at(48.1, function (c, w) { thump(c, w, 1); pop(c, w, .7, 900); sparkle(c, w, 10, .55); bells(c, w, [84, 88, 91, 96], .5); shimmer(c, w, 1.6, .3); });
    at(49.1, function (c, w) { pop(c, w, .45, 1400); });
    at(53.2, function (c, w) { sparkle(c, w, 4, .4); });
    at(55.0, function (c, w) { bells(c, w, [60, 67, 72, 76, 79, 84], .55); bass(c, w, 36, BEAT * 4, .9); });
    at(55.4, function (c, w) { shimmer(c, w, 2.4, .22); });
    E.push({ t: END - 2.5, fn: function (c, w) { out.hum.gain.setTargetAtTime(0, w, .7); } });
    E.sort(function (a, b) { return a.t - b.t; });
    return E;
  }

  /* ---- the instruments, all synthesised ---- */
  var ac = null, out = null, verb = null, noiseBuf = null;
  function tone(c, dest, type, f, w, a, d, peak, ramp) {
    var o = c.createOscillator(), gn = c.createGain();
    o.type = type; o.frequency.setValueAtTime(f, w);
    if (ramp) o.frequency.exponentialRampToValueAtTime(ramp[0], w + ramp[1]);
    gn.gain.setValueAtTime(0, w);
    gn.gain.linearRampToValueAtTime(peak, w + a);
    gn.gain.exponentialRampToValueAtTime(.0001, w + a + d);
    o.connect(gn); gn.connect(dest);
    o.start(w); o.stop(w + a + d + .05);
    return gn;
  }
  function noise(c, dest, w, dur, peak, filt, f0, f1, q, a) {
    var s = c.createBufferSource(); s.buffer = noiseBuf;
    var f = c.createBiquadFilter(); f.type = filt; f.frequency.setValueAtTime(f0, w);
    if (f1) f.frequency.exponentialRampToValueAtTime(f1, w + dur);
    f.Q.value = q || 1;
    var gn = c.createGain();
    gn.gain.setValueAtTime(0, w);
    gn.gain.linearRampToValueAtTime(peak, w + (a == null ? dur * .3 : a));
    gn.gain.exponentialRampToValueAtTime(.0001, w + dur);
    s.connect(f); f.connect(gn); gn.connect(dest);
    s.start(w, Math.random() * 1.5); s.stop(w + dur + .05);
    return gn;
  }
  function send(node, amt) { var s = ac.createGain(); s.gain.value = amt; node.connect(s); s.connect(verb); }
  function musicBox(c, w, m, len, v) {
    var f = mtof(m), d = clamp(2.4 - (m - 60) * .03, .9, 2.4);
    var a = tone(c, out.music, "sine", f, w, .004, d, .20 * v);
    var b = tone(c, out.music, "sine", f * 2, w, .003, d * .45, .05 * v);
    var h = tone(c, out.music, "sine", f * 4, w, .002, .1, .018 * v);
    send(a, .5); send(b, .5); send(h, .3);
  }
  function marimba(c, w, m, v) {
    var f = mtof(m);
    var a = tone(c, out.music, "sine", f, w, .003, .38, .14 * v);
    var b = tone(c, out.music, "sine", f * 4, w, .002, .07, .05 * v);
    send(a, .25); send(b, .15);
  }
  function bass(c, w, m, len, v) {
    var f = mtof(m), o = c.createOscillator(), lp = c.createBiquadFilter(), gn = c.createGain();
    o.type = "triangle"; o.frequency.value = f;
    lp.type = "lowpass"; lp.frequency.setValueAtTime(1400, w); lp.frequency.exponentialRampToValueAtTime(300, w + .25);
    gn.gain.setValueAtTime(0, w); gn.gain.linearRampToValueAtTime(.26 * v, w + .008);
    gn.gain.exponentialRampToValueAtTime(.0001, w + len + .3);
    o.connect(lp); lp.connect(gn); gn.connect(out.music);
    o.start(w); o.stop(w + len + .4);
    send(gn, .12);
  }
  function pad(c, w, notes, len, v) {
    notes.forEach(function (m) {
      /* soft and airy, like far-off strings: detuned triangles, darkened */
      [-3, 3].forEach(function (cents) {
        var o = c.createOscillator(), lp = c.createBiquadFilter(), gn = c.createGain();
        o.type = "triangle"; o.frequency.value = mtof(m); o.detune.value = cents;
        lp.type = "lowpass"; lp.frequency.value = 700; lp.Q.value = .2;
        gn.gain.setValueAtTime(0, w);
        gn.gain.linearRampToValueAtTime(.02 * v, w + Math.min(1.1, len * .45));
        gn.gain.setValueAtTime(.02 * v, w + len - .1);
        gn.gain.exponentialRampToValueAtTime(.0001, w + len + 1.2);
        o.connect(lp); lp.connect(gn); gn.connect(out.music);
        o.start(w); o.stop(w + len + 1.3);
        send(gn, .6);
      });
    });
  }
  function bubble(c, w, f, v) {
    var a = tone(c, out.sfx, "sine", f, w, .004, .11, .22 * v, [f * 2.6, .09]);
    send(a, .25);
  }
  function plip(c, w, v) {
    bubble(c, w, 380, v);
    var a = tone(c, out.sfx, "sine", 1400, w + .05, .003, .22, .12 * v, [700, .2]);
    send(a, .5);
  }
  function pop(c, w, v, f) {
    noise(c, out.sfx, w, .07, .35 * v, "bandpass", f || 1300, null, 1.2, .004);
    bubble(c, w + .01, (f || 1300) * .35, v);
  }
  function sparkle(c, w, n, v) {
    var notes = [84, 86, 88, 91, 93, 96];
    for (var i = 0; i < n; i++) {
      var a = tone(c, out.sfx, "sine", mtof(notes[Math.floor(Math.random() * notes.length)]), w + i * .05, .003, .5, .045 * v);
      send(a, .9);
    }
  }
  function shimmer(c, w, dur, v, down) {
    var notes = [72, 76, 79, 84, 88, 91, 96, 100];
    if (down) notes.reverse();
    var step = dur / notes.length / 2;
    for (var i = 0; i < notes.length * 2; i++) {
      var a = tone(c, out.sfx, "sine", mtof(notes[i % notes.length]), w + i * step, .01, .6, .035 * v * (1 - i / (notes.length * 2)));
      send(a, 1);
    }
  }
  function windDown(c, w, dur, v) {
    var a = tone(c, out.music, "sine", 523, w, .5, dur, .04 * v, [330, dur]);
    send(a, .8);
  }
  function ding(c, w, v, m) {
    var f = mtof(m || 91);
    var a = tone(c, out.sfx, "sine", f, w, .002, 1.4, .16 * v);
    var b = tone(c, out.sfx, "sine", f * 2, w, .002, .6, .04 * v);
    send(a, .6); send(b, .5);
  }
  function gong(c, w, v) {
    [60, 64, 67, 72, 76, 79, 84].forEach(function (m, i) {
      var a = tone(c, out.sfx, "sine", mtof(m), w + i * .012, .01, 2.6, .07 * v);
      send(a, .9);
    });
    noise(c, out.sfx, w, 1.4, .08 * v, "highpass", 5000, null, .7, .01);
  }
  function clank(c, w, v) {
    [523, 1307, 2211, 3121].forEach(function (f, i) {
      var a = tone(c, out.sfx, "sine", f, w, .001, .35 - i * .06, .12 * v / (i + 1));
      send(a, .4);
    });
    noise(c, out.sfx, w, .08, .3 * v, "lowpass", 2500, null, 1, .002);
  }
  function ratchet(c, w, dur, v) {
    for (var x = 0; x < dur; x += .055 + x * .012) noise(c, out.sfx, w + x, .03, .25 * v, "highpass", 3000, null, 3, .002);
  }
  function stream(c, w, dur, v) {
    var gn = noise(c, out.sfx, w, dur, .22 * v, "lowpass", 380, 520, .3, 1.8);
    send(gn, .2);
  }
  function whoosh(c, w, dur, v, down) {
    var gn = noise(c, out.sfx, w, dur, .6 * v, "bandpass", down ? 2600 : 300, down ? 300 : 2600, .9, dur * .55);
    send(gn, .4);
  }
  function bells(c, w, notes, v) {
    notes.forEach(function (m, i) {
      var f = mtof(m), t = w + i * .045;
      var a = tone(c, out.sfx, "sine", f, t, .002, 2.4, .12 * v);
      var b = tone(c, out.sfx, "sine", f * 2, t, .002, .9, .035 * v);
      var h = tone(c, out.sfx, "sine", f * 3, t, .001, .3, .015 * v);
      send(a, .8); send(b, .6); send(h, .5);
    });
  }
  /* a precise little latch: one clean metallic click */
  function click(c, w, v) {
    noise(c, out.sfx, w, .025, .35 * v, "bandpass", 3200, null, 6, .001);
    var a = tone(c, out.sfx, "sine", 1760, w, .001, .12, .08 * v);
    var b = tone(c, out.sfx, "sine", 2637, w, .001, .08, .05 * v);
    send(a, .4); send(b, .3);
  }
  /* water opening up: a smooth airy swell, no grit */
  function rush(c, w, dur, v) {
    var gn = noise(c, out.sfx, w, dur, .2 * v, "lowpass", 300, 900, .3, dur * .6);
    send(gn, .4);
  }
  /* the valve seating: a solid, well-oiled metal clunk - precise, not grinding */
  function clunk(c, w, v) {
    tone(c, out.sfx, "sine", 150, w, .003, .18, .6 * v, [90, .15]);
    var a = tone(c, out.sfx, "sine", 740, w, .001, .22, .12 * v);
    var b = tone(c, out.sfx, "sine", 1110, w, .001, .14, .07 * v);
    noise(c, out.sfx, w, .05, .35 * v, "bandpass", 2400, null, 2, .001);
    send(a, .35); send(b, .3);
  }
  /* a stamp landing */
  function stampHit(c, w, v) {
    thump(c, w, v);
    noise(c, out.sfx, w, .12, .45 * v, "lowpass", 1600, 500, .8, .002);
  }
  function tick(c, w, f, v) { tone(c, out.sfx, "sine", f, w, .001, .035, .2 * v); }
  function thump(c, w, v) {
    tone(c, out.sfx, "sine", 120, w, .004, .32, .9 * v, [48, .25]);
    noise(c, out.sfx, w, .09, .25 * v, "lowpass", 900, null, .7, .003);
  }
  function crack(c, w, v) {
    noise(c, out.sfx, w, .05, .5 * v, "highpass", 2500, null, 2, .001);
    noise(c, out.sfx, w + .03, .04, .3 * v, "bandpass", 4200, null, 4, .001);
  }
  function riser(c, w, dur, v) {
    var gn = noise(c, out.sfx, w, dur, .35 * v, "bandpass", 400, 5000, 2, dur * .9);
    send(gn, .4);
    tone(c, out.sfx, "sine", 300, w, dur * .9, .1, .06 * v, [1200, dur]);
  }
  function boing(c, w, v) {
    var o = c.createOscillator(), gn = c.createGain(), lfo = c.createOscillator(), lg = c.createGain();
    o.type = "sine"; o.frequency.setValueAtTime(260, w); o.frequency.exponentialRampToValueAtTime(520, w + .25);
    lfo.frequency.value = 22; lg.gain.value = 30; lfo.connect(lg); lg.connect(o.frequency);
    gn.gain.setValueAtTime(0, w); gn.gain.linearRampToValueAtTime(.18 * v, w + .01);
    gn.gain.exponentialRampToValueAtTime(.0001, w + .5);
    o.connect(gn); gn.connect(out.sfx);
    o.start(w); lfo.start(w); o.stop(w + .55); lfo.stop(w + .55);
  }
  function crickets(c, w, dur, v) {
    for (var x = 0; x < dur; x += .7 + (x * 13 % 1) * .5) {
      for (var k = 0; k < 3; k++) tone(c, out.sfx, "sine", 4300 + (x * 97 % 300), w + x + k * .06, .005, .04, .05 * v);
    }
  }

  /* ---- the engine: water hum underneath, events scheduled just ahead ---- */
  function makeAudio() {
    var C = window.AudioContext || window.webkitAudioContext;
    if (!C) return null;
    try { if (navigator.audioSession) navigator.audioSession.type = "playback"; } catch (e) {}
    var c = new C();
    var len = c.sampleRate * 2;
    noiseBuf = c.createBuffer(1, len, c.sampleRate);
    var d = noiseBuf.getChannelData(0);
    for (var i = 0; i < len; i++) d[i] = Math.random() * 2 - 1;
    return c;
  }
  function makeBus() {
    /* level: the synths are gentle, so lift them to where web video sits,
       even out with a compressor and catch the peaks with a limiter */
    var master = ac.createGain(); master.gain.value = muted ? 0 : 1;
    var lift = ac.createGain(); lift.gain.value = 2.6;
    var comp = ac.createDynamicsCompressor();
    comp.threshold.value = -20; comp.knee.value = 8; comp.ratio.value = 3.5; comp.attack.value = .008; comp.release.value = .25;
    var lim = ac.createDynamicsCompressor();
    lim.threshold.value = -2; lim.knee.value = 0; lim.ratio.value = 20; lim.attack.value = .001; lim.release.value = .08;
    master.connect(lift); lift.connect(comp); comp.connect(lim); lim.connect(ac.destination);
    var music = ac.createGain(); music.gain.value = .75; music.connect(master);
    var sfx = ac.createGain(); sfx.gain.value = .9; sfx.connect(master);
    /* a small room: decaying stereo noise as the impulse */
    var cv = ac.createConvolver(), n = ac.sampleRate * 2.6, ir = ac.createBuffer(2, n, ac.sampleRate);
    for (var ch = 0; ch < 2; ch++) {
      var x = ir.getChannelData(ch);
      for (var i = 0; i < n; i++) x[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / n, 3.2);
    }
    cv.buffer = ir;
    var vg = ac.createGain(); vg.gain.value = .32;
    cv.connect(vg); vg.connect(master);
    verb = cv;
    /* the hum of water */
    var s = ac.createBufferSource(); s.buffer = noiseBuf; s.loop = true;
    var lp = ac.createBiquadFilter(); lp.type = "bandpass"; lp.frequency.value = 260; lp.Q.value = .6;
    var hum = ac.createGain(); hum.gain.value = 0;
    hum.gain.setValueAtTime(0, ac.currentTime);
    hum.gain.linearRampToValueAtTime(.045, ac.currentTime + 2);
    s.connect(lp); lp.connect(hum); hum.connect(master);
    s.start();
    return { master: master, music: music, sfx: sfx, hum: hum, humSrc: s };
  }

  /* ============================================================ player === */
  var state = "idle", t0 = 0, clock0 = 0, pausedAt = 0, nextEv = 0, raf = 0, muted = false;
  var playBtn = host.querySelector(".efPlay"), bar = host.querySelector(".efBar i");
  var ctrlPause = host.querySelector("[data-ef=pause]"), ctrlMute = host.querySelector("[data-ef=mute]");
  var ctrlFull = host.querySelector("[data-ef=full]");

  function now() { return ac ? ac.currentTime : performance.now() / 1000; }
  function time() { return state === "playing" ? now() - clock0 : pausedAt; }

  function size() {
    var r = host.getBoundingClientRect();
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var w = Math.round(Math.min(r.width * dpr, 2560));
    if (w && canvas.width !== w) { canvas.width = w; canvas.height = Math.round(w * 9 / 16); }
  }
  function poster() {
    size();
    frame(POSTER);
  }
  function schedule() {
    if (!ac || !out) return;
    var t = time(), ahead = t + .35;
    while (nextEv < EVENTS.length && EVENTS[nextEv].t <= ahead) {
      var e = EVENTS[nextEv++];
      if (e.t >= t - .05) e.fn(ac, clock0 + e.t);
    }
  }
  function loop() {
    raf = 0;
    if (state !== "playing") return;
    var t = time();
    if (t >= END) { end(); return; }
    schedule();
    size();
    frame(t);
    if (bar) bar.style.transform = "scaleX(" + (t / END) + ")";
    raf = requestAnimationFrame(loop);
  }
  function start() {
    if (!ac) ac = makeAudio();
    if (ac && ac.state === "suspended") ac.resume();
    if (!EVENTS) EVENTS = buildEvents();
    if (out && ac) {
      /* a replay: let the old bus ring out and silence it */
      var old = out; old.master.gain.setTargetAtTime(0, ac.currentTime, .05);
      setTimeout(function () { try { old.humSrc.stop(); old.master.disconnect(); } catch (e) {} }, 400);
    }
    out = ac ? makeBus() : null;
    nextEv = 0;
    clock0 = now() + .08;
    state = "playing";
    host.classList.add("playing"); host.classList.remove("ended", "paused");
    if (!raf) raf = requestAnimationFrame(loop);
  }
  function pause() {
    if (state !== "playing") return;
    pausedAt = time(); state = "paused";
    if (ac) ac.suspend();
    host.classList.add("paused");
  }
  function resume() {
    if (state !== "paused") return;
    var p = ac ? ac.resume() : Promise.resolve();
    p.then(function () {
      clock0 = now() - pausedAt; state = "playing";
      host.classList.remove("paused");
      if (!raf) raf = requestAnimationFrame(loop);
    });
  }
  function end() {
    state = "ended"; pausedAt = END - .01;
    frame(END - .01);
    host.classList.add("ended"); host.classList.remove("playing");
    if (out) out.hum.gain.setTargetAtTime(0, ac.currentTime, .6);
  }

  playBtn.addEventListener("click", function () {
    host.classList.add("loading");
    loadArt().then(function () { host.classList.remove("loading"); start(); });
  });
  canvas.addEventListener("click", function () {
    if (state === "playing") pause(); else if (state === "paused") resume();
  });
  ctrlPause.addEventListener("click", function () {
    if (state === "playing") pause(); else if (state === "paused") resume(); else start();
  });
  ctrlMute.addEventListener("click", function () {
    muted = !muted;
    host.classList.toggle("muted", muted);
    if (out) out.master.gain.setTargetAtTime(muted ? 0 : 1, ac.currentTime, .03);
  });
  var fsEl = host.requestFullscreen ? "requestFullscreen" : host.webkitRequestFullscreen ? "webkitRequestFullscreen" : null;
  if (!fsEl) ctrlFull.hidden = true;
  ctrlFull.addEventListener("click", function () {
    var inFs = document.fullscreenElement || document.webkitFullscreenElement;
    if (inFs) (document.exitFullscreen || document.webkitExitFullscreen).call(document);
    else host[fsEl]();
  });
  window.addEventListener("resize", function () { if (state !== "playing" && IMG.bgTitle) { size(); frame(time() || POSTER); } });
  document.addEventListener("fullscreenchange", function () { setTimeout(function () { size(); if (state !== "playing") frame(time() || POSTER); }, 60); });

  /* the language button redraws a still frame in the other language */
  var lb = document.getElementById("langBtn");
  if (lb) lb.addEventListener("click", function () { setTimeout(function () { if (state !== "playing" && IMG.bgTitle) frame(state === "idle" ? POSTER : time()); }, 0); });

  /* stop when scrolled away; load the art only as the film comes near */
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) { loadArt().then(function () { if (state === "idle") poster(); }); }
        else if (state === "playing") pause();
      });
    }, { rootMargin: "600px 0px" }).observe(host);
  } else loadArt().then(poster);
  document.addEventListener("visibilitychange", function () { if (document.hidden) pause(); });

  /* for checking: window.__eggFilm.frame(t) draws any moment, and renderAudio()
     plays the whole soundtrack offline into a WAV (base64) - tools/egg_film_video.py */
  function renderAudio() {
    var rate = 44100, keep = [ac, out, verb];
    var off = new OfflineAudioContext(2, Math.ceil(rate * (END + .5)), rate);
    ac = off;
    noiseBuf = off.createBuffer(1, rate * 2, rate);
    var d = noiseBuf.getChannelData(0);
    for (var i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
    muted = false;
    out = makeBus();
    if (!EVENTS) EVENTS = buildEvents();
    EVENTS.forEach(function (e) { e.fn(off, e.t + .08); });
    out.hum.gain.setTargetAtTime(0, END - 2.5, .7);
    ac = keep[0]; out = keep[1]; verb = keep[2];
    return off.startRendering().then(function (buf) {
      var n = buf.length, L = buf.getChannelData(0), R = buf.getChannelData(1);
      var view = new DataView(new ArrayBuffer(44 + n * 4));
      function str(o, s) { for (var k = 0; k < s.length; k++) view.setUint8(o + k, s.charCodeAt(k)); }
      str(0, "RIFF"); view.setUint32(4, 36 + n * 4, true); str(8, "WAVEfmt ");
      view.setUint32(16, 16, true); view.setUint16(20, 1, true); view.setUint16(22, 2, true);
      view.setUint32(24, rate, true); view.setUint32(28, rate * 4, true);
      view.setUint16(32, 4, true); view.setUint16(34, 16, true); str(36, "data"); view.setUint32(40, n * 4, true);
      for (var j = 0, o = 44; j < n; j++, o += 4) {
        view.setInt16(o, clamp(L[j], -1, 1) * 32767, true);
        view.setInt16(o + 2, clamp(R[j], -1, 1) * 32767, true);
      }
      var bytes = new Uint8Array(view.buffer), s = "";
      for (var b = 0; b < bytes.length; b += 32768) s += String.fromCharCode.apply(null, bytes.subarray(b, b + 32768));
      return btoa(s);
    });
  }
  window.__eggFilm = { frame: function (t) { size(); frame(t); }, END: END, ready: loadArt, renderAudio: renderAudio };
})();
