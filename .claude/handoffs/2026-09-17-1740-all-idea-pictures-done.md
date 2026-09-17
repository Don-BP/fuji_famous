# Every idea now has a picture — 2026-09-17

## Continue exactly here

The last thing I said:

> Done — the four-scene picture is live in the voice section, the two old ones
> are gone, and no placeholders remain anywhere on the site.
>
> That's all thirteen ideas with pictures.

**In flight:** nothing in flight — last task completed. Everything is built,
committed on both `main` and `gh-pages`, and verified live.

**Literal next action:** ask the user what they want to do with the remaining
thirteen days before entries close on 30 September 2026 — the picture programme
is finished, so there is no default task waiting.

**Do NOT do next:** do not regenerate or "improve" any of the thirteen idea
pictures — every one was chosen by hand and several were hand-edited by the
owner afterwards. Do not touch the manhole covers, the open day picture, the
Sturgeon Day picture or the voice picture. Do not reorder or restyle the hub.
Do not touch the deck or the entry sheet. Do not open the browser pane on
`promo/index.html` — the app pops that file open on every edit and it always
looks broken unstyled; check the live site with `curl` instead.

## Background

Where we got to: the hub's five chapters and thirteen ideas all carry pictures
now. Today finished the last three — the open day, Sturgeon Day, and giving
Fujie a voice.

Decisions that would otherwise be re-litigated:
- Nobody eats beside open water tanks. The open day tasting happens outdoors or
  in a clean room, never in the rearing hall.
- The picture generator cannot draw Fujie at screen size — it always produces a
  dolphin — and it invents nonsense Japanese for captions and news straps. So
  screens are generated with the caption strip and avatar circle left blank, and
  the real artwork and real type are composited on afterwards.
- Those composite scripts write to `*_plate*.png`, never to `*_final.png`, so
  re-running them can never overwrite a picture finished by hand.
- Everyone in a farm picture is Japanese. Two takes came back with European
  keepers and hands and were thrown away.
- One picture per idea. The voice idea was briefly given two and they repeated
  the same water and phone twice; it is one picture of four distinct scenes now.
- Decisions recorded in a handoff are settled — build them, do not re-ask them.

Gotchas:
- Gallery ids must not contain `_fuji`; that string switches on a set-tab feature.
- Entry sheet must stay at 3 pages. Hidden Word hangs; run it visibly.
- Deploying: rebuild with `tools/build_site.py`, copy `dist/` into the gh-pages
  worktree's `studio-fa519005bf/`, push `ghp-deploy:gh-pages`. Path is in
  `git worktree list`. GitHub Pages lags a minute; verify with `curl` and a
  cache-busting query, not from a browser tab that may be serving a cached page.

Files that matter: `promo/index.html`, `promo/data.js`, `promo/cases.js`,
`promo/hub.js`, `tools/build_site.py`, `tools/gen.py`,
`tools/run_ideas_openday.py`, `tools/run_ideas_sturgeonday.py`,
`tools/run_ideas_voice.py`, `tools/build_sday_screen.py`,
`tools/build_voice_screen.py`, `Fujie_Creative/20_new_ideas/`.

Deadline: entries close 30 September 2026.
