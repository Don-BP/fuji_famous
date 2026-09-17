# New idea images: letter and manholes done, three left — 2026-09-17

## Continue exactly here

The last thing I said:

> Fixed and put aside. He's saved with the rest of the new-ideas work, not used anywhere.
>
> Noted for good: the decided Chibi Fujie is what's in `Fujie_Creative/01_character`.
>
> **Three pictures left:** the open day, Sturgeon Day, and "Give Fujie a voice."

**In flight:** nothing — everything is finished, committed and deployed.

**Literal next action:** ask the user which of the three remaining ideas to picture
first (the open day, Sturgeon Day, or "Give Fujie a voice"), then generate three
takes of that one scene, send them, let them pick, wire the pick into
`promo/index.html` and `tools/build_site.py`, rebuild, commit, deploy.

**Do NOT do next:** do not touch the manhole covers — six are chosen, live and
clickable, and the user picked them by hand. Do not use or promote the swimming
Chibi from `chibi_swimmer_sheet.png`; it is kept for later only. Do not regenerate
the hundred-year letter picture. Do not touch the deck or entry sheet for images —
they only carry text. Do not reorder or restyle the hub.

## Background

Where we got to: the hub is five chapters with thirteen ideas. Ten now have
pictures. Today added the hundred-year letter scene and six manhole covers.

Decisions that would otherwise be re-litigated:
- The Satomi farm is an indoor recirculating hall with deep round tanks, about
  3,000 square metres, over ten thousand fish. Never draw it as an open-air pond.
  No public photos of the inside exist, so any interior is a reconstruction.
- A manhole cover must be drawn as one casting with the character supplied as a
  reference. Pasting artwork onto a generated blank never reads as metal — that
  was tried twice and rejected. The working script is `tools/run_ideas_manhole_whole.py`.
- Covers carry no text at all, so there is no invented kanji to defend.
- Because the covers are drawn, the official Fujie on them is a redrawing, not the
  original file. The case copy already says the manual's owner signs off colour.
- The decided Chibi Fujie is the artwork in `Fujie_Creative/01_character`. Variants
  that fall out of scenes are kept in `20_new_ideas` but never promoted.
- Decisions recorded in a handoff are settled — build them, do not re-ask them.

Gotchas:
- Gallery ids must not contain `_fuji`; that string switches on a set-tab feature.
- Hidden Word hangs; the entry-sheet script runs Word visibly on purpose.
- Entry sheet must stay at 3 pages. Check the page count after any change.
- Deploying: rebuild with `tools/build_site.py`, copy `dist/` into the gh-pages
  worktree's `studio-fa519005bf/`, push `ghp-deploy:gh-pages`. Path is in `git worktree list`.
- Browser-pane screenshots often come back black; read the DOM instead.

Files that matter: `promo/index.html`, `promo/data.js`, `promo/cases.js`,
`promo/hub.js`, `promo/hub.css`, `tools/build_site.py`, `tools/gen.py`,
`tools/run_ideas_manhole_whole.py`, `tools/build_manhole_sheet.py`,
`Fujie_Creative/21_manholes/`, `Fujie_Creative/20_new_ideas/`.

Deadline: entries close 30 September 2026.
