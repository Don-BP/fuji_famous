# Fujie game — art pass and care logic
**2026-09-16**

## Continue exactly here

**Last thing I said, verbatim:**

> That was just the wait timer from the auto-play run finishing — no new
> information, and nothing changed. The work from your last request is complete
> and verified as reported above.
>
> Still outstanding from before this session, whenever you want them: the live
> GitHub Pages URL serves the old game, the offline single-file copy is out of
> date (and will need rebuilding to inline the new art, since it currently only
> handles images referenced from the HTML), and deck slide 16 still describes
> the old "control the valve" piece rather than the game as it now stands.

**In flight right now:** Nothing in flight — the last task (stage-specific
expressions + care logic) was completed and verified in the browser.

**The literal next action:** Rebuild the offline single-file copy of the game so
it actually contains the new art. `tools/make_portable.py` only inlines images
referenced from the HTML, so it will miss every piece of art referenced from the
stylesheet and the game script, and all the `.jpg` backgrounds. It also does not
inline the stylesheet or the scripts at all, so the current output is still the
old single-screen version.

**Then, if the user asks:**
1. Push the rebuilt game to `gh-pages` so the live URL stops serving the old
   version. This publishes — get their go-ahead first.
2. Update deck slide 16's wording. Layout is fine; only the text is wrong.
3. English sticker sheets (40 stickers), still not started.

**Do NOT do next:**
- Do not regenerate the character art, backgrounds, UI kit, icons or expression
  sets. All done and visually checked this session.
- Do not touch sticker sheets 01 and 02. Sheet 03 was *added* for dynamic poses;
  the first two are the known-good set and must be left alone.
- Do not rebalance the need decay rates or add a fifth need. Deliberate.
- Do not redraw the adult stage. It is Fujikin's official mascot (Article 7).
- Do not re-QA the deck for layout.

## Background

The whole game was reskinned: painted backgrounds behind every screen, real
sprites for all four mini-games, an illustrated UI (buttons, panels, meters,
icons, menu rows), game fonts, a full-bleed responsive layout, and per-stage
facial expressions wired to the care loop.

**Decisions made, do not re-open:**
- Expression sprites must reference ONLY their own stage image. Passing the
  chibi master as a reference drags every stage into that silhouette — it made
  the larva look like a fry and the slim juvenile look like a chubby chibi.
- Egg and adult stages have no expressions by design; the thought bubble and
  pulsing buttons carry the signal there.
- Button and meter art is a wide pill rebuilt by `tools/repill.py` and then
  9-sliced, so the rounded ends never stretch. Do not go back to stretching a
  square plate.
- Fonts are Dela Gothic One (titles, numbers) and Zen Maru Gothic (everything
  else). This traded some of the old Mincho gravitas on the 1992 screen for a
  game feel — a deliberate call the user asked for.

**Gotchas:**
- The browser caches art hard. `ui_gauge.png` is referenced with `?v=2` for that
  reason. If art looks stale, suspect cache before suspecting the file.
- The gauge art had a white interior that painted over the groove; it was
  flood-filled dark, and its slice must include the rim rows (`12 32 fill`).
  `0 32 fill` renders pale and wrong.
- Timers throttle badly in the preview pane, so real-time playtests run in slow
  motion. Budget minutes, not seconds, for a full playthrough check.

**Files that matter:**
- `site/` — the game (index.html, app.css, game.js, i18n.js) and `site/art/`
- `tools/run_game_art*.py`, `run_ui_kit.py`, `run_faces2.py`, `repill.py`,
  `optimise_game_art.py` — the generators, all re-runnable
- `Fujie_Creative/06_game/` — full-resolution masters for everything in site/art
- `Fujie_Creative/02_stickers/sticker_sheet_03_action.png` — the new action set
