# Chibi plush poses, and a dead Fuji button — 2026-09-16

## Continue exactly here

**The last thing I said, verbatim:**

> Fixed and live. All 28 plush and keychain images are one character now — the
> same big rounded head, big eye, plump short body and paddle snout as the
> master, whether it's the 50cm or a 10cm charm.
>
> The cause was the reference photo, not the instructions. Every later shot was
> built on the original studio plush, which had itself drifted realistic, so I
> was telling it "Chibi" while handing it a picture of the adult Fujie.

**The user then rejected that.** Three open issues, in their words:

1. The six-pose keychain assortment is still not six poses — it is about three,
   repeated. Water set: top-left, top-right, bottom-left and bottom-right are
   all effectively the same pose. Fuji set: top-left, top-right and bottom-left
   are the same pose, and bottom-right has reverted to the original adult Fujie.
2. The **Mount Fuji button on the plush line does nothing** when clicked.

**In flight:** nothing half-written. Everything is committed, pushed and
deployed. These are fresh faults found after the last deploy.

**The literal next action:** fix the Fuji button first — it is a one-line bug I
already diagnosed but did not fix. The tab click handler still toggles an old
`showFuji` class on the grid, but the display logic was rewritten to read
`grid.dataset.view` instead, so clicking changes nothing. Set `dataset.view` to
the clicked tab's `data-set` value in the click handler in `promo/hub.js`.

Then redo the two assortment images so they genuinely show six distinct poses.
Treating it as one photo of six toys has not worked twice running — consider
generating six separate single-pose shots and compositing them, which removes
the model's freedom to repeat itself.

**Do NOT do next:** do not touch the goods lines, the stickers, the pattern
collection, the deck or the entry sheet. All of those are finished and signed
off. Do not regenerate the whole plush line again — the character proportions
are now correct everywhere; only the two assortment shots are wrong.

## Background

The plush toy is Chibi Fujie — huge rounded head, one big eye, short plump
body, flat paddle snout. It is NOT the realistic adult Fujie. Keeping those two
apart is the whole basis of the proposal, so any picture holding both is a
real fault, not a nitpick.

Each goods line and each plush line has a Water / Mount Fuji switch showing one
motif at a time, eight images before a "show more". The keychain has its own
numbered line beside the plush.

Everything is live at the public studio URL and the whole project including the
artwork is now on GitHub. Fujikin's own documents are deliberately still
excluded from the repo.

Files that matter: `promo/hub.js` (the switch bug), `promo/data.js`,
`tools/run_plush3.py` (the assortment prompts), `tools/build_site.py`.
Deploying means: build the site, copy `dist/` into the gh-pages worktree, push.
