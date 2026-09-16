/* FUJIE STUDIO - galleries, language, lightbox. */
(function () {
  "use strict";

  /* ---------------- galleries ---------------- */
  var CAPS = {};
  document.querySelectorAll("[data-gallery]").forEach(function (host) {
    var items = window.DATA[host.dataset.gallery] || [];
    host.innerHTML = items.map(function (it) {
      CAPS[it[0]] = { ja: it[1], en: it[2] };
      return '<figure class="card" data-id="' + it[0] + '">' +
             '<img loading="lazy" src="assets/t/' + it[0] + '.jpg" alt="">' +
             '<figcaption data-cap="' + it[0] + '">' + it[1] + "</figcaption></figure>";
    }).join("");
  });

  /* ---------------- language ---------------- */
  var EN = {
    navWork: "Work", navChar: "Character", navGoods: "Goods", navWamon: "Patterns",
    heroKicker: "FUJIKIN MASCOT PROPOSAL",
    heroTitle: "Fujie is<br>a real fish.",
    heroLede: "Not an invented character. A sturgeon that has been swimming in a tank in Ibaraki since 1987. That one fact is what the whole proposal is built on.",
    heroPlay: "Raise one", heroStory: "Forty years",
    heroMeta: "1987 — 2026　/　THE WORLD'S FIRST FULL-CYCLE STURGEON FARMING",
    workEyebrow: "WHAT WE MADE", workH: "Two things you can actually play with.",
    tagGame: "RAISING SIM", gameH: "Raise Fujie",
    gameB: "Feed, play, sleep, flow. Four kinds of care and four mini-games take a single egg all the way to a grown fish. About ninety seconds. Japanese and English.",
    gameGo: "Play →",
    tagStory: "SCROLLING TIMELINE", storyH: "From a single egg",
    storyB: "From one remark in 1987 to the world's first full-cycle farming, Japan's first caviar, and the Fujie of 2026. Forty years, one scroll.",
    storyGo: "Read →",
    charEyebrow: "PROPOSAL", charH: "Chibi Fujie — a second form",
    charB: "The official Fujie is not touched. As Article 7 of the manual requires, the original artwork is used exactly as supplied. Chibi Fujie is proposed as a <strong>second form</strong> to stand beside it: the sharp real fish for adults, this one for children.",
    stkEyebrow: "GIVEAWAY", stkH: "One hundred stickers",
    stkB: "Sixty in Japanese, forty in English. Given away free for adding the LINE official account, so Fujie ends up inside people's conversations. The English forty carry straight over to WhatsApp and Telegram.",
    goodsEyebrow: "GOODS", goodsH: "Four lines",
    goodsB: "One fish, four different shelves: the children's shelf, the gift shelf, the travel shelf and the craft shelf.",
    line1H: "01 — Chibi Fujie / toys and daily things",
    line1B: "The visitor-centre shelf and the capsule machine. Cheap, high volume, taken home.",
    line2H: "02 — The official line / gifts and ceremony",
    line2B: "Built only from the official artwork and the ripple motif Fujikin already uses. The original illustration is untouched.",
    line3H: "03 — Maison Fujie / leather and canvas",
    line3B: "One fish and one ripple, worked into a monogram and put on travel goods. It imitates no existing house.",
    line5H: "04 — Wamon goods / things you carry",
    line5B: "The pattern collection put straight onto everyday objects: fans, wallets, bags, pouches, handkerchiefs, notepads, furoshiki. Every print is the same artwork as the swatches above.",
    line4H: "05 — Wa / the language of craft",
    line4B: "Woodblock, gold screens, maki-e, blue-and-white, indigo. What happens when Japanese craft draws a sturgeon the way it has always drawn carp and cranes.",
    wamonEyebrow: "PATTERNS", wamonH: "The Fujie pattern collection",
    wamonB: "Japanese patterns have always been chosen for what they mean. Seigaiha is the sea, uroko is a fish's scales, tatewaku is rising current, asanoha is growing. Eighteen patterns chosen for this fish and drawn for it: valve handwheels at the tortoise-shell nodes, arrows pointing upstream, caviar as a komon.",
    plushEyebrow: "PROTOTYPE", plushH: "Plush",
    footNote: "The official illustration is used in accordance with Article 7 of the character manual ver 1.0 — no reshaping, recolouring, transparency, overlaid text, or added or removed elements. Chibi Fujie, the pattern collection and the Maison line are new work proposed alongside it.",
    lang: "日本語"
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
    document.querySelectorAll("[data-cap]").forEach(function (el) {
      var c = CAPS[el.getAttribute("data-cap")];
      if (c) el.textContent = lang === "en" ? c.en : c.ja;
    });
    document.getElementById("langBtn").textContent = lang === "en" ? "日本語" : "EN";
    document.title = lang === "en"
      ? "Fujie is a real fish | FUJIE STUDIO"
      : "フジィは実在する ｜ FUJIE STUDIO";
  }
  document.getElementById("langBtn").addEventListener("click", function () {
    lang = lang === "en" ? "ja" : "en";
    applyLang();
  });
  applyLang();

  /* ---------------- reveal ---------------- */
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add("on"); io.unobserve(e.target); }
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
  var cards = [].slice.call(document.querySelectorAll(".card"));
  cards.forEach(function (c, i) {
    c.style.transitionDelay = (i % 4) * 60 + "ms";
    io.observe(c);
  });

  /* ---------------- lightbox ---------------- */
  var lb = document.getElementById("lb"),
      lbImg = document.getElementById("lbImg"),
      lbCap = document.getElementById("lbCap");
  function open(id) {
    lbImg.src = "assets/" + id + ".jpg";
    var c = CAPS[id];
    lbCap.textContent = c ? (lang === "en" ? c.en : c.ja) : "";
    lb.hidden = false;
    document.body.style.overflow = "hidden";
  }
  function close() {
    lb.hidden = true;
    lbImg.src = "";
    document.body.style.overflow = "";
  }
  document.addEventListener("click", function (e) {
    var card = e.target.closest(".card");
    if (card) { open(card.dataset.id); return; }
    if (e.target === lb || e.target.id === "lbClose") close();
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !lb.hidden) close();
  });
})();
