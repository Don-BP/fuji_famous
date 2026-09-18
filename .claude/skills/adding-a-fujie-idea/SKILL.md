---
name: adding-a-fujie-idea
description: Use when adding, removing, renaming or reordering an idea or a goods line in the Fuji Famous proposal - anything that changes what the hub, the deck and the entry sheet say. Also use when a stated count is wrong, such as the number of ideas, chapters, goods lines or deck slides, or when one surface shows an idea that another surface does not.
---

# Adding an idea everywhere it lives

## Overview

One idea appears on five surfaces that do not know about each other. Changing it
in one place and not the others is the single most repeated mistake in this
project, and the counts ("thirteen ideas", "five lines", "25 slides") are stated
as words in several files and drift apart silently.

**The rule: an idea is not added until all five surfaces agree and every count
has been recounted, not remembered.**

## The five surfaces

| Surface | File | What goes in |
|---|---|---|
| Hub section | `promo/index.html` | A `<section id="…" class="band idea">` with its art, body copy and a `data-case` button. Alternates `band idea` / `band dark idea` down the page |
| Hub contents grid | `promo/index.html` (`#contents`) | A card linking to the new section id |
| Hub wording | `promo/hub.js` | The Japanese and English strings for every `data-t` key used in the new section |
| The full case | `promo/cases.js` | One entry keyed by the section id, **both `ja` and `en`**, exactly five beats in the entry sheet's order: the scene, how it reaches people, why they come to like Fujie and Fujikin, expected effect, the first step |
| The deck | `tools/deck.js` | A slide, plus its line in the contents slide |
| The entry sheet | `tools/entry_fields.json` + `tools/fill_entry.ps1` | The idea text in the submitted document |

The section id, the `data-case` key and the `cases.js` key must be the same word.

## Steps

**Never write the shape from scratch.** For each surface, copy the nearest
existing idea's entry — section, contents card, case, slide — and change the
words. The shapes are not documented anywhere else.

1. Write the five beats first, in Japanese and English. Everything else is a
   trimmed version of them — nothing in the hub or the deck is ever a new fact.
2. Add the `cases.js` entry.
3. Add the hub section and its contents card, in the right chapter, with the
   right alternating band colour.
4. Add every new `data-t` string to both languages in `hub.js`.
5. Add the deck slide and its contents line.
6. Update the entry sheet.
7. **Recount.** See below.
8. Rebuild: `python tools/build_site.py`, then `python tools/make_portable.py`.
9. Check it on a phone as well as on desktop.

## Recounting

Never trust a number already written down. Count them:

- Ideas — the top-level keys in `promo/cases.js`.
- Idea sections — `<section>` tags carrying `class="… idea"` in `promo/index.html`.
- Contents cards — entries in the `#contents` grid.

These three must be equal. Then fix the places that say the number in words:

- `promo/hub.js` → `tocH` (both languages)
- `promo/index.html` → the `#contents` heading and the `<meta name="description">`
- the deck's own contents slide
- the README and any send-off note that states a slide count
- any section body that says "five lines" or similar about its own list

## Gotchas

| Gotcha | What to do |
|---|---|
| The entry sheet script hangs on Word | Kill `WINWORD`, delete the `~$…` lock file next to the document, run again |
| The offline single-file copy is stale | `make_portable.py` is a step, not an afterthought — run it last, every time |
| Deck slides do not pick up data changes | The deck is built from `tools/deck.js`, not from `data.js`. Edit it directly |
| A count is right in Japanese and wrong in English | Both languages state it separately. Fix both |
| An idea shows on the hub but not in the deck | The five surfaces are independent. Walk the table again |
