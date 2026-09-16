"""Fold the second act - conservation, the shark line, the 2027 anniversary -
into the entry sheet text, then rebuild the filled Word document.

Idempotent: every insertion is skipped if its anchor text is already present.
"""
import json, pathlib, subprocess, sys

F = pathlib.Path(r"D:\Fuji_Famous\tools\entry_fields.json")
d = json.loads(F.read_text(encoding="utf-8"))

CONSERVATION = (
    "さらに、この物語には続きがあります。チョウザメはIUCNレッドリストで「もっとも絶滅の危機にある"
    "生物群」とされ、現存する全種が絶滅危惧種です。完全養殖とは、「もう川から一尾も獲らなくていい」"
    "という技術にほかなりません。フジキンがつくったのは珍味ではなく、この魚を獲らずに済ませる方法でした。"
    "食の話にとどめず保全の話として語ることで、広報だけでなくサステナビリティ・統合報告の文脈にも"
    "乗せられます。"
)

SHARK = (
    "⑦「サメじゃないです。」を入口の一言にする"
    "チョウザメは「蝶のサメ」と書くため、ほぼ全員が最初にサメだと誤解します。フジキンのキャビアサイトにも"
    "「サメとの違い」というページがあるほどです。この誤解を直すのではなく、入口として使います。"
    "「サメじゃないです。」に続けて「サメより、ずっと少ないんです。」と言えば、二行でチョウザメの正体と、"
    "この魚がおかれた状況が同時に伝わります。キャラクター最大の弱点（サメに見えること）が、"
    "そのまま最大の入口になります。なお、この一言を発するのは「ちびフジィ」であり、"
    "公式フジィに文字を重ねることはしません（マニュアル第7条）。"
)

TIMING = (
    "実施時期について。2027年は、1987年の挑戦開始から40年、2002年の初出荷から25年にあたります。"
    "本コンテストの結果発表は2026年12月であり、本企画はそのまま2027年度の計画に乗せることができます。"
    "2028年には完全養殖から30年、そして2030年には創業100周年。創業100周年を、フジィが有名になった"
    "状態で迎えることを目標とします。"
)

EFFECT7 = (
    "７．複数部門で推進できるフジィが「絶滅危惧種を、獲らずに育てる技術」の象徴になることで、"
    "広報活動だけでなく、統合報告書・サステナビリティ報告・SDGs（目標14「海の豊かさを守ろう」）の"
    "文脈でも語れるようになります。予算と推進主体を一部門に依存しない企画になります。"
)

EFFECT8 = (
    "８．来年度の計画として、すぐに動かせる2027年という明確な節目があるため、"
    "「いつか実施する案」ではなく「2027年度に実施する計画」として検討できます。"
    "第1期の制作物（ちびフジィ、スタンプ108種、体験版）は本エントリーにすべて添付済みです。"
)

s = d["summary"]
if "IUCN" not in s:
    anchor = "しかし現在、この物語はフジィと結びついていません。"
    s = s.replace(anchor, CONSERVATION + anchor, 1)
s = s.replace("②LINEスタンプ40種を無料配布する", "②LINEスタンプ108種を無料配布する", 1)
s = s.replace("実際に使用可能な40種を制作し別資料に添付しています。",
              "実際に使用可能な108種（日本語64種・英語44種）を制作し、"
              "一点ずつ切り出した状態で別資料に添付しています。", 1)
if "サメじゃないです" not in s:
    s = s + SHARK
if "2027年" not in s:
    s = s + TIMING
d["summary"] = s

e = d["effect"]
if "７．" not in e:
    e = e + EFFECT7
if "８．" not in e:
    e = e + EFFECT8
d["effect"] = e

F.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"summary {len(d['summary'])} chars, effect {len(d['effect'])} chars")

if "--fill" in sys.argv:
    r = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
                        "-File", r"D:\Fuji_Famous\tools\fill_entry.ps1"],
                       capture_output=True, text=True)
    print(r.stdout.strip()[-400:] or r.stderr.strip()[-400:])
