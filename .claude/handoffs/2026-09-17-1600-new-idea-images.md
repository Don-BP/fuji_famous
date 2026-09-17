# Five new ideas: generating their images for the hub — 2026-09-17

## Continue exactly here

The last thing I said:

> Five placeholders left: the hundred-year letter, the manhole covers, the open day, Sturgeon Day, and "Give Fujie a voice."
>
> **Next up — the hundred-year letter.** Before I generate, one choice: the scene is a child writing at the tank edge on open day. Do you want the sealed box in the picture too (a wooden or steel box with "2030" on it), or keep it to the child, the letter and the fish?

**In flight:** nothing — the Aqua World image is on the hub, live, and committed. The question above was not answered.

**Literal next action:** ask that one question about the sealed box, then generate three takes of the hundred-year letter scene with the same script pattern as `tools/run_ideas_aquaworld.py` (Gemini image, Chibi Fujie reference, 4:3, three takes into `Fujie_Creative/20_new_ideas/`), send them to the user, let them pick, then wire the pick into `promo/index.html` (section image + contents tile), `tools/build_site.py` (VERBATIM list), rebuild, commit, deploy.

**Do NOT do next:** do not touch the deck or entry sheet for images — they only carry text. Do not reorder or restyle the hub; the chapter structure is settled. Do not regenerate the Aqua World image. Do not generate all five images unasked — the user picks each scene one at a time and chooses between takes.

## Background

Where we got to: the hub is five chapters with a contents grid and thirteen ideas. Five new ideas were agreed and written up in both languages (cases, hub sections, deck slides, entry sheet). One of the five has its picture — Aqua World — the other four plus "Give Fujie a voice" still show an "image in production" frame.

Decisions that would otherwise be re-litigated:
- A living sturgeon needs a full exhibit tank, never a small display box; all copy says so now.
- Chibi Fujie is the only one who may "speak" (text on his panel). The official Fujie appears only on his own surface with no text over him. Images that show both should keep that split.
- The hundred-year letter is written to "the class of 2027" (the year-group), not one fish — no tagging needed.
- Manhole covers: 3–5 across Hitachiota, both Chibi and official designs; official ones need exact colours.
- Open day: 40 local families by lottery, letters in the morning, first caviar in the afternoon, on Sturgeon Day = Fujie's birthday.
- Never invent numbers or proof; English is linted with SlopMonster (clone in the scratchpad; re-clone from github.com/ItsssssJack/SlopMonster if the scratchpad is gone).

Gotchas:
- Hidden Word hangs; the entry-sheet script runs Word visibly on purpose. If it fails, kill WINWORD and delete `~$` lock files in Documents_for_dev.
- Entry sheet must stay at 3 pages (box text is 8.5pt). Check page count after any change.
- Deploying: rebuild with `tools/build_site.py`, copy `dist/` into the gh-pages worktree's `studio-fa519005bf/`, push `ghp-deploy:gh-pages`. Worktree path is in `git worktree list`.
- Screenshots in the browser pane often come back black; check the page with DOM reads instead.

Files that matter: `promo/index.html`, `promo/hub.js`, `promo/cases.js`, `promo/hub.css`, `tools/build_site.py`, `tools/run_ideas_aquaworld.py`, `tools/gen.py`, `tools/deck.js`, `tools/entry_fields.json`, `tools/fill_entry.ps1`, `docs/superpowers/specs/2026-09-17-hub-chapters-design.md`.

Deadline: entries close 30 September 2026.
