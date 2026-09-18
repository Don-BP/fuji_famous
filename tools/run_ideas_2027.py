"""Chapter 05 - one day in 2027. The last tile on the contents page.

The chapter is four moments of a single ordinary day, and its argument is that
in every one of them somebody is telling Fujikin's story in their own words,
without Fujikin having bought the space. So the picture is the day, not a
product: four moments, four times of day, four different places.

  MORNING   Satomi farm, seven o'clock. The surface boils at feeding time and a
            keeper films twenty seconds of it on a phone.
  MIDDAY    A social studies room in an Osaka high school. The class scans a code
            and forty phones fill with a swimming sturgeon.
  EVENING   Two university friends, one showing the other something on a phone
            and laughing.
  NIGHT     A family table. A small round tin of domestic caviar, opened.

Nothing in the picture may carry the mascot or any writing: the sticker in the
chat and the fish on the caviar tin are exactly the things the model invents
badly, so the tin lid is generated PLAIN and the phone screens carry only water
or fish, never an interface. If the lid is ever wanted with the official Fujie
on it, that is composited afterwards from the real artwork.

Output: Fujie_Creative/20_new_ideas/day2027_*.png
Once one is chosen, copy it to day2027_final.png, add it to VERBATIM in
build_site.py as idea_day2027.png and point the 2027 contents tile at it.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen

OUT = "D:/Fuji_Famous/Fujie_Creative/20_new_ideas/"

RULES = (
    "*** MASCOT RULE ***\n"
    "Do NOT draw any mascot, cartoon character, sticker, logo, brand mark or illustration anywhere "
    "in this picture - not on a phone screen, not on a tin, not on clothing, not on a wall, not on "
    "a poster. Every such surface is left plain. The real artwork is added afterwards by hand and "
    "anything drawn here would have to be painted out.\n\n"
    "*** TEXT RULE ***\n"
    "There must be NO text anywhere in the picture at all: no words, no kanji, no kana, no Latin "
    "letters, no numbers, no captions, no subtitles, no app names, no interface labels, no buttons "
    "with writing on them, no signage, no book or worksheet text, no packaging text, no watermark. "
    "Every printed surface, screen edge, label and page is blank. Earlier attempts filled screens "
    "and packaging with invented nonsense Japanese and were thrown away.\n\n"
    "*** SCREEN RULE ***\n"
    "Where a phone screen is visible it shows ONLY a photograph filling the screen edge to edge - "
    "either churning water or one swimming sturgeon. There is no interface of any kind on it: no "
    "bars, no icons, no buttons, no chat bubbles, no time, no battery. Just the picture.\n\n"
    "*** PEOPLE RULE ***\n"
    "This is Japan. Every person in the picture is JAPANESE - Japanese face, Japanese features, "
    "black hair, and Japanese hands where hands are shown. No European, white or Western-looking "
    "people anywhere, and no light brown or blonde hair. An earlier attempt came back with a "
    "European keeper and was thrown away.\n\n"
    "*** FISH RULE ***\n"
    "Any sturgeon shown is a REAL photographed fish: silver-grey, a long flat pointed snout, four "
    "barbels beneath it, rows of bony scutes along the back and flanks, a shark-like upswept tail. "
    "Real animals, never drawings, never cartoons. Do NOT draw sharks, dolphins or generic fish.\n\n"
    "*** FARM RULE ***\n"
    "Where the farm is shown it is an INDOOR recirculating hall: a clean, high, daylit building "
    "with rows of deep round grey-green fibreglass tanks about four metres across and chest-high, "
    "grey pipework and filtration along the wall, wet concrete floor with drainage channels. Never "
    "an open-air pond, never an aquarium with viewing glass.\n\n"
)

GRID4 = (
    "*** LAYOUT ***\n"
    "This image is a FOUR-PANEL editorial photo grid: two panels across and two panels down, four "
    "equal rectangles filling the frame, separated by thin, clean, even white gutters and sitting "
    "flush to the edges. All four are photographs in the same documentary style and colour. No "
    "text on the layout, no captions, no numbering, no border around the outside.\n\n"
)

BIG_LEFT = (
    "*** LAYOUT ***\n"
    "This image is a FOUR-PANEL editorial photo layout. One LARGE VERTICAL panel fills the left "
    "half of the frame, and THREE smaller panels are stacked one above another filling the right "
    "half. The panels are separated by thin, clean, even white gutters and sit flush to the edges. "
    "All four are photographs in the same documentary style and colour. No text on the layout, no "
    "captions, no numbering, no border around the outside.\n\n"
)

FOUR = (
    "The four panels are FOUR MOMENTS OF ONE ORDINARY DAY, each appearing ONCE, each in a "
    "different place and at a different hour. Nothing is repeated between panels.\n"
    "MORNING - seven o'clock at the sturgeon farm. Inside the hall, the surface of the nearest "
    "round tank is BOILING at feeding time: dozens of big sturgeon crowding and turning through "
    "the surface, backs and snouts breaking the water, white spray frozen in the air. A young "
    "JAPANESE keeper in a clean farm coat holds an ordinary smartphone out over the water in one "
    "hand, filming it, completely absorbed and not looking at the camera. Low early light through "
    "the roof panels. The phone screen shows only the churning water, no interface.\n"
    "MIDDAY - a social studies room in a Japanese high school, bright flat daylight through big "
    "windows. Japanese teenagers in school uniform at their desks, several of them holding their "
    "phones up, and on every visible screen the same photograph of one sturgeon swimming in dark "
    "water, filling the screen with no interface on it. Ordinary school furniture, a plain blank "
    "whiteboard, nothing written anywhere.\n"
    "EVENING - two Japanese university students outdoors at dusk, shoulder to shoulder, one "
    "leaning in to show the other something on a phone held between them and both laughing. The "
    "screen is turned away from the camera at an angle so its contents cannot be read, and its "
    "glow lights their faces. Warm street light and a blue evening sky behind them.\n"
    "NIGHT - a family dining table at home under a warm low lamp. A small round metal tin of "
    "caviar sits open on a plate among the dishes, its dark beads catching the light, a mother-of-"
    "pearl spoon beside it. THE LID OF THE TIN IS COMPLETELY PLAIN: bare brushed metal with "
    "nothing on it at all - no picture, no fish, no emblem, no writing. Japanese hands reach in. "
    "Quiet, warm, domestic.\n"
)

TAKES = {
    "day2027_a": GRID4 + FOUR + (
        "Arrange them in reading order: morning at the top left, midday at the top right, evening "
        "at the bottom left, night at the bottom right, so the grid runs through the day."),

    "day2027_b": BIG_LEFT + FOUR + (
        "The LARGE LEFT panel is MIDDAY, the classroom full of raised phones. The three stacked "
        "panels on the right are, from top to bottom: morning, evening, night."),

    "day2027_c": BIG_LEFT + FOUR + (
        "The LARGE LEFT panel is MORNING, the keeper filming the boiling tank. The three stacked "
        "panels on the right are, from top to bottom: midday, evening, night."),
}

# ---------------------------------------------------------------------------
# Single-image takes. The grid tells the whole chapter, but a tile is small, and
# one photograph may simply carry it better. The classroom is the strongest of
# the four moments on its own: forty phones, one fish, nobody paid for any of it.
# ---------------------------------------------------------------------------

TAKES["day2027_room"] = (
    "PHOTOREALISTIC editorial documentary photograph of a social studies classroom in a Japanese "
    "high school at midday, bright flat daylight through big windows along one side. Japanese "
    "teenagers in school uniform at ordinary school desks, seen from the front of the room, MANY "
    "of them holding their smartphones up at arm's length. On every visible screen is the same "
    "photograph: ONE real sturgeon swimming in dark water, filling the screen edge to edge with no "
    "interface on it. The repetition of that one image across the room is the subject of the "
    "picture. A plain blank whiteboard behind them. Honest colour, 35mm documentary photograph.")

TAKES["day2027_table"] = (
    "PHOTOREALISTIC editorial food-documentary photograph of a Japanese family dining table at "
    "night under a warm low lamp, shot close and slightly from above. Among the evening dishes a "
    "small round metal tin of caviar stands open on a plate, its dark beads glossy in the lamp "
    "light, a mother-of-pearl spoon resting beside it. THE LID OF THE TIN IS COMPLETELY PLAIN: "
    "bare brushed metal with nothing on it at all - no picture, no fish, no emblem, no writing, no "
    "label of any kind. Japanese hands reaching in from the edge of the frame. Warm, quiet, "
    "domestic, shallow depth of field.")


if __name__ == "__main__":
    wanted = sys.argv[1:] or list(TAKES)
    for name in wanted:
        print(name, flush=True)
        gen(RULES + TAKES[name], OUT + name + ".png", aspect="4:3")
