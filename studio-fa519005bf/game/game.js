/* フジィを育てよう / Raise Fujie — care loop + four mini-games */
(function(){
"use strict";

var $ = function(id){ return document.getElementById(id); };
var L;
var saved = localStorage.getItem("fujieLang");
var lang = saved || ((navigator.language || "ja").slice(0,2) === "en" ? "en" : "ja");
if (!window.I18N[lang]) lang = "ja";

/* ---------------- growth stages ---------------- */
/* `face` is the folder key for that stage's expression sprites. The egg has no
   face, and the adult is Fujikin's official mascot artwork, which is never
   redrawn - both fall back to their single image. */
var STAGES = [
  { g:0,  img:"stage_1_egg.png",    key:"st_egg",   fs:"16%", t1:"#05121A", t2:"#0A2230", face:null },
  { g:16, img:"stage_2_larva.png",  key:"st_larva", fs:"26%", t1:"#071A25", t2:"#0D2B38", face:"larva" },
  { g:38, img:"stage_3_fry.png",    key:"st_fry",   fs:"40%", t1:"#092330", t2:"#103544", face:"fry" },
  { g:64, img:"stage_4_young.png",  key:"st_young", fs:"62%", t1:"#0C2D3C", t2:"#16485A", face:"young" },
  { g:88, img:"fujie-official.png", key:"st_adult", fs:"86%", t1:"#0F3949", t2:"#1D5566", face:null }
];
/* which expression each need maps to, and which button fixes it */
var FACES = { water:"sick", hunger:"hungry", energy:"sleepy", mood:"bored" };
var MS_AT = [16, 38, 52, 64, 88];

/* ---------------- game art ----------------
   Sprites are drawn to canvas, so they are preloaded as Image objects.
   Backgrounds are applied in CSS; they are touched here only to warm the cache. */
var ART = {};
["fujie_shell","fujie_shell_happy","roe_egg","shark_pop","shark_hurt","urchin",
 "fujie_whack","fujie_ouch","hit_burst","fujie_dash","rock_pillar","shell_closed",
 "pearl","title_fujie","fujie_cheer","fujie_sad"].forEach(function(n){
  var i = new Image(); i.src = "art/" + n + ".png"; ART[n] = i;
});
["bg_title","bg_egg","bg_shark","bg_race","bg_shell","bg_tank_early","bg_tank_grown",
 "bg_result","bg_lost","bg_win","bg_sheet"].forEach(function(n){
  var i = new Image(); i.src = "art/" + n + ".jpg";
});
/* expression sprites - preloaded so the face swaps without a flash */
["larva","fry","young"].forEach(function(st){
  ["hungry","sleepy","bored","sick"].forEach(function(f){
    var n = "face_" + st + "_" + f;
    var i = new Image(); i.src = "art/" + n + ".png"; ART[n] = i;
  });
});

/* ---------------- state ---------------- */
var S, timer = null, shown = {}, noteT = null, bubbleT = null;
function fresh(){
  return { hunger:72, mood:72, energy:82, water:100, growth:0,
           flow:30, t:0, stage:-1, asleep:false, over:false, paused:false };
}

/* ---------------- i18n ---------------- */
function applyLang(){
  L = window.I18N[lang];
  document.documentElement.lang = L.html;
  document.title = L.title + (lang === "ja" ? " ｜ フジキン" : " | Fujikin");
  $("langBtn").textContent = L.langBtn;

  var m = {
    lbHunger:"hunger", lbMood:"mood", lbEnergy:"energy", lbWater:"water", lbGrowth:"growth",
    actFeedT:"feed", actPlayT:"play", actSleepT:"sleep", actFlowT:"flow",
    startMark:"startMark", startBtn:"startBtn",
    flowTitle:"flowTitle", flowNote:"flowNote", flowClose:"close",
    pickTitle:"pickTitle", pickClose:"close",
    miniExit:"back", retryBtn:"retry", againBtn:"retry",
    winMark:"winMark", lostMark:"lostMark"
  };
  Object.keys(m).forEach(function(id){ var e = $(id); if (e) e.textContent = L[m[id]]; });

  var h = { startQuote:"startQuote", startBody:"startBody",
            lostTitle:"lostTitle", lostBody:"lostBody", lostHint:"lostHint",
            winTitle:"winTitle", winBody:"winBody" };
  Object.keys(h).forEach(function(id){ var e = $(id); if (e) e.innerHTML = L[h[id]]; });

  [["gEggT","g_egg"],["gEggD","g_egg_d"],["gSharkT","g_shark"],["gSharkD","g_shark_d"],
   ["gRaceT","g_race"],["gRaceD","g_race_d"],["gShellT","g_shell"],["gShellD","g_shell_d"]]
    .forEach(function(p){ var e = $(p[0]); if (e) e.textContent = L[p[1]]; });

  if (S) { paint(); setStage(true); }
}
$("langBtn").addEventListener("click", function(){
  lang = lang === "ja" ? "en" : "ja";
  localStorage.setItem("fujieLang", lang);
  applyLang();
});

/* ---------------- flow band ---------------- */
function band(g){ var c = 22 + g*0.58, w = 20 - g*0.07;
  return { lo:Math.max(0,c-w), hi:Math.min(100,c+w) }; }
function drawZone(){
  var b = band(S.growth);
  $("zone").style.left = b.lo + "%";
  $("zone").style.width = (b.hi - b.lo) + "%";
}

/* ---------------- stage ---------------- */
function setStage(force){
  var idx = 0;
  for (var i = 0; i < STAGES.length; i++) if (S.growth >= STAGES[i].g) idx = i;
  if (idx === S.stage && !force) return;
  var grew = idx > S.stage && S.stage >= 0;
  S.stage = idx;
  var st = STAGES[idx];
  $("fish").style.setProperty("--fs", st.fs);
  applyFace();
  $("stageName").textContent = L[st.key];
  $("tank").style.setProperty("--t1", st.t1);
  $("tank").style.setProperty("--t2", st.t2);
  // the nursery trough gives way to the big rearing tank once he is a fry
  $("tankArt").style.backgroundImage =
    'url("art/' + (idx >= 2 ? "bg_tank_grown" : "bg_tank_early") + '.jpg")';
  if (grew) cheer();
}
function cheer(){
  var f = $("fish");
  f.classList.remove("happy"); void f.offsetWidth; f.classList.add("happy");
}

/* ---------------- needs ----------------
   One source of truth. The face, the thought bubble and the pulsing button all
   read from worstNeed(), so what Fujie looks like always matches what he needs
   and which button fixes it. */
/* `at` is where Fujie starts asking for help. Every one of these sits ABOVE the
   matching cut-off in the growth gate below (water 38, hunger 22, mood 22,
   energy 15), so he always warns you before he quietly stops growing. Water
   used to warn at 34, under its own gate of 38, and stalled him in silence. */
var NEEDS = [
  { k:"water",  at:45 },
  { k:"hunger", at:30 },
  { k:"energy", at:26 },
  { k:"mood",   at:32 }
];
function worstNeed(){
  var worst = null, deepest = 0;
  for (var i = 0; i < NEEDS.length; i++){
    var n = NEEDS[i], v = S[n.k];
    if (v >= n.at) continue;
    var d = (n.at - v) / n.at;      // how far below its threshold, 0..1
    if (d > deepest){ deepest = d; worst = n.k; }
  }
  return worst;
}

/* ---- expression ---- */
function currentFace(){
  if (S.asleep) return "sleepy";
  var n = worstNeed();
  return n ? FACES[n] : null;
}
/* Returns true when a real expression sprite was used, so paint() knows whether
   it still needs the CSS colour wash to carry the message. */
function applyFace(){
  var st = STAGES[Math.max(0, S.stage)], f = currentFace(), src = st.img, drawn = false;
  if (f && st.face){
    var key = "face_" + st.face + "_" + f;
    if (ART[key] && ART[key].naturalWidth){ src = "art/" + key + ".png"; drawn = true; }
  }
  var img = $("fish");
  if (img.getAttribute("src") !== src) img.setAttribute("src", src);
  return drawn;
}

function showBubble(){
  var n = worstNeed(), b = $("bubble");
  if (S.asleep || !n) { b.classList.remove("on"); return; }
  b.textContent = L["need_" + n];
  b.classList.add("on");
}
function markUrgent(){
  // The face and the bubble can only show one thing, so they show the most
  // urgent need - but EVERY unmet need pulses its own button, or a player
  // following the pulse could starve him while fixing something else.
  var low = {};
  if (!S.asleep) for (var i = 0; i < NEEDS.length; i++){
    if (S[NEEDS[i].k] < NEEDS[i].at) low[NEEDS[i].k] = true;
  }
  $("actFeed").classList.toggle("urgent", !!low.hunger);
  $("actPlay").classList.toggle("urgent", !!low.mood);
  $("actSleep").classList.toggle("urgent", !!low.energy);
  $("actFlow").classList.toggle("urgent", !!low.water);
  // you cannot feed or play with a sleeping fish, so say so
  $("actFeed").disabled = S.asleep;
  $("actPlay").disabled = S.asleep;
  $("actSleepT").textContent = S.asleep ? L.wake : L.sleep;
}

/* ---------------- milestones ---------------- */
function showNote(i){
  if (shown[i]) return;
  shown[i] = true;
  var n = L.ms[i];
  $("note").querySelector("b").textContent = n.t;
  $("note").querySelector("span").textContent = n.d;
  $("note").classList.add("on");
  clearTimeout(noteT);
  noteT = setTimeout(function(){ $("note").classList.remove("on"); }, 7500);
}

/* ---------------- paint ---------------- */
function bar(id, v, good){
  var e = $(id); e.style.width = Math.max(0, Math.min(100, v)) + "%";
  e.style.background = good ? good : (v > 55 ? "var(--good)" : v > 26 ? "var(--warn)" : "var(--bad)");
}
function paint(){
  bar("bHunger", S.hunger); bar("bMood", S.mood);
  bar("bEnergy", S.energy); bar("bWater", S.water);
  bar("bGrowth", S.growth, "var(--flow)");
  $("growVal").textContent = Math.round(S.growth);
  $("year").textContent = 1987 + Math.floor(S.t / 60);
  var hasFace = applyFace();
  // the wash is only needed where there is no unwell sprite (egg, adult)
  $("fish").classList.toggle("sick", currentFace() === "sick" && !hasFace);
  $("fish").classList.toggle("asleep", S.asleep);
  $("veil").classList.toggle("on", S.asleep);
  showBubble(); markUrgent();
}

/* ---------------- floating feedback ---------------- */
function pop(text, colour){
  var d = document.createElement("div");
  d.className = "pop"; d.textContent = text;
  if (colour) d.style.color = colour;
  d.style.left = (36 + Math.random()*28) + "%";
  d.style.top = "46%";
  $("tank").appendChild(d);
  d.animate([{ transform:"translateY(0)", opacity:1 },
             { transform:"translateY(-56px)", opacity:0 }],
            { duration:1100, easing:"ease-out" }).onfinish = function(){ d.remove(); };
}

/* ---------------- main tick (100 ms) ---------------- */
function tick(){
  if (S.over || S.paused) return;
  S.t++;

  var b = band(S.growth), inBand = S.flow >= b.lo && S.flow <= b.hi;
  var rate = S.asleep ? 0.35 : 1;   // needs decay slower while asleep

  S.water += inBand ? 0.5 : -0.75;
  if (S.hunger > 92) S.water -= 0.35;          // overfeeding fouls the water
  S.water = Math.max(0, Math.min(100, S.water));

  S.hunger -= (0.26 + S.growth*0.0030) * rate;
  S.mood   -= (0.22 + S.growth*0.0018) * rate;
  S.energy -= S.asleep ? -0.9 : (0.20 + S.growth*0.0016);

  S.hunger = Math.max(0, Math.min(100, S.hunger));
  S.mood   = Math.max(0, Math.min(100, S.mood));
  S.energy = Math.max(0, Math.min(100, S.energy));

  if (S.asleep && S.energy >= 99) wake();

  // growth needs every need met
  var well = S.water > 38 && S.hunger > 22 && S.mood > 22 && S.energy > 15;
  if (well && !S.asleep) S.growth = Math.min(100, S.growth + 0.16);

  $("flowState").textContent = inBand ? L.flowGood : L.flowBad;
  $("flowState").style.color = inBand ? "var(--good)" : "var(--dim)";

  setStage(); drawZone(); paint();
  for (var i = 0; i < MS_AT.length; i++) if (S.growth >= MS_AT[i]) showNote(i);

  if (S.water <= 0 || S.hunger <= 0) return end(false);
  if (S.growth >= 100) return end(true);
}

/* ---------------- actions ---------------- */
$("actFeed").addEventListener("click", function(){
  if (!S || S.over || S.asleep) return;
  var wasHungry = S.hunger < 30;
  S.hunger = Math.min(100, S.hunger + 16);
  S.mood = Math.min(100, S.mood + 3);
  dropPellets(); pop("+" + L.hunger);
  if (wasHungry && S.hunger >= 30) cheer();   // he perks up the moment it is fixed
  paint();
});
$("actSleep").addEventListener("click", function(){
  if (!S || S.over) return;
  S.asleep ? wake() : sleep();
});
function sleep(){ S.asleep = true; $("veil").classList.add("on"); paint(); }
function wake(){
  var rested = S.energy >= 60;
  S.asleep = false; $("veil").classList.remove("on");
  if (rested) cheer();
  paint();
}
$("veil").addEventListener("click", wake);

$("actFlow").addEventListener("click", function(){ openSheet("flowSheet"); });
$("flowClose").addEventListener("click", function(){ closeSheets(); });
$("flow").addEventListener("input", function(){ if (S) S.flow = +this.value; });

$("actPlay").addEventListener("click", function(){
  if (!S || S.over || S.asleep) return;
  openSheet("pickSheet");
});
$("pickClose").addEventListener("click", function(){ closeSheets(); });

function openSheet(id){ S.paused = true; $(id).classList.add("on"); }
function closeSheets(){
  document.querySelectorAll(".sheet").forEach(function(s){ s.classList.remove("on"); });
  if (S && !S.over) S.paused = false;
}

function dropPellets(){
  var r = $("tank").getBoundingClientRect();
  for (var i = 0; i < 5; i++){
    var p = document.createElement("div");
    p.style.cssText = "position:absolute;width:7px;height:7px;border-radius:50%;" +
      "background:radial-gradient(circle at 32% 30%,#C9A86A,#6B5326);pointer-events:none;top:-10px;" +
      "left:" + (20 + Math.random()*60) + "%";
    $("tank").appendChild(p);
    p.animate([{ transform:"translateY(0)", opacity:1 },
               { transform:"translateY(" + r.height*0.72 + "px)", opacity:0 }],
              { duration:1300 + Math.random()*800, easing:"cubic-bezier(.3,.6,.5,1)" })
      .onfinish = function(){ this.effect.target.remove(); };
  }
}

/* ================================================================
   MINI-GAMES
   ================================================================ */
var MG = { active:null, raf:null, timer:null, score:0, left:0, onTap:null, cleanup:null };

function startMini(kind){
  closeSheets();
  S.paused = true;
  MG.active = kind; MG.score = 0; MG.left = 30;
  $("mini").className = "on mg-" + kind;   // per-game background plate
  $("miniScore").textContent = L.score + " 0";
  $("miniTime").textContent = L.time + " 30";
  $("miniDom").innerHTML = "";
  $("miniCanvas").style.display = "none";
  $("miniDom").style.display = "block";

  var titles = { egg:"g_egg", shark:"g_shark", race:"g_race", shell:"g_shell" };
  var ctl = { egg:"ctl_egg", shark:"ctl_shark", race:"ctl_race", shell:"ctl_shell" };
  $("miniTitle").textContent = L[titles[kind]];
  $("miniFoot").textContent = L[ctl[kind]];

  if (kind === "egg")        initEgg();
  else if (kind === "shark") initShark();
  else if (kind === "race")  initRace();
  else                       initShell();

  if (kind !== "shell"){
    MG.timer = setInterval(function(){
      MG.left--;
      $("miniTime").textContent = L.time + " " + MG.left;
      if (MG.left <= 0) endMini();
    }, 1000);
  }
}

function bumpScore(n){
  MG.score += n;
  $("miniScore").textContent = L.score + " " + MG.score;
}

function endMini(){
  clearInterval(MG.timer); MG.timer = null;
  if (MG.raf) cancelAnimationFrame(MG.raf), MG.raf = null;
  if (MG.cleanup) MG.cleanup(), MG.cleanup = null;
  $("mini").classList.remove("on");

  var moodGain = Math.min(42, 14 + MG.score * 1.6);
  var growGain = Math.min(3.2, MG.score * 0.14);
  S.mood = Math.min(100, S.mood + moodGain);
  S.growth = Math.min(100, S.growth + growGain);
  S.energy = Math.max(0, S.energy - 5);

  $("resScore").textContent = MG.score;
  $("resTitle").textContent = L.resultTitle;
  $("resMood").textContent = L.moodUp;
  $("resGrow").textContent = L.growUp;
  $("resAgain").textContent = L.again;
  $("resBack").textContent = L.back;
  $("resultScreen").classList.add("on");
  cheer(); paint();
}
$("resAgain").addEventListener("click", function(){
  $("resultScreen").classList.remove("on"); startMini(MG.active);
});
$("resBack").addEventListener("click", function(){
  $("resultScreen").classList.remove("on"); S.paused = false;
});
$("miniExit").addEventListener("click", function(){
  clearInterval(MG.timer);
  if (MG.raf) cancelAnimationFrame(MG.raf), MG.raf = null;
  if (MG.cleanup) MG.cleanup(), MG.cleanup = null;
  $("mini").classList.remove("on"); S.paused = false;
});

/* ---- shared canvas helper ---- */
function canvasSetup(){
  var c = $("miniCanvas");
  $("miniDom").style.display = "none";
  c.style.display = "block";
  var r = c.getBoundingClientRect();
  var dpr = Math.min(2, window.devicePixelRatio || 1);
  c.width = r.width * dpr; c.height = r.height * dpr;
  var x = c.getContext("2d"); x.scale(dpr, dpr);
  return { c:c, x:x, w:r.width, h:r.height };
}

/* ---- 1. EGG CATCH ---- */
function initEgg(){
  var g = canvasSetup(), W = g.w, H = g.h;
  var px = W/2, eggs = [], spawn = 0, missed = 0;
  var img = ART.fujie_shell, egg = ART.roe_egg;
  var bits = [], happy = 0;   // catch sparkles, and how long Fujie stays delighted
  // Fujie holds the shell low and to his right, so the catch mouth is not the
  // centre of the sprite. BOWL_* locate the shell rim inside the artwork.
  var BOWL_X = 0.32, BOWL_Y = 0.52, BOWL_W = 0.33;
  var fw = Math.min(150, W*0.42);

  function at(e){
    var r = g.c.getBoundingClientRect();
    var t = e.touches ? e.touches[0] : e;
    px = Math.max(fw*BOWL_W, Math.min(W - fw*BOWL_W, t.clientX - r.left));
  }
  function down(e){ e.preventDefault(); at(e); }
  g.c.addEventListener("pointerdown", down);
  g.c.addEventListener("pointermove", function(e){ if (e.buttons || e.pointerType === "touch") at(e); });
  MG.cleanup = function(){ g.c.removeEventListener("pointerdown", down); };

  /* a little shower of sparks and a rising "+1" when an egg lands */
  function burst(x, y){
    for (var k = 0; k < 11; k++){
      var a = Math.random()*6.2832, s = 1.4 + Math.random()*3.2;
      bits.push({ x:x, y:y, vx:Math.cos(a)*s, vy:Math.sin(a)*s - 1.1,
                  life:1, r:1.6 + Math.random()*2.4, txt:null });
    }
    bits.push({ x:x, y:y-8, vx:0, vy:-1.5, life:1, r:0, txt:"+1" });
  }
  function drawBits(){
    for (var k = bits.length-1; k >= 0; k--){
      var b = bits[k];
      b.x += b.vx; b.y += b.vy; b.vy += 0.09; b.life -= 0.028;
      if (b.life <= 0){ bits.splice(k,1); continue; }
      if (b.txt){
        g.x.fillStyle = "rgba(232,192,113," + b.life + ")";
        g.x.font = "700 17px sans-serif"; g.x.textAlign = "center";
        g.x.fillText(b.txt, b.x, b.y); g.x.textAlign = "left";
      } else {
        g.x.fillStyle = "rgba(255,247,226," + b.life + ")";
        g.x.beginPath(); g.x.arc(b.x, b.y, b.r*b.life + 0.6, 0, 6.2832); g.x.fill();
      }
    }
  }

  function frame(){
    g.x.clearRect(0,0,W,H);

    var fh = fw * (img.naturalHeight/img.naturalWidth || 1);
    var topY = H - fh - 4;
    var catchY = topY + fh*BOWL_Y, catchW = fw*BOWL_W;

    // Fujie is drawn FIRST so the eggs always fall in front of him and stay
    // readable right up to the moment they drop into the shell.
    var pose = (happy > 0 && ART.fujie_shell_happy.naturalWidth)
             ? ART.fujie_shell_happy : img;
    if (pose.naturalWidth) g.x.drawImage(pose, px - fw*BOWL_X, topY, fw, fh);
    if (happy > 0) happy--;

    spawn--;
    if (spawn <= 0){ eggs.push({ x:30 + Math.random()*(W-60), y:-14,
                                 v:1.9 + Math.random()*1.7 }); spawn = 26 + Math.random()*22; }
    for (var i = eggs.length-1; i >= 0; i--){
      var e = eggs[i]; e.y += e.v;
      // a soft halo lifts the dark egg off the dark water
      var gl = g.x.createRadialGradient(e.x, e.y, 2, e.x, e.y, 19);
      gl.addColorStop(0, "rgba(232,192,113,.40)");
      gl.addColorStop(1, "rgba(232,192,113,0)");
      g.x.fillStyle = gl;
      g.x.beginPath(); g.x.arc(e.x, e.y, 19, 0, 6.2832); g.x.fill();
      if (egg.naturalWidth) g.x.drawImage(egg, e.x-13, e.y-13, 26, 26);
      else {
        g.x.beginPath(); g.x.arc(e.x, e.y, 9, 0, 6.2832);
        g.x.fillStyle = "#6B7A80"; g.x.fill();
      }
      if (e.y > catchY && e.y < catchY + 62 && Math.abs(e.x - px) < catchW){
        eggs.splice(i,1); bumpScore(1); burst(e.x, e.y); happy = 34;
      } else if (e.y > H+16){ eggs.splice(i,1); missed++; }
    }

    drawBits();
    g.x.fillStyle = "rgba(191,207,214,.75)"; g.x.font = "12px sans-serif";
    g.x.fillText(L.missed + " " + missed, 12, 20);
    MG.raf = requestAnimationFrame(frame);
  }
  frame();
}

/* ---- 2. WHACK-A-SHARK ---- */
function initShark(){
  var wrap = $("miniDom");
  wrap.innerHTML = '<div id="holes"></div>' +
    '<img id="whacker" src="art/fujie_whack.png" alt="">';
  var holes = $("holes"), cells = [], streak = 0, best = 0, timers = [], iv = null;

  function showStreak(){
    $("miniFoot").textContent = streak > 1
      ? L.streak + " " + streak + " ×" + comboMult()
      : L.ctl_shark;
  }
  function comboMult(){ return streak >= 9 ? 3 : streak >= 5 ? 2 : 1; }

  for (var i = 0; i < 9; i++){
    var d = document.createElement("div");
    d.className = "hole";
    d.innerHTML = '<div class="splash"></div>' +
      '<div class="shark"><img src="art/shark_pop.png" alt=""></div>' +
      '<div class="fx"><img src="art/hit_burst.png" alt=""></div>';
    (function(cell){
      cell.addEventListener("pointerdown", function(){
        if (!cell.classList.contains("up")) return;
        cell.classList.remove("up");
        var w = $("whacker"), urchin = cell.dataset.kind === "urchin";

        if (urchin){
          // the one thing you must not hit: lose the streak, take a knock
          cell.classList.add("bad");
          streak = 0;
          MG.score = Math.max(0, MG.score - 2);
          $("miniScore").textContent = L.score + " " + MG.score;
          $("mini").classList.remove("shake"); void $("mini").offsetWidth;
          $("mini").classList.add("shake");
          $("miniFoot").textContent = L.ouch;
          if (w){ w.src = "art/fujie_ouch.png"; w.classList.remove("swing"); }
          timers.push(setTimeout(function(){
            if (w) w.src = "art/fujie_whack.png";
            $("mini").classList.remove("shake");
            cell.classList.remove("bad");
            showStreak();
          }, 700));
          return;
        }

        cell.classList.add("hit");
        cell.querySelector(".shark img").src = "art/shark_hurt.png";
        streak++; if (streak > best) best = streak;
        bumpScore(comboMult());
        showStreak();
        if (w){ w.classList.remove("swing"); void w.offsetWidth; w.classList.add("swing"); }
        timers.push(setTimeout(function(){ cell.classList.remove("hit"); }, 420));
      });
    })(d);
    holes.appendChild(d); cells.push(d);
  }

  // Pacing: starts deliberately slow and tightens as the streak builds, so the
  // first few pops are easy and a good run turns frantic.
  function gap(){ return Math.max(360, 1050 - streak * 58); }
  function upFor(){ return Math.max(620, 1250 - streak * 46); }

  function pop(){
    var free = cells.filter(function(c){ return !c.classList.contains("up") &&
                                                !c.classList.contains("hit"); });
    if (free.length){
      var c = free[Math.floor(Math.random()*free.length)];
      // urchins only start appearing once the player is warmed up
      var urchin = streak >= 2 && Math.random() < 0.22;
      c.dataset.kind = urchin ? "urchin" : "shark";
      c.querySelector(".shark img").src = urchin ? "art/urchin.png" : "art/shark_pop.png";
      c.classList.toggle("isUrchin", urchin);
      c.classList.add("up");
      timers.push(setTimeout(function(){
        if (c.classList.contains("up")){
          c.classList.remove("up");
          if (!urchin && streak){ streak = 0; showStreak(); }   // a missed shark breaks the run
        }
      }, upFor()));
    }
    iv = setTimeout(pop, gap());
  }

  showStreak();
  iv = setTimeout(pop, 500);
  MG.cleanup = function(){
    clearTimeout(iv);
    timers.forEach(clearTimeout);
    $("mini").classList.remove("shake");
    var w = $("whacker"); if (w) w.src = "art/fujie_whack.png";
  };
}

/* ---- 3. UPSTREAM DASH ---- */
function initRace(){
  var g = canvasSetup(), W = g.w, H = g.h;
  var y = H/2, vy = 0, rocks = [], spawn = 0, dist = 0, dead = false;
  var img = ART.fujie_dash, rock = ART.rock_pillar, RW = 52;

  // Stack the pillar art at its own aspect ratio rather than stretching one copy
  // over the whole column, which smears the rock texture. `tipUp` puts the
  // jagged crystal end at the top of the rect instead of the bottom.
  function drawRock(x, top, h, tipUp){
    if (h <= 0) return;
    if (!rock.naturalWidth){
      g.x.fillStyle = "#1B4557"; g.x.fillRect(x, top, RW, h);
      g.x.strokeStyle = "#2D6479"; g.x.lineWidth = 2; g.x.strokeRect(x, top, RW, h);
      return;
    }
    var seg = RW * (rock.naturalHeight / rock.naturalWidth), o;
    g.x.save();
    g.x.beginPath(); g.x.rect(x, top, RW, h); g.x.clip();
    if (tipUp){
      g.x.translate(x, top); g.x.scale(1, -1);
      for (o = 0; o < h; o += seg) g.x.drawImage(rock, 0, -o - seg, RW, seg);
    } else {
      for (o = 0; o < h; o += seg) g.x.drawImage(rock, x, top + h - o - seg, RW, seg);
    }
    g.x.restore();
  }

  function flap(e){ e.preventDefault(); if (!dead) vy = -4.2; }
  g.c.addEventListener("pointerdown", flap);
  MG.cleanup = function(){ g.c.removeEventListener("pointerdown", flap); };

  function frame(){
    g.x.clearRect(0,0,W,H);
    // current streaks
    g.x.strokeStyle = "rgba(191,207,214,.10)"; g.x.lineWidth = 2;
    for (var s = 0; s < 7; s++){
      var sy = (s*H/7 + (dist*2)%(H/7));
      g.x.beginPath(); g.x.moveTo(0, sy); g.x.lineTo(W, sy); g.x.stroke();
    }
    vy += 0.22; y += vy;
    if (y < 24){ y = 24; vy = 0; }
    if (y > H-24){ y = H-24; vy = 0; }

    spawn--;
    if (spawn <= 0){
      var gapY = 60 + Math.random()*(H-120), gapH = 118;
      rocks.push({ x:W+30, gy:gapY, gh:gapH, passed:false });
      spawn = 78;
    }
    for (var i = rocks.length-1; i >= 0; i--){
      var r = rocks[i]; r.x -= 2.9;
      // the jagged crystal end always points into the gap
      drawRock(r.x, 0, r.gy - r.gh/2, false);
      drawRock(r.x, r.gy + r.gh/2, H - (r.gy + r.gh/2), true);
      if (!r.passed && r.x + RW < 60){ r.passed = true; bumpScore(1); }
      if (60+20 > r.x && 60-20 < r.x+RW &&
          (y-16 < r.gy - r.gh/2 || y+16 > r.gy + r.gh/2)){
        if (!dead){ dead = true; setTimeout(endMini, 700); }
      }
      if (r.x < -40) rocks.splice(i,1);
    }
    dist++;
    var fw = 96, fh = fw * (img.naturalHeight/img.naturalWidth || .42);
    g.x.save();
    g.x.translate(60, y);
    g.x.rotate(Math.max(-0.5, Math.min(0.5, vy*0.06)));
    if (img.naturalWidth) g.x.drawImage(img, -fw/2, -fh/2, fw, fh);
    g.x.restore();
    if (!dead) MG.raf = requestAnimationFrame(frame);
  }
  frame();
}

/* ---- 4. WHICH SHELL? ---- */
function initShell(){
  var wrap = $("miniDom"); wrap.innerHTML = '<div id="shells"></div>';
  var host = $("shells"), round = 0, busy = false;
  $("miniTime").textContent = L.round + " 1/5";

  var shells = [];
  for (var i = 0; i < 3; i++){
    var d = document.createElement("div");
    d.className = "shell";
    d.innerHTML = '<img class="pearlDot" src="art/pearl.png" alt="">' +
                  '<img class="shellImg" src="art/shell_closed.png" alt="">';
    (function(el, idx){
      el.addEventListener("pointerdown", function(){ pick(idx, el); });
    })(d, i);
    host.appendChild(d); shells.push(d);
  }
  var answer = 0;

  function newRound(){
    busy = true;
    round++;
    $("miniTime").textContent = L.round + " " + Math.min(round,5) + "/5";
    answer = Math.floor(Math.random()*3);
    shells.forEach(function(s,i){
      s.classList.remove("lift");
      s.querySelector(".pearlDot").style.opacity = i === answer ? "1" : "0";
    });
    shells[answer].classList.add("lift");
    setTimeout(function(){
      shells.forEach(function(s){
        s.classList.remove("lift");
        s.querySelector(".pearlDot").style.opacity = "0";
      });
      shuffle(0);
    }, 900);
  }
  function shuffle(n){
    if (n >= 5 + round){ busy = false; $("miniFoot").textContent = L.ctl_shell; return; }
    $("miniFoot").textContent = "…";
    shells.forEach(function(s){
      var dx = (Math.random()-0.5) * 90;
      s.style.transform = "translateX(" + dx + "px)";
    });
    setTimeout(function(){
      shells.forEach(function(s){ s.style.transform = ""; });
      setTimeout(function(){ shuffle(n+1); }, 130);
    }, 170);
  }
  function pick(i, el){
    if (busy) return;
    busy = true;
    el.classList.add("lift");
    var ok = i === answer;
    el.querySelector(".pearlDot").style.opacity = ok ? "1" : "0";
    if (!ok){ shells[answer].classList.add("lift");
              shells[answer].querySelector(".pearlDot").style.opacity = "1"; }
    if (ok) bumpScore(2);
    $("miniFoot").textContent = ok ? L.correct : L.wrong;
    setTimeout(function(){
      if (round >= 5) endMini();
      else newRound();
    }, 1100);
  }
  newRound();
  MG.cleanup = function(){};
}

$("gEgg").addEventListener("click", function(){ startMini("egg"); });
$("gShark").addEventListener("click", function(){ startMini("shark"); });
$("gRace").addEventListener("click", function(){ startMini("race"); });
$("gShell").addEventListener("click", function(){ startMini("shell"); });

/* ---------------- endings ---------------- */
function end(won){
  S.over = true;
  clearInterval(timer); timer = null;
  $("note").classList.remove("on");
  $("bubble").classList.remove("on");
  if (won) $("winYears").textContent = L.winDays + " : " + Math.floor(S.t/60) + (lang==="ja"?" 年":" yrs");
  $(won ? "winScreen" : "lostScreen").classList.add("on");
}

function start(){
  S = fresh(); shown = {};
  $("flow").value = S.flow;
  $("note").classList.remove("on");
  document.querySelectorAll(".screen").forEach(function(s){ s.classList.remove("on"); });
  closeSheets();
  S.stage = -1; setStage(); drawZone(); paint();
  clearInterval(timer);
  timer = setInterval(tick, 100);
}
$("startBtn").addEventListener("click", start);
$("retryBtn").addEventListener("click", start);
$("againBtn").addEventListener("click", start);

/* ---------------- ambient bubbles ---------------- */
var cv = $("bubbles"), cx = cv.getContext("2d"), B = [];
function sizeC(){ var r = $("tank").getBoundingClientRect(); cv.width = r.width; cv.height = r.height; }
addEventListener("resize", sizeC); setTimeout(sizeC, 60);
for (var i = 0; i < 30; i++) B.push({ x:Math.random(), y:Math.random(),
  r:Math.random()*1.8+.4, s:Math.random()*.0022+.0006, o:Math.random()*.26+.06 });
(function loop(){
  if (cv.width){
    cx.clearRect(0,0,cv.width,cv.height);
    for (var n = 0; n < B.length; n++){
      var q = B[n]; q.y -= q.s; if (q.y < -0.02){ q.y = 1.02; q.x = Math.random(); }
      cx.beginPath(); cx.arc(q.x*cv.width, q.y*cv.height, q.r, 0, 6.2832);
      cx.fillStyle = "rgba(191,207,214," + q.o + ")"; cx.fill();
    }
  }
  requestAnimationFrame(loop);
})();

/* ---------------- boot ---------------- */
S = fresh();
applyLang();
setStage(); drawZone(); paint();
})();
