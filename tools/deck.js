const pptx = require("pptxgenjs");
const P = new pptx();
P.layout = "LAYOUT_WIDE"; // 13.3 x 7.5

/* ---------------- design system ---------------- */
const C = {
  deep:   "0B2430",  // deep tank water - dominant dark
  deeper: "061620",
  mid:    "12323F",  // card on dark
  light:  "F2F6F7",  // light ground
  card:   "FFFFFF",
  steel:  "BFCFD6",
  cyan:   "00A0E9",  // Fujikin corporate blue
  ink:    "0A1419",
  muted:  "5A7480",
  dimOnDark: "8FA9B4",
  roe:    "0A0806",
};
const FH = "Yu Gothic";   // headings
const FB = "Meiryo";      // body

/* The way we want the judges to see this: the whole studio, live, in a browser.
   It is unlisted and carries a no-index instruction, so it works for anyone who
   has the link and cannot be found by searching. Printed on the cover, on the
   game slide and on the closing slide, because a link buried once gets missed.
   The offline file attached to the mail is the fallback, not the main route. */
const LIVE = "https://don-bp.github.io/fuji_famous/studio-fa519005bf/";
const IMG = "D:/Fuji_Famous/Fujie_Creative/";

const W = 13.3, H = 7.5, M = 0.75;

function dark(s, deeper) {
  s.background = { color: deeper ? C.deeper : C.deep };
}
function light(s) {
  s.background = { color: C.light };
}
function title(s, txt, opts) {
  const o = Object.assign({
    x: M, y: 0.62, w: W - M * 2, h: 1.15,
    fontFace: FH, fontSize: 34, bold: true, color: C.ink,
    align: "left", valign: "top", isTextBox: true, margin: 0, lineSpacing: 46,
  }, opts || {});
  s.addText(txt, o);
}
function eyebrow(s, txt, onDark, y) {
  s.addText(txt, {
    x: M, y: y === undefined ? 0.34 : y, w: W - M * 2, h: 0.3,
    fontFace: FB, fontSize: 11, bold: true, charSpacing: 3,
    color: onDark ? C.cyan : C.cyan, isTextBox: true, margin: 0,
  });
}
function body(s, txt, o) {
  s.addText(txt, Object.assign({
    fontFace: FB, fontSize: 14, color: C.muted, lineSpacing: 26,
    isTextBox: true, margin: 0, valign: "top",
  }, o));
}
function numDot(s, n, x, y, onDark) {
  s.addShape(P.ShapeType.ellipse, {
    x: x, y: y, w: 0.42, h: 0.42,
    fill: { color: C.cyan }, line: { color: C.cyan, width: 0 },
  });
  s.addText(String(n), {
    x: x, y: y, w: 0.42, h: 0.42, fontFace: FH, fontSize: 14, bold: true,
    color: "FFFFFF", align: "center", valign: "middle", isTextBox: true, margin: 0,
  });
}
function card(s, x, y, w, h, onDark) {
  s.addShape(P.ShapeType.roundRect, {
    x: x, y: y, w: w, h: h, rectRadius: 0.06,
    fill: { color: onDark ? C.mid : C.card },
    line: { color: onDark ? C.mid : "E2EAED", width: 1 },
  });
}
/* Images.
   pptxgenjs's `sizing` option does not survive into the file - every picture came
   out as a plain stretch filling its box, so tall art was squashed and wide art
   pulled. So we read each file's real pixel size and place it at its own aspect
   ratio, fitted inside the box we wanted it to occupy and centred there.
   `align`/`valign` pin it to an edge of that box instead. */
const fs = require("fs");
const SIZE_CACHE = {};

function pixels(file) {
  if (SIZE_CACHE[file]) return SIZE_CACHE[file];
  const b = fs.readFileSync(file);
  let d = null;
  if (b[0] === 0x89 && b[1] === 0x50) {                       // PNG: IHDR
    d = { w: b.readUInt32BE(16), h: b.readUInt32BE(20) };
  } else if (b[0] === 0xFF && b[1] === 0xD8) {                // JPEG: first SOFn
    let i = 2;
    while (i < b.length - 9) {
      if (b[i] !== 0xFF) { i++; continue; }
      const m = b[i + 1];
      if (m >= 0xC0 && m <= 0xCF && m !== 0xC4 && m !== 0xC8 && m !== 0xCC) {
        d = { h: b.readUInt16BE(i + 5), w: b.readUInt16BE(i + 7) };
        break;
      }
      i += 2 + b.readUInt16BE(i + 2);
    }
  }
  if (!d) throw new Error("could not read image size: " + file);
  SIZE_CACHE[file] = d;
  return d;
}

function img(s, file, x, y, bw, bh, o) {
  o = o || {};
  const path = IMG + file, d = pixels(path), ar = d.w / d.h;
  let w = bw, h = bw / ar;
  if (h > bh) { h = bh; w = bh * ar; }
  const ax = o.align || "center", ay = o.valign || "middle";
  const px = ax === "left" ? x : ax === "right" ? x + bw - w : x + (bw - w) / 2;
  const py = ay === "top" ? y : ay === "bottom" ? y + bh - h : y + (bh - h) / 2;
  s.addImage({ path: path, x: px, y: py, w: w, h: h });
}

function foot(s, txt, onDark) {
  s.addText(txt, {
    x: M, y: H - 0.55, w: W - M * 2, h: 0.3, fontFace: FB, fontSize: 9.5,
    color: onDark ? "4E6874" : "9BB0BA", isTextBox: true, margin: 0,
  });
}

/* =============== 1. TITLE =============== */
let s = P.addSlide(); dark(s, true);
img(s, "deck_assets/04_campaign/fujie-official.png", 6.4, 2.35, 6.6, 2.0);
s.addText("フジィを有名にする！アイデアコンテスト", {
  x: M, y: 1.55, w: 8, h: 0.34, fontFace: FB, fontSize: 12, bold: true,
  charSpacing: 2.5, color: C.cyan, isTextBox: true, margin: 0 });
s.addText("フジィは、\n実在する。", {
  x: M, y: 2.05, w: 7.2, h: 2.5, fontFace: FH, fontSize: 60, bold: true,
  color: "FFFFFF", lineSpacing: 74, isTextBox: true, margin: 0 });
s.addText("世界初の完全養殖という事実を起点に、\n十三の施策でフジィを「シンボル」から「キャラクター」へ。", {
  x: M, y: 4.62, w: 7.2, h: 0.9, fontFace: FB, fontSize: 14.5,
  color: C.steel, lineSpacing: 27, isTextBox: true, margin: 0 });
s.addShape(P.ShapeType.roundRect, { x: M, y: 5.62, w: 7.2, h: 0.55, rectRadius: 0.08,
  fill: { color: C.mid }, line: { color: C.cyan, width: 1 } });
s.addText([
  { text: "企画の全体像はこちらで　", options: { fontSize: 11, color: C.steel, bold: true } },
  { text: LIVE, options: { fontSize: 12, color: C.cyan, bold: true, hyperlink: { url: LIVE } } },
], { x: M + 0.3, y: 5.74, w: 6.6, h: 0.32, fontFace: FB, isTextBox: true, margin: 0 });
s.addText("株式会社ブレインパワー　大阪　／　Vittorio Zumpano", {
  x: M, y: H - 1.0, w: 7, h: 0.35, fontFace: FB, fontSize: 11.5,
  color: C.dimOnDark, isTextBox: true, margin: 0 });
s.addNotes("表紙。結論を先に置く：フジィは想像上のキャラクターではなく、フジキンが実際に育てている魚である。企画の全体像は表紙のリンクからそのまま開ける。");

/* =============== 2. 課題 =============== */
s = P.addSlide(); light(s);
eyebrow(s, "課題");
title(s, "問題は「知られていない」ことではない。\n「語る材料」が表に出ていないことである。");
body(s, "募集要項にはこうあります ——「半導体業界などで高い知名度を誇る企業ですが、一般層にはまだ広く知られていない」。\nしかしフジキンには、一般層がもっとも強く反応する材料が、すでに社内にあります。それがフジィと結びついていないだけです。",
  { x: M, y: 2.35, w: 11.8, h: 1.1, fontSize: 14.5 });

const stats = [
  ["114", "公式Instagram\nフォロワー数", "売上 2,212 億円・従業員 6,742 名の企業として"],
  ["0", "一般消費者向けの\n自社商品", "キャビアは飲食店・卸売のみへ販売"],
  ["40年", "語られていない\n挑戦の記録", "1987 年から続く世界初への道のり"],
];
stats.forEach((st, i) => {
  const x = M + i * 4.03;
  card(s, x, 3.9, 3.75, 2.35);
  s.addText(st[0], { x: x + 0.35, y: 4.12, w: 3.05, h: 0.85, fontFace: FH, fontSize: 40,
    bold: true, color: C.cyan, isTextBox: true, margin: 0 });
  s.addText(st[1], { x: x + 0.35, y: 5.0, w: 3.05, h: 0.62, fontFace: FB, fontSize: 12.5,
    bold: true, color: C.ink, lineSpacing: 18, isTextBox: true, margin: 0 });
  s.addText(st[2], { x: x + 0.35, y: 5.66, w: 3.05, h: 0.5, fontFace: FB, fontSize: 10,
    color: C.muted, lineSpacing: 15, isTextBox: true, margin: 0 });
});
foot(s, "出典：募集概要、フジキン会社概要（2026年3月期）、公式Instagram");

/* =============== 3. 診断 =============== */
s = P.addSlide(); light(s);
eyebrow(s, "診断");
title(s, "フジィは「シンボル」であって、\nまだ「キャラクター」ではない。");
body(s, "マニュアル第 7 条は正しい。企業シンボルは厳格に守られるべきです。しかしシンボルのままでは、有名にはなれません。",
  { x: M, y: 2.35, w: 11.8, h: 0.6, fontSize: 14.5 });

const cols = [
  ["シンボル", "いまのフジィ", ["企業の信頼を示す", "製品の品質を象徴する", "広告・会社案内で映える"],
   ["笑うことができない", "動くことができない", "抱きしめられない", "ファンが描けない"], C.muted],
  ["キャラクター", "必要なフジィ", ["感情を持つ", "日常に入り込む", "グッズになれる", "人が共有したくなる"],
   [], C.cyan],
];
cols.forEach((col, i) => {
  const x = M + i * 6.05;
  card(s, x, 3.3, 5.75, 3.35);
  s.addText(col[0], { x: x + 0.45, y: 3.55, w: 4.9, h: 0.45, fontFace: FH, fontSize: 21,
    bold: true, color: col[4], isTextBox: true, margin: 0 });
  s.addText(col[1], { x: x + 0.45, y: 4.02, w: 4.9, h: 0.3, fontFace: FB, fontSize: 10.5,
    color: C.muted, isTextBox: true, margin: 0 });
  const canDo = col[2].map((t, n) => ({ text: "できる：" + t, options: { breakLine: n < col[2].length - 1 } }));
  s.addText(canDo, { x: x + 0.45, y: 4.45, w: 4.9, h: 1.0, fontFace: FB, fontSize: 11.5,
    color: C.ink, lineSpacing: 20, isTextBox: true, margin: 0 });
  if (col[3].length) {
    const cant = col[3].map((t, n) => ({ text: "できない：" + t, options: { breakLine: n < col[3].length - 1 } }));
    s.addText(cant, { x: x + 0.45, y: 5.45, w: 4.9, h: 1.0, fontFace: FB, fontSize: 11.5,
      color: "B04A4A", lineSpacing: 20, isTextBox: true, margin: 0 });
  } else {
    img(s, "deck_assets/01_character/master_v3_wave.jpg", x + 3.15, 4.8, 2.35, 1.75);
  }
});

/* =============== 4. REVEAL =============== */
s = P.addSlide(); dark(s, true);
img(s, "deck_assets/04_campaign/stage_4_young.png", 7.6, 1.5, 5.2, 4.4);
eyebrow(s, "この企画の起点", true, 1.5);
s.addText("フジィは、実在する。", {
  x: M, y: 2.0, w: 7.0, h: 1.3, fontFace: FH, fontSize: 46, bold: true,
  color: "FFFFFF", isTextBox: true, margin: 0 });
s.addText("10,000", { x: M, y: 3.5, w: 4.2, h: 1.1, fontFace: FH, fontSize: 64, bold: true,
  color: C.cyan, isTextBox: true, margin: 0 });
s.addText("尾 以上", { x: 3.55, y: 4.16, w: 2, h: 0.4, fontFace: FB, fontSize: 15,
  color: C.steel, isTextBox: true, margin: 0 });
s.addText("茨城県常陸太田市・里美養魚場。\nフジィは想像上の生きものではありません。フジキンが 40 年かけて、\n本当に育ててきた魚です。", {
  x: M, y: 4.85, w: 6.6, h: 1.3, fontFace: FB, fontSize: 14, color: C.steel,
  lineSpacing: 26, isTextBox: true, margin: 0 });

/* =============== 5. 絶滅危惧種 =============== */
s = P.addSlide(); dark(s, true);
img(s, "15_act2/endangered_water.jpg", 7.15, 1.35, 5.4, 3.05);
eyebrow(s, "この魚について", true, 1.35);
s.addText("フジィは、実在する。\n──そして、絶滅危惧種である。", {
  x: M, y: 1.95, w: 6.3, h: 1.6, fontFace: FH, fontSize: 26, bold: true,
  color: "FFFFFF", lineSpacing: 40, isTextBox: true, margin: 0 });
s.addText("チョウザメは、IUCN レッドリストで「もっとも絶滅の危機にある生物群」とされています。\n現存する全種が、絶滅危惧種です。",
  { x: M, y: 4.1, w: 6.2, h: 0.9, fontFace: FB, fontSize: 12.5, color: C.steel,
    lineSpacing: 22, isTextBox: true, margin: 0 });
const rare = [
  ["2 億年", "恐竜より古く、ほとんど姿を変えなかった魚。\n「進化」を名に持つフジィは、進化する\n必要がなかった魚でもあります。"],
  ["全 種", "現存するチョウザメは、すべて絶滅危惧種。\nキャビアのために、世界中で獲られ続けました。"],
  ["1998 年", "完全養殖の成立以降、この魚は水槽の中だけで\n世代をつないでいます。川から獲る必要が、ない。"],
];
rare.forEach((r, i) => {
  const x = M + i * 4.03;
  s.addShape(P.ShapeType.roundRect, { x: x, y: 5.05, w: 3.8, h: 1.55, rectRadius: 0.06,
    fill: { color: C.mid }, line: { color: C.mid, width: 0 } });
  s.addText(r[0], { x: x + 0.3, y: 5.22, w: 3.2, h: 0.45, fontFace: FH, fontSize: 19,
    bold: true, color: C.cyan, isTextBox: true, margin: 0 });
  s.addText(r[1], { x: x + 0.3, y: 5.72, w: 3.25, h: 0.8, fontFace: FB, fontSize: 10,
    color: C.steel, lineSpacing: 16, isTextBox: true, margin: 0 });
});
s.addText("フジキンがつくったのは、珍味ではありません。「もう川から獲らなくていい」という技術です。", {
  x: M, y: 6.8, w: 11.8, h: 0.4, fontFace: FB, fontSize: 13, bold: true,
  color: "FFFFFF", isTextBox: true, margin: 0 });
s.addNotes("物語に「重さ」を与えるスライド。キャビアの話を、食の話から保全の話へ引き上げる。統合報告書・サステナビリティ部門にも共有できる論点になる。");

/* =============== 6. TIMELINE =============== */
s = P.addSlide(); light(s);
eyebrow(s, "物語");
title(s, "バルブメーカーが、日本の国産キャビアを生んだ。");
const tl = [
  ["1987", "始まり", "最高技術顧問・故 西堀栄三郎先生の一言。\n「フジキンのバルブを使って、\nチョウザメの養殖を始めてみないか？」"],
  ["1992", "民間初", "日本の民間企業として初めて\n人工ふ化に成功。\nしかし初年度の生残率はわずか 5%。"],
  ["1998", "世界初", "水槽での完全養殖に成功。\n生残率は 60% へ。\n卵から育てた魚が、また卵を産んだ。"],
  ["2002", "日本初", "日本初のキャビア出荷。\nいま国内に流通する国産キャビアの\n多くは、ここから広がっている。"],
];
tl.forEach((t, i) => {
  const x = M + i * 3.03;
  s.addText(t[0], { x: x, y: 2.5, w: 2.8, h: 0.75, fontFace: FH, fontSize: 36, bold: true,
    color: i === 2 ? C.cyan : C.steel, isTextBox: true, margin: 0 });
  s.addText(t[1], { x: x, y: 3.24, w: 2.8, h: 0.34, fontFace: FB, fontSize: 12, bold: true,
    color: C.ink, isTextBox: true, margin: 0 });
  s.addText(t[2], { x: x, y: 3.66, w: 2.8, h: 1.7, fontFace: FB, fontSize: 11,
    color: C.muted, lineSpacing: 19, isTextBox: true, margin: 0 });
});
card(s, M, 5.55, 11.8, 1.05);
s.addText("この 11 年間こそ、企業ポリシー「極限への挑戦」そのものです。説明する言葉ではなく、実話として語れます。", {
  x: M + 0.45, y: 5.75, w: 10.9, h: 0.4, fontFace: FB, fontSize: 13.5, bold: true,
  color: C.ink, isTextBox: true, margin: 0 });
s.addText("フジィは、この物語の魚です。いま里美養魚場に泳ぐ 1 万尾は一尾残らずこの物語の続きで、会社案内の銀色の魚は、その 1 万尾の顔です。", {
  x: M + 0.45, y: 6.15, w: 10.9, h: 0.35, fontFace: FB, fontSize: 11.5,
  color: C.cyan, isTextBox: true, margin: 0 });

/* =============== 6. WHY STORY =============== */
s = P.addSlide(); light(s);
eyebrow(s, "方針");
title(s, "グッズは配り終わる。\n物語は、人が人に話す。");
body(s, "募集要項にも「グッズ製作などの枠にとどまらない、幅広い視点のアイデア」とあります。本企画はグッズを否定しません。順序を変えます —— 物語を先に立て、グッズはその受け皿にします。",
  { x: M, y: 2.4, w: 11.8, h: 0.9, fontSize: 14.5 });
const ways = [
  ["従来の順序", "グッズをつくる　→　配る　→　終わる", "配布数が上限。話題は一度きり。", "9BB0BA"],
  ["本企画の順序", "物語を立てる　→　キャラクターが受け皿になる　→　人が人に話す", "「バルブの会社が日本のキャビアをつくった」は、聞いた人が翌日 誰かに話したくなる強度を持っています。広告費をかけずに伝播する、唯一の資産です。", C.cyan],
];
ways.forEach((w2, i) => {
  const y = 3.5 + i * 1.6;
  card(s, M, y, 11.8, 1.4);
  s.addText(w2[0], { x: M + 0.45, y: y + 0.2, w: 2.4, h: 0.35, fontFace: FH, fontSize: 14,
    bold: true, color: w2[3], isTextBox: true, margin: 0 });
  s.addText(w2[1], { x: M + 2.95, y: y + 0.18, w: 8.5, h: 0.38, fontFace: FB, fontSize: 13,
    bold: true, color: C.ink, isTextBox: true, margin: 0 });
  s.addText(w2[2], { x: M + 2.95, y: y + 0.63, w: 8.5, h: 0.65, fontFace: FB, fontSize: 11,
    color: C.muted, lineSpacing: 18, isTextBox: true, margin: 0 });
});

/* =============== 8. サメじゃないです =============== */
s = P.addSlide(); light(s);
eyebrow(s, "入口");
title(s, "「サメじゃないです。」", { y: 0.75 });
body(s, "チョウザメは「蝶のサメ」と書くため、ほぼ全員が最初にサメだと思います。フジキンのキャビアサイトにも「サメとの違い」というページがあるほどです。\nならば、誤解を直す努力をやめて、誤解のほうを入口にします。",
  { x: M, y: 2.35, w: 6.75, h: 1.3, fontSize: 13 });
img(s, "15_act2/shark_vs_sturgeon_cut.png", 7.75, 1.95, 4.8, 2.7);
const diff = [
  ["サメ", "歯がある／軟骨魚／海／ヒゲなし", "9BB0BA"],
  ["チョウザメ", "歯がない／硬骨魚／淡水／ヒゲ 4 本・背中に硬い板", C.cyan],
];
diff.forEach((d, i) => {
  const y = 3.82 + i * 0.74;
  card(s, M, y, 7.1, 0.62);
  s.addText(d[0], { x: M + 0.35, y: y + 0.15, w: 1.75, h: 0.34, fontFace: FH, fontSize: 13.5,
    bold: true, color: d[2], isTextBox: true, margin: 0 });
  s.addText(d[1], { x: M + 2.15, y: y + 0.17, w: 4.8, h: 0.34, fontFace: FB, fontSize: 11.5,
    color: C.ink, isTextBox: true, margin: 0 });
});
s.addShape(P.ShapeType.roundRect, { x: M, y: 5.4, w: 11.8, h: 1.2, rectRadius: 0.06,
  fill: { color: C.deep }, line: { color: C.deep, width: 0 } });
s.addText("「サメじゃないです。」　→　「サメより、ずっと少ないんです。」", {
  x: M + 0.45, y: 5.6, w: 10.9, h: 0.42, fontFace: FH, fontSize: 17, bold: true,
  color: "FFFFFF", isTextBox: true, margin: 0 });
s.addText("冗談で入口を開け、事実で残す。この二行で「チョウザメとは何か」と「なぜ大切か」が同時に伝わります。スタンプもグッズもミニゲームも、すべてここから展開できます。", {
  x: M + 0.45, y: 6.08, w: 10.9, h: 0.35, fontFace: FB, fontSize: 10.5,
  color: C.steel, isTextBox: true, margin: 0 });
foot(s, "※ この一言を発するのは「ちびフジィ」です。公式フジィに文字を重ねることはしません（マニュアル第 7 条）。");
s.addNotes("キャラクターの最大の弱点（サメに見える）を、そのまま最大の入口に変える。フジキン自身のサイトが根拠。");

/* =============== 9. SIX MOVES =============== */
s = P.addSlide(); dark(s);
eyebrow(s, "全体像", true);
s.addText("11 の施策", { x: M, y: 0.62, w: 8, h: 0.8, fontFace: FH, fontSize: 34,
  bold: true, color: "FFFFFF", isTextBox: true, margin: 0 });
s.addText("上から順に実施します。①がなければ②以降は成立しません。", {
  x: M, y: 1.5, w: 9, h: 0.35, fontFace: FB, fontSize: 13, color: C.steel,
  isTextBox: true, margin: 0 });
const moves = [
  ["ちびフジィ", "表情と親しみを担う第 2 の姿を公式に追加する"],
  ["LINE スタンプ 128 種", "友だち追加を条件に無料配布する"],
  ["フジィに「中の人」を", "誰も見たことのない養魚場の映像を出す"],
  ["ちびフジィの無償開放", "稚魚取引先のパッケージを広告に変える"],
  ["会いに行けるマスコット", "里美養魚場を限定公開する"],
  ["1987 年の物語を映像化", "ロケ地はすべて自社保有"],
  ["水族館のサメの隣に", "アクアワールド大洗に本物のフジィの水槽を"],
  ["100 年の手紙", "同い年の「2027 年組」に書き、100 周年に開封"],
  ["フジィのマンホール", "常陸太田市内に 3〜5 枚"],
  ["年に一度の公開日", "地元 40 家族。手紙と、はじめてのキャビア"],
  ["「チョウザメの日」を登録", "日本記念日協会へ。誕生日と公開日を重ねる"],
];
moves.forEach((m, i) => {
  const col = i % 3, row = Math.floor(i / 3);
  const x = M + col * 4.03, y = 2.05 + row * 1.2;
  card(s, x, y, 3.8, 1.05, true);
  numDot(s, i + 1, x + 0.3, y + 0.34, true);
  s.addText(m[0], { x: x + 0.85, y: y + 0.14, w: 2.85, h: 0.34, fontFace: FH, fontSize: 12.5,
    bold: true, color: "FFFFFF", isTextBox: true, margin: 0 });
  s.addText(m[1], { x: x + 0.85, y: y + 0.5, w: 2.85, h: 0.48, fontFace: FB, fontSize: 9.5,
    color: C.dimOnDark, lineSpacing: 14, isTextBox: true, margin: 0 });
});

/* =============== 8. 施策1 ちびフジィ =============== */
s = P.addSlide(); light(s);
eyebrow(s, "施策 1");
title(s, "ちびフジィ ―― 表情を持つ、第 2 の姿。");
body(s, "現行マニュアルの規定は一切変更しません。従来のフジィは企業シンボルとして厳格に保護したまま、\n公の場で人と接するための姿を新たに追加します。",
  { x: M, y: 2.3, w: 11.8, h: 0.8, fontSize: 14 });
img(s, "deck_assets/01_character/master_v3_wave.jpg", M, 3.15, 3.5, 3.3);
img(s, "deck_assets/01_character/master_expressions.jpg", 4.6, 3.15, 7.95, 3.3);
s.addNotes("チョウザメの特徴（銀色のボディ、長い吻、背中の硬鱗、4本のひげ、大きな黒い目）はすべて継承。ひれのみで、脚はありません。");

/* =============== 9. マニュアル遵守 =============== */
s = P.addSlide(); light(s);
eyebrow(s, "施策 1 ―― マニュアルとの関係");
title(s, "第 7 条は、破りません。足します。");
const rel = [
  ["従来のフジィ", "企業シンボル", "会社案内・広告・名刺・製品資料\n\nマニュアル ver1.0 の規定どおり、変形・色変更・透過・\n文字の重ね・デザイン変更・要素の追加削除は一切行いません。", C.ink, "E2EAED"],
  ["ちびフジィ", "パブリック・キャラクター", "SNS・スタンプ・グッズ・イベント・地域連携\n\nマニュアル ver2.0 として新たに規定を設け、\n表情差分や利用ルールを整備します。", C.cyan, C.cyan],
];
rel.forEach((r, i) => {
  const x = M + i * 6.05;
  s.addShape(P.ShapeType.roundRect, { x: x, y: 2.5, w: 5.75, h: 3.9, rectRadius: 0.06,
    fill: { color: C.card }, line: { color: r[4], width: i === 1 ? 2 : 1 } });
  s.addText(r[0], { x: x + 0.45, y: 2.8, w: 4.9, h: 0.45, fontFace: FH, fontSize: 20,
    bold: true, color: r[3], isTextBox: true, margin: 0 });
  s.addText(r[1], { x: x + 0.45, y: 3.3, w: 4.9, h: 0.32, fontFace: FB, fontSize: 11,
    bold: true, color: C.muted, isTextBox: true, margin: 0 });
  s.addText(r[2], { x: x + 0.45, y: 3.8, w: 4.9, h: 2.3, fontFace: FB, fontSize: 11.5,
    color: C.muted, lineSpacing: 20, isTextBox: true, margin: 0 });
});
foot(s, "シンボルは守り、キャラクターは育てる。両立させるための提案です。");

/* =============== 10. LINEスタンプ =============== */
s = P.addSlide(); light(s);
eyebrow(s, "施策 2");
title(s, "LINE スタンプ 128 種を、無料配布する。");
body(s, "日本でもっとも費用対効果の高い認知獲得手段です。スタンプは「友人が」「私的な会話の中で」「自発的に」送るため、広告では決して到達できない場所に届きます。一度制作すれば、送信されるたびに露出が続きます。",
  { x: M, y: 2.3, w: 11.8, h: 0.85, fontSize: 13.5 });
img(s, "deck_assets/02_stickers/sticker_board_01.jpg", M, 3.2, 3.6, 3.4);
img(s, "deck_assets/02_stickers/sticker_board_02.jpg", 4.5, 3.2, 3.6, 3.4);
card(s, 8.45, 3.2, 4.1, 3.4);
s.addText("すでに制作済みです", { x: 8.85, y: 3.5, w: 3.3, h: 0.4, fontFace: FH, fontSize: 16,
  bold: true, color: C.cyan, isTextBox: true, margin: 0 });
s.addText([
  { text: "日常語 40 種：おはよう／ありがとう／おつかれさま ほか", options: { breakLine: true, bullet: true } },
  { text: "動きのある 24 種：ながれにのれ／ロケット／ハイタッチ ほか", options: { breakLine: true, bullet: true } },
  { text: "英語 64 種：海外拠点・WhatsApp にもそのまま使えます", options: { breakLine: true, bullet: true } },
  { text: "一番手は「サメじゃないです」。この一言が会話を始めます", options: { breakLine: true, bullet: true } },
  { text: "配布条件：公式アカウント友だち追加", options: { bullet: true } },
], { x: 8.85, y: 4.05, w: 3.3, h: 2.3, fontFace: FB, fontSize: 10.5, color: C.muted,
  lineSpacing: 17, paraSpaceAfter: 8, isTextBox: true, margin: 0 });

/* =============== 11. SNS =============== */
s = P.addSlide(); light(s);
eyebrow(s, "施策 3");
title(s, "フジィに「中の人」を。\n114 フォロワーは弱点ではなく、余白です。");
body(s, "誰も見たことのない映像を、フジキンだけが持っています。制作費はほぼかかりません。すでに社内にある光景です。",
  { x: M, y: 2.55, w: 11.8, h: 0.6, fontSize: 14 });
const sns = [
  ["1 万尾の給餌", "水面が一斉に沸き立つ数十秒。説明不要で強い映像です。"],
  ["ふ化の瞬間", "卵から出てくる一尾。40 年の研究の核心が数秒で伝わります。"],
  ["夜明けの養魚場", "静かな水面と作業の始まり。企業の日常が、そのまま物語になります。"],
  ["雌雄判別の技術", "フジキンが確立した専門ノウハウ。技術系メディアが反応します。"],
];
sns.forEach((n, i) => {
  const col = i % 2, row = Math.floor(i / 2);
  const x = M + col * 6.05, y = 3.35 + row * 1.6;
  card(s, x, y, 5.75, 1.38);
  numDot(s, i + 1, x + 0.38, y + 0.48);
  s.addText(n[0], { x: x + 1.0, y: y + 0.26, w: 4.5, h: 0.36, fontFace: FH, fontSize: 14.5,
    bold: true, color: C.ink, isTextBox: true, margin: 0 });
  s.addText(n[1], { x: x + 1.0, y: y + 0.68, w: 4.5, h: 0.55, fontFace: FB, fontSize: 10.5,
    color: C.muted, lineSpacing: 17, isTextBox: true, margin: 0 });
});

/* =============== 12. 無償開放 =============== */
s = P.addSlide(); light(s);
eyebrow(s, "施策 4 ―― 他社に真似できない施策");
title(s, "取引先のパッケージを、そのまま広告に変える。");
body(s, "フジキンはチョウザメの稚魚を全国の養殖業者へ販売しています。その取引先にちびフジィを無償開放すれば、日本中の国産キャビア生産者の商品に、フジィが載ります。追加費用はかからず、既存の取引網だけで成立します。",
  { x: M, y: 2.35, w: 11.8, h: 0.9, fontSize: 14 });
const loop = [
  ["フジキン", "稚魚を販売\n（既存事業）"],
  ["全国の養殖業者", "ちびフジィを\n無償で使用"],
  ["国産キャビア商品", "パッケージに\nフジィが載る"],
  ["一般消費者", "食卓でフジィと\n出会う"],
];
loop.forEach((l, i) => {
  const x = M + i * 3.16;
  s.addShape(P.ShapeType.roundRect, { x: x, y: 3.5, w: 2.75, h: 1.75, rectRadius: 0.06,
    fill: { color: i === 3 ? C.cyan : C.card }, line: { color: i === 3 ? C.cyan : "E2EAED", width: 1 } });
  s.addText(l[0], { x: x + 0.25, y: 3.78, w: 2.25, h: 0.42, fontFace: FH, fontSize: 14,
    bold: true, color: i === 3 ? "FFFFFF" : C.ink, isTextBox: true, margin: 0 });
  s.addText(l[1], { x: x + 0.25, y: 4.26, w: 2.25, h: 0.75, fontFace: FB, fontSize: 10.5,
    color: i === 3 ? "E8F6FD" : C.muted, lineSpacing: 17, isTextBox: true, margin: 0 });
  if (i < 3) {
    s.addText("→", { x: x + 2.78, y: 4.15, w: 0.38, h: 0.45, fontFace: FB, fontSize: 19,
      color: C.steel, align: "center", isTextBox: true, margin: 0 });
  }
});
card(s, M, 5.55, 11.8, 1.05);
s.addText("BtoB 企業が BtoC に到達する、現実的で低コストな経路です。フジキン以外の企業には、この取引網がありません。", {
  x: M + 0.45, y: 5.82, w: 10.9, h: 0.5, fontFace: FB, fontSize: 13.5, bold: true,
  color: C.ink, isTextBox: true, margin: 0 });

/* =============== 13. 会いに行ける =============== */
s = P.addSlide(); light(s);
eyebrow(s, "施策 5");
title(s, "日本で唯一、「餌やりができる」企業マスコットへ。");
body(s, "里美養魚場（茨城県常陸太田市）の限定公開。1 万尾の本物のフジィに会える場所をつくります。\n茨城県は「霞ヶ浦キャビア」で国内一の産地を目指しており、県・自治体・地元メディアを\n無償の拡散チャネルとして活用できます。",
  { x: M, y: 2.35, w: 7.5, h: 1.4, fontSize: 13 });
const visit = [
  ["小学校・自治体との連携", "地元の社会科見学・食育プログラムとして"],
  ["採用広報への転用", "学生が「極限への挑戦」を体験として理解する"],
  ["メディアの取材動線", "テレビ・新聞が撮りたくなる絵がある"],
];
visit.forEach((v, i) => {
  const y = 4.32 + i * 0.8;
  numDot(s, i + 1, M, y);
  s.addText(v[0], { x: M + 0.62, y: y - 0.02, w: 3.6, h: 0.3, fontFace: FH, fontSize: 12.5,
    bold: true, color: C.ink, isTextBox: true, margin: 0 });
  s.addText(v[1], { x: M + 0.62, y: y + 0.28, w: 6.6, h: 0.3, fontFace: FB, fontSize: 10.5,
    color: C.muted, isTextBox: true, margin: 0 });
});
img(s, "deck_assets/04_campaign/stage_3_fry.png", 8.6, 2.6, 4.0, 3.9);

/* =============== 14. 映像化 =============== */
s = P.addSlide(); dark(s);
eyebrow(s, "施策 6", true);
s.addText("1987 年の物語を、映像化する。", { x: M, y: 0.62, w: 11.8, h: 0.9,
  fontFace: FH, fontSize: 34, bold: true, color: "FFFFFF", isTextBox: true, margin: 0 });
s.addText("ロケ地はすべて自社保有。制作費以外の追加投資を必要としません。", {
  x: M, y: 1.6, w: 11.8, h: 0.35, fontFace: FB, fontSize: 13, color: C.steel,
  isTextBox: true, margin: 0 });
const film = [
  ["旧ソ連視察", "ボルガ川を行く船の上で、はじめて口にしたフレッシュキャビア。\nなぜ世界三大珍味なのかを、舌で理解した瞬間。"],
  ["生残率 5%", "100 尾のうち 95 尾が育たなかった初年度。\nこの数字こそ、物語の芯になります。"],
  ["世界初への 11 年", "1987 年の一言から 1998 年の完全養殖まで。\n企業ポリシー「極限への挑戦」の、最も具体的な証拠。"],
];
film.forEach((f, i) => {
  const x = M + i * 4.03;
  card(s, x, 2.4, 3.75, 3.5, true);
  numDot(s, i + 1, x + 0.4, 2.75, true);
  s.addText(f[0], { x: x + 0.4, y: 3.4, w: 3.0, h: 0.45, fontFace: FH, fontSize: 17,
    bold: true, color: C.cyan, isTextBox: true, margin: 0 });
  s.addText(f[1], { x: x + 0.4, y: 3.95, w: 3.0, h: 1.7, fontFace: FB, fontSize: 11,
    color: C.dimOnDark, lineSpacing: 19, isTextBox: true, margin: 0 });
});
foot(s, "短尺縦型（SNS）と長尺（会社案内・採用）の 2 形態で展開", true);

/* =============== 施策 7 =============== */
s = P.addSlide(); light(s);
eyebrow(s, "施策 7 ―― 水族館と組めば");
title(s, "サメの水槽の隣に、サメじゃない魚を。");
body(s, "アクアワールド茨城県大洗水族館はサメの展示で知られています。その隣に本物の展示水槽をひとつ設け、里美養魚場から来たフジィを何尾も泳がせます。パネルの一言は「サメじゃないです。サメより、ずっと少ないんです」。誰もがサメだと思う魚を、本物のサメの隣に。これ以上わかりやすい入口はありません。水族館の判断が前提の提案です。", { x: M, y: 2.35, w: 7.0, h: 2.0, fontSize: 13 });
const pts7 = [
  ["届く相手", "フジキンが自前では集められない規模の来館者に、年間を通じて"],
  ["好きになる理由", "水族館に来る人は、はじめから魚を好きになりに来ている"],
  ["最初の一歩", "2027 年度にチョウザメの展示水槽を提案。実現すれば 40 周年の企画展へ"],
];
pts7.forEach((v, i) => {
  const y = 4.45 + i * 0.78;
  numDot(s, i + 1, M, y);
  s.addText(v[0], { x: M + 0.62, y: y - 0.02, w: 4.2, h: 0.3, fontFace: FH, fontSize: 12.5,
    bold: true, color: C.ink, isTextBox: true, margin: 0 });
  s.addText(v[1], { x: M + 0.62, y: y + 0.28, w: 6.0, h: 0.3, fontFace: FB, fontSize: 10.5,
    color: C.muted, isTextBox: true, margin: 0 });
});
img(s, "deck_assets/20_new_ideas/aquaworld_c_both.jpg", 7.85, 3.10, 4.68, 3.52);

/* =============== 施策 8 =============== */
s = P.addSlide(); light(s);
eyebrow(s, "施策 8 ―― 同い年の魚に");
title(s, "100 年の手紙。");
body(s, "養魚場を訪れた子どもが、その年に卵からかえった「2027 年組」に手紙を書きます。封をして、開けるのは 2030 年、創業 100 周年の日。一尾ずつを追う必要はありません。魚は年ごとの組で育てられ、いつかえったかは必ずわかっています。チョウザメは人より長く生きることがあります。同い年の魚は、一生の相手になります。", { x: M, y: 2.35, w: 7.0, h: 2.0, fontSize: 13 });
const pts8 = [
  ["届く相手", "学校・家庭・地域。「預けたもの」としてフジキンの名前が残る"],
  ["好きになる理由", "「あの会社の魚」が「わたしの年の魚」になる"],
  ["最初の一歩", "2027 年の公開日に最初の手紙を集める。便箋と、封をする箱と、開封の日付だけ"],
];
pts8.forEach((v, i) => {
  const y = 4.45 + i * 0.78;
  numDot(s, i + 1, M, y);
  s.addText(v[0], { x: M + 0.62, y: y - 0.02, w: 4.2, h: 0.3, fontFace: FH, fontSize: 12.5,
    bold: true, color: C.ink, isTextBox: true, margin: 0 });
  s.addText(v[1], { x: M + 0.62, y: y + 0.28, w: 6.0, h: 0.3, fontFace: FB, fontSize: 10.5,
    color: C.muted, isTextBox: true, margin: 0 });
});
img(s, "deck_assets/20_new_ideas/letter_final.jpg", 7.85, 3.10, 4.68, 3.52);

/* =============== 施策 9 =============== */
s = P.addSlide(); light(s);
eyebrow(s, "施策 9 ―― 常陸太田市と");
title(s, "常陸太田に、フジィのマンホール。");
body(s, "駅前、市役所、養魚場の門。市内に 3〜5 枚。カラーの蓋には公式のフジィを原画どおりの色で（色の再現はマニュアル管理者の確認を条件に）、別の蓋にはちびフジィを。キャラクターのマンホールは日本では収集の対象で、地元紙が必ず報じ、蓋を巡って旅をする人がいます。", { x: M, y: 2.35, w: 7.0, h: 2.0, fontSize: 13 });
const pts9 = [
  ["届く相手", "見つけた人が自分で撮り、自分で載せる。写真は撮った本人が広める"],
  ["残るもの", "一度置けば何十年も。維持費はほぼなし。常陸太田が「フジィのふるさと」に"],
  ["最初の一歩", "2027 年度に市へ共同設置を提案。デザインは本エントリー添付を叩き台に"],
];
pts9.forEach((v, i) => {
  const y = 4.45 + i * 0.78;
  numDot(s, i + 1, M, y);
  s.addText(v[0], { x: M + 0.62, y: y - 0.02, w: 4.2, h: 0.3, fontFace: FH, fontSize: 12.5,
    bold: true, color: C.ink, isTextBox: true, margin: 0 });
  s.addText(v[1], { x: M + 0.62, y: y + 0.28, w: 6.0, h: 0.3, fontFace: FB, fontSize: 10.5,
    color: C.muted, isTextBox: true, margin: 0 });
});
img(s, "deck_assets/20_new_ideas/cover_set_sheet.jpg", 7.85, 3.10, 4.68, 3.52);

/* =============== 施策 10 =============== */
s = P.addSlide(); light(s);
eyebrow(s, "施策 10 ―― 里美養魚場");
title(s, "年に一度の公開日 ―― 手紙と、はじめてのキャビア。");
body(s, "抽選で選ばれた地元の 40 家族。午前は「2027 年組」への手紙、午後は小さな匙で、日本で初めてこの魚からつくられたキャビアを一口。1987 年にボルガ川の船の上でフジキンの社員が初めて口にしたのと、同じものです。40 席しかないから、話になります。ロケ地もキャビアも自社のもので、外に頼むものがありません。", { x: M, y: 2.35, w: 7.0, h: 2.0, fontSize: 13 });
const pts10 = [
  ["届く相手", "地元紙は毎年取材に来る。当たった家族は載せ、外れた家族は来年を待つ"],
  ["好きになる理由", "遠い高級品が、自分の町の誇りに変わる"],
  ["最初の一歩", "2027 年、初回は 40 家族から。応募は市の広報と公式アカウントで"],
];
pts10.forEach((v, i) => {
  const y = 4.45 + i * 0.78;
  numDot(s, i + 1, M, y);
  s.addText(v[0], { x: M + 0.62, y: y - 0.02, w: 4.2, h: 0.3, fontFace: FH, fontSize: 12.5,
    bold: true, color: C.ink, isTextBox: true, margin: 0 });
  s.addText(v[1], { x: M + 0.62, y: y + 0.28, w: 6.0, h: 0.3, fontFace: FB, fontSize: 10.5,
    color: C.muted, isTextBox: true, margin: 0 });
});
img(s, "deck_assets/20_new_ideas/openday_final.jpg", 7.85, 3.10, 4.68, 3.52);

/* =============== 施策 11 =============== */
s = P.addSlide(); light(s);
eyebrow(s, "施策 11 ―― 記念日登録");
title(s, "「チョウザメの日」を、正式に登録する。");
body(s, "日本記念日協会に登録すると、記念日はカレンダーや「今日は何の日」の枠に載り、地方紙や情報番組が毎年拾います。費用は登録料だけ。日付はフジィの誕生日（ふ化の季節に定めた日）とし、公開日と手紙をこの日に重ねます。現存するチョウザメは全種が絶滅危惧種ですが、この魚のための日はまだありません。", { x: M, y: 2.35, w: 7.0, h: 2.0, fontSize: 13 });
const pts11 = [
  ["届く相手", "毎年、何もしなくても一度は名前が出る日ができる"],
  ["好きになる理由", "一社のマスコットではなく、一つの種の顔になる"],
  ["最初の一歩", "2027 年度、日付を決めて登録。書類一式と登録料で済む"],
];
pts11.forEach((v, i) => {
  const y = 4.45 + i * 0.78;
  numDot(s, i + 1, M, y);
  s.addText(v[0], { x: M + 0.62, y: y - 0.02, w: 4.2, h: 0.3, fontFace: FH, fontSize: 12.5,
    bold: true, color: C.ink, isTextBox: true, margin: 0 });
  s.addText(v[1], { x: M + 0.62, y: y + 0.28, w: 6.0, h: 0.3, fontFace: FB, fontSize: 10.5,
    color: C.muted, isTextBox: true, margin: 0 });
});
img(s, "deck_assets/20_new_ideas/sday_final.jpg", 7.85, 3.10, 4.68, 3.52);

/* =============== 15. グッズ =============== */
s = P.addSlide(); light(s);
eyebrow(s, "受け皿となるグッズ");
title(s, "ぬいぐるみは、3 サイズで「成長」を見せる。");
body(s, "稚魚・幼魚・成魚。フジキンが世界で初めて成功させた「完全養殖」＝ 一生をまるごと育てる技術が、そのまま商品ラインになります。グッズが物語を説明してくれます。",
  { x: M, y: 2.3, w: 11.8, h: 0.8, fontSize: 13.5 });
img(s, "deck_assets/03_plushie/plush_size_lineup.jpg", M, 3.15, 7.3, 3.3);
img(s, "deck_assets/03_plushie/plush_keychain_lifestyle.jpg", 8.35, 3.15, 2.0, 3.3);
img(s, "deck_assets/03_plushie/plush_studio_front.jpg", 10.5, 3.15, 2.05, 3.3);
/* The keychain had a slide to itself, arguing a six-variant blind-box
   assortment. That assortment was dropped - six photographs of one sewn toy
   only ever read as one toy photographed six times - and the portfolio site
   now shows a single design, so the slide was promising the reviewer
   something the site does not deliver. The keychain is simply the smallest
   plush, and this slide already says so: the 10cm IS the keychain. Its one
   argument worth keeping - cheapest, travels furthest, seen every day - moves
   into the line below. */
foot(s, "10cm キーホルダー／25cm／50cm。いちばん小さい 10cm がいちばん安く、鞄に下がって毎日人目に触れます。いずれも試作イメージです。");

/* =============== 15b. 五つの棚 =============== */
s = P.addSlide(); light(s);
eyebrow(s, "受け皿となるグッズ");
title(s, "一匹の魚から、五つの棚。");
body(s, "同じ一匹から、客層のちがう棚をつくります。子どもの棚、贈答の棚、旅の棚、文様の棚、工芸の棚。公式原画を使う棚では、マニュアル第 7 条のとおり原画に一切手を入れていません。",
  { x: M, y: 2.25, w: 11.8, h: 0.8, fontSize: 13.5 });
[
  ["ちびフジィ", "07_merch_chibi/gacha_capsule_set.jpg", "見学者センターとガチャ"],
  ["公式ライン", "12_merch_official_2/official_gift_set.jpg", "贈答と式典"],
  ["Maison Fujie", "09_merch_maison/maison_tote.jpg", "革と帆布"],
  ["和紋", "13_merch_wamon/wamon_shop_table.jpg", "文様を持ちあるく"],
  ["和", "10_merch_wa/wa_ukiyoe_wave.jpg", "工芸のことば"],
].forEach((it, i) => {
  const x = M + i * 2.37;
  card(s, x, 3.15, 2.2, 3.35);
  img(s, "deck_assets/" + it[1], x + 0.1, 3.25, 2.0, 2.05);
  s.addText(it[0], { x: x + 0.12, y: 5.45, w: 1.96, h: 0.34, fontFace: FH, fontSize: 13,
    bold: true, color: C.ink, align: "center", isTextBox: true, margin: 0 });
  s.addText(it[2], { x: x + 0.06, y: 5.82, w: 2.08, h: 0.5, fontFace: FB, fontSize: 9.5,
    color: C.muted, align: "center", lineSpacing: 14, isTextBox: true, margin: 0 });
});
foot(s, "全 100 点超を制作済み。全点は添付のポートフォリオサイトでご覧いただけます。");

/* =============== 15c. 富士 =============== */
s = P.addSlide(); light(s);
eyebrow(s, "もう一つの意匠");
title(s, "フジキンの名は、富士に由来する。");
body(s, "社名の由来がそのまま意匠になります。水にくわえて富士を据えると、五つの棚すべてが一本の筋でつながります。浮世絵の遠景に、金屏風の右隻に、青海波を抜いた白地に、絹の中央に、そして 40 周年の記章に。",
  { x: M, y: 2.25, w: 11.8, h: 0.9, fontSize: 13.5 });
card(s, M, 3.2, 6.15, 3.3);
img(s, "deck_assets/19_fujisan/wa/wa_fuji_ukiyoe.jpg", M + 0.1, 3.3, 5.95, 3.1);
[
  ["19_fujisan/badge_40_fuji.jpg", "40 周年の記章"],
  ["19_fujisan/chibi/chibi_fuji_gacha.jpg", "ちびフジィ ガチャ"],
  ["19_fujisan/maison/maison_fuji_scarf.jpg", "Maison スカーフ"],
  ["19_fujisan/wamon/wamon_fuji_furoshiki.jpg", "青海波 風呂敷"],
].forEach((it, i) => {
  const x = 7.15 + (i % 2) * 2.75, y = 3.2 + Math.floor(i / 2) * 1.72;
  card(s, x, y, 2.55, 1.58);
  img(s, "deck_assets/" + it[0], x + 0.08, y + 0.07, 2.39, 1.06);
  s.addText(it[1], { x: x + 0.06, y: y + 1.17, w: 2.43, h: 0.32, fontFace: FB, fontSize: 9,
    color: C.muted, align: "center", isTextBox: true, margin: 0 });
});
foot(s, "富士は公式原画の隣に置く意匠であり、原画そのものには重ねていません。");

/* =============== 15d. 和紋 =============== */
s = P.addSlide(); light(s);
eyebrow(s, "文様");
title(s, "この魚のために、文様を 18 種描いた。");
body(s, "日本の文様は意味で選ばれてきました。青海波は海、鱗は魚の鱗、立涌はのぼる流れ、麻の葉は育つこと。そこへこの魚の要素を描き足しています —— 亀甲の節にはバルブのハンドル、矢絣は逆流、小紋の粒はキャビア。",
  { x: M, y: 2.25, w: 11.8, h: 0.9, fontSize: 13.5 });
card(s, M, 3.2, 5.55, 3.3);
img(s, "deck_assets/11_wamon/wamon_collection_board.jpg", M + 0.1, 3.3, 5.35, 3.1);
[
  ["13_merch_wamon/wamon_sensu.jpg", "扇子"],
  ["19_fujisan/wa_official/wao_fuji_byobu.jpg", "金屏風 ／ 公式原画"],
  ["19_fujisan/official/official_fuji_glass.jpg", "クリスタル ／ 公式原画"],
].forEach((it, i) => {
  const x = 6.55 + i * 2.02;
  card(s, x, 3.2, 1.87, 3.3);
  img(s, "deck_assets/" + it[0], x + 0.08, 3.3, 1.71, 2.6);
  s.addText(it[1], { x: x + 0.04, y: 5.98, w: 1.79, h: 0.4, fontFace: FB, fontSize: 8.5,
    color: C.muted, align: "center", lineSpacing: 12, isTextBox: true, margin: 0 });
});
foot(s, "同じ版を風呂敷・手ぬぐい・扇子・包装紙・化粧箱へ展開しています。");

/* =============== 16. 体験版 =============== */
s = P.addSlide(); dark(s, true);
eyebrow(s, "本エントリーの添付資料", true);
s.addText("「フジィを育てよう」\n―― 実際に遊べる育成シミュレーターを制作しました。", {
  x: M, y: 1.1, w: 11.8, h: 1.5, fontFace: FH, fontSize: 32, bold: true,
  color: "FFFFFF", lineSpacing: 46, isTextBox: true, margin: 0 });
s.addText("ごはん・あそぶ・ねむる・水流（バルブ開度）の四つの世話で、一粒の卵から成魚まで育てます。\nあそぶはミニゲーム四種。フジィの表情が空腹や眠気を伝えます。所要 90 秒。スマートフォンでもそのまま開けます。", {
  x: M, y: 2.46, w: 11.8, h: 0.66, fontFace: FB, fontSize: 12.5, color: C.steel,
  lineSpacing: 24, isTextBox: true, margin: 0 });
const stages = [
  ["1987", "stage_1_egg.png", "一粒の卵から"],
  ["1992", "stage_2_larva.png", "生残率 5%"],
  ["1998", "stage_3_fry.png", "世界初の完全養殖"],
  ["2002", "stage_4_young.png", "日本初のキャビア"],
  ["2027", "fujie-official.png", "そして、40年目へ"],
];
stages.forEach((st, i) => {
  const x = M + i * 2.42;
  s.addShape(P.ShapeType.roundRect, { x: x, y: 3.25, w: 2.2, h: 2.5, rectRadius: 0.06,
    fill: { color: C.mid }, line: { color: C.mid, width: 0 } });
  img(s, "deck_assets/04_campaign/" + st[1], x + 0.3, 3.45, 1.6, 1.3);
  s.addText(st[0], { x: x + 0.2, y: 4.85, w: 1.8, h: 0.38, fontFace: FH, fontSize: 16,
    bold: true, color: C.cyan, align: "center", isTextBox: true, margin: 0 });
  s.addText(st[2], { x: x + 0.1, y: 5.25, w: 2.0, h: 0.35, fontFace: FB, fontSize: 9.5,
    color: C.dimOnDark, align: "center", isTextBox: true, margin: 0 });
});
s.addShape(P.ShapeType.roundRect, { x: M, y: 5.95, w: 11.8, h: 0.62, rectRadius: 0.08,
  fill: { color: C.mid }, line: { color: C.cyan, width: 1 } });
s.addText([
  { text: "いますぐ開けます　", options: { fontSize: 12, color: C.steel, bold: true } },
  { text: LIVE, options: { fontSize: 13.5, color: C.cyan, bold: true, hyperlink: { url: LIVE } } },
  { text: "　／　オフラインでご覧の場合は添付のHTMLから", options: { fontSize: 11, color: C.dimOnDark } },
], { x: M + 0.4, y: 6.08, w: 11.0, h: 0.38, fontFace: FB, isTextBox: true, margin: 0 });

/* =============== 17. ROADMAP =============== */
s = P.addSlide(); light(s);
eyebrow(s, "進め方");
title(s, "2027 年は、40 年目です。");
body(s, "1987 年の一言から 40 年、2002 年の初出荷から 25 年。2027 年はその両方が重なる年です。結果発表は 2026 年 12 月 —— 2027 年度の計画に、そのまま乗せられます。",
  { x: M, y: 1.95, w: 11.8, h: 0.8, fontSize: 13.5 });
const phases = [
  ["2027", "春", "挑戦から 40 年", "ちびフジィ確定\nマニュアル ver2.0 策定\nLINE スタンプ 128 種公開", "ふ化の季節に合わせ、\nフジィの誕生日を定める", "低", true],
  ["2027", "通年", "初出荷から 25 年", "SNS 運用開始\n養魚場の映像を蓄積\n取引先への無償開放を案内", "25 周年の国産キャビアとして\n地域・行政に持ち込める", "低〜中", false],
  ["2028", "", "完全養殖から 30 年", "里美養魚場の限定公開\n茨城県との連携協議\nぬいぐるみ等グッズ化", "「会いに行けるマスコット」の\n開始年として節目が立つ", "中", false],
  ["2030", "", "創業 100 周年", "ドキュメンタリー公開\n採用広報への本格転用", "フジィ自身も 5 歳。\n100 周年の顔になる", "中〜高", false],
];
phases.forEach((p, i) => {
  const x = M + i * 3.03;
  s.addShape(P.ShapeType.roundRect, { x: x, y: 2.85, w: 2.8, h: 3.2, rectRadius: 0.06,
    fill: { color: C.card }, line: { color: p[6] ? C.cyan : "E2EAED", width: p[6] ? 2 : 1 } });
  s.addText(p[0], { x: x + 0.3, y: 3.02, w: 1.5, h: 0.5, fontFace: FH, fontSize: 24,
    bold: true, color: p[6] ? C.cyan : C.ink, isTextBox: true, margin: 0 });
  s.addText(p[1], { x: x + 1.55, y: 3.22, w: 0.9, h: 0.3, fontFace: FB, fontSize: 10.5,
    color: C.muted, isTextBox: true, margin: 0 });
  s.addText(p[2], { x: x + 0.3, y: 3.56, w: 2.25, h: 0.3, fontFace: FB, fontSize: 10.5,
    bold: true, color: p[6] ? C.cyan : C.muted, isTextBox: true, margin: 0 });
  s.addText(p[3], { x: x + 0.3, y: 3.95, w: 2.25, h: 1.25, fontFace: FB, fontSize: 10.5,
    color: C.ink, lineSpacing: 18, isTextBox: true, margin: 0 });
  s.addText(p[4], { x: x + 0.3, y: 5.25, w: 2.25, h: 0.55, fontFace: FB, fontSize: 9,
    color: C.muted, lineSpacing: 14, isTextBox: true, margin: 0 });
  s.addText("想定コスト：" + p[5], { x: x + 0.3, y: 5.72, w: 2.25, h: 0.25, fontFace: FB,
    fontSize: 9, bold: true, color: C.muted, isTextBox: true, margin: 0 });
});
s.addShape(P.ShapeType.roundRect, { x: M, y: 6.25, w: 11.8, h: 0.66, rectRadius: 0.06,
  fill: { color: C.deep }, line: { color: C.deep, width: 0 } });
s.addText("創業 100 周年を、フジィが有名になった状態で迎える。", {
  x: M + 0.45, y: 6.42, w: 10.9, h: 0.38, fontFace: FH, fontSize: 16, bold: true,
  color: "FFFFFF", isTextBox: true, margin: 0 });
s.addNotes("2027 年という締切を置くことで、この企画は「いつかやる案」ではなく「来年度の計画」になる。第 1 期の制作物は本エントリーにすべて添付済み。");

/* =============== 17b. 2027 年の、ある一日 =============== */
s = P.addSlide(); light(s);
eyebrow(s, "期待される効果");
title(s, "2027 年の、ある一日。");
body(s, "テレビ CM は考えていない、と募集要項にあります。ここに並べたものは、どれも買った枠ではありません。ですから効果は視聴率ではなく、こういう一日として現れます。",
  { x: M, y: 1.95, w: 11.8, h: 0.8, fontSize: 13.5 });
const day = [
  ["朝", "常陸太田の給餌、7 時", "里美養魚場で水面が一斉に沸き立ちます。飼育員がスマートフォンで 20 秒撮り、ちびフジィの声で「今日もごはん。1 万匹分」と添えて投稿します。114 人だったフォロワーは、この一年、毎週この光景を見てきました。県の水産課の担当者もその一人で、今日の投稿を庁内に転送します。"],
  ["昼", "大阪の高校、社会科の教室", "先生が配った資料の QR コードを、生徒が読み取ります。90 秒後、教室の 40 台のスマートフォンに成魚が泳いでいます。「先生、この会社なに？」「バルブの会社。この魚を世界で初めて卵から育てた」。その生徒の一人が、三年後の採用説明会でこの日のことを話します。"],
  ["夕", "友だちのグループチャット", "大学生が「サメじゃないです」のスタンプを送ります。「何これ」「チョウザメ。絶滅しそうな魚を、獲らずに増やせるようにした会社がいるんだって」。フジキンはこの会話に一円も払っていません。送った本人は、二週間前に友だちからこのスタンプをもらった人です。"],
  ["夜", "どこかの家の食卓", "お歳暮の国産キャビアの缶に、小さな銀色の魚が描かれています。「これ、里美のやつだ。今度見に行こう」。缶をつくった生産者は、フジキンから稚魚を買っている会社です。ロゴの使用料は、かかっていません。"],
];
day.forEach((d, i) => {
  const x = M + i * 3.03;
  card(s, x, 2.85, 2.8, 3.25);
  s.addText(d[0], { x: x + 0.3, y: 3.02, w: 0.7, h: 0.5, fontFace: FH, fontSize: 24,
    bold: true, color: C.cyan, isTextBox: true, margin: 0 });
  s.addText(d[1], { x: x + 0.3, y: 3.56, w: 2.25, h: 0.3, fontFace: FB, fontSize: 10.5,
    bold: true, color: C.ink, isTextBox: true, margin: 0 });
  s.addText(d[2], { x: x + 0.3, y: 3.95, w: 2.25, h: 2.05, fontFace: FB, fontSize: 9.5,
    color: C.muted, lineSpacing: 16, isTextBox: true, margin: 0 });
});
s.addShape(P.ShapeType.roundRect, { x: M, y: 6.25, w: 11.8, h: 0.66, rectRadius: 0.06,
  fill: { color: C.deep }, line: { color: C.deep, width: 0 } });
s.addText("四つの場面に共通点が一つ。誰かがフジキンの話を、自分の言葉でしている。それが「覚えられる会社」と「語られる会社」の差です。", {
  x: M + 0.45, y: 6.42, w: 10.9, h: 0.38, fontFace: FH, fontSize: 13, bold: true,
  color: "FFFFFF", isTextBox: true, margin: 0 });

/* =============== 18. 効果 =============== */
s = P.addSlide(); light(s);
eyebrow(s, "期待される効果");
title(s, "一度つくれば、翌年の土台になる。");
const eff = [
  ["「覚えられる会社」から「語られる会社」へ", "「バルブの会社が日本のキャビアをつくった」は、聞いた人が翌日 誰かに話したくなる強度を持っています。"],
  ["一般層への継続的な到達", "LINE スタンプは送信されるかぎり露出が続きます。一度の制作費で、最も信頼された場所に繰り返し現れます。"],
  ["取引先を通じた面の拡大", "フジキンが直接リーチできない一般消費者の食卓に、フジィが届きます。"],
  ["採用広報への波及", "生残率 5% から世界初に至った 11 年間は、学生がもっとも反応する種類の物語です。"],
  ["地域・行政との連携", "茨城県の産地化政策と目的が一致し、無償の拡散チャネルになります。"],
  ["資産が積み上がる", "キャラクター・スタンプ・映像・公開体制。いずれも残り、時間とともに価値が増します。"],
];
eff.forEach((e, i) => {
  const col = i % 2, row = Math.floor(i / 2);
  const x = M + col * 6.05, y = 2.35 + row * 1.42;
  numDot(s, i + 1, x, y + 0.08);
  s.addText(e[0], { x: x + 0.62, y: y + 0.02, w: 5.1, h: 0.38, fontFace: FH, fontSize: 13.5,
    bold: true, color: C.ink, isTextBox: true, margin: 0 });
  s.addText(e[1], { x: x + 0.62, y: y + 0.44, w: 5.1, h: 0.85, fontFace: FB, fontSize: 10.5,
    color: C.muted, lineSpacing: 17, isTextBox: true, margin: 0 });
});

/* =============== 19. CLOSING =============== */
s = P.addSlide(); dark(s, true);
img(s, "deck_assets/04_campaign/fujie-official.png", 3.35, 1.55, 6.6, 2.0);
s.addText("このフジィは、実在します。", { x: 0.9, y: 3.95, w: 11.5, h: 0.95,
  fontFace: FH, fontSize: 42, bold: true, color: "FFFFFF", align: "center",
  isTextBox: true, margin: 0 });
s.addText("フジキンが 40 年かけて育ててきた魚を、\n日本中が知っている名前にしたいと考えています。", {
  x: 0.9, y: 5.0, w: 11.5, h: 0.9, fontFace: FB, fontSize: 14.5, color: C.steel,
  align: "center", lineSpacing: 28, isTextBox: true, margin: 0 });
s.addText("2027 年、40 年目。　創業 100 周年を、フジィが有名になった状態で迎える。", {
  x: 0.9, y: 5.82, w: 11.5, h: 0.4, fontFace: FH, fontSize: 15, bold: true,
  color: C.cyan, align: "center", isTextBox: true, margin: 0 });
s.addText([
  { text: "企画の全体像・年表・体験版はこちらで　", options: { fontSize: 11, color: C.steel } },
  { text: LIVE, options: { fontSize: 12.5, color: C.cyan, bold: true, hyperlink: { url: LIVE } } },
], { x: 0.9, y: 6.28, w: 11.5, h: 0.34, fontFace: FB, align: "center", isTextBox: true, margin: 0 });
s.addText("株式会社ブレインパワー　大阪　／　Vittorio Zumpano", { x: 0.9, y: 6.66, w: 11.5, h: 0.35,
  fontFace: FB, fontSize: 11, color: C.dimOnDark, align: "center", isTextBox: true, margin: 0 });

P.writeFile({ fileName: "D:/Fuji_Famous/Fujie_Creative/05_submission/フジィは実在する_企画書.pptx" })
  .then(f => console.log("WROTE", f));
