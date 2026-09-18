# The phone film still does not start at the top — 2026-09-18

## Continue exactly here

The last thing I said:

> It's already live — went up about a minute ago.
> https://don-bp.github.io/fuji_famous/studio-fa519005bf/
> **What changed:** the dark wash is now measured against the headline block
> rather than against the whole screen... It also now stops just short of the
> hero's bottom edge, so there's nothing left dark to be cut off in a straight
> line, which is what the seam was.

The owner then said: on a **real phone in Chrome**, after refreshing, the
background still does not animate from the very top of the page. It looks
right in the side preview window at phone size. So the fix works in the
emulated pane but not on the actual device.

**In flight:** nothing half-written. Everything is committed on `main` and
deployed to `gh-pages`, and the live stylesheet is `hub.css?v=ffd09d37`.

**Literal next action:** work out why the upright film does not appear to run
at the top of the page on a real Android Chrome phone when it does at the same
size in the preview pane. Prime suspects, in order: (1) Chrome's address bar
collapsing on first scroll changes the viewport height, fires resize, and the
film's scroll range is recalculated mid-scroll; (2) the film's scroll range is
derived from the first white band, which sits about 3,240px down on a phone, so
the early frames each get ~45px of scroll — and the video's own first quarter
barely moves, so real motion may genuinely not be visible until roughly one
screen down; (3) the phone is still being served a cached stylesheet.

Rule out (3) first — have the owner confirm the live page reports
`hub.css?v=ffd09d37` — before changing any code.

**Do NOT do next:**
- Do not re-cut the mobile film frames. They are cut from the owner's own
  video with ffmpeg and are correct.
- Do not regenerate any of the thirteen idea pictures, the manhole covers, or
  the three woodblock/scroll prints. All settled.
- Do not touch the deck, the entry sheet or the email. All current.
- Do not change the desktop hero. It was verified unaffected and is fine.
- Do not trust the browser pane's screenshots without passing `tabId`
  explicitly — see the gotcha below. This cost most of an hour today.

## Background

Where we got to: the hub now plays an upright version of the hero film on
phones, cut from the owner's portrait video. The five new ideas carry their
pictures into the deck. Three prints that had the official Fujie looking stuck
on were regenerated so the fish is printed into the paper.

Decisions that would otherwise be re-litigated:
- Only one film ever downloads: upright on a tall screen, wide on a landscape
  one. A phone turned sideways swaps to the *small* wide pass, because the
  large one only makes sense above 1000px wide.
- The dark wash behind the hero copy is measured against the copy block, not
  the hero. Measured against the hero it blacks out open water on tall windows.
- It stops 60px short of the hero's foot. The hero clips its own background, so
  anything still dark at that edge gets cut off in a straight line — that was
  the seam the owner reported.
- The dark band no longer blurs what is behind it on phones. The blur switched
  on exactly at the hero's bottom edge and was the other half of the seam. The
  cards blur their own backdrop, so nothing needed it.
- The film's slow opening is the video's own pacing and the owner has said that
  is fine. Do not "improve" it unless asked again.

Gotchas:
- In the browser pane, `computer` actions go to the *fronted* tab, not the tab
  you last ran script in. Always pass `tabId`. Screenshots taken without it
  silently showed a different tab and looked like a bug that was not there.
- The pane also pauses animation frames while hidden, so scroll-driven redraws
  do not happen; dispatching a `resize` event forces one synchronously.
- Deploying: rebuild with `tools/build_site.py`, copy `dist/` into the
  gh-pages worktree's `studio-fa519005bf/`, push `ghp-deploy:gh-pages`. Path is
  in `git worktree list`. Pages lags about 30s; verify with `curl` and a
  cache-busting query, never from a browser tab.
- Gallery ids must not contain `_fuji`. Entry sheet must stay at 3 pages.

Files that matter: `promo/hub.css` (the film's media queries and the hero
wash), `promo/hero.js` (which film, and the scroll-to-frame mapping),
`promo/film/m480/`, `promo/film/m720/`, `tools/build_mobile_film.py`,
`tools/build_site.py`, `tools/deck.js`, `tools/run_wa_official_prints.py`.

Deadline: entries close 30 September 2026.
