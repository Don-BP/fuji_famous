# Widescreen plates, the studio site, and the author credit
**2026-09-16**

## Continue exactly here

**Last thing I said, verbatim:**

> The crash caught it between rendering and deploying — all eleven plates had
> finished, nothing was lost, and it's all shipped now.
>
> **You were right about both plates.** Asked to widen the scene, the model tiled
> the portrait one instead: `bg_tank_grown` grew two extra tank walls standing in
> the middle of the frame, `bg_tank_early` did the same, and `bg_shell` came back
> as three panels with visible seams down it. All three are repainted.

**In flight right now:** Nothing in flight. Everything is built, deployed and
verified against the live servers.

**The literal next action:** Show the user the eight widescreen background plates
they have not looked at yet and repaint any they dislike. `bg_lost` is the one I
would query first — it came back as a concrete tunnel rather than the abandoned
hatchery tank the portrait version shows. `tools/run_bg_wide_fix.py` is the
re-run script; add the plate name to its list and adjust the scene sentence.

**Do NOT do next:**
- Do not move the studio site from its unlisted address to the main URL. That is
  a deliberate choice until after the contest deadline, 30 September 2026, and
  needs the user's say-so.
- Do not regenerate the character art, sticker sheets, plushies, merch sets or
  the wamon collections. All finished and accepted.
- Do not re-tune the pet game's needs or the mini-game difficulty. Three rounds
  of tuning were accepted this session.
- Do not redraw the official Fujie illustration in any form (Article 7).

## Background

The game now has a companion site. `dist/` is assembled by `tools/build_site.py`
from `site/` (the game, untouched) and `promo/` (a portfolio hub plus a scrolling
40-year timeline), and deployed into an unlisted folder on the gh-pages branch
whose name is stored in `promo/.studio_path`. The public game link at the site
root is unchanged and still what the deck points at.

**Decisions made, do not re-open:**
- The studio site is published unlisted and carries a no-index instruction. The
  user chose this over the main URL because the contest deadline has not passed.
- Author credit is **Vittorio Zumpano ／ 株式会社ブレインパワー 大阪**, taken from
  `tools/entry_fields.json`, shown at the top, in the hero and in the footer of
  both pages, in both languages.
- Widescreen plates load only above 1100px; phones keep the portrait set and
  never download them.
- The roaming chibi wears a neutral face and only switches to the happy sparkly
  pose while the cursor is touching him.

**Gotchas:**
- The preview pane throttles timers and often returns black screenshots. Verify
  by reading the page's own state, not by how an animation looks in the pane.
- Comparing a live file to a local one with a checksum always fails on Windows
  because of line endings. Strip carriage returns before comparing.
- The game's files are version-stamped (`app.css?v=3`). Bump that number when
  changing them or returning visitors keep the cached copies.

**Files that matter:**
- `promo/` — the hub, timeline, roaming chibi and gallery manifest
- `tools/build_site.py`, `tools/make_portable.py` — site build and offline build
- `tools/run_bg_wide.py`, `tools/run_bg_wide_fix.py` — the widescreen plates
- `Fujie_Creative/12_`, `13_`, `14_` — the newest merch sets
