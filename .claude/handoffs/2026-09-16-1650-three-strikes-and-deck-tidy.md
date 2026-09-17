# Three strikes in the games, and the deck caught up — 2026-09-16

## Continue exactly here

**The last thing I said, verbatim:**

> The keychain slide is gone. Your plush slide was already making the argument
> — its bottom line reads 10cm キーホルダー／25cm／50cm, so the keychain is simply
> the smallest of the three sizes... And to answer your original question
> properly: no, it wasn't all updated. Two things were stale and both are fixed
> now.

**In flight:** nothing. Everything is committed, pushed, deployed and checked
against the live server and the rebuilt files.

**The literal next action:** none pending — the next piece of work is the
user's to choose. If they open with "is everything still fine", the answer is
yes: site, game, deck, entry sheet and the attached single-file game all agree
with each other as of this session.

**Do NOT do next:**
- Do not revive the six-variant / blind-box mascot keychain in any form. Killed
  across two sessions now, and its deck slide was deleted today.
- Do not change the swimming chibi's movement. It floats over the goods on
  purpose — the user said so explicitly today.
- Do not fold the plush and keychain into the goods lines as 06 and 07. Asked
  and answered today: they stay their own section.
- Do not merge the Wamon line into the Wa line. Five lines is correct and settled.

## Background

The four mini-games now share one rule: three mistakes ends the game, and
finishing any of them cheers Fujie up by exactly the same amount. The score is
still kept and shown but buys nothing. Each game defines its own mistake — an
egg on the floor, a shark that gets away, a crash, a wrong shell. Upstream Dash
survives three crashes with a moment of blinking invulnerability after each.

Six real bugs came out of a full audit of the game, the worst being that the
game's scripts carried a hand-typed cache number — the same fault that hid two
fixes last session. The build stamps them with a hash of the file now, so it
cannot recur.

Copy fixes: the goods section said four lines when there are five (both
languages, and the Japanese was missed on the first pass). The plush section
was labelled PROTOTYPE / 試作, implying the other lines were already in
production — nothing is. Line numbers were printing twice in English.

**Deploying is fiddly and getting it wrong cost a full restore once.** The
published branch is `gh-pages` but the local worktree branch is called
`ghp-deploy`, so it pushes as `ghp-deploy:gh-pages`. The branch root holds the
PUBLIC GAME; the studio goes in `studio-fa519005bf/`, and that folder needs its
own copy of the game at `studio-fa519005bf/game/` because the hub links to
`game/`.

Files that matter: `site/game.js`, `site/i18n.js`, `promo/hub.js`,
`promo/index.html`, `tools/build_site.py`, `tools/deck.js`,
`tools/make_portable.py`.
