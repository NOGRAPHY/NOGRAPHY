import os
import sys
import string
import random
import argparse

from tqdm import tqdm
from imgaug import parameters as iap
from fontTools.ttLib import TTFont


def rename_font(_font, number):
    old_name = ""

    for n in _font['name'].names:
        if n.nameID == 4:   # Find full name of the font.
            old_name = n.toStr()

    font_info = {
        0: f"{old_name}",  # Copyright notice
        1: f"PerturbedGlyphs-{number}",  # Font Family
        4: f"PerturbedGlyphs-{number}",  # Full name of the font.
        5: "1.0",  # Version
        6: f"PerturbedGlyphs-{number}",  # PostScript name of the font
        9: "nography",  # Designer; name of the designer of the typeface.
    }

    for name in _font['name'].names:
        if name.nameID in font_info.keys():
            _font['name'].setName(font_info[name.nameID], name.nameID, name.platformID, name.platEncID, name.langID)
        else:
            _font['name'].removeNames(nameID=name.nameID)

    return _font


def perturb_glyphs(_font, number_of_points):
    chars = string.ascii_letters    # TODO: add Umlaute
    poisson_distribution = iap.RandomSign(iap.Poisson(5))

    for char in chars:
        glyph = _font.getGlyphSet().get(char)

        random_indexes = random.sample(population=range(len(glyph._glyph.coordinates)),
                                       k=min(number_of_points, len(glyph._glyph.coordinates)))

        for index in random_indexes:
            glyph._glyph.coordinates[index] = (glyph._glyph.coordinates[index][0] + poisson_distribution.draw_sample(),
                                               glyph._glyph.coordinates[index][1] + poisson_distribution.draw_sample())

    return _font


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Perturbs lower and upper ASCII glyphs of a given font file.")
    parser.add_argument("-f", "--font", type=str, required=True, help="Font file to be perturbed.")
    parser.add_argument("-o", "--output", type=str, required=True, help="Directory where all perturbed fonts will be saved.")
    parser.add_argument("-n", "--number", type=int, required=True, help="Number of perturbed fonts.")
    parser.add_argument("-p", "--points", type=int, required=True, help="Number of points to modify.")

    args = parser.parse_args()

    if not os.path.isfile(args.font):
        raise NotADirectoryError(args.fonts)

    if not os.path.isdir(args.output):
        raise NotADirectoryError(args.output)

    if len(os.listdir(args.output)) != 0:
        user_input = input(f"Output directory '{args.output}' is not empty. Still want to continue? (y/n) ")
        if user_input.lower() != "y":
            print("Quitting...")
            sys.exit(0)

    original_font_name, extension = os.path.splitext(args.font)

    for i in tqdm(range(args.number)):
        font = TTFont(args.font)

        font = rename_font(font, i+1)
        font = perturb_glyphs(font, args.points)

        font.save(os.path.join(args.output, f"{original_font_name}-PerturbedGlyphs-{i+1}{extension}"))
