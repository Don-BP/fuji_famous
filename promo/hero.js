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

  /* --- tall, narrow screens keep the hero they already have.
         Must stay in step with the media query in hub.css. --- */
  var FITS = "(min-width:700px) and (min-aspect-ratio:11/10)";
  if (!window.matchMedia(FITS).matches) return;

  var reduce  = window.matchMedia("(prefers-reduced-motion:reduce)").matches;

  /* --- a slow connection or a data-saver gets the still, never 73 files --- */
  var conn    = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
  var thrifty = !!(conn && (conn.saveData ||
                   /^(slow-2g|2g|3g)$/.test(conn.effectiveType || "")));

  if (reduce || thrifty) { still(); return; }

  /* ---------------- which size ---------------- */
  var big = window.matchMedia("(min-width:1100px)").matches ||
            (window.devicePixelRatio || 1) > 1.5;
  var dir = BASE + (big ? "w1280/" : "w720/");

  /* ---------------- load ---------------- */
  var frames  = new Array(COUNT);
  var ready   = 0;
  var loaded  = false;
  var failed  = false;

  function pad(n) { return ("00" + n).slice(-3); }

  function load() {
    for (var i = 0; i < COUNT; i++) {
      (function (i) {
        var im = new Image();
        im.decoding = "async";
        im.onload  = function () { frames[i] = im; if (++ready === 1) { start(); } if (ready === COUNT) loaded = true; };
        im.onerror = function () { if (!failed && ready === 0) { failed = true; still(); } };
        im.src = dir + "f_" + pad(i + 1) + ".webp";
      })(i);
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

  function start() {
    document.documentElement.classList.add("filmOn");
    root.classList.add("isLive");
    resize();
    addEventListener("scroll", onScroll, { passive: true });
    addEventListener("resize", debounce(resize, 120));
    addEventListener("orientationchange", debounce(resize, 200));
  }

  function debounce(fn, ms) {
    var t;
    return function () { clearTimeout(t); t = setTimeout(fn, ms); };
  }

  load();
})();
