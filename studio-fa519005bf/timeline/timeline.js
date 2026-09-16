/* ============================================================
   一粒の卵から - scroll behaviour.
   Three things follow the scroll: the backdrop, the creature in
   the middle of the tank, and the reveal of each beat.
   ============================================================ */
(function () {
  "use strict";

  var $ = function (id) { return document.getElementById(id); };

  /* ---------------- art the page swaps between ---------------- */
  var SKY = {
    egg:   "../assets/bg_egg.jpg",
    early: "../assets/bg_tank_early.jpg",
    grown: "../assets/bg_tank_grown.jpg",
    win:   "../assets/bg_win.jpg"
  };
  var STAGE = [
    { img: "../assets/stage_1_egg.png",   w: "min(26vw,220px)" },
    { img: "../assets/stage_2_larva.png", w: "min(38vw,330px)" },
    { img: "../assets/stage_3_fry.png",   w: "min(46vw,420px)" },
    { img: "../assets/stage_4_young.png", w: "min(58vw,540px)" },
    { img: "../assets/fujie-official.png", w: "min(74vw,720px)" }
  ];
  Object.keys(SKY).forEach(function (k) { new Image().src = SKY[k]; });
  STAGE.forEach(function (s) { new Image().src = s.img; });

  /* ---------------- language ---------------- */
  var EN = {
    back: "Back",
    kicker: "FUJIKIN STURGEON PROGRAMME",
    heroTitle: "From a single egg",
    heroLede: "In 1987 it started with one scientist's remark.<br>This is the record of the forty years it took to reach a world first.",
    scroll: "SCROLL",
    y87h: "The remark that started it",
    y87b: "“Why not use Fujikin's valves to try farming sturgeon?” — with those words from Eizaburo Nishibori, a valve maker took on a fish.",
    y87n: "A company that makes valves, raising fish. There was no precedent for it inside the company either.",
    y92h: "A first for private industry in Japan",
    y92b: "Artificial hatching succeeded. In that first year, though, only about five fish in a hundred lived.",
    y92s: "SURVIVAL RATE, FIRST YEAR",
    y98h: "A world first: the full cycle in a tank",
    y98b: "Fish raised from eggs laid eggs of their own. A whole generation turned over inside the tanks — the first time anywhere in the world.",
    y98s: "SURVIVAL RATE NOW",
    y98n: "Water temperature, flow, dissolved oxygen. What settled it was the ultra-precise fluid control Fujikin had spent its working life perfecting.",
    y02h: "Japan's first domestic caviar",
    y02b: "The first shipment. Much of the domestic caviar sold in Japan today descends from these tanks.",
    y02n: "Satomi Fish Farm, Ibaraki. More than ten thousand sturgeon still swim there.",
    y26h: "And so, Fujie",
    y26b: "Year forty. The fish that became the company mascot is not an invention. It is an animal that is actually swimming.",
    y26n: "Creating the Flow for Sustainability",
    outroH: "The rest is up to your tank.",
    outroB: "From a single 1987 egg to a grown fish — about ninety seconds.",
    outroCta: "Raise Fujie",
    outroBack: "See everything"
  };
  var JA = {};
  document.querySelectorAll("[data-t]").forEach(function (el) {
    JA[el.getAttribute("data-t")] = el.innerHTML;
  });

  var lang = (navigator.language || "ja").toLowerCase().indexOf("ja") === 0 ? "ja" : "en";
  function applyLang() {
    var dict = lang === "en" ? EN : JA;
    document.documentElement.lang = lang;
    document.querySelectorAll("[data-t]").forEach(function (el) {
      var v = dict[el.getAttribute("data-t")];
      if (v) el.innerHTML = v;
    });
    $("langBtn").textContent = lang === "en" ? "日本語" : "EN";
    document.title = lang === "en"
      ? "From a single egg | Forty years of Fujie"
      : "一粒の卵から ｜ フジィ 40年の記録";
  }
  $("langBtn").addEventListener("click", function () {
    lang = lang === "en" ? "ja" : "en";
    applyLang();
  });
  applyLang();

  /* ---------------- reveal + stage swap ---------------- */
  var beats = [].slice.call(document.querySelectorAll(".beat"));
  var layers = [$("skyA"), $("skyB")], active = 0;
  var creature = $("creature"), cimg = $("creatureImg");
  var currentSky = null, currentStage = -1;

  function setSky(key) {
    if (key === currentSky || !SKY[key]) return;
    currentSky = key;
    var next = layers[1 - active];
    next.style.backgroundImage = 'url("' + SKY[key] + '")';
    next.classList.add("on");
    layers[active].classList.remove("on");
    active = 1 - active;
  }
  function setStage(i) {
    if (i === currentStage) return;
    currentStage = i;
    var s = STAGE[i];
    cimg.src = s.img;
    creature.style.width = s.w;
    creature.classList.remove("swap");
    void creature.offsetWidth;
    creature.classList.add("swap");
  }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.classList.add("on");
      setSky(e.target.dataset.sky);
      setStage(+e.target.dataset.stage);
      countUp(e.target);
    });
  }, { threshold: 0.42 });
  beats.forEach(function (b) { io.observe(b); });
  setSky("egg");
  setStage(0);

  /* numbers that climb once, when their beat arrives */
  function countUp(beat) {
    beat.querySelectorAll("[data-count]").forEach(function (el) {
      if (el.dataset.done) return;
      el.dataset.done = "1";
      var to = +el.dataset.count, t0 = performance.now(), ms = 1500;
      (function step(t) {
        var k = Math.min(1, (t - t0) / ms);
        el.textContent = Math.round(to * (1 - Math.pow(1 - k, 3)));
        if (k < 1) requestAnimationFrame(step);
      })(t0);
    });
  }

  /* progress bar */
  var bar = document.querySelector("#progress i");
  addEventListener("scroll", function () {
    var h = document.documentElement.scrollHeight - innerHeight;
    bar.style.width = (h > 0 ? (scrollY / h) * 100 : 0) + "%";
  }, { passive: true });

  /* ---------------- drifting motes ---------------- */
  var cv = $("motes"), ctx = cv.getContext("2d"), motes = [];
  function size() {
    cv.width = innerWidth;
    cv.height = innerHeight;
    motes = [];
    var n = Math.min(70, Math.round(innerWidth / 18));
    for (var i = 0; i < n; i++) {
      motes.push({
        x: Math.random() * cv.width,
        y: Math.random() * cv.height,
        r: 0.6 + Math.random() * 2.2,
        s: 0.10 + Math.random() * 0.42,
        a: 0.06 + Math.random() * 0.20,
        d: Math.random() * Math.PI * 2
      });
    }
  }
  function draw() {
    ctx.clearRect(0, 0, cv.width, cv.height);
    for (var i = 0; i < motes.length; i++) {
      var m = motes[i];
      m.y -= m.s;
      m.d += 0.012;
      m.x += Math.sin(m.d) * 0.28;
      if (m.y < -6) { m.y = cv.height + 6; m.x = Math.random() * cv.width; }
      ctx.beginPath();
      ctx.arc(m.x, m.y, m.r, 0, 6.283);
      ctx.fillStyle = "rgba(190,235,255," + m.a + ")";
      ctx.fill();
    }
    requestAnimationFrame(draw);
  }
  if (!matchMedia("(prefers-reduced-motion: reduce)").matches) {
    addEventListener("resize", size);
    size();
    draw();
  } else {
    cv.style.display = "none";
  }
})();
