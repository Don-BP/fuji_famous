/* FUJIE STUDIO - galleries, language, lightbox. */
(function () {
  "use strict";

  /* ---------------- galleries ----------------
     Most lines exist twice: the original water pieces and the Fuji collection.
     Showing both at once would make a line unreadably long, so a line that has
     both grows a switch and shows one view at a time. Long views are further cut
     to data-preview rows with a "show more" underneath.

     Fuji assets are the ones whose id carries _fuji; nothing older does. */
  var CAPS = {};

  function isFuji(id) { return id.indexOf("_fuji") > -1; }

  function inView(card, view) {
    return (card.dataset.set === "fuji") === (view === "fuji");
  }

  document.querySelectorAll("[data-gallery]").forEach(function (host) {
    var items = window.DATA[host.dataset.gallery] || [];
    host.innerHTML = items.map(function (it) {
      CAPS[it[0]] = { ja: it[1], en: it[2] };
      return '<figure class="card" data-id="' + it[0] + '"' +
             (isFuji(it[0]) ? ' data-set="fuji"' : "") + ">" +
             '<img loading="lazy" src="assets/t/' + it[0] + '.jpg" alt="">' +
             '<figcaption data-cap="' + it[0] + '">' + it[1] + "</figcaption></figure>";
    }).join("");

    /* only the long lines split; a short section shows everything */
    var views = [];
    if (parseInt(host.dataset.preview, 10) > 0 &&
        items.some(function (it) { return isFuji(it[0]); }) &&
        items.some(function (it) { return !isFuji(it[0]); })) {
      views = ["water", "fuji"];
    }
    if (views.length) {
      host.dataset.views = views.join(",");
      host.dataset.view = "water";
      var tabs = document.createElement("div");
      tabs.className = "setTabs";
      tabs.innerHTML = views.map(function (v) {
        return '<button type="button" class="setTab" data-set="' + v + '"></button>';
      }).join("");
      host.insertAdjacentElement("beforebegin", tabs);
    }
    if (parseInt(host.dataset.preview, 10)) {
      host.classList.add("collapsed");
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "moreBtn";
      host.insertAdjacentElement("afterend", btn);
    }
    sync(host);
  });

  /* Decide what the grid shows: the active set, cut to the preview count while
     collapsed. Called again whenever a switch, a toggle or the language moves. */
  function sync(grid) {
    var split = !!grid.dataset.views,
        view = grid.dataset.view || "water",
        shut = grid.classList.contains("collapsed"),
        cap = parseInt(grid.dataset.preview, 10) || 0,
        live = grid.dataset.touched === "1",
        seen = 0, buried = 0;

    [].forEach.call(grid.children, function (c) {
      if (split && !inView(c, view)) { c.classList.add("off"); return; }
      seen++;
      var over = cap && seen > cap && shut;
      c.classList.toggle("off", over);
      if (over) buried++;
      else if (live) c.classList.add("on");
    });

    var tabs = grid.previousElementSibling;
    if (tabs && tabs.classList.contains("setTabs")) {
      [].forEach.call(tabs.children, function (t) {
        var mine = t.dataset.set === view;
        t.classList.toggle("on", mine);
        t.setAttribute("aria-pressed", mine ? "true" : "false");
      });
    }

    var btn = grid.nextElementSibling;
    if (btn && btn.classList.contains("moreBtn")) {
      var hidden = buried || (seen > cap ? seen - cap : 0);
      btn.classList.toggle("off", seen <= cap);
      btn.textContent = lang === "en"
        ? (shut ? "Show " + hidden + " more" : "Show fewer")
        : (shut ? "ほか " + hidden + " 点を見る" : "閉じる");
      btn.setAttribute("aria-expanded", shut ? "false" : "true");
    }
  }

  function syncAll() {
    document.querySelectorAll("[data-gallery]").forEach(sync);
    document.querySelectorAll(".setTab").forEach(function (t) {
      t.textContent = t.dataset.set === "fuji"
        ? (lang === "en" ? "Mount Fuji" : "富士の意匠")
        : (lang === "en" ? "Water" : "水の意匠");
    });
  }

  /* ---------------- language ---------------- */
  var EN = {
    navWork: "Work", navChar: "Character", navFish: "The fish", navGoods: "Goods", navWamon: "Patterns",
    navBy: "Vittorio Zumpano / Brain Power Inc.",
    heroBy: "Conceived and produced by Vittorio Zumpano — Brain Power Inc., Osaka",
    footCredit: "Concept, design and build by <b>Vittorio Zumpano</b><br>Brain Power Inc., Osaka",
    heroKicker: "ENTRY — THE \"MAKE FUJIE FAMOUS\" IDEA CONTEST",
    heroTitle: "Fujie is<br>a real fish.",
    heroLede: "Not an invented character. A sturgeon that began with one remark from the late Eizaburo Nishibori in 1987, and of which more than ten thousand now swim at the Satomi farm in Hitachiota, Ibaraki. Any company can commission a drawn mascot. Only Fujikin has one that is alive. Everything past this point is what that single fact can be stretched into.",
    heroPlay: "Raise one", heroStory: "Forty years",
    heroMeta: "1987 — 2027　/　FORTY YEARS OF THE WORLD'S FIRST FULL-CYCLE STURGEON FARMING",
    workEyebrow: "MADE FOR THIS ENTRY", workH: "Two things that are not goods at all.",
    workB: "The brief asks for ideas that do not stay inside the frame of merchandise, so this starts outside it. Both open in a browser. No app, no sign-up. The tablet in the visitor centre, the recruiting page, a link handed out on a school visit — the places to put them already exist inside the company.",
    tagGame: "RAISING SIM", gameH: "Raise Fujie",
    gameB: "Feed, play, sleep, flow. Four kinds of care and four mini-games take a single egg all the way to a grown fish. It is over in ninety seconds, and by then the player knows that Fujikin is the company that raised a sturgeon from egg to egg — without having read a line of the company brochure. Japanese and English.",
    gameGo: "Play →",
    tagStory: "SCROLLING TIMELINE", storyH: "From a single egg",
    storyB: "From one remark in 1987 to the world's first full-cycle farming, Japan's first caviar, and on to the fortieth year in 2027. Forty years go past under one thumb. It is written as a story rather than a company history. People come out of it liking a valve company.",
    storyGo: "Read →",
    fishEyebrow: "ABOUT THIS FISH", fishH: "Fujie is real. Fujie is also endangered.",
    fishB: "Sturgeon are listed by the IUCN as the most critically endangered group of species on earth; every surviving species is threatened. What Fujikin closed in 1998 was the full life cycle in a tank — which is to say, <strong>a way to make caviar without ever taking another fish from a river</strong>. What they built was not a delicacy. It was a way to stop catching them. In the first year 5% survived — 95 of every 100 fish died. They kept going for eleven years; in 1998 a fish raised from an egg laid eggs of its own, and in 2002 Japan's first domestic caviar shipped.<br>This is the strongest thing in the proposal. A mascot that is only cute gets forgotten. Fujie comes with a reason to care. Valves for semiconductor fabs are a long way from most people's lives. A company that worked out how to increase a fish without catching any is not. 2027 is the fortieth year of that work.",
    charEyebrow: "PROPOSAL", charH: "Chibi Fujie — a second form",
    charB: "The official Fujie is not touched. As Article 7 of the manual requires, the original artwork is used exactly as supplied. Chibi Fujie is proposed as a <strong>second form</strong> to stand beside it: the sharp real fish for adults, this one for children. One form trying to reach every age reaches neither well. Two forms take the gift counter and the capsule machine at the same time.",
    stkEyebrow: "LINE STICKERS", stkH: "A hundred and twenty-eight stickers",
    stkB: "Sixty-four in Japanese, sixty-four in English, every one cut out on its own and finished to the LINE spec. Free for adding the official account.<br>Stickers do something advertising cannot: <strong>people send them to each other</strong>. Every time one is sent, Fujie lands on a screen nobody paid to reach. First in the pack is \"Not a shark!\" — one line, and the sturgeon conversation has started. The English sixty-four carry straight over to WhatsApp and Telegram.",
    goodsEyebrow: "GOODS", goodsH: "Five lines",
    goodsB: "One fish, five different shelves: the children's shelf, the gift shelf, the travel shelf, the pattern shelf and the craft shelf. There is no need to choose between them — one piece of artwork, five ways out of the building.<br>And Mount Fuji on every one of them. The name Fujikin comes from the mountain, so it now stands beside the water as the second house motif. Hand one of these to an overseas customer and the explanation takes a sentence.",
    line1H: "Chibi Fujie / toys and daily things",
    line1B: "The visitor-centre shelf and the capsule machine. Cheap, high volume, taken home. From the day a child carries one out, the name Fujikin gets said at that family's dinner table.",
    line2H: "The official line / gifts and ceremony",
    line2B: "Built only from the official artwork and the ripple motif Fujikin already uses. The original illustration is untouched, so it can go out at a ceremony or to a visiting client as it is. Something that stays on a client's desk keeps working long after a campaign has stopped.",
    line3H: "Maison Fujie / leather and canvas",
    line3B: "One fish and one ripple, worked into a monogram and put on travel goods. It imitates no existing house. This is the line that does not look like corporate merchandise, and if people actually use it, Fujie turns up in airports and on business trips.",
    line5H: "Wamon goods / things you carry",
    line5B: "The pattern collection put straight onto everyday objects: fans, wallets, bags, pouches, handkerchiefs, notepads, furoshiki. Every print is the same artwork as the swatches above. Draw it once and it goes onto anything.",
    line4H: "Wa / the language of craft",
    line4B: "Woodblock, gold screens, maki-e, blue-and-white, indigo. What happens when Japanese craft draws a sturgeon the way it has always drawn carp and cranes. Carp and cranes are finished. Nobody has drawn this fish yet.",
    wamonEyebrow: "PATTERNS", wamonH: "The Fujie pattern collection",
    wamonB: "Japanese patterns have always been chosen for what they mean. Seigaiha is the sea, uroko is a fish's scales, tatewaku is rising current, asanoha is growing. Eighteen patterns chosen for this fish and drawn for it: valve handwheels at the tortoise-shell nodes, arrows pointing upstream, caviar as a komon. Because each pattern means something, it can be explained when it is handed over — and a pattern that can be explained becomes a gift.",
    plushEyebrow: "PLUSH", plushH: "Plush and mascot",
    plushB: "The same fish split in two: one you can hold, one you can hang on a bag. The first sits on a shelf, the second goes out into the city. Advertising runs for as long as it is paid for. This runs for as long as people keep buying it.",
    plush1H: "Plush / three sizes",
    plush1B: "10cm, 25cm, 50cm. Fry, young fish, grown fish — the three stages are the product line. It is a fish that grows, so the sizes mean something.",
    plush2H: "Mascot keychain",
    plush2B: "The cheapest single item in the range and the one that travels furthest. From the moment it is hanging on a bag it is seen every day: on the train, in a classroom, in an airport abroad. The person who bought it becomes the medium.",
    rtEyebrow: "TWO WITHOUT PHOTOS YET", rtH: "Two routes only Fujikin has.",
    rtB: "Everything above this could be made by anyone who chose to. These two cannot: they need the farm, and the fry trade network. Neither is a new investment. Both are things the company already owns, brought out into the open.",
    rt1H: "Give Fujie a voice",
    rt1B: "Feeding time, when the whole surface boils for a few dozen seconds. A single fish hatching from an egg. Footage nobody has seen, and only Fujikin has it. Every location is company-owned and it costs almost nothing to shoot. The official Instagram's 114 followers are not a weakness but room.",
    rt2H: "Turn trade customers' packaging into advertising",
    rt2B: "Fujikin sells sturgeon fry to farms across Japan. Release Chibi Fujie to those customers free of charge and Fujie appears on tins of domestic caviar nationwide. No extra cost, only the existing trade network. A B2B company reaching the dinner table by a route no other company can copy.",
    fxT1: "AM", fxT2: "NOON", fxT3: "PM", fxT4: "NIGHT",
    fxEyebrow: "EXPECTED EFFECT", fxH: "One day in 2027.",
    fxB: "Everything above this line is finished and attached to this entry. This is what it adds up to, told as one day.<br>The brief says television advertising is not being considered. Nothing here is bought space. So the effect does not show up as a ratings figure. It shows up as a day like this one.",
    fx1H: "Hitachiota, feeding time, 7 a.m.",
    fx1B: "At the Satomi farm the whole surface of the water boils. A keeper films twenty seconds on a phone and posts it in Chibi Fujie's voice: \"Breakfast again. For ten thousand of us.\" The followers, 114 a year ago, have watched this every week since. One of them works in the prefecture's fisheries office and forwards today's post around the building.",
    fx2H: "A high school in Osaka, social studies",
    fx2B: "Students scan the QR code on the handout. Ninety seconds later there is a grown fish swimming on forty phones. \"Sir, what is this company?\" \"A valve maker. First in the world to raise this fish from the egg.\" Three years on, one of those students mentions this lesson at a Fujikin recruiting session.",
    fx3H: "A group chat, early evening",
    fx3B: "A university student sends the \"Not a shark!\" sticker. \"What is that?\" \"A sturgeon. Some company worked out how to breed an endangered fish without catching any.\" Fujikin paid nothing for this conversation. The sender got the sticker from a friend two weeks ago.",
    fx4H: "A dinner table, somewhere",
    fx4B: "On a year-end gift tin of domestic caviar, a small silver fish. \"That's the Satomi one. Let's go and see them.\" The producer who made the tin buys its fry from Fujikin. It paid nothing to use the character.<br>These four scenes have one thing in common: in each, somebody is telling the Fujikin story in their own words. That is the difference between a company that is remembered and a company that is talked about.",
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
    syncAll();
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
    var tab = e.target.closest(".setTab");
    if (tab) {
      var tgrid = tab.parentElement.nextElementSibling;
      tgrid.dataset.touched = "1";
      tgrid.dataset.view = tab.dataset.set;
      tgrid.classList.add("collapsed");
      sync(tgrid);
      return;
    }
    var btn = e.target.closest(".moreBtn");
    if (btn) {
      var grid = btn.previousElementSibling;
      grid.dataset.touched = "1";
      var opening = grid.classList.contains("collapsed");
      grid.classList.toggle("collapsed");
      sync(grid);
      if (!opening) grid.scrollIntoView({ behavior: "smooth", block: "start" });
      return;
    }
    var card = e.target.closest(".card");
    if (card) { open(card.dataset.id); return; }
    if (e.target === lb || e.target.id === "lbClose") close();
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !lb.hidden) close();
  });
})();
