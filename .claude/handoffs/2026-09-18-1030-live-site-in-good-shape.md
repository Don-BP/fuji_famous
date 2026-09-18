# The live site is in good shape — 2026-09-18

## Continue exactly here

The last thing I said:

> Good — glad it's landed. Everything from today is committed on `main` and
> live on the deployed site. Nothing is left half-done.

**In flight:** nothing. Everything is committed on `main`, deployed to
`gh-pages` and confirmed live. The owner has said the live site looks good.

**Literal next action:** none is outstanding — wait for the owner to name the
next piece of work. The only thing already on the table is weighting the phone
hero film's scroll so its lively middle arrives sooner; he has been offered it
twice and has not taken it up.

**Do NOT do next:**
- Do not change the hero film's scroll pacing unless he asks for it.
- Do not regenerate any artwork. The thirteen idea pictures, the manhole
  covers, the prints, the plush and the stickers are settled — including the
  two made on 18 September.
- Do not touch the deck, the entry sheet or the email.
- Do not revisit the phone hero wash or the band frosting. Both were fixed on
  18 September and he has confirmed the result.

## Background

Four things landed on 18 September: the phone hero stopped blacking itself out;
the band under the hero stopped frosting the film; three contents tiles that had
been sitting blank got the pictures that already existed further down the page;
and two new pictures were made.

Decisions that would otherwise be re-litigated:
- On a phone the copy is two thirds of the screen, so the dark wash behind it
  stays nearly clear across the kicker and headline and only closes up over the
  paragraph. The fish is meant to be seen *through* the top of the copy — the
  upright frame crops sideways, so there is no room for clear water above the
  words.
- Only the contents band loses its frosting. Every dark band further down keeps
  it, because they start against another band rather than against open film.
- Chapter 01's fish was replaced because it did not read at tile size. The old
  one is archived beside it; three other takes are in `20_new_ideas`.
- The 2027 tile uses the single classroom picture, not a four-panel day — grids
  turn to mush at tile size.

Gotchas:
- A narrow desktop preview window runs the same phone rules and can look right
  while a real phone is broken. Check at 412x832 and 360x740.
- In the browser pane always pass `tabId`; dispatch a `resize` event to force a
  scroll-driven redraw.
- Deploying: rebuild with `tools/build_site.py`, copy `dist/` into the gh-pages
  worktree's `studio-fa519005bf/`, push `ghp-deploy:gh-pages`. Verify with curl
  and a cache-busting query, never a browser tab. Pages lags about 30s.
- The build now stops if any page points at a missing file, or if a contents
  tile is blank while its idea has a picture. Read all of its check lines
  before calling anything done.

Files that matter: `promo/hub.css`, `promo/index.html`, `tools/build_site.py`,
`tools/run_endangered_water.py`, `tools/run_ideas_2027.py`,
`Fujie_Creative/20_new_ideas/`, `Fujie_Creative/17_act2_gallery/`.

Deadline: entries close 30 September 2026.
