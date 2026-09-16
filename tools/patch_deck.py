import io

p = r"D:\Fuji_Famous\tools\deck.js"
s = io.open(p, encoding="utf-8").read()
n = 0


def sub(old, new, label):
    global s, n
    if old not in s:
        raise SystemExit("NOT FOUND: " + label)
    c = s.count(old)
    s = s.replace(old, new)
    n += c
    print("patched:", label, f"({c}x)")


# --- QA fix 1: slide 13, body copy wrapped onto a 4th line and crowded the list ---
sub(
    'body(s, "里美養魚場（茨城県常陸太田市）の限定公開。1 万尾の本物のフジィに会える場所をつくります。\\n茨城県は「霞ヶ浦キャビア」で国内一の産地を目指しており、協力相手として利害が完全に一致します。県・自治体・地元メディアを無償の拡散チャネルとして活用できます。",\n  { x: M, y: 2.35, w: 7.4, h: 1.5, fontSize: 13.5 });',
    'body(s, "里美養魚場（茨城県常陸太田市）の限定公開。1 万尾の本物のフジィに会える場所をつくります。\\n茨城県は「霞ヶ浦キャビア」で国内一の産地を目指しており、県・自治体・地元メディアを\\n無償の拡散チャネルとして活用できます。",\n  { x: M, y: 2.35, w: 7.5, h: 1.4, fontSize: 13 });',
    "s13 body copy shortened",
)
sub("  const y = 4.05 + i * 0.83;", "  const y = 4.32 + i * 0.8;", "s13 list moved down")

# --- QA fix 2: slide 3, mascot too close to the card's bottom-right corner ---
sub(
    's.addImage({ path: IMG + "01_character/master_v3_wave.png", x: x + 3.15, y: 5.15, w: 2.3, h: 1.35,\n      sizing: { type: "contain", w: 2.3, h: 1.35 } });',
    's.addImage({ path: IMG + "01_character/master_v3_wave.png", x: x + 3.0, y: 4.92, w: 2.15, h: 1.25,\n      sizing: { type: "contain", w: 2.15, h: 1.25 } });',
    "s03 mascot padding",
)

# --- slide 16 now describes a playable simulator with a live URL ---
sub(
    's.addText("「フジィを育てよう」\\n―― 実際に動く体験版を同梱しています。", {\n  x: M, y: 1.1, w: 11.8, h: 1.5, fontFace: FH, fontSize: 32, bold: true,\n  color: "FFFFFF", lineSpacing: 46, isTextBox: true, margin: 0 });\ns.addText("スマートフォンでもパソコンでも開けます。所要 90 秒。インターネット接続もアプリも不要です。", {\n  x: M, y: 2.65, w: 11.8, h: 0.35, fontFace: FB, fontSize: 13, color: C.steel,\n  isTextBox: true, margin: 0 });',
    's.addText("「フジィを育てよう」\\n―― 実際に遊べる育成シミュレーターを制作しました。", {\n  x: M, y: 1.1, w: 11.8, h: 1.5, fontFace: FH, fontSize: 32, bold: true,\n  color: "FFFFFF", lineSpacing: 46, isTextBox: true, margin: 0 });\ns.addText("バルブの開度で水質を保ち、餌をやり、一粒の卵から成魚まで育てます。所要 90 秒。\\nスマートフォンでもパソコンでも、そのまま開けます。", {\n  x: M, y: 2.6, w: 11.8, h: 0.7, fontFace: FB, fontSize: 13, color: C.steel,\n  lineSpacing: 24, isTextBox: true, margin: 0 });',
    "s16 simulator description",
)
sub(
    's.addText("添付ファイル：フジィを育てよう.html　（ダブルクリックで開きます）", {\n  x: M, y: 6.05, w: 11.8, h: 0.35, fontFace: FB, fontSize: 12, bold: true,\n  color: C.steel, isTextBox: true, margin: 0 });',
    's.addShape(P.ShapeType.roundRect, { x: M, y: 5.95, w: 11.8, h: 0.62, rectRadius: 0.08,\n  fill: { color: C.mid }, line: { color: C.cyan, width: 1 } });\ns.addText([\n  { text: "いますぐ開けます　", options: { fontSize: 12, color: C.steel, bold: true } },\n  { text: "https://don-bp.github.io/fuji_famous/", options: { fontSize: 13.5, color: C.cyan, bold: true } },\n  { text: "　／　添付：フジィを育てよう.html", options: { fontSize: 11, color: C.dimOnDark } },\n], { x: M + 0.4, y: 6.08, w: 11.0, h: 0.38, fontFace: FB, isTextBox: true, margin: 0 });',
    "s16 live URL",
)

# stage 5 of the strip should be the official artwork the character grows into
sub('["2026", "master.png", "そして、フジィへ"],', '["2026", "fujie-official.png", "そして、フジィへ"],', "s16 final stage art")

io.open(p, "w", encoding="utf-8").write(s)
print("\ntotal replacements:", n)
