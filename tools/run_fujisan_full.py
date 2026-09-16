"""The Fuji-san collection - Mount Fuji added across all six merch lines.

Fujikin is named for the mountain, so Fuji joins the water as the second house
motif. Each line keeps its own native language: the craft lines stay hand-made,
official stays a corporate gift, maison stays leather-and-monogram, wamon stays
pattern-on-cloth, chibi stays cute.

Nothing existing is touched. Everything lands in Fujie_Creative/19_fujisan/
under a folder per line. Re-runnable; gen.py archives on write.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen import gen

OFFICIAL = "D:/Fuji_Famous/Documents_for_dev/05_fujie_絵柄例.png"
MASTER = "D:/Fuji_Famous/Fujie_Creative/01_character/master_v3_wave.png"
TURN = "D:/Fuji_Famous/Fujie_Creative/01_character/master_turnaround.png"
MONO = "D:/Fuji_Famous/Fujie_Creative/09_merch_maison/monogram_ecru.png"
MONO_D = "D:/Fuji_Famous/Fujie_Creative/09_merch_maison/monogram_midnight.png"
T = "D:/Fuji_Famous/Fujie_Creative/11_wamon/tiles/"
T2 = "D:/Fuji_Famous/Fujie_Creative/11_wamon/tiles2/"
BASE = "D:/Fuji_Famous/Fujie_Creative/19_fujisan/"


# ---------------------------------------------------------------------------
# Shared blocks
# ---------------------------------------------------------------------------

FUJI = (
    "*** MOUNT FUJI RULE - CRITICAL ***\n"
    "Mount Fuji must be instantly recognisable and correctly proportioned. It is a LOW, WIDE, "
    "CALM cone: the base is roughly THREE TIMES as wide as the mountain is tall, the slopes are "
    "long, shallow and gently concave, sweeping far out to the sides before they meet the ground. "
    "The summit is slightly FLATTENED with a small shallow crater notch - never a sharp point. "
    "The snow cap is a soft scalloped band across only the top third.\n"
    "It is a lone free-standing volcano: no mountain range behind it, no jagged alpine peaks, no "
    "twin summits, no foothills crowding it, no steep narrow triangle. If the mountain looks like "
    "a tall sharp triangle or a party hat, it is WRONG - flatten it and spread the base wider.\n\n"
)

LOCK_OFFICIAL = (
    "The attached image is the OFFICIAL illustration of 'Fujie', Fujikin's sturgeon mascot: a "
    "realistic polished chrome-silver sturgeon in profile, long flat pointed snout, four barbels "
    "beneath it, five rows of pale bony scutes, a small dark eye set high and forward, a large "
    "swept tail.\n\n"
    "*** ARTWORK RULE - CRITICAL ***\n"
    "Reproduce this illustration EXACTLY as drawn wherever it appears: same silhouette, same "
    "proportions, same metallic rendering. Do NOT redraw, restyle, cartoon, recolour or "
    "reproportion it, never give it a big cartoon eye, a smile, arms or legs. On the product it is "
    "a print, a foil stamp, an engraving, an embroidery or an inlay of this exact artwork, at "
    "whatever single flat colour the process implies.\n\n"
)

LOCK_CHIBI = (
    "The attached image is the LOCKED master design of 'Chibi Fujie', the cute young form of "
    "Fujikin's sturgeon mascot. Reproduce this EXACT character on every item.\n\n"
    "*** IT IS A STURGEON, NOT A DOLPHIN, NOT A WHALE, NOT A SHARK ***\n"
    "The snout is LONG, FLAT and SPADE-SHAPED, sticking straight out well in front of the mouth "
    "like a paddle - not a rounded dolphin beak, not a smiling melon head. FOUR barbel whiskers "
    "hang underneath that snout, in front of the mouth. A row of rounded bony scute bumps runs "
    "along the back AND a second row along each flank. The body is polished chrome-silver with a "
    "pale silver belly, one large glossy black eye with a bright white catchlight, a crescent "
    "tail fin, a bold dark navy outline and flat cel shading.\n\n"
    "*** ABSOLUTE RULE: NO LEGS, NO FEET, NO TOES, NO STANDING NUBS. ***\n"
    "The only appendages are two soft pectoral fins at the sides used expressively like little "
    "arms, a dorsal fin, small pelvic fins near the tail and the crescent tail. The belly is a "
    "smooth continuous curve with nothing protruding downward.\n\n"
)

NOTEXT_CRAFT = (
    "*** TEXT RULE - ABSOLUTE ***\n"
    "NO writing of any kind anywhere in the image. No kanji, no kana, no hiragana, no katakana, "
    "no cartouche, no title block, no artist signature, no carved inscription, no roman letters, "
    "no numbers, no captions, no watermark. The ONLY mark permitted is a single small plain red "
    "seal-shaped stamp with no legible characters inside it. Leave surfaces blank rather than "
    "filling them with text.\n\n"
)

TEXT_GOODS = (
    "*** TEXT RULE - CRITICAL ***\n"
    "The only words allowed anywhere are FUJIE and FUJIKIN, small and discreet, or a single small "
    "plain red seal-shaped stamp. No other words in any language, no slogans, no shop names, no "
    "invented kanji or kana, no captions, no small print, no price tags. Leave surfaces blank "
    "rather than filling them with text. Any allowed word that appears must be spelled exactly as "
    "written here.\n\n"
)

CRAFT = (
    "Authentic traditional Japanese craft, photographed or reproduced faithfully. No modern "
    "graphic-design gloss, no cartoon styling, no big shiny cartoon eye, nothing plasticky. "
    "Natural side light, quiet composition, generous empty space, wabi-sabi restraint.\n\n"
)

FISH_REDRAW = (
    "The attached image shows the fish this motif is based on: a sturgeon with a long flat pointed "
    "snout, four barbels hanging beneath it, five rows of bony scutes along the body, a small eye "
    "set high and forward, a large sweeping upper tail lobe. Keep that silhouette and those "
    "features exactly - it must always read as a sturgeon, never a carp, never a koi, never a "
    "dolphin, never a shark. Do NOT copy the chrome rendering: redraw the fish in the traditional "
    "medium described below.\n\n"
)

OFFICIAL_SHOT = (
    "PHOTOREALISTIC product photography for a premium Japanese corporate gift line. Restrained "
    "palette: deep navy, charcoal, warm off-white washi, brushed silver and a single accent of "
    "Fujikin corporate blue. Fine concentric water-ripple line work is the house graphic device. "
    "Soft directional studio light, shallow depth of field, generous empty space, nothing "
    "cluttered.\n\n"
)

MAISON_SHOT = (
    "PHOTOREALISTIC luxury goods photography for an original Japanese maison: hand-finished "
    "leather trim in deep espresso or midnight navy, brushed gold or palladium hardware, saddle "
    "stitching in waxed linen thread, clean edge painting. Studio lighting on a warm stone or "
    "marble surface, shallow depth of field, magazine-quality still life, restrained and "
    "expensive.\n\n"
    "*** BRAND RULE - CRITICAL ***\n"
    "This is an original house. Do NOT reproduce, imitate or include the monogram, logo, flower "
    "motif, initials, stripes or hardware stamp of any real fashion brand. No real brand names or "
    "logos anywhere in the image.\n\n"
)

CHIBI_SHOT = (
    "PHOTOREALISTIC commercial product photography, Japanese character-goods quality, crisp focus, "
    "soft even studio lighting, gentle contact shadows, clean uncluttered composition. Do not "
    "invent a different mascot - every character shown is the attached one.\n\n"
    "*** MATERIAL RULE - CRITICAL ***\n"
    "This is a PHOTOGRAPH OF REAL OBJECTS, not a drawing of them. The dark navy outline and the "
    "flat cel shading described above belong ONLY where the character is printed flat: on a "
    "sticker, on cloth, on paper, on packaging, on a flat acrylic panel.\n"
    "Wherever the character is MOULDED, SCULPTED, SEWN, CAST or BAKED - a PVC figure, a plush, a "
    "rubber charm, a sweet - it is a solid three-dimensional object made of real material. It has "
    "NO drawn outline of any kind, NO flat cel shading and NO cartoon linework. Instead it has "
    "real form: rounded volume, a genuine surface (brushed metallic paint, soft short-pile fleece, "
    "glossy vinyl, sugar glaze), real highlights and real shadows falling on it, a visible parting "
    "line or seam where the manufacturing would leave one, and it casts a soft contact shadow on "
    "the surface it sits on. Photograph it with real depth of field.\n"
    "If any three-dimensional object in the frame looks like a flat drawing with a dark line round "
    "it, that is WRONG.\n\n"
)

WAMON_LOCK = (
    "TWO images are attached.\n"
    "IMAGE 1 is the OFFICIAL illustration of 'Fujie', Fujikin's sturgeon mascot: a realistic "
    "polished chrome-silver sturgeon in profile, long flat pointed snout, four barbels beneath it, "
    "five rows of pale bony scutes, a small dark eye set high and forward, a large swept tail. "
    "Reproduce it EXACTLY as drawn wherever it appears. Never redraw, restyle, cartoon, recolour "
    "or reproportion it, and never give it a big cartoon eye or a smile. On the product it is a "
    "print, a foil stamp, an embroidery, an inlay or an engraving of this exact artwork.\n"
    "IMAGE 2 is the PATTERN: a traditional Japanese wamon drawn for this project. Reproduce that "
    "exact pattern - same motif, same geometry, same two colours - as the cloth, paper or printed "
    "surface of the product. Do not substitute a different Japanese pattern.\n\n"
)

WAMON_SHOT = (
    "PHOTOREALISTIC product photography of finely made Japanese goods. Real materials: dyed cotton "
    "and silk, indigo, washi, lacquer, brass, leather, wood. Natural side light, quiet "
    "composition, a lot of empty space, wabi-sabi restraint. Nothing plasticky, no modern "
    "graphic-design gloss.\n\n"
)


# ---------------------------------------------------------------------------
# 0. The anniversary badge, re-cut with a properly proportioned cone
# ---------------------------------------------------------------------------

BADGE = [
    ("badge_40_fuji.png", "1:1", None,
     "A refined circular anniversary emblem for a Japanese corporate campaign, on a pure flat "
     "white background. A thin elegant double-ring roundel in Fujikin corporate cyan blue "
     "(#00A0E9) and deep midnight navy.\n\n"
     "Inside the roundel, occupying only the LOWER THIRD, a clean flat-vector MOUNT FUJI: a low "
     "wide deep-midnight-navy silhouette whose long shallow slopes run almost to the left and "
     "right edges of the inner circle before meeting a band of thin concentric cyan water ripples "
     "at its foot. The summit is flattened with a small crater notch and sits well below the "
     "middle of the roundel. The snow cap is cut out in white with a soft scalloped lower edge "
     "across the top of the cone only.\n\n"
     "Above the mountain, in the clear upper half of the roundel, the numeral 40 set very large in "
     "a confident modern geometric sans-serif, deep midnight navy. Directly beneath the numeral, "
     "much smaller, the years 1987-2027 in clean cyan lettering, with clear white space between "
     "the lettering and the summit.\n\n"
     + FUJI +
     "Flat vector logo design. Crisp geometry, perfectly circular, perfectly symmetrical, no "
     "gradients, no shading, no texture. Only those two pieces of lettering appear: the numeral 40 "
     "and the years 1987-2027, both spelled exactly as given. No other words, no Japanese "
     "characters, no company name, no fish, no sun, no clouds, no cherry blossom."),
]


# ---------------------------------------------------------------------------
# 1. Chibi line - the playful, mass-market half
# ---------------------------------------------------------------------------

CHIBI = [
    ("chibi_fuji_acrylic_stands.png", "4:3", [MASTER, TURN],
     "A set of three clear ACRYLIC STANDS on a pale grey shelf, each a printed acrylic figure "
     "slotted into a small clear base. The tallest is a layered diorama: behind sits a flat "
     "acrylic cut-out of a pastel MOUNT FUJI - soft blue slopes, rounded white snow cap, low and "
     "wide - and Chibi Fujie floats in front of it on a little curl of cartoon wave, one pectoral "
     "fin raised in a cheerful wave. The two smaller stands are Chibi Fujie alone: one napping "
     "curled on its belly, one peeking out from behind a tiny Mount Fuji."),

    ("chibi_fuji_gacha.png", "4:3", [MASTER, TURN],
     "A GACHAPON CAPSULE TOY SET photographed on a pale surface: six small collectible PVC figures "
     "of Chibi Fujie, each moulded on its own little round base, each paired with Mount Fuji - one "
     "sitting in front of a low wide Fuji base, one wearing a tiny Fuji-shaped hat, one poking its "
     "snout over a moulded cloud, one curled asleep on a Fuji-shaped cushion, one riding a moulded "
     "wave with Fuji behind, one holding a tiny snow-capped Fuji charm. Two open clear plastic "
     "capsules and a scatter of closed pastel-blue capsules around them.\n"
     "The figures are SOLID INJECTION-MOULDED PLASTIC painted in brushed metallic silver: rounded "
     "sculpted volume, soft specular highlights curving over the body, real shadows in the "
     "undercuts, a faint mould parting line, and a soft contact shadow under each base. Shot with "
     "a real lens at a slight three-quarter angle, shallow depth of field, the back figures a "
     "little softer than the front ones."),

    ("chibi_fuji_pins.png", "1:1", [MASTER],
     "A set of six HARD ENAMEL PINS arranged on a soft grey felt board, each with a bright polished "
     "silver metal edge and glossy enamel fill. The designs: Chibi Fujie in front of a low wide "
     "snow-capped Mount Fuji; a Mount Fuji silhouette alone in navy and white with ripple lines at "
     "its base; Chibi Fujie's head peeking over a Fuji ridge; a round Fuji-and-wave badge; Chibi "
     "Fujie napping on a Fuji-shaped cushion; a tiny Fuji with a single cloud band. Macro product "
     "shot, crisp specular highlights on the metal."),

    ("chibi_fuji_apparel.png", "4:3", [MASTER],
     "An APPAREL FLATLAY photographed from directly above on a pale linen backdrop: a soft cream "
     "heavyweight T-shirt with a large chest print of Chibi Fujie floating in front of a low wide "
     "pastel Mount Fuji above a band of cartoon waves; a navy hoodie folded beside it with a small "
     "embroidered Fuji-and-ripple mark on the chest; a folded cream tote with the same Fuji print "
     "small. Fabric texture visible, soft natural daylight, neat and calm."),

    ("chibi_fuji_stationery.png", "4:3", [MASTER],
     "A STATIONERY SET arranged neatly on a pale wooden desk: a ring-bound notebook whose cover "
     "shows Chibi Fujie in front of a low wide Mount Fuji, a set of washi tapes printed with tiny "
     "repeating Fuji and wave motifs, a clear file folder with a large pale Fuji print, a set of "
     "die-cut sticker flakes of Chibi Fujie and little Fujis, and two pencils with Fuji-shaped "
     "erasers on the ends. Soft pastel blue, cream and navy palette."),

    ("chibi_fuji_sweets.png", "4:3", [MASTER],
     "A JAPANESE SOUVENIR SWEETS BOX open on a pale cloth: a pastel blue paper box whose lid is "
     "printed with Chibi Fujie beside a low wide snow-capped Mount Fuji. Inside, in a fitted tray, "
     "sit individually wrapped manju - each small round cake stamped with a Fuji silhouette - and "
     "a row of white-chocolate-dipped biscuits shaped like a low wide Mount Fuji with a white "
     "snow cap. Appetising, clean, gift-shop quality."),

    ("chibi_fuji_lunch.png", "4:3", [MASTER],
     "A CHILDREN'S LUNCH SET on a pale table: a two-tier bento box in pastel blue and cream, the "
     "lid printed with Chibi Fujie in front of a low wide Mount Fuji. The open lower tier holds a "
     "rice mound moulded into a low wide Fuji shape with a nori base and a white sesame snow cap. "
     "Beside it a matching thermos with a Fuji band, chopsticks in a printed case and a small "
     "cloth napkin with a repeating Fuji pattern."),

    ("chibi_fuji_shop.png", "16:9", [MASTER],
     "A VISITOR-CENTRE GIFT SHOP CORNER photographed with a real camera from a slight angle, so "
     "the shelves recede and the goods have depth and thickness. Pale wood shelving against a soft "
     "blue wall, with a painted low wide snow-capped Mount Fuji on the wall behind the display.\n"
     "On the shelves: plush Chibi Fujie in three sizes in SOFT SHORT-PILE FLEECE with visible "
     "stitched seams, embroidered eyes and a slight slump where the stuffing gives; boxed sweets "
     "in printed card; ceramic mugs with a glossy glaze; folded cotton tote bags; and a row of "
     "flat printed acrylic stands, which are the only flat items in the frame. A large soft plush "
     "Chibi Fujie sits on the counter in the foreground, close to the lens.\n"
     "Warm shop lighting from above, real shadows between the shelves, shallow depth of field. "
     "Bright, tidy, inviting retail photography - not an illustration of a shop."),
]


# ---------------------------------------------------------------------------
# 2. Official line, widened - real goods carrying the OFFICIAL artwork
# ---------------------------------------------------------------------------

OFFICIAL2 = [
    ("official_fuji_glass.png", "4:3", [OFFICIAL],
     "THE PRODUCT: a solid optical-crystal paperweight, a clean rectangular block with polished "
     "bevelled edges, standing on a dark brushed-steel plinth on a charcoal surface. Laser-etched "
     "inside the crystal in fine white subsurface dots: a low wide Mount Fuji with its scalloped "
     "snow cap, and the official Fujie swimming across its foot through a few thin concentric "
     "water rings. The etching is delicate and monochrome; the glass catches a cool blue edge "
     "light."),

    ("official_fuji_tote.png", "4:3", [OFFICIAL],
     "THE PRODUCT: a heavyweight natural canvas TOTE BAG standing upright on a pale concrete "
     "surface, navy webbing handles. Screen-printed on the front in two flat colours: a low wide "
     "Mount Fuji drawn as a single navy outline with a solid navy snow cap, and beneath it the "
     "official Fujie in Fujikin corporate blue swimming through three thin concentric ripple "
     "rings. Crisp ink sitting in the weave of the cloth."),

    ("official_fuji_notebooks.png", "4:3", [OFFICIAL],
     "THE PRODUCT: three hardcover NOTEBOOKS fanned on a charcoal desk - one deep navy, one warm "
     "off-white washi, one charcoal. Each cover is blind-debossed with a low wide Mount Fuji and a "
     "band of fine concentric ripples at its foot; on the navy one the official Fujie is stamped "
     "across the ripples in brushed silver foil. Exposed binding thread, rounded corners, a slim "
     "elastic closure."),

    ("official_fuji_pin_set.png", "1:1", [OFFICIAL],
     "THE PRODUCT: a boxed LAPEL PIN SET presented on navy suede inside a slim charcoal gift box. "
     "Three pins: a solid brushed-silver low wide Mount Fuji with a polished snow cap; a small "
     "round enamel badge in navy and corporate blue showing Fuji above ripple lines; and the "
     "official Fujie rendered as a fine silver relief pin. Macro product shot, crisp specular "
     "highlights."),

    ("official_fuji_umbrella.png", "4:3", [OFFICIAL],
     "THE PRODUCT: a long-handled UMBRELLA with a polished wooden crook, open and resting against "
     "a pale plaster wall. The canopy is deep navy; one panel carries a large low wide Mount Fuji "
     "printed in off-white with fine concentric ripples running across the panels at its foot, and "
     "the official Fujie printed small in silver swimming through them. Taut fabric, fine ribs, a "
     "single silver tip."),

    ("official_fuji_wall_relief.png", "16:9", [OFFICIAL],
     "THE PRODUCT: a large WALL RELIEF in a corporate reception, photographed at a slight angle. A "
     "warm off-white plaster panel carved with long shallow concentric water ripples, out of which "
     "rises a low wide Mount Fuji in deeper relief with a smooth flattened summit. Across the "
     "ripples, the official Fujie is set into the wall in brushed stainless steel, catching the "
     "raking light. Calm, architectural, expensive."),

    ("official_fuji_desk_set.png", "4:3", [OFFICIAL],
     "THE PRODUCT: an executive DESK SET on a dark walnut desk - a navy leather desk pad, a "
     "brushed-steel pen rest, a lacquered business-card holder and a small stainless paperweight. "
     "The card holder's lid is inlaid with a low wide Mount Fuji in pale mother-of-pearl; the "
     "paperweight is machined into the shape of a low wide Fuji with the official Fujie etched "
     "across its slope. Soft directional light, shallow depth of field."),

    ("official_fuji_gift_set.png", "4:3", [OFFICIAL],
     "THE PRODUCT: a premium corporate GIFT BOX open on a pale linen cloth. The navy lid, tilted "
     "behind, is foil-stamped in silver with a low wide Mount Fuji over fine concentric ripples. "
     "Inside, nested in off-white washi shred: a small tin, a folded navy furoshiki cloth printed "
     "with the Fuji mark, a slim notebook and a lacquered card case. The official Fujie appears "
     "once, small and silver, on the tin lid."),
]


# ---------------------------------------------------------------------------
# 3. Wa line - the sturgeon redrawn by traditional craft
# ---------------------------------------------------------------------------

WA = [
    ("wa_fuji_ukiyoe.png", "4:3", [OFFICIAL],
     "AN ORIGINAL EDO-PERIOD UKIYO-E WOODBLOCK PRINT, newly composed for this project. A great "
     "sturgeon rides the curl of a large breaking wave in the foreground, the wave drawn with the "
     "clawed foam fingers of classical Japanese prints in Prussian blue and indigo gradations. Far "
     "beyond the water, small and serene, a low wide snow-capped Mount Fuji stands against a pale "
     "dawn sky with soft bokashi shading. Flat areas of colour with fine keyblock outlines, "
     "visible woodgrain, the soft fibre of aged washi paper. Compose it freshly - do not copy the "
     "framing of any existing famous print."),

    ("wa_fuji_byobu.png", "16:9", [OFFICIAL],
     "A RINPA GOLD-LEAF BYOBU FOLDING SCREEN, four panels, photographed straight on. Gold leaf "
     "ground with visible leaf seams. A low wide Mount Fuji painted across the right panels in "
     "soft malachite green and indigo with a thick snow cap in raised white gofun pigment, its "
     "base wrapped in stylised gold cloud bands. Across the left panels, silver water in flowing "
     "parallel lines and whirlpools, with the sturgeon painted into it in fine silver and ink - "
     "drawn by the screen painter's own hand, stylised and flat, not metallic or photographic. "
     "Black lacquer frame, fabric hinges."),

    ("wa_fuji_arita.png", "1:1", [OFFICIAL],
     "A LARGE ARITA SOMETSUKE PORCELAIN CHARGER seen from above on a dark wooden table: brilliant "
     "white glazed porcelain painted in cobalt underglaze blue. A low wide Mount Fuji fills the "
     "upper half of the plate, brushed in graded cobalt washes with the snow cap left as bare "
     "white porcelain; below it the sturgeon swims through stylised wave lines that curl around "
     "the well of the plate. A fine double blue line rings the rim. Soft glaze pooling, tiny kiln "
     "grit on the foot."),

    ("wa_fuji_makie.png", "4:3", [OFFICIAL],
     "A BLACK URUSHI LACQUER BOX on dark cloth, the lid slightly offset to show the vermilion "
     "interior: deep glossy black lacquer, a low wide Mount Fuji rendered across the lid in gold "
     "maki-e powder with the snow cap in raised silver, standing above concentric gold water rings "
     "in which the sturgeon is drawn in fine gold line and mother-of-pearl chips. A thin gold rim "
     "line. The lacquer reflects a single soft window."),

    ("wa_fuji_noren.png", "4:3", [OFFICIAL],
     "A DEEP INDIGO NOREN SHOP CURTAIN hanging in a doorway, two panels parted slightly, warm light "
     "behind. Hand-dyed katazome: a low wide Mount Fuji reserved in undyed white cloth spans both "
     "panels, its snow cap a crisp white band, and the sturgeon is dyed in white below it swimming "
     "through a few simple curved water lines. The cloth is thick slubby cotton with the soft "
     "bleed of real resist dyeing."),

    ("wa_fuji_obi.png", "16:9", [OFFICIAL],
     "A WOVEN SILK OBI laid flat and softly curved across a pale tatami mat, photographed close. "
     "Nishijin brocade: a ground of deep midnight silk with a low wide Mount Fuji woven large in "
     "gold and silver metallic thread, snow cap in matte silver, and the sturgeon woven below it "
     "in pale grey and gold swimming through stylised wave bands. Visible weft floats, the sheen "
     "of real silk, slight shadow in the folds."),

    ("wa_fuji_sumie.png", "4:3", [OFFICIAL],
     "A HANGING SUMI-E SCROLL on a pale wall, mounted in silk with wooden rollers. On the aged "
     "paper, painted in black ink alone: a low wide Mount Fuji suggested in two long confident dry "
     "strokes with the snow left as bare paper, mist washed across its base, and below it a "
     "sturgeon rendered in a few economical wet strokes, the body a single sweeping load of ink. "
     "Enormous empty space. Visible brush texture and ink bleed."),

    ("wa_fuji_tea.png", "4:3", [OFFICIAL],
     "A TEA SETTING on a dark wooden tray beside a tatami edge, natural side light: a rough raku "
     "chawan tea bowl glazed in charcoal and ash, its outer wall bearing a low wide Mount Fuji "
     "brushed in iron oxide with the snow cap left as pale clay; a bamboo chasen and chashaku "
     "laid beside it; a small lacquer natsume whose lid carries the sturgeon in gold maki-e "
     "swimming through ripple lines. Quiet, imperfect, wabi-sabi."),
]


# ---------------------------------------------------------------------------
# 4. Wa-official - the same craft media carrying the OFFICIAL artwork
# ---------------------------------------------------------------------------

WAO = [
    ("wao_fuji_byobu.png", "16:9", [OFFICIAL],
     "A RINPA GOLD-LEAF BYOBU FOLDING SCREEN, four panels, photographed straight on. Gold leaf "
     "ground with visible leaf seams. Across the two right panels, a low wide Mount Fuji painted "
     "large in soft malachite green and indigo with a thick snow cap in raised white gofun "
     "pigment, its base wrapped in stylised gold cloud bands. Across the two left panels, stylised "
     "silver water in flowing parallel lines and whirlpools, and the official Fujie applied in "
     "silver leaf and fine metallic pigment, swimming through the water toward the mountain. Black "
     "lacquer frame, fabric hinges, the faint texture of the leaf."),

    ("wao_fuji_makie_box.png", "4:3", [OFFICIAL],
     "A BLACK URUSHI LACQUER BOX on dark cloth, the lid slightly offset showing a vermilion "
     "interior: deep glossy black lacquer, a low wide Mount Fuji laid across the lid in gold "
     "maki-e powder with the snow cap in raised silver, concentric gold water rings radiating from "
     "its foot, and the official Fujie inlaid across the centre in polished silver and "
     "mother-of-pearl. A fine gold rim line."),

    ("wao_fuji_noren.png", "4:3", [OFFICIAL],
     "A DEEP INDIGO NOREN SHOP CURTAIN hanging in a doorway, two panels parted slightly, warm light "
     "behind. A low wide Mount Fuji is reserved in undyed white cloth across both panels with a "
     "crisp white snow cap, and the official Fujie is stencilled in white below it, swimming "
     "through a few simple curved water lines. Thick slubby cotton, the soft bleed of real resist "
     "dyeing."),

    ("wao_fuji_porcelain.png", "1:1", [OFFICIAL],
     "A LARGE ARITA SOMETSUKE PORCELAIN CHARGER seen from above on a dark wooden table: brilliant "
     "white glazed porcelain painted in cobalt underglaze blue. A low wide Mount Fuji fills the "
     "upper half in graded cobalt washes with the snow cap left as bare white porcelain; below it "
     "the official Fujie is transferred in crisp cobalt line, swimming through stylised wave "
     "lines. A fine double blue line rings the rim. Soft glaze pooling."),

    ("wao_fuji_obi.png", "16:9", [OFFICIAL],
     "A WOVEN SILK OBI laid flat and softly curved across a pale tatami mat, photographed close. "
     "Nishijin brocade on deep midnight silk: a low wide Mount Fuji woven large in gold and silver "
     "metallic thread with a matte silver snow cap, and the official Fujie woven below it in pale "
     "grey and silver thread, swimming through stylised wave bands. Visible weft floats, the sheen "
     "of real silk."),

    ("wao_fuji_scroll.png", "4:3", [OFFICIAL],
     "A HANGING SCROLL on a pale wall, mounted in silk with wooden rollers. On aged paper: a low "
     "wide Mount Fuji suggested in two long dry ink strokes with the snow left as bare paper and "
     "mist washed across its base, and below it the official Fujie applied as a fine silver "
     "pigment transfer, exact and metallic against the soft ink. Enormous empty space."),

    ("wao_fuji_tea_setting.png", "4:3", [OFFICIAL],
     "A TEA SETTING on a dark wooden tray beside a tatami edge, natural side light: a rough raku "
     "chawan glazed in charcoal and ash, a low wide Mount Fuji brushed on its outer wall in iron "
     "oxide with the snow cap left as pale clay; a bamboo chasen and chashaku beside it; a small "
     "lacquer natsume whose lid carries the official Fujie inlaid in silver over gold ripple "
     "lines. Quiet, imperfect, wabi-sabi."),

    ("wao_fuji_ukiyoe.png", "4:3", [OFFICIAL],
     "AN ORIGINAL EDO-PERIOD UKIYO-E WOODBLOCK PRINT, newly composed for this project: a large "
     "breaking wave in Prussian blue and indigo gradations with clawed foam fingers, a low wide "
     "snow-capped Mount Fuji small and serene beyond the water under a pale bokashi sky, and the "
     "official Fujie laid into the foreground water exactly as drawn - metallic and precise "
     "against the flat woodblock colour, as though a modern plate had been printed over an old "
     "block. Visible woodgrain and washi fibre. Compose it freshly - do not copy the framing of "
     "any existing famous print."),
]


# ---------------------------------------------------------------------------
# 5. Wamon goods - the pattern collection on real objects
# ---------------------------------------------------------------------------

WAMON = [
    ("wamon_fuji_furoshiki.png", "1:1", T + "seigaiha_indigo.png",
     "THE PRODUCT: a large deep-indigo dyed cotton FUROSHIKI wrapping cloth laid out flat and "
     "slightly rumpled on a pale wooden table. The seigaiha pattern covers the whole cloth in "
     "indigo. Reserved out of the pattern in the centre, in undyed white cloth, stands a low wide "
     "MOUNT FUJI with a scalloped snow cap - the wave scales of the pattern forming the sea at its "
     "foot. The official Fujie is printed in white across the water in front of the mountain."),

    ("wamon_fuji_tenugui.png", "4:3", T + "mizuwa_indigo.png",
     "THE PRODUCT: a long cotton TENUGUI hand towel hanging from a slim wooden rail against a "
     "plaster wall, the lower end curling forward. The rippling mizuwa pattern runs the full "
     "length in indigo on undyed cloth. A low wide Mount Fuji is dyed across the upper third in a "
     "deeper indigo, its snow cap left white, and the official Fujie swims across the ripples "
     "below it in a single flat indigo."),

    ("wamon_fuji_sensu.png", "4:3", T2 + "seigaiha_fujie_indigo.png",
     "THE PRODUCT: a SENSU FOLDING FAN opened on a dark wooden table, polished bamboo ribs and a "
     "silk tassel at the rivet. The silk leaf carries the pattern across the whole fan; a low wide "
     "Mount Fuji is printed large across the centre in deep indigo with a white snow cap, rising "
     "out of the wave arcs, and the official Fujie is printed in silver swimming across its foot."),

    ("wamon_fuji_umbrella.png", "4:3", T + "asanoha_indigo.png",
     "THE PRODUCT: a long-handled UMBRELLA with a polished bamboo crook, open and resting against a "
     "pale plaster wall. The canopy carries the asanoha pattern in indigo on off-white. One panel "
     "holds a large low wide Mount Fuji printed in solid indigo with a white snow cap, and the "
     "official Fujie is printed small in silver swimming across the panel below it. Taut fabric, "
     "fine ribs."),

    ("wamon_fuji_pouches.png", "4:3", T2 + "roe_komon_indigo.png",
     "THE PRODUCT: three small drawstring POUCHES of different sizes standing together on a pale "
     "linen cloth, each sewn from the patterned fabric with a contrasting indigo cord. The largest "
     "has a low wide Mount Fuji appliqued in undyed cloth across its face with a white snow cap; "
     "the middle one carries the official Fujie embroidered in silver thread; the smallest is "
     "plain pattern. Soft folds, natural side light."),

    ("wamon_fuji_sake_set.png", "4:3", T + "uroko_indigo.png",
     "THE PRODUCT: a SAKE SET on a dark wooden tray - a white porcelain tokkuri flask and two "
     "guinomi cups. The uroko triangle pattern is painted around the lower body of the flask in "
     "cobalt underglaze; above it a low wide Mount Fuji is brushed in graded cobalt with the snow "
     "cap left as bare porcelain, and the official Fujie is transferred in fine cobalt line around "
     "one cup. Soft glaze pooling, a folded indigo cloth beneath."),

    ("wamon_fuji_card_case.png", "1:1", T2 + "karakusa_nagare_gold.png",
     "THE PRODUCT: a slim black URUSHI LACQUER BUSINESS-CARD CASE lying on dark cloth, a few cards "
     "fanned beside it. The flowing karakusa pattern is drawn across the lid in fine gold maki-e; "
     "a low wide Mount Fuji rises through it in deeper gold with a snow cap in raised silver, and "
     "the official Fujie is inlaid across its foot in polished silver and mother-of-pearl. A thin "
     "gold rim line, deep mirror-black lacquer."),

    ("wamon_fuji_shop_table.png", "16:9", T + "seigaiha_indigo.png",
     "A SHOP DISPLAY TABLE photographed at a slight angle in a calm Japanese craft store: pale "
     "wood, natural daylight from the left. Laid out on a runner of the patterned cloth are folded "
     "furoshiki and tenugui, a stack of pouches, a folded fan, a lacquer card case and a small "
     "porcelain dish - all carrying the same low wide Mount Fuji and the official Fujie. Behind "
     "the table, a short indigo noren with a reserved white Fuji. Uncluttered, generous empty "
     "space."),
]


# ---------------------------------------------------------------------------
# 6. Maison - the luxury leather line built on the monogram canvas
# ---------------------------------------------------------------------------

CANVAS = (
    "The attached sheet is the HOUSE MONOGRAM CANVAS: a coated canvas printed with a small "
    "repeating sturgeon motif, concentric ripple rings and a small ring-and-wave crest. Reproduce "
    "this canvas faithfully on the product - same motif, same scale relative to the object, same "
    "colours, printed flat with no gloss of its own.\n\n"
)

MAISON = [
    ("maison_fuji_scarf.png", "1:1", [MONO],
     "THE PRODUCT: a large square SILK TWILL SCARF, loosely folded and draped on a warm stone "
     "surface so the centre and one corner are readable. The border is a dense band of the house "
     "monogram in espresso brown on ecru. The centre medallion is a serene low wide MOUNT FUJI "
     "rendered in fine engraved-line hatching - midnight navy, espresso and a single pale gold - "
     "its long shallow slopes reaching almost to the medallion's edge, rising above a lake of "
     "concentric ripple rings drawn from the same monogram vocabulary. Rolled hand-stitched hem, "
     "soft silk sheen."),

    ("maison_fuji_tote.png", "4:3", [MONO],
     "THE PRODUCT: a structured TOTE BAG in the monogram canvas standing on a warm stone surface, "
     "espresso leather handles, trim and base, brushed gold feet. On the front panel, a low wide "
     "MOUNT FUJI is inlaid in smooth espresso leather with a snow cap in pale ivory leather, "
     "appliqued over the canvas and saddle-stitched around its edge, with three fine embossed "
     "ripple lines running across the canvas at its foot."),

    ("maison_fuji_midnight_bag.png", "4:3", [MONO_D],
     "THE PRODUCT: a compact structured SHOULDER BAG in the midnight monogram canvas, photographed "
     "three-quarters on a dark marble surface under a single soft light. Midnight navy leather "
     "trim, palladium hardware, a slim chain-and-leather strap. The flap is embossed with a low "
     "wide MOUNT FUJI in blind deboss, catching the light only on its long shallow slopes, its "
     "snow cap picked out in matte silver foil."),

    ("maison_fuji_trunk.png", "4:3", [MONO],
     "THE PRODUCT: a hard-sided travel TRUNK standing closed on a pale stone floor: monogram canvas "
     "body, espresso leather corner caps and straps, brass lock plate and studded edging, cream "
     "and navy painted stripe bands running around it. Centred on the lid band, painted by hand in "
     "navy and ivory, a low wide MOUNT FUJI with a scalloped snow cap above three fine ripple "
     "lines. Museum-quality still life."),

    ("maison_fuji_small_goods.png", "4:3", [MONO],
     "THE PRODUCT: a group of SMALL LEATHER GOODS arranged on a warm stone surface - a long bifold "
     "wallet, a card holder, a key pouch and a slim passport cover, all in monogram canvas with "
     "espresso leather trim and brushed gold hardware. Each piece carries a small low wide MOUNT "
     "FUJI hot-stamped in gold foil, and the card holder has the mountain inlaid in ivory leather "
     "at a larger scale. Shallow depth of field."),

    ("maison_fuji_duffle.png", "4:3", [MONO],
     "THE PRODUCT: a soft-sided weekend DUFFLE in monogram canvas resting on a stone bench, "
     "espresso leather handles rolled together with a leather cuff, a luggage tag hanging from "
     "one handle, brushed gold zip pulls. The end panel is a solid espresso leather roundel "
     "embossed with a low wide MOUNT FUJI over concentric ripple rings. Warm side light, relaxed "
     "slump in the canvas."),

    ("maison_fuji_boutique.png", "16:9", [MONO],
     "A MAISON BOUTIQUE WINDOW photographed straight on at dusk: a warm stone frame, a single pane, "
     "and inside a spare travertine plinth arrangement holding a tote, a duffle, a folded silk "
     "scarf and two small leather goods, all in the monogram canvas. Behind them, a tall backdrop "
     "panel of brushed brass etched with an enormous low wide MOUNT FUJI in fine engraved lines "
     "over concentric ripples. Soft pooled downlighting, deep shadow, nothing cluttered."),
]


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

SETS = [
    ("", BADGE, lambda p: p),
    ("chibi", CHIBI, lambda p: LOCK_CHIBI + FUJI + CHIBI_SHOT + TEXT_GOODS + p),
    ("official", OFFICIAL2, lambda p: LOCK_OFFICIAL + FUJI + OFFICIAL_SHOT + TEXT_GOODS + p),
    ("wa", WA, lambda p: FISH_REDRAW + FUJI + CRAFT + NOTEXT_CRAFT + p),
    ("wa_official", WAO, lambda p: LOCK_OFFICIAL + FUJI + CRAFT + NOTEXT_CRAFT + p),
    ("wamon", WAMON, lambda p: WAMON_LOCK + FUJI + WAMON_SHOT + TEXT_GOODS + p),
    ("maison", MAISON, lambda p: CANVAS + FUJI + MAISON_SHOT + TEXT_GOODS + p),
]

if __name__ == "__main__":
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for folder, jobs, wrap in SETS:
        if only and folder != only:
            continue
        out = BASE + (folder + "/" if folder else "")
        pathlib.Path(out).mkdir(parents=True, exist_ok=True)
        for job in jobs:
            name, aspect, refs, prompt = job
            if isinstance(refs, str):          # wamon: official + one pattern tile
                refs = [OFFICIAL, refs]
            print(f"-> {folder or 'badge'}/{name}", flush=True)
            r = gen(wrap(prompt), out + name, refs, aspect)
            ok = isinstance(r, list)
            print(f"   {'ok' if ok else r}", flush=True)
