/* Bilingual strings for フジィを育てよう / Raise Fujie */
window.I18N = {

ja: {
  html:"ja",
  title:"フジィを育てよう",
  sub:"フジキン 完全養殖ストーリー",
  langBtn:"EN",

  /* start */
  startMark:"1987 — FUJIKIN",
  startQuote:"「フジキンのバルブを使って、<br>チョウザメの養殖を始めてみないか？」",
  startBody:"最高技術顧問・故 西堀栄三郎先生の一言から、<br>フジキンの挑戦は始まりました。<br>水の“ながれ”を制御して、一粒の卵を育ててください。",
  startBtn:"はじめる",

  /* stats */
  hunger:"おなか", mood:"きげん", energy:"げんき", water:"水質", growth:"成長",

  /* actions */
  feed:"ごはん", play:"あそぶ", sleep:"ねむる", flow:"水流",

  /* stages */
  st_egg:"たまご", st_larva:"仔魚", st_fry:"稚魚", st_young:"幼魚", st_adult:"成魚",

  /* needs */
  need_hunger:"おなかすいた", need_mood:"ひまだな…", need_energy:"ねむい…",
  need_water:"水がよごれてる。水流を調整して", need_ok:"ごきげん！",

  /* flow panel */
  flowTitle:"バルブ開度（流量）",
  flowGood:"良好な流量です", flowBad:"緑の帯に合わせる",
  flowNote:"フジキンの超精密流体制御技術。水質はここで決まります。",
  close:"とじる",

  /* sleep */
  sleeping:"おやすみ…", wake:"おこす",

  /* mini-game picker */
  pickTitle:"なにしてあそぶ？",
  g_egg:"たまごキャッチ", g_egg_d:"落ちてくる卵を受けとめよう",
  g_shark:"サメたたき",   g_shark_d:"暗闇から出るサメをたたけ",
  g_race:"ながれをさかのぼれ", g_race_d:"逆流を泳ぎきれ",
  g_shell:"どのカイにいる？", g_shell_d:"真珠のありかを当てよう",

  /* in-game */
  score:"スコア", time:"のこり", tapStart:"タップでスタート",
  ready:"よういはいい？", go:"スタート！",
  missed:"ミス", round:"ラウンド",
  ctl_egg:"左右にドラッグしてフジィを動かす",
  ctl_shark:"出てきたサメをタップ／ウニはたたかないで！",
  ctl_race:"タップで上へ泳ぐ",
  ctl_shell:"真珠の入ったカイをタップ",
  streak:"れんぞく", ouch:"いたっ！",
  resultTitle:"けっか", moodUp:"きげんが上がった！", growUp:"すこし成長した！",
  again:"もういちど", back:"もどる",
  correct:"せいかい！", wrong:"はずれ…",

  /* milestones */
  ms:[
    {t:"1992年・人工ふ化成功",
     d:"民間企業として日本で初めて、チョウザメの人工ふ化に成功。しかし初年度の生残率はわずか5％でした。"},
    {t:"個体識別という発想",
     d:"一尾ずつを見分け、個体ごとに記録をとる。ベステル種100尾から始まった観察が、のちの技術を支えました。"},
    {t:"雌雄判別の技術",
     d:"キャビアが採れるのは雌だけ。フジキンは雌雄を見分ける専門技術を確立し、いまも出張指導を行っています。"},
    {t:"1998年・世界初の完全養殖",
     d:"水槽での完全養殖に世界で初めて成功。生残率は60％へ。卵から育てた魚が、また卵を産みました。"},
    {t:"2002年・日本初のキャビア出荷",
     d:"バルブメーカーが、日本の食卓に国産キャビアを届けました。いま国内に流通する国産キャビアの多くは、ここから広がっています。"}
  ],

  /* endings */
  lostMark:"1992",
  lostTitle:"育ちませんでした。",
  lostBody:"フジキンが人工ふ化に成功した初年度、<br>100尾のうち <b>95尾</b> が育ちませんでした。<br>生残率 5%。ここから6年かけて、60%まで引き上げます。",
  lostHint:"世話を続け、流量を緑の帯に保ってください。",
  retry:"もういちど育てる",

  winMark:"1987 — 2026",
  winTitle:"このフジィは、実在します。",
  winBody:"茨城県常陸太田市・里美養魚場。<br>いまも1万尾を超えるチョウザメが泳いでいます。<br><b>バルブメーカーが、日本の国産キャビアを生みました。</b>",
  winDays:"育てた年数"
},

en: {
  html:"en",
  title:"Raise Fujie",
  sub:"The Fujikin sturgeon story",
  langBtn:"日本語",

  startMark:"1987 — FUJIKIN",
  startQuote:"“Why not use Fujikin’s valves<br>to start farming sturgeon?”",
  startBody:"One sentence from Fujikin’s chief technical advisor,<br>the late Eizaburo Nishibori, began everything.<br>Control the flow of the water, and raise a single egg.",
  startBtn:"Begin",

  hunger:"Food", mood:"Mood", energy:"Energy", water:"Water", growth:"Growth",

  feed:"Feed", play:"Play", sleep:"Sleep", flow:"Flow",

  st_egg:"Egg", st_larva:"Larva", st_fry:"Fry", st_young:"Juvenile", st_adult:"Adult",

  need_hunger:"I'm hungry", need_mood:"I'm bored…", need_energy:"I'm sleepy…",
  need_water:"The water's dirty - check Flow", need_ok:"Happy!",

  flowTitle:"Valve opening (flow rate)",
  flowGood:"Flow is good", flowBad:"Match the green band",
  flowNote:"Fujikin’s ultra-precision fluid control. Water quality is decided here.",
  close:"Close",

  sleeping:"Sleeping…", wake:"Wake up",

  pickTitle:"What shall we play?",
  g_egg:"Egg Catch",      g_egg_d:"Catch the falling eggs",
  g_shark:"Whack-a-Shark", g_shark_d:"Smack the sharks from the dark",
  g_race:"Upstream Dash",  g_race_d:"Swim against the current",
  g_shell:"Which Shell?",  g_shell_d:"Find the hidden pearl",

  score:"Score", time:"Time", tapStart:"Tap to start",
  ready:"Ready?", go:"Go!",
  missed:"Missed", round:"Round",
  ctl_egg:"Drag left and right to move Fujie",
  ctl_shark:"Tap the sharks — but never the urchin!",
  streak:"Streak", ouch:"Ouch!",
  ctl_race:"Tap to swim upward",
  ctl_shell:"Tap the shell hiding the pearl",
  resultTitle:"Result", moodUp:"Mood went up!", growUp:"Grew a little!",
  again:"Play again", back:"Back",
  correct:"Correct!", wrong:"Not that one…",

  ms:[
    {t:"1992 — Artificial hatching",
     d:"The first private company in Japan to hatch sturgeon artificially. That first year, only 5% survived."},
    {t:"Knowing every fish",
     d:"Telling each fish apart and keeping records on every individual. Observation that began with 100 bester sturgeon became the foundation of the technology."},
    {t:"Telling male from female",
     d:"Only females produce caviar. Fujikin established the expert technique for sexing sturgeon and still teaches it on site today."},
    {t:"1998 — A world first",
     d:"The first complete tank-based sturgeon aquaculture in the world. Survival rose to 60%. Fish raised from eggs laid eggs of their own."},
    {t:"2002 — Japan’s first caviar",
     d:"A valve manufacturer put domestic caviar on Japanese tables. Most Japanese caviar sold today traces back to here."}
  ],

  lostMark:"1992",
  lostTitle:"It didn’t survive.",
  lostBody:"In the first year Fujikin hatched sturgeon,<br><b>95 of every 100</b> did not make it.<br>A 5% survival rate. It took six more years to reach 60%.",
  lostHint:"Keep up the care, and hold the flow inside the green band.",
  retry:"Raise another",

  winMark:"1987 — 2026",
  winTitle:"This Fujie is real.",
  winBody:"Satomi fish farm, Hitachiota, Ibaraki.<br>More than 10,000 sturgeon still swim there today.<br><b>A valve manufacturer created Japan’s domestic caviar.</b>",
  winDays:"Years raised"
}

};
