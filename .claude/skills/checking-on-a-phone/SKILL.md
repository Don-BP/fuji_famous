---
name: checking-on-a-phone
description: Use before calling any Fuji Famous layout, hero film, scroll effect or panel change finished, and whenever something looks right on a desktop preview but is reported broken on a phone. Also use when a preview screenshot comes back black, when a change appears not to have taken effect, or when checking the hub, the game or the timeline after editing CSS or scroll behaviour.
---

# Checking it on a phone

## Overview

A narrow desktop window is not a phone. It runs the same CSS rules but keeps a
desktop pointer, a desktop user agent and a desktop device pixel ratio, so the
load-time gates and the touch behaviour never fire — and that is exactly where
the bugs have been. Every phone bug in this project's history was invisible in a
narrow desktop preview.

**Check at a real phone size: 412 × 832.**

## Steps

1. Start the server: `preview_start {name: "fujie-site"}` for the game, or serve
   `dist/` with `fujie-dist` for the hub.
2. `resize_window {preset: "mobile"}` — or `{width: 412, height: 832}`.
3. **Reload the page.** Load-time device gates only re-run on a fresh load, so a
   resize alone proves nothing.
4. Walk the list below.
5. `resize_window {preset: "desktop"}` when finished, and check desktop again —
   several phone fixes have broken the wide layout.

## What to look at

| Thing | What has gone wrong before |
|---|---|
| The hero film | Did not start at all on a real phone while working in preview |
| The wash over the hero | Covered the water instead of the words; the water must stay readable behind the text as it scrolls away |
| Hero into the dark band | A visible seam where the two meet |
| Panels and close buttons | The case panel's close button sat on top of the title |
| The bottom of the game | Four controls crowd each other on a small phone |
| Background plates | The widescreen plates only load above 1100px — the portrait art is a different file and must be looked at separately |

## Where the phone-sensitive things live

| Thing | File |
|---|---|
| The scroll-driven hero film | `promo/hero.js`, frames in `promo/film/` (`m480` / `m720` for phones, `w1280` for wide, plus posters) |
| The wash, the bands, the seam, the panels | `promo/hub.css` |
| Contents, chapters, case panel, language switch | `promo/hub.js` |
| The swimming Chibi | `promo/buddy.js` |
| The game's controls and backgrounds | `site/game.js`, `site/art/` |

## When the screenshot comes back black

The preview pane sometimes returns a black image. That is the capture failing,
not the page. Do not conclude anything from it. Instead:

- `read_page` for structure and text,
- `javascript_tool` for computed styles and element positions,
- `read_console_messages` and `preview_logs` for errors,
- or fetch the live URL with `curl` and read the markup.

## When a change seems not to have taken effect

Browsers cache the art hard. Art referenced with a version marker (`…png?v=2`)
must have that number bumped when the file changes, and the numbers are typed by
hand in more than one place. If a fix looks absent, check the version number
before re-fixing anything. After deploying, allow about a minute before the live
site serves the new files.

## Do not

- Do not compare files by checksum to decide whether a deploy landed. It has been
  unreliable here. Load the page and look.
- Do not "fix" the swimming Chibi drifting across the goods photographs. That is
  intentional.
- Do not leave the viewport emulated at mobile when the check is done.
