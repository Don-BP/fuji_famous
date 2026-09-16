# Fujie contest entry — game expansion
**2026-09-15**

## Continue exactly here

**Last thing I said, verbatim:**

> Whack-a-shark works. Testing the other three.

**In flight right now:** The interactive piece was just rebuilt from a simple
tap-through story into a full virtual-pet raising game, split across four files
in `site/`. Whack-a-shark is tested and working. The browser test of the other
three mini-games (Egg Catch, Upstream Dash, Which Shell) was cut off before it
returned a result — they are written but **unverified**.

**The literal next action:** Serve `site/` on port 8777, open it, and play
through Egg Catch, Upstream Dash and Which Shell one at a time to confirm each
starts, scores, ends and returns to the tank without a console error. Fix
whatever breaks.

**Then, in order:**
1. Push the rebuilt game to the `gh-pages` branch so the live URL updates —
   it currently still serves the OLD single-screen version.
2. Rebuild the offline single-file copy (it is also still the old version).
3. Update deck slide 16 — it describes the old "control the valve" piece, not
   the new game with four mini-games.
4. Generate English sticker sheets (40 stickers). Still not started, and the
   user asked for everything bilingual.

**Do NOT do next:**
- Do not rebuild or re-QA the deck for layout. It passed a full 19-slide visual
  check and is ready. Only slide 16's *wording* needs updating.
- Do not regenerate the LINE stickers to "match the fins". That was tried and
  came back worse (duplicate captions, one sticker turned orange). The good set
  was restored from `02_stickers/old/`. Leave it.
- Do not touch the entry sheet. It is filled in and correct.
- Do not republish the claude.ai artifact. GitHub Pages replaced it.

## Background

Contest: Fujikin's internal "Make Fujie Famous" idea contest. Deadline
**30 September 2026**. Gold prize ¥200,000. Entrant: Vittorio Zumpano,
Brain Power Osaka, entering solo.

The entry's whole argument is that Fujikin invented Japanese caviar — a real
world-first sturgeon aquaculture programme running since 1987 — and that their
mascot is that actual fish. Headline: 「フジィは、実在する。」

**Decisions already made, do not re-open:**
- The cute character is framed as ちびフジィ, a *proposed second form*, never as
  an alteration of the official Fujie. The manual's Article 7 is respected.
- The public GitHub repo deliberately excludes `Fujie_Creative/` so another
  entrant cannot read the submission before the deadline.
- Character master is `master_v3_wave.png` — fins only, swept back, no feet.

**Gotcha:** PowerShell 5.1 mangles Japanese in `.ps1` files. All Japanese for
the entry sheet lives in `tools/entry_fields.json`; the script stays ASCII.

**Files that matter:**
- `site/` — the game (index.html, app.css, game.js, i18n.js) + stage images
- `Fujie_Creative/05_submission/` — the three files that get emailed
- `Fujie_Creative/05_submission/README_提出手順.md` — email address, subject
  line, Japanese email body, pre-send checklist
- `tools/gen.py` — image generation; archives old versions to `old/` on write
- Live: https://don-bp.github.io/fuji_famous/ (serving the old version)

## Genre research (arrived after the above — already reflected in the build)

Checked the game against Tamagotchi P1/P2, Tamagotchi Uni, and the Digimon
virtual pets. What it confirmed:

- **Four care stats is the genre norm** (Tamagotchi P1 uses hunger, happiness,
  discipline, health). Ours uses food, mood, energy, water quality — correct
  count, and water quality is the Fujikin-specific one. Do not add a fifth.
- **The pet must signal needs without a tutorial** — Tamagotchi uses a beep
  plus an attention icon. Ours uses a thought bubble over the fish plus a
  pulsing outline on whichever action button is needed. Matches the convention.
- **Care quality should gate growth, not just time.** Ours only accrues growth
  when all four needs are healthy. Correct.
- **Modern entries removed permanent death.** Ours has a lose state, but it
  restarts in one tap and is framed as the real 1992 story — 95 of 100 didn't
  survive. Keep that; it is the emotional centre of the whole entry.

**Deliberate difference — do not "fix" it:** real Tamagotchi decay is about six
minutes per point, tuned for a pet you keep for weeks. Ours is far faster
because this has to be a complete arc in roughly 90 seconds in a judging room.
If a future session thinks the decay rates look aggressive, that is why.

## Second research pass — two things worth acting on

**1. UI convention we currently break.** Across Pou, Talking Tom and the idle
aquarium games, the stat bars sit along the TOP edge and only the action
buttons occupy the bottom bar — the bottom is kept clear as the tap zone.
Ours stacks four stat bars AND the growth bar AND four action buttons all in
the bottom panel, which is crowded on a small phone. Worth moving the four
stat bars up under the year/stage header. Not urgent, but it is the one place
the build diverges from every successful title.

**2. Whack-a-Shark is more on-brand than it looks — use this.** Fujikin's own
caviar site has a page titled 「サメとの違い」 (How it differs from a shark),
because チョウザメ literally reads as "butterfly shark" and people constantly
assume sturgeon are sharks. So a game where Fujie smacks the sharks he keeps
being mistaken for is a real joke rooted in the company's own material, not a
generic arcade filler. Say so in the game's caption and on the deck — it turns
the weakest-looking mini-game into a talking point.

Research also flagged that mini-games should tie to the pet rather than being
reskinned arcade games. Egg Catch (sturgeon roe) and Upstream Dash (Fujie's
official profile says he "swims up the reverse current named extremity") are
already tied. Which Shell is the only genuinely generic one — lowest priority
if anything has to be cut.
