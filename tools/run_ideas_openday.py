"""Idea 10 - one open day a year: the letters, and a first taste of caviar.

The AFTERNOON half of the open day. The morning half (the letters at the tanks)
is already pictured by run_ideas_letter.py.

Decisions baked in, do not undo:
- The tasting does NOT happen in the rearing hall. Nobody serves food beside open
  water tanks on a wet working floor. Families eat outdoors beside the building,
  or in a clean visitor room. The fish appear in their own panel or through a
  window instead.
- Three-panel editorial layout is wanted here: the tasting, a real sturgeon, and
  the caviar close up. The single wide outdoor shot is kept as one take.
- The tables must line up DEAD STRAIGHT. Crooked, mismatched, jutting tables read
  as a mistake.
- The people are ENJOYING it. Smiling, laughing, delighted. The earlier "quiet and
  formal" direction made everyone look miserable and was rejected.

Caviar is served properly: a small glass dish on crushed ice and a
mother-of-pearl spoon, never steel.

Output: Fujie_Creative/20_new_ideas/openday_*.png
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen

OUT = "D:/Fuji_Famous/Fujie_Creative/20_new_ideas/"

RULES = (
    "*** TEXT RULE ***\n"
    "There must be NO text anywhere in the picture at all. No words, no kanji, no kana, no Latin "
    "letters, no numbers, no signage, no banners, no menu cards, no name tags, no labels, no "
    "printing on aprons or tents, no equipment markings, no watermark. Every surface is blank.\n\n"
    "*** MOOD RULE ***\n"
    "THE PEOPLE ARE HAPPY. This is a treat and a good day out, and every face shows it. Children "
    "grin, laugh and pull delighted surprised faces at the taste; parents and grandparents smile "
    "broadly, lean in to watch their children, talk to each other, laugh. Bright, warm, sociable "
    "and relaxed. Do NOT make anyone look solemn, stiff, blank, bored, nervous or sad. No rows of "
    "still faces with hands folded in laps, no funeral atmosphere, nobody staring straight ahead.\n\n"
    "*** TABLE RULE ***\n"
    "The tables form ONE DEAD STRAIGHT line: identical tables of the same height pushed end to end "
    "in perfect alignment, edges flush, a single unbroken straight run receding into the picture. "
    "The white cloths are smooth and pulled square, hanging evenly. The chairs are lined up evenly "
    "along both sides. Nothing is crooked, angled, jutting out, mismatched or set at a different "
    "height. The line of the table must look deliberate and tidy.\n\n"
    "*** HYGIENE RULE ***\n"
    "The eating happens in a clean, dry, food-safe place - outdoors, or a plain visitor room. There "
    "must be NO open water tank in the same space as the food, no wet concrete under the tables, no "
    "floor drainage channels under the tables, no pipework or hoses over the tables.\n\n"
    "*** FISH RULE ***\n"
    "Any sturgeon shown are REAL photographed fish: large live silver-grey fish over a metre long, "
    "long flat pointed snouts, four barbels hanging under the snout, rows of bony scutes down the "
    "back and flanks, shark-like upswept tail. Real animals in deep water, never drawings, never "
    "cartoons. Do NOT draw sharks, dolphins or generic fish.\n\n"
    "*** CAVIAR RULE ***\n"
    "The caviar is a SMALL, restrained portion: a spoonful of fine dark grey-black sturgeon roe, "
    "each egg a distinct glossy bead. It is served in a small clear glass dish set on crushed ice, "
    "with a pale MOTHER-OF-PEARL spoon - never a steel or silver spoon. This is a taste, not a "
    "heaped luxury platter: no towers, no gold, no champagne, no garnish sprays.\n\n"
)

LOOK = (
    "PHOTOREALISTIC editorial documentary photography, spring afternoon in rural Ibaraki, Japan. "
    "Ordinary local Japanese families in everyday clothes - parents, grandparents and children "
    "together, all of them smiling and enjoying themselves. In front of each person is a small "
    "clear glass dish of dark sturgeon caviar on crushed ice, a pale mother-of-pearl spoon, and a "
    "plain glass of water. A woman in a clean white coat serves along the table, smiling as she "
    "goes. Natural light, real skin tones, honest colour, 35mm documentary photograph, "
    "no watermark. "
)

OUTDOOR = (
    "Setting: OUTDOORS on the dry concrete apron beside the fish farm on a bright spring afternoon. "
    "A simple plain white marquee is pitched over one long dead-straight run of tables under smooth "
    "white cloths. Behind the marquee stands the farm's long low steel-clad rearing hall with its "
    "shutter door rolled open, and beyond it low green hills and bare early spring trees. "
)

PANEL_LAYOUT = (
    "*** LAYOUT ***\n"
    "This image is a THREE-PANEL editorial photo layout, like a magazine spread. One LARGE "
    "VERTICAL panel fills the left half of the frame, and TWO smaller panels are stacked one above "
    "the other filling the right half. The three panels are separated by thin, clean, even white "
    "gutters and sit flush to the edges of the frame. All three are photographs in the same "
    "documentary style, light and colour. No text, no captions, no page numbers, no borders around "
    "the outside.\n\n"
)

GRID4 = (
    "*** LAYOUT ***\n"
    "This image is a FOUR-PANEL editorial photo grid: two panels across and two panels down, four "
    "equal rectangles filling the frame, separated by thin, clean, even white gutters and sitting "
    "flush to the edges. All four are photographs in the same documentary style, light and colour. "
    "No text, no captions, no numbering, no border around the outside.\n\n"
)

GRID6 = (
    "*** LAYOUT ***\n"
    "This image is a SIX-PANEL editorial photo grid: three panels across and two panels down, six "
    "equal rectangles filling the frame, separated by thin, clean, even white gutters and sitting "
    "flush to the edges. All six are photographs in the same documentary style, light and colour. "
    "No text, no captions, no numbering, no border around the outside.\n\n"
)

POSTURE = (
    "*** POSTURE RULE ***\n"
    "Everyone sits upright and naturally in their own chair at their own place. NOBODY leans across "
    "the table, stoops over another person, or pushes their head into someone else's space. No face "
    "looms oddly large at the edge of a panel, no head is jammed against the frame, no body is "
    "bent at an unnatural angle over the cloth. Comfortable, ordinary seated posture throughout.\n\n"
)

TAKES = {
    # What the user asked for: the multi-panel, built on the outdoor scene.
    # CHOSEN. openday_a is the picked image for this idea - do not regenerate it.
    "openday_a": PANEL_LAYOUT + LOOK + OUTDOOR +
                 "LEFT LARGE PANEL: the outdoor marquee tasting seen along the straight table - "
                 "families laughing and smiling together, a child in the foreground pulling a "
                 "delighted surprised face at their first spoonful while their father grins at "
                 "them, the open rearing hall and green hills behind. "
                 "TOP RIGHT PANEL: a single large REAL sturgeon photographed through the clear "
                 "deep water of a rearing tank, seen from the side, whole fish in frame, dark "
                 "green-black water around it. "
                 "BOTTOM RIGHT PANEL: an extreme close-up on the table cloth of one small glass "
                 "dish of dark caviar on crushed ice with the mother-of-pearl spoon beside it, and "
                 "a smiling child's hand reaching in for the spoon.",

    # Same layout, different panel emphasis - the face is the hero.
    # SUPERSEDED by the b1/b2/b3 set: the user liked the girl close-up but the woman
    # beside her leant right over the table and read strangely. Kept for the record.
    "openday_b": PANEL_LAYOUT + LOOK + OUTDOOR +
                 "LEFT LARGE PANEL: a close portrait of one child of about eight at the outdoor "
                 "table, caught mid-laugh with the mother-of-pearl spoon just leaving their mouth, "
                 "eyes screwed up in a big delighted grin at the strange new taste; their mother "
                 "beside them laughing with them. "
                 "TOP RIGHT PANEL: the straight run of tables under the white marquee seen from the "
                 "end, forty smiling local people along both sides in the spring light, the farm's "
                 "long steel hall behind them. "
                 "BOTTOM RIGHT PANEL: a REAL sturgeon moving through the deep clear water of a "
                 "rearing tank, photographed close, its long flat snout and four barbels clear.",

    # The B revision: every panel is a DIFFERENT person enjoying the taste.
    "openday_b1": PANEL_LAYOUT + POSTURE + LOOK + OUTDOOR +
                  "Every panel shows a DIFFERENT person tasting the caviar and enjoying it. "
                  "LEFT LARGE PANEL: a close portrait of a girl of about eight, alone in frame, "
                  "caught mid-laugh with the mother-of-pearl spoon just leaving her mouth, eyes "
                  "screwed up in a big delighted grin at the strange new taste, the blurred white "
                  "marquee and spring hills behind her. "
                  "TOP RIGHT PANEL: a different person - an elderly man of about seventy, alone in "
                  "frame, head tipped back laughing with surprise as he lowers his spoon. "
                  "BOTTOM RIGHT PANEL: a different person again - a young mother with a toddler on "
                  "her knee, both of them laughing, the toddler licking the little spoon.",

    "openday_b2": GRID4 + POSTURE + LOOK + OUTDOOR +
                  "Each of the four panels is a close portrait of a DIFFERENT person at the outdoor "
                  "table, each one alone in their panel, each caught in the moment of tasting the "
                  "caviar and loving it. "
                  "TOP LEFT: a girl of about eight, mid-laugh, the mother-of-pearl spoon just "
                  "leaving her mouth, eyes screwed up in a huge grin. "
                  "TOP RIGHT: an elderly woman, eyes closed, smiling broadly with quiet pleasure as "
                  "she tastes. "
                  "BOTTOM LEFT: a boy of about five pulling a big delighted surprised face, "
                  "eyebrows up, the empty spoon still in his hand. "
                  "BOTTOM RIGHT: a father in his thirties laughing out loud, looking sideways at "
                  "his child out of frame.",

    "openday_b3": GRID6 + POSTURE + LOOK + OUTDOOR +
                  "Each of the six panels is a close portrait of a DIFFERENT person at the outdoor "
                  "table, each one alone in their panel, every one of them smiling, laughing or "
                  "grinning at the taste: a girl of about eight mid-laugh with the spoon just "
                  "leaving her mouth; an elderly man laughing with his head tipped back; a young "
                  "woman smiling with her eyes closed as she tastes; a small boy pulling a "
                  "delighted surprised face; an elderly woman beaming and saying something to "
                  "someone out of frame; a teenage girl grinning wide-eyed at her empty spoon. Six "
                  "different ages, six different faces, all clearly the same afternoon in the same "
                  "light at the same table.",

    # The single wide outdoor shot, tables fixed straight, everyone happy.
    "openday_c": LOOK + OUTDOOR +
                 "ONE single photograph filling the whole frame - not a collage, not a panel "
                 "layout. MEDIUM WIDE SHOT from the end of the perfectly straight table looking "
                 "down its length: in the near foreground a small child sitting on their father's "
                 "knee has just taken their first spoonful and is turning to him laughing, and he "
                 "is laughing back; along the table beyond them the other families are all smiling, "
                 "talking and watching their own children taste, the white marquee above and the "
                 "open rearing hall and hills behind.",
}

if __name__ == "__main__":
    # Name takes on the command line to regenerate only those, e.g.
    #   python tools/run_ideas_openday.py openday_b1 openday_b2
    wanted = sys.argv[1:] or list(TAKES)
    for name in wanted:
        print(name, flush=True)
        gen(RULES + TAKES[name], OUT + name + ".png", aspect="4:3")
