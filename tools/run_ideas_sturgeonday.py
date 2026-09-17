"""Idea 11 - register "Sturgeon Day" officially.

The idea is that once a year the name comes up on its own, in ordinary life:
a calendar app lists the day, and a morning show fills its "today is the day of"
slot with it, with Chibi Fujie on screen for a second.

So the picture is a normal Japanese morning at home, not a ceremony. Multi-panel,
because that is the house style for these now.

TEXT: this is the one picture in the set that NEEDS text - a day with no name on
screen is not a day. Exactly one string is allowed, チョウザメの日, spelled out
character by character in the prompt. Everything else stays blank. If the model
mangles it, fall back to generating blank screens and compositing the caption
with PIL in a real Japanese font, the way build_manhole_sheet.py composites.

Output: Fujie_Creative/20_new_ideas/sday_*.png
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen

CHIBI = "D:/Fuji_Famous/Fujie_Creative/01_character/master_v3_wave.png"
OUT = "D:/Fuji_Famous/Fujie_Creative/20_new_ideas/"

NO_FISH = (
    "*** MASCOT RULE ***\n"
    "Do NOT draw any fish, mascot, animal, cartoon character or illustration anywhere in this "
    "picture - not on the television, not on the phone, not on the walls, nowhere. The real mascot "
    "artwork is added afterwards by hand and any fish drawn here would have to be painted out. "
    "Where the mascot will go, leave a CLEAN EMPTY PALE AREA: on the television's lower-third band, "
    "the day's name sits in the RIGHT-HAND part of the band, and the LEFT-HAND part of the band is "
    "left completely empty, plain and evenly lit - an unbroken pale panel about as tall as the band "
    "and about as wide as it is tall, with nothing on it at all.\n\n"
)

RULES = (
    "*** TEXT RULE - READ CAREFULLY ***\n"
    "Exactly ONE piece of text is allowed in this picture, and it is the name of the day. It is "
    "seven Japanese characters in a straight horizontal row, in this exact order:\n"
    "  1. katakana チ\n"
    "  2. small katakana ョ\n"
    "  3. katakana ウ\n"
    "  4. katakana ザ (with the two small dagger strokes at its top right)\n"
    "  5. katakana メ\n"
    "  6. hiragana の\n"
    "  7. kanji 日 (a simple upright rectangle divided by one horizontal bar)\n"
    "Written together: チョウザメの日\n"
    "Set it in a clean modern sans-serif Japanese screen font, evenly spaced, upright, every "
    "character complete and correctly formed, none doubled, none merged, none invented. "
    "NOTHING ELSE anywhere in the picture may carry text. This is absolute. In particular the "
    "television must show NO other writing at all: no programme title, no corner banner, no red or "
    "coloured news strap, no headline box, no channel logo, no clock, no ticker, no subtitles. "
    "Earlier attempts filled those straps with invented nonsense Japanese and were thrown away. "
    "Also no app names, no weekday names, no newspaper text, no packaging text, no watermark. "
    "Plain calendar date digits in a month grid are allowed; a year number is NOT. Every other "
    "surface in the picture is blank.\n\n"
    "*** SCREEN RULE ***\n"
    "Screens are photographed as real screens: slight glare, correct perspective, the picture "
    "sitting behind glass, not pasted flat onto the frame. The morning show graphic is ONE simple "
    "clean pale lower-third band across the bottom of the television picture and nothing else - the "
    "day's name in the right-hand part of it, the left-hand part left empty. Behind the band the "
    "television shows an ordinary bright morning studio with two presenters at a desk. The band "
    "must be large, level, unobstructed and easy to read.\n\n"
    "*** MOOD RULE ***\n"
    "An ordinary, unremarkable weekday morning. Nobody is celebrating and nobody is posing. This is "
    "the point of the idea: the name simply turns up. Warm, relaxed, domestic, gently lit.\n\n"
)

PANEL_LAYOUT = (
    "*** LAYOUT ***\n"
    "This image is a THREE-PANEL editorial photo layout. One LARGE VERTICAL panel fills the left "
    "half of the frame, and TWO smaller panels are stacked one above the other filling the right "
    "half. The three panels are separated by thin, clean, even white gutters and sit flush to the "
    "edges of the frame. All three are photographs in the same documentary style, light and colour. "
    "No captions on the layout itself, no page numbers, no border around the outside.\n\n"
)

LOOK = (
    "PHOTOREALISTIC editorial documentary photography, early morning in an ordinary modern Japanese "
    "home. Soft daylight through a window, plain tidy interior, wooden floor, a low table, "
    "breakfast things. Real skin tones, honest colour, 35mm documentary photograph, no watermark. "
)

TAKES = {
    # The day arriving at home, with the screen as the hero.
    "sday_a": PANEL_LAYOUT + LOOK +
              "LEFT LARGE PANEL: a family at breakfast in the living room - a mother and two "
              "children at a low table with rice bowls and tea. The television is on across the "
              "room, and on its screen a morning information programme is running its 'today is the "
              "day of' segment: the day's name on the right of a pale lower-third band, the left of "
              "the band empty. One of the children has looked up from breakfast at the screen. "
              "TOP RIGHT PANEL: a close, slightly angled shot of a smartphone held in one hand, its "
              "calendar app open on the month view, plain date digits in a grid, and the day's name "
              "printed small in the cell for that date - the only words on the screen. "
              "BOTTOM RIGHT PANEL: the television screen filling the panel, photographed straight "
              "on: the morning show picture with the day's name on the right of the lower-third "
              "band and the left of the band empty, a faint reflection of the room in the glass.",

    # The screen itself as the hero panel.
    "sday_b": PANEL_LAYOUT + LOOK +
             "LEFT LARGE PANEL: the television screen fills most of the panel, photographed at a "
             "slight angle from the sofa, with the edge of the room and a cup of tea soft in the "
             "foreground. On screen, the morning programme's 'today is the day of' segment: the "
             "day's name on the right of a pale lower-third band, the left of the band empty. "
             "TOP RIGHT PANEL: a woman in her thirties in a kitchen, drying her hands, half turned "
             "towards the television in the next room, catching the segment as she passes. "
             "BOTTOM RIGHT PANEL: a close shot of a smartphone lying on the low table beside a tea "
             "cup, its calendar app open on the month view, plain date digits in a grid and the "
             "day's name small in that day's cell.",

    # Quieter and more everyday: the phone is the hero.
    "sday_c": PANEL_LAYOUT + LOOK +
             "LEFT LARGE PANEL: a close over-the-shoulder shot of a young woman sitting on the "
             "train in the morning, looking at the calendar app on her phone - the month view with "
             "plain date digits and the day's name small in today's cell. Ordinary commuters and "
             "train window light soft behind her. "
             "TOP RIGHT PANEL: a living room television across an empty room, the morning "
             "programme's segment on screen with the day's name on the right of a pale lower-third "
             "band and the left of the band empty, nobody watching. "
             "BOTTOM RIGHT PANEL: an elderly man at a kitchen table with his tea, glancing up at a "
             "small television on the counter showing the same segment.",
}

if __name__ == "__main__":
    wanted = sys.argv[1:] or list(TAKES)
    for name in wanted:
        print(name, flush=True)
        gen(NO_FISH + RULES + TAKES[name], OUT + name + ".png", aspect="4:3")
