"""Idea 05 - give Fujie a voice: footage nobody has ever seen.

The scene is feeding time at the Satomi farm, when the whole surface of the water
boils for a few dozen seconds. A keeper films it on a phone and it goes out in
Chibi Fujie's voice. So the picture is the filming, the water, and the post.

The farm interior is the decided one: an indoor recirculating hall with deep round
tanks, never an open-air pond.

Screens are generated EMPTY - no mascot, no caption. The model cannot draw Fujie
at that size and invents nonsense Japanese for captions, so both are composited
afterwards by build_voice_screen.py from the real artwork and a real font. Same
lesson as the Sturgeon Day picture.

Output: Fujie_Creative/20_new_ideas/voice_*.png
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen

OUT = "D:/Fuji_Famous/Fujie_Creative/20_new_ideas/"

RULES = (
    "*** MASCOT RULE ***\n"
    "Do NOT draw any mascot, cartoon character, logo or illustration anywhere in this picture - not "
    "on the phone, not on clothing, not on the walls. The real mascot artwork is added afterwards "
    "by hand and anything drawn here would have to be painted out.\n\n"
    "*** TEXT RULE ***\n"
    "There must be NO text anywhere in the picture at all: no words, no kanji, no kana, no Latin "
    "letters, no numbers, no captions, no subtitles, no app names, no interface labels, no buttons "
    "with writing on them, no signage, no equipment markings, no watermark. Every surface is blank. "
    "Earlier attempts filled screens with invented nonsense Japanese and were thrown away.\n\n"
    "*** PHONE SCREEN RULE ***\n"
    "Where a phone screen is shown, it shows ONLY the video: the churning water filling the whole "
    "screen, edge to edge, as a vertical clip. Across the LOWER THIRD of the screen lay one plain, "
    "clean, EMPTY dark translucent strip, evenly lit, with absolutely nothing on it - no writing, no "
    "icons, no buttons. At the LEFT end of that strip leave a plain EMPTY circle, about as tall as "
    "the strip, a flat pale disc with nothing inside it. The strip and the circle are left blank on "
    "purpose and are filled in afterwards.\n\n"
    "*** PEOPLE RULE ***\n"
    "This farm is in Ibaraki, Japan. Every person in the picture is JAPANESE - Japanese face, "
    "Japanese features, black hair, and Japanese hands where hands are shown. No European, white or "
    "Western-looking people anywhere, and no light brown or blonde hair. The first attempt came "
    "back with a European keeper and was thrown away.\n\n"
    "*** FISH RULE ***\n"
    "The sturgeon are REAL photographed fish: silver-grey, long flat pointed snouts, four barbels "
    "under the snout, rows of bony scutes down the back and flanks, shark-like upswept tails. Real "
    "animals, never drawings, never cartoons. Do NOT draw sharks, dolphins or generic fish.\n\n"
)

PANEL_LAYOUT = (
    "*** LAYOUT ***\n"
    "This image is a THREE-PANEL editorial photo layout. One LARGE VERTICAL panel fills the left "
    "half of the frame, and TWO smaller panels are stacked one above the other filling the right "
    "half. The three panels are separated by thin, clean, even white gutters and sit flush to the "
    "edges of the frame. All three are photographs in the same documentary style, light and colour. "
    "No captions on the layout itself, no page numbers, no border around the outside.\n\n"
)

HALL = (
    "PHOTOREALISTIC editorial documentary photography INSIDE a modern Japanese land-based sturgeon "
    "farm - a large clean indoor aquaculture hall, not an aquarium and not an outdoor pond. High "
    "steel roof structure, bright even daylight through roof panels, pale walls. Rows of LARGE DEEP "
    "circular rearing tanks: dark grey-green fibreglass tanks about four metres across and "
    "chest-high, filled to the brim with deep clear water. Grey pipework, feed lines and a "
    "filtration plant run neatly along the wall; the wet concrete floor has drainage channels. "
    "Natural light, honest colour, 35mm documentary photograph, no watermark. "
)

BOIL = (
    "It is feeding time, and the surface of the nearest tank is BOILING: dozens of big sturgeon "
    "crowding and turning just under and through the surface, backs and snouts breaking the water, "
    "white spray and churn everywhere, the water alive. Violent, thrilling and completely real - "
    "photographed at a fast shutter speed with the droplets frozen in the air. "
)

TAKES = {
    # The filming itself: a keeper, a phone, and the water going mad.
    "voice_a": PANEL_LAYOUT + HALL + BOIL +
               "LEFT LARGE PANEL: a young JAPANESE keeper with black hair, in a clean farm coat and waders stands at the tank "
               "rim holding an ordinary smartphone out over the boiling water in one hand, filming "
               "it, entirely absorbed - no posing, no looking at the camera. The churn fills the "
               "bottom of the panel. "
               "TOP RIGHT PANEL: the phone held upright in a Japanese hand, filling the panel, its screen "
               "showing the churning water as a vertical clip with one empty dark strip across the "
               "lower third and an empty pale circle at the left end of that strip. "
               "BOTTOM RIGHT PANEL: an extreme close-up of a single translucent amber sturgeon egg "
               "at the moment of hatching, a tiny larva emerging, shot under soft hatchery light "
               "against dark water.",

    # The phone is the hero: what the post actually looks like.
    "voice_b": PANEL_LAYOUT + HALL + BOIL +
               "LEFT LARGE PANEL: an ordinary smartphone held upright in two Japanese hands fills most of "
               "the panel, seen slightly from above. Its screen is entirely filled by the vertical "
               "clip of the boiling water, with one empty dark strip across the lower third of the "
               "screen and an empty pale circle at the left end of that strip. Behind and around "
               "the phone, softly out of focus, the real tank rim and the real churn. "
               "TOP RIGHT PANEL: the boiling surface photographed straight down from above, filling "
               "the panel - backs, snouts and spray, no people. "
               "BOTTOM RIGHT PANEL: a Japanese keeper's hands tipping feed from a scoop into the "
               "tank, the water already beginning to rise to meet it. The TANK IS CENTRED in this "
               "panel: the round tank sits squarely in the middle of the frame with its far rim "
               "visible, the falling feed and the rising water at the centre of the picture, and "
               "roughly equal space to left and right. Do not push the tank off to one side and do "
               "not let the walkway or the floor take over the frame.",

    # The water itself carries the panel; the phone is the proof.
    "voice_c": PANEL_LAYOUT + HALL + BOIL +
               "LEFT LARGE PANEL: the boiling water fills the whole panel, shot low from the tank "
               "rim - a wall of churning sturgeon and spray, the hall roof soft and bright above. "
               "No people. "
               "TOP RIGHT PANEL: a Japanese keeper seen from behind on the walkway between the tanks, one "
               "arm out, filming the water on a phone, small in a wide clean shot of the hall. "
               "BOTTOM RIGHT PANEL: the phone screen filling the panel, photographed straight on, "
               "showing the churning water as a vertical clip with one empty dark strip across the "
               "lower third and an empty pale circle at the left end of that strip.",
}

if __name__ == "__main__":
    wanted = sys.argv[1:] or list(TAKES)
    for name in wanted:
        print(name, flush=True)
        gen(RULES + TAKES[name], OUT + name + ".png", aspect="4:3")
