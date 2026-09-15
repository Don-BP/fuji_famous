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
function foot(s, txt, onDark) {
  s.addText(txt, {
    x: M, y: H - 0.55, w: W - M * 2, h: 0.3, fontFace: FB, fontSize: 9.5,
    color: onDark ? "4E6874" : "9BB0BA", isTextBox: true, margin: 0,
  });
}

/* =============== 1. TITLE =============== */
let s = P.addSlide(); dark(s, true);
s.addImage({ path: IMG + "04_campaign/fujie-official.png", x: 6.4, y: 2.35, w: 6.6, h: 2.0,
  sizing: { type: "contain", w: 6.6, h: 2.0 } });
s.addText("フジィを有名にする！アイデアコンテスト", {
  x: M, y: 1.55, w: 8, h: 0.34, fontFace: FB, fontSize: 12, bold: true,
  charSpacing: 2.5, color: C.cyan, isTextBox: true, margin: 0 });
s.addText("フジィは、\n実在する。", {
  x: M, y: 2.05, w: 7.2, h: 2.5, fontFace: FH, fontSize: 60, bold: true,
  color: "FFFFFF", lineSpacing: 74, isTextBox: true, margin: 0 });
s.addText("世界初の完全養殖ストーリーで、\nフジィを「シンボル」から「キャラクター」へ。", {
  x: M, y: 4.62, w: 7.2, h: 0.9, fontFace: FB, fontSize: 14.5,
  color: C.steel, lineSpacing: 27, isTextBox: true, margin: 0 });
s.addText("株式会社ブレインパワー　／　〔氏名〕", {
  x: M, y: H - 1.0, w: 7, h: 0.35, fontFace: FB, fontSize: 11.5,
  color: C.dimOnDark, isTextBox: true, margin: 0 });
s.addNotes("表紙。結論を先に置く：フジィは想像上のキャラクターではなく、フジキンが実際に育てている魚である。");

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
    s.addImage({ path: IMG + "01_character/master_v3_wave.png", x: x + 3.15, y: 5.15, w: 2.3, h: 1.35,
      sizing: { type: "contain", w: 2.3, h: 1.35 } });
  }
});

/* =============== 4. REVEAL =============== */
s = P.addSlide(); dark(s, true);
s.addImage({ path: IMG + "04_campaign/stage_4_young.png", x: 7.6, y: 1.5, w: 5.2, h: 4.4,
  sizing: { type: "contain", w: 5.2, h: 4.4 } });
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

/* =============== 5. TIMELINE =============== */
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
  x: M + 0.45, y: 5.82, w: 10.9, h: 0.5, fontFace: FB, fontSize: 13.5, bold: true,
  color: C.ink, isTextBox: true, margin: 0 });

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

/* =============== 7. SIX MOVES =============== */
s = P.addSlide(); dark(s);
eyebrow(s, "全体像", true);
s.addText("6 つの施策", { x: M, y: 0.62, w: 8, h: 0.8, fontFace: FH, fontSize: 34,
  bold: true, color: "FFFFFF", isTextBox: true, margin: 0 });
s.addText("上から順に実施します。①がなければ②以降は成立しません。", {
  x: M, y: 1.5, w: 9, h: 0.35, fontFace: FB, fontSize: 13, color: C.steel,
  isTextBox: true, margin: 0 });
const moves = [
  ["ちびフジィ", "表情と親しみを担う第 2 の姿を公式に追加する"],
  ["LINE スタンプ 40 種", "友だち追加を条件に無料配布する"],
  ["フジィに「中の人」を", "誰も見たことのない養魚場の映像を出す"],
  ["ちびフジィの無償開放", "稚魚取引先のパッケージを広告に変える"],
  ["会いに行けるマスコット", "里美養魚場を限定公開する"],
  ["1987 年の物語を映像化", "ロケ地はすべて自社保有"],
];
moves.forEach((m, i) => {
  const col = i % 2, row = Math.floor(i / 2);
  const x = M + col * 6.05, y = 2.2 + row * 1.52;
  card(s, x, y, 5.75, 1.3, true);
  numDot(s, i + 1, x + 0.35, y + 0.44, true);
  s.addText(m[0], { x: x + 0.95, y: y + 0.24, w: 4.6, h: 0.38, fontFace: FH, fontSize: 15,
    bold: true, color: "FFFFFF", isTextBox: true, margin: 0 });
  s.addText(m[1], { x: x + 0.95, y: y + 0.66, w: 4.6, h: 0.5, fontFace: FB, fontSize: 11,
    color: C.dimOnDark, lineSpacing: 17, isTextBox: true, margin: 0 });
});

/* =============== 8. 施策1 ちびフジィ =============== */
s = P.addSlide(); light(s);
eyebrow(s, "施策 1");
title(s, "ちびフジィ ―― 表情を持つ、第 2 の姿。");
body(s, "現行マニュアルの規定は一切変更しません。従来のフジィは企業シンボルとして厳格に保護したまま、\n公の場で人と接するための姿を新たに追加します。",
  { x: M, y: 2.3, w: 11.8, h: 0.8, fontSize: 14 });
s.addImage({ path: IMG + "01_character/master_v3_wave.png", x: M, y: 3.15, w: 3.5, h: 3.3,
  sizing: { type: "contain", w: 3.5, h: 3.3 } });
s.addImage({ path: IMG + "01_character/master_expressions.png", x: 4.6, y: 3.15, w: 7.95, h: 3.3,
  sizing: { type: "contain", w: 7.95, h: 3.3 } });
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
title(s, "LINE スタンプ 40 種を、無料配布する。");
body(s, "日本でもっとも費用対効果の高い認知獲得手段です。スタンプは「友人が」「私的な会話の中で」「自発的に」送るため、広告では決して到達できない場所に届きます。一度制作すれば、送信されるたびに露出が続きます。",
  { x: M, y: 2.3, w: 11.8, h: 0.85, fontSize: 13.5 });
s.addImage({ path: IMG + "02_stickers/sticker_sheet_01.png", x: M, y: 3.2, w: 3.6, h: 3.4,
  sizing: { type: "contain", w: 3.6, h: 3.4 } });
s.addImage({ path: IMG + "02_stickers/sticker_sheet_02.png", x: 4.5, y: 3.2, w: 3.6, h: 3.4,
  sizing: { type: "contain", w: 3.6, h: 3.4 } });
card(s, 8.45, 3.2, 4.1, 3.4);
s.addText("すでに制作済みです", { x: 8.85, y: 3.5, w: 3.3, h: 0.4, fontFace: FH, fontSize: 16,
  bold: true, color: C.cyan, isTextBox: true, margin: 0 });
s.addText([
  { text: "日常語 20 種：おはよう／ありがとう／おつかれさま／りょうかい ほか", options: { breakLine: true, bullet: true } },
  { text: "フジキン語 20 種：ながれにのれ／きわみへ／キャビア ほか", options: { breakLine: true, bullet: true } },
  { text: "配布条件：公式アカウント友だち追加", options: { breakLine: true, bullet: true } },
  { text: "スタンプが SNS の入口になり、以降の施策の土台になります", options: { bullet: true } },
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
body(s, "里美養魚場（茨城県常陸太田市）の限定公開。1 万尾の本物のフジィに会える場所をつくります。\n茨城県は「霞ヶ浦キャビア」で国内一の産地を目指しており、協力相手として利害が完全に一致します。県・自治体・地元メディアを無償の拡散チャネルとして活用できます。",
  { x: M, y: 2.35, w: 7.4, h: 1.5, fontSize: 13.5 });
const visit = [
  ["小学校・自治体との連携", "地元の社会科見学・食育プログラムとして"],
  ["採用広報への転用", "学生が「極限への挑戦」を体験として理解する"],
  ["メディアの取材動線", "テレビ・新聞が撮りたくなる絵がある"],
];
visit.forEach((v, i) => {
  const y = 4.05 + i * 0.83;
  numDot(s, i + 1, M, y);
  s.addText(v[0], { x: M + 0.62, y: y - 0.02, w: 3.6, h: 0.3, fontFace: FH, fontSize: 12.5,
    bold: true, color: C.ink, isTextBox: true, margin: 0 });
  s.addText(v[1], { x: M + 0.62, y: y + 0.28, w: 6.6, h: 0.3, fontFace: FB, fontSize: 10.5,
    color: C.muted, isTextBox: true, margin: 0 });
});
s.addImage({ path: IMG + "04_campaign/stage_3_fry.png", x: 8.6, y: 2.6, w: 4.0, h: 3.9,
  sizing: { type: "contain", w: 4.0, h: 3.9 } });

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

/* =============== 15. グッズ =============== */
s = P.addSlide(); light(s);
eyebrow(s, "受け皿となるグッズ");
title(s, "ぬいぐるみは、3 サイズで「成長」を見せる。");
body(s, "稚魚・幼魚・成魚。フジキンが世界で初めて成功させた「完全養殖」＝ 一生をまるごと育てる技術が、そのまま商品ラインになります。グッズが物語を説明してくれます。",
  { x: M, y: 2.3, w: 11.8, h: 0.8, fontSize: 13.5 });
s.addImage({ path: IMG + "03_plushie/plush_size_lineup.png", x: M, y: 3.15, w: 7.3, h: 3.3,
  sizing: { type: "contain", w: 7.3, h: 3.3 } });
s.addImage({ path: IMG + "03_plushie/plush_keychain_lifestyle.png", x: 8.35, y: 3.15, w: 2.0, h: 3.3,
  sizing: { type: "contain", w: 2.0, h: 3.3 } });
s.addImage({ path: IMG + "03_plushie/plush_studio_front.png", x: 10.5, y: 3.15, w: 2.05, h: 3.3,
  sizing: { type: "contain", w: 2.05, h: 3.3 } });
foot(s, "10cm キーホルダー／25cm／50cm。いずれも試作イメージです。");

/* =============== 16. 体験版 =============== */
s = P.addSlide(); dark(s, true);
eyebrow(s, "本エントリーの添付資料", true);
s.addText("「フジィを育てよう」\n―― 実際に動く体験版を同梱しています。", {
  x: M, y: 1.1, w: 11.8, h: 1.5, fontFace: FH, fontSize: 32, bold: true,
  color: "FFFFFF", lineSpacing: 46, isTextBox: true, margin: 0 });
s.addText("スマートフォンでもパソコンでも開けます。所要 90 秒。インターネット接続もアプリも不要です。", {
  x: M, y: 2.65, w: 11.8, h: 0.35, fontFace: FB, fontSize: 13, color: C.steel,
  isTextBox: true, margin: 0 });
const stages = [
  ["1987", "stage_1_egg.png", "一粒の卵から"],
  ["1992", "stage_2_larva.png", "生残率 5%"],
  ["1998", "stage_3_fry.png", "世界初の完全養殖"],
  ["2002", "stage_4_young.png", "日本初のキャビア"],
  ["2026", "master.png", "そして、フジィへ"],
];
stages.forEach((st, i) => {
  const x = M + i * 2.42;
  s.addShape(P.ShapeType.roundRect, { x: x, y: 3.25, w: 2.2, h: 2.5, rectRadius: 0.06,
    fill: { color: C.mid }, line: { color: C.mid, width: 0 } });
  s.addImage({ path: IMG + "04_campaign/" + st[1], x: x + 0.3, y: 3.45, w: 1.6, h: 1.3,
    sizing: { type: "contain", w: 1.6, h: 1.3 } });
  s.addText(st[0], { x: x + 0.2, y: 4.85, w: 1.8, h: 0.38, fontFace: FH, fontSize: 16,
    bold: true, color: C.cyan, align: "center", isTextBox: true, margin: 0 });
  s.addText(st[2], { x: x + 0.1, y: 5.25, w: 2.0, h: 0.35, fontFace: FB, fontSize: 9.5,
    color: C.dimOnDark, align: "center", isTextBox: true, margin: 0 });
});
s.addText("添付ファイル：フジィを育てよう.html　（ダブルクリックで開きます）", {
  x: M, y: 6.05, w: 11.8, h: 0.35, fontFace: FB, fontSize: 12, bold: true,
  color: C.steel, isTextBox: true, margin: 0 });

/* =============== 17. ROADMAP =============== */
s = P.addSlide(); light(s);
eyebrow(s, "進め方");
title(s, "小さく始めて、積み上げる。");
const phases = [
  ["第 1 期", "0 〜 3 ヶ月", "ちびフジィ確定\nマニュアル ver2.0 策定\nLINE スタンプ公開", "低", C.cyan],
  ["第 2 期", "3 〜 9 ヶ月", "SNS 運用開始\n養魚場の映像を蓄積\n取引先への無償開放を案内", "低〜中", C.steel],
  ["第 3 期", "9 〜 18 ヶ月", "ぬいぐるみ等グッズ化\n養魚場の限定公開を試行\n茨城県との連携協議", "中", C.steel],
  ["第 4 期", "18 ヶ月 〜", "ドキュメンタリー公開\n採用広報への本格転用", "中〜高", C.steel],
];
phases.forEach((p, i) => {
  const x = M + i * 3.03;
  s.addShape(P.ShapeType.roundRect, { x: x, y: 2.5, w: 2.8, h: 3.55, rectRadius: 0.06,
    fill: { color: C.card }, line: { color: i === 0 ? C.cyan : "E2EAED", width: i === 0 ? 2 : 1 } });
  s.addText(p[0], { x: x + 0.3, y: 2.78, w: 2.2, h: 0.4, fontFace: FH, fontSize: 17,
    bold: true, color: p[4] === C.cyan ? C.cyan : C.ink, isTextBox: true, margin: 0 });
  s.addText(p[1], { x: x + 0.3, y: 3.2, w: 2.2, h: 0.3, fontFace: FB, fontSize: 10.5,
    color: C.muted, isTextBox: true, margin: 0 });
  s.addText(p[2], { x: x + 0.3, y: 3.68, w: 2.2, h: 1.6, fontFace: FB, fontSize: 11,
    color: C.ink, lineSpacing: 19, isTextBox: true, margin: 0 });
  s.addText("想定コスト：" + p[3], { x: x + 0.3, y: 5.5, w: 2.2, h: 0.3, fontFace: FB,
    fontSize: 10, bold: true, color: C.muted, isTextBox: true, margin: 0 });
});
foot(s, "第 1 期はすでに本エントリーで制作済みのため、実質的に着手済みの状態から始められます。");

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
s.addImage({ path: IMG + "04_campaign/fujie-official.png", x: 3.35, y: 1.55, w: 6.6, h: 2.0,
  sizing: { type: "contain", w: 6.6, h: 2.0 } });
s.addText("このフジィは、実在します。", { x: 0.9, y: 3.95, w: 11.5, h: 0.95,
  fontFace: FH, fontSize: 42, bold: true, color: "FFFFFF", align: "center",
  isTextBox: true, margin: 0 });
s.addText("フジキンが 40 年かけて育ててきた魚を、\n日本中が知っている名前にしたいと考えています。", {
  x: 0.9, y: 5.0, w: 11.5, h: 0.9, fontFace: FB, fontSize: 14.5, color: C.steel,
  align: "center", lineSpacing: 28, isTextBox: true, margin: 0 });
s.addText("株式会社ブレインパワー　／　〔氏名〕", { x: 0.9, y: 6.35, w: 11.5, h: 0.35,
  fontFace: FB, fontSize: 11, color: C.dimOnDark, align: "center", isTextBox: true, margin: 0 });

P.writeFile({ fileName: "D:/Fuji_Famous/Fujie_Creative/05_submission/フジィは実在する_企画書.pptx" })
  .then(f => console.log("WROTE", f));
