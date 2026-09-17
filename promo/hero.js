/* ============================================================
   hero.js - the scroll-driven hero film.

   A fixed canvas sits behind the whole page. The hero and the
   dark "work" band are translucent, so it shows through them.
   Every opaque band below (washi, cream, footer) simply covers
   it, so the film ends exactly at the dark-to-white edge with
   no fade to manage.

   The film is 73 stills, not a <video>: seeking a video on
   scroll is unreliable on Safari and stutters on touch. Stills
   drawn to a canvas are exact and reversible.

   There are two films of the same 73 moments: a wide one shot
   for landscape screens, and an upright one shot for phones.
   Cropping the wide frame down to a phone would leave a sliver,
   so the upright pass exists to be shown whole.
   ============================================================ */
(function () {
  "use strict";

  var COUNT   = 73;
  var BASE    = "assets/film/";   // poster.jpg here is the CSS fallback

  var root    = document.getElementById("heroFilm");
  if (!root) return;

  var canvas  = document.getElementById("heroFilmC");
  var ctx     = canvas.getContext("2d", { alpha: false });
  var stop    = document.querySelector(".band:not(.dark)");   // first white band
  if (!stop) return;

  /* --- which of the two films this screen gets.
         Must stay in step with the media queries in hub.css. --- */
  var WIDE = "(min-width:700px) and (min-aspect-ratio:11/10)";
  var TALL = "(max-aspect-ratio:9/10)";

  function whichFilm() {
    var retina = (window.devicePixelRatio || 1) > 1.5;
    if (window.matchMedia(WIDE).matches) {
      /* A phone turned on its side lands here too, and it has already paid
         for the upright film once. Size the wide film by how wide the
         window actually is rather than by pixel density, so a rotated
         phone fetches the small pass and a real desktop still gets the
         large one. The widest phone in landscape is under 1000. */
      return BASE + (window.matchMedia("(min-width:1000px)").matches
                     ? "w1280/" : "w720/");
    }
    if (window.matchMedia(TALL).matches) {
      return BASE + (retina ? "m720/" : "m480/");
    }
    /* anything in between - a short landscape phone, a narrow desktop
       window - is a bad fit for either film, and the CSS hides the canvas
       there anyway, so the hero keeps the water it was painted with */
    return null;
  }

  if (!whichFilm()) return;

  var reduce  = window.matchMedia("(prefers-reduced-motion:reduce)").matches;

  /* --- a slow connection or a data-saver gets the still, never 73 files --- */
  var conn    = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
  var thrifty = !!(conn && (conn.saveData ||
                   /^(slow-2g|2g|3g)$/.test(conn.effectiveType || "")));

  if (reduce || thrifty) { still(); return; }

  /* ---------------- load ---------------- */
  var dir     = null;
  var frames  = new Array(COUNT);
  var ready   = 0;
  var loaded  = false;
  var failed  = false;

  function pad(n) { return ("00" + n).slice(-3); }

  function load() {
    var want = whichFilm();
    if (!want || want === dir) return;    // already showing the right one

    /* a phone turned on its side is a different film, not the same one
       cropped: throw the frames away and fetch the other pass. The old
       ones stay on screen until the first new frame lands. */
    dir = want;
    frames = new Array(COUNT);
    ready = 0;
    loaded = false;
    shown = -1;

    for (var i = 0; i < COUNT; i++) {
      (function (i, mine) {
        var im = new Image();
        im.decoding = "async";
        im.onload  = function () {
          if (dir !== mine) return;       // a rotation overtook this frame
          frames[i] = im;
          if (++ready === 1) { start(); }
          if (ready === COUNT) loaded = true;
          draw(true);
        };
        im.onerror = function () { if (!failed && ready === 0) { failed = true; still(); } };
        im.src = mine + "f_" + pad(i + 1) + ".webp";
      })(i, dir);
    }
  }

  /* ---------------- the still fallback ---------------- */
  function still() {
    root.classList.add("isStill");     // the poster is already the CSS background
    document.documentElement.classList.add("filmOn");
  }

  /* ---------------- sizing ---------------- */
  var dpr = 1, cw = 0, ch = 0;

  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    cw  = root.clientWidth;
    ch  = root.clientHeight;
    canvas.width  = Math.round(cw * dpr);
    canvas.height = Math.round(ch * dpr);
    canvas.style.width  = cw + "px";
    canvas.style.height = ch + "px";
    draw(true);
  }

  /* ---------------- progress ---------------- */
  function progress() {
    // 0 at the very top of the page, 1 when the white band reaches the
    // top of the viewport - the moment the film is fully covered.
    var end = stop.getBoundingClientRect().top + window.scrollY - window.innerHeight * 0.35;
    if (end <= 1) return 0;
    var p = window.scrollY / end;
    return p < 0 ? 0 : p > 1 ? 1 : p;
  }

  /* ---------------- draw ---------------- */
  var shown = -1;

  function draw(force) {
    var idx = Math.round(progress() * (COUNT - 1));
    if (idx === shown && !force) return;

    var im = frames[idx];
    if (!im) {                       // not downloaded yet - hold the nearest one we have
      for (var d = 1; d < COUNT && !im; d++) {
        im = frames[idx - d] || frames[idx + d];
      }
      if (!im) return;
    }
    shown = loaded ? idx : -1;       // redraw once the real frame lands

    var iw = im.naturalWidth, ih = im.naturalHeight;
    var s  = Math.max((cw * dpr) / iw, (ch * dpr) / ih);   // cover
    var w  = iw * s, h = ih * s;
    var x  = ((cw * dpr) - w) / 2;
    var y  = ((ch * dpr) - h) * 0.42;                      // bias up: keeps the fish off the copy

    ctx.fillStyle = "#04121a";
    ctx.fillRect(0, 0, cw * dpr, ch * dpr);
    ctx.drawImage(im, x, y, w, h);
    root.classList.add("hasFrame");
  }

  /* ---------------- run ---------------- */
  var queued = false;

  function onScroll() {
    if (queued) return;
    queued = true;
    requestAnimationFrame(function () { queued = false; draw(false); });
  }

  var running = false;

  function start() {
    document.documentElement.classList.add("filmOn");
    root.classList.add("isLive");
    resize();
    if (running) return;              // a rotation reloads frames, not listeners
    running = true;
    addEventListener("scroll", onScroll, { passive: true });
    addEventListener("resize", debounce(refit, 120));
    addEventListener("orientationchange", debounce(refit, 200));
  }

  /* the window changed shape: the canvas has to be remeasured, and the
     shape may have crossed from one film to the other */
  function refit() {
    resize();
    load();
  }

  function debounce(fn, ms) {
    var t;
    return function () { clearTimeout(t); t = setTimeout(fn, ms); };
  }

  load();
})();
