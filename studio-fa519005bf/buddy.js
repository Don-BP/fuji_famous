/* ============================================================
   Chibi Fujie swims around the page.

   Three moods, picked at random, each held for 4 to 8 seconds:
     follow  - swims toward the cursor and hovers near it
     avoid   - bolts away from the cursor
     wander  - ignores the cursor and drifts along its own path

   Movement is steering, not teleporting: it accelerates toward a
   target and coasts, so it always reads as swimming.
   ============================================================ */
(function () {
  "use strict";

  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  var el = document.getElementById("buddy");
  if (!el) return;
  var art = el.querySelector("img");

  var MOODS = ["follow", "avoid", "wander"];
  var MIN_MS = 4000, MAX_MS = 8000;      // how long a mood is held
  var EDGE = 26;                          // keep clear of the window edges
  var TOP = 74;                           // keep clear of the fixed nav bar

  var W = innerWidth, H = innerHeight;
  var size = el.offsetWidth || 110;
  var x = W * 0.74, y = H * 0.68;         // starts where the hero art sits
  var vx = 0, vy = 0;
  var tx = x, ty = y;
  var face = -1, tilt = 0;

  var pointer = { x: W / 2, y: H / 2, seen: false };
  var fine = matchMedia("(pointer: fine)").matches;

  var mood = "wander", moodUntil = 0, nextWander = 0;

  function rand(a, b) { return a + Math.random() * (b - a); }
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }

  function measure() {
    W = innerWidth; H = innerHeight;
    size = el.offsetWidth || size;
  }

  function wanderTarget(now) {
    tx = rand(EDGE + size / 2, W - EDGE - size / 2);
    ty = rand(TOP + size / 2, H - EDGE - size / 2);
    nextWander = now + rand(1400, 2600);
  }

  function newMood(now) {
    var pool = MOODS.filter(function (m) { return m !== mood; });
    // with no real cursor there is nothing to follow or flee
    if (!fine || !pointer.seen) pool = ["wander"];
    mood = pool[Math.floor(Math.random() * pool.length)];
    moodUntil = now + rand(MIN_MS, MAX_MS);
    if (mood === "wander") wanderTarget(now);
  }

  addEventListener("pointermove", function (e) {
    pointer.x = e.clientX;
    pointer.y = e.clientY;
    pointer.seen = true;
  }, { passive: true });
  addEventListener("resize", measure, { passive: true });

  function step(now) {
    if (now > moodUntil) newMood(now);

    if (mood === "follow") {
      // hang just off the cursor rather than sitting on top of it
      var a = Math.atan2(y - pointer.y, x - pointer.x);
      tx = pointer.x + Math.cos(a) * 72;
      ty = pointer.y + Math.sin(a) * 72;
    } else if (mood === "avoid") {
      var dx = x - pointer.x, dy = y - pointer.y;
      var d = Math.hypot(dx, dy) || 1;
      if (d > Math.max(W, H) * 0.55) {
        // already far away - drift instead of pinning to a corner
        if (now > nextWander) wanderTarget(now);
      } else {
        tx = x + (dx / d) * 420;
        ty = y + (dy / d) * 420;
      }
    } else if (now > nextWander) {
      wanderTarget(now);
    }

    tx = clamp(tx, EDGE + size / 2, W - EDGE - size / 2);
    ty = clamp(ty, TOP + size / 2, H - EDGE - size / 2);

    var pull = mood === "avoid" ? 0.0042 : 0.0022;
    var drag = mood === "avoid" ? 0.915 : 0.935;
    vx = (vx + (tx - x) * pull) * drag;
    vy = (vy + (ty - y) * pull) * drag;

    var cap = mood === "avoid" ? 13 : 8;
    var sp = Math.hypot(vx, vy);
    if (sp > cap) { vx = vx / sp * cap; vy = vy / sp * cap; }

    x = clamp(x + vx, EDGE, W - EDGE);
    y = clamp(y + vy, TOP, H - EDGE);

    // turn to face the way it is swimming, and nose up or down a little
    if (Math.abs(vx) > 0.3) face = vx > 0 ? -1 : 1;
    tilt += (clamp(vy * 1.6, -14, 14) - tilt) * 0.08;

    el.style.transform = "translate3d(" + (x - size / 2) + "px," + (y - size / 2) + "px,0)";
    art.style.transform = "scaleX(" + face + ") rotate(" + (tilt * -face) + "deg)";

    requestAnimationFrame(step);
  }

  measure();
  newMood(performance.now());
  requestAnimationFrame(step);
})();
