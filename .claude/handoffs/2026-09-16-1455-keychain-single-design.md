# One keychain design, and a browser cache that hid two fixes — 2026-09-16

## Continue exactly here

**The last thing I said, verbatim:**

> Both things were actually fixed and deployed each time — I checked the live
> files from the server just now and they're correct: no six-pose sheet in the
> gallery list, and the Mount Fuji switch has the working handler. Your browser
> was serving its own saved copies of the two files that matter...
>
> **You will need one hard reload** — Ctrl+Shift+R on the studio page.

**In flight:** nothing. Everything is committed, pushed, deployed and verified
against the live server.

**The literal next action:** wait for the user to hard-reload the studio and say
whether the keychain line and the Mount Fuji switch now look right. If they do,
this thread is closed and the next piece of work is theirs to choose.

**Do NOT do next:** do not revive the six-variant / six-pose keychain assortment
in any form — it was tried five times, rejected every time, and killed by the
user's explicit instruction. Do not regenerate the plush or keychain artwork.
Do not touch the goods lines, the stickers, the pattern collection, the deck or
the entry sheet.

## Background

The keychain now shows as ONE design in one pose. The line opens on the shot of
the charm hanging from a canvas bag strap in the street — the user's own pick,
and the best image in the line. The grey studio shot was dropped from the
gallery entirely. The Mount Fuji sheet keeps a single studio shot of the charm
in its knitted cap.

Why the assortment died: six photographs of one stuffed toy only ever read as
one toy photographed six times. A plush keeps its sewn shape, so all that
changes between shots is which way it faces. Recolouring them into six editions
did not rescue it either.

The real fault of the session was invisible caching. The studio's scripts are
always called data.js and hub.js, so the user's browser kept serving yesterday's
gallery list and yesterday's switch however many times I deployed. Every asset
reference is now stamped with a fingerprint of the file, so it refetches only
when the file genuinely changes. That cannot recur.

**Deploy layout — got this wrong once, cost a full restore.** The published
branch root holds the PUBLIC GAME. The studio goes inside `studio-fa519005bf/`.
Copying the build to the root flattens the game and erases the studio.

Files that matter: `promo/data.js`, `promo/hub.js`, `promo/index.html`,
`tools/build_site.py`. `tools/run_plush_set.py` generates the abandoned six-pose
assortment and is now dead weight.
