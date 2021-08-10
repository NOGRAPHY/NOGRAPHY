import os
import sys
import string
import random
import argparse
import base64
from io import BytesIO

from tqdm import tqdm
from fontTools.ttLib import TTFont
from imgaug import parameters as iap
from PIL import Image, ImageDraw, ImageFont
from cv2 import cv2

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from expose.app.ocr import ocr


class GlyphPerturber:
    # To add Umlauts you might uncomment the list concat in this line
    characters = list(string.ascii_letters) # + ["adieresis", "odieresis", "udieresis", "Adieresis", "Odieresis", "Udieresis"]

    @staticmethod
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

    @staticmethod
    def perturb_glyphs(_font, number_of_points):
        poisson_distribution = iap.RandomSign(iap.Poisson(5))

        for char in GlyphPerturber.characters:
            if char in font.getGlyphSet():
                glyph = _font.getGlyphSet().get(char)

                random_indexes = random.sample(population=range(len(glyph._glyph.coordinates)),
                                               k=min(number_of_points, len(glyph._glyph.coordinates)))

                for index in random_indexes:
                    glyph._glyph.coordinates[index] = (glyph._glyph.coordinates[index][0] + poisson_distribution.draw_sample(),
                                                       glyph._glyph.coordinates[index][1] + poisson_distribution.draw_sample())
            else:
                raise LookupError(f"Given font has no glyph for the char '{char}'.")

        return _font


class PdfGenerator:
    @staticmethod
    def setup_document(letterspace=25):
        document = Document(document_options='a4paper', geometry_options={'left': '10mm', 'top': '10mm'},
                            lmodern=False, inputenc=None,
                            page_numbers=False, indent=False)

        # Add Font integration and glyph spacing.
        document.packages.append(Package('fontspec'))
        document.packages.append(Command('defaultfontfeatures', arguments=f"LetterSpace={letterspace}"))

        return document

    @staticmethod
    def generate_preview(perturbed_fonts):
        document = PdfGenerator.setup_document()

        for perturbed_font in perturbed_fonts:
            document.append(Command('setmainfont', arguments=NoEscape(perturbed_font)))
            document.append(string.ascii_lowercase + string.ascii_uppercase)
            document.append("\n")

        return document


class PngGenerator:
    def __init__(self, dpi):
        self.TEXT = string.ascii_letters

        self.CHARACTER_SPACING = int(0.01 * dpi)
        self.FONT_SIZE = int(0.24 * dpi)
        self.MARGIN = int(2.13 * dpi)

        self.IMAGE_WIDTH = int(8.267717 * dpi)
        self.IMAGE_HEIGHT = self._calc_image_height()

    def _calc_image_height(self):
        letters_per_line = self.IMAGE_WIDTH / self.FONT_SIZE / 0.53
        number_of_lines = len(self.TEXT) // letters_per_line + 1

        height_without_margin = 1.1 * self.FONT_SIZE * number_of_lines

        return int(height_without_margin) + self.MARGIN

    @staticmethod
    def break_into_lines(text, width, font_to_draw, draw):
        if not text:
            return
        lo = 0
        hi = len(text)
        while lo < hi:
            mid = (lo + hi + 1) // 2
            w, h = draw.textsize(text[:mid], font=font_to_draw)
            if w <= width:
                lo = mid
            else:
                hi = mid - 1
        w, h = draw.textsize(text[:lo], font=font_to_draw)
        yield text[:lo], w, h
        yield from PngGenerator.break_into_lines(text[lo:], width, font_to_draw, draw)

    def generate_training_data(self, perturbed_font, output_path):
        img = Image.new("RGB", (self.IMAGE_WIDTH, self.IMAGE_HEIGHT), 'white')
        draw = ImageDraw.Draw(img)

        font_to_draw = ImageFont.truetype(perturbed_font, self.FONT_SIZE)

        width = img.size[0] - 2 - self.MARGIN
        lines = list(PngGenerator.break_into_lines(self.TEXT, width, font_to_draw, draw))
        height = sum(line[2] for line in lines)

        y = (img.size[1] - height) // 2
        for t, w, h in lines:
            x = (img.size[0] - w - self.CHARACTER_SPACING * len(t)) // 2
            for char in t:
                draw.text((x, y), char, font=font_to_draw, fill='black')
                x = x + draw.textsize(char, font=font_to_draw)[0] + self.CHARACTER_SPACING
            y += h

        filename, _ = os.path.splitext(os.path.basename(perturbed_font))
        filename = f"{os.path.join(output_path, filename)}.png"
        img.save(filename, format="PNG")

        return filename


class GlyphExtractor:
    @staticmethod
    def extract_glyphs(png_path):
        with BytesIO() as buffer:
            img = Image.open(png_path)
            img.save(buffer, format="PNG")
            image_base64 = base64.b64encode(buffer.getvalue())

        boxes = ocr.recognize_boxes(image_base64, check_whitelist=False)

        if len(GlyphPerturber.characters) != len(boxes):
            raise RuntimeError("OCR was not able to recognize all glyphs.")

        glyphs = ocr.create_glyph_images(boxes, image_base64, 200)

        png_filename = os.path.splitext(os.path.basename(png_path))[0]
        new_png_path = os.path.join(os.path.dirname(png_path), png_filename)
        os.makedirs(new_png_path, exist_ok=True)

        for index, glyph in enumerate(glyphs):
            cv2.imwrite(os.path.join(new_png_path, f"{png_filename}_{index:02}.png"), glyph)

        os.remove(png_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Perturbs glyphs of a given TTF-font file.")
    parser.add_argument("-f", "--font", type=str, required=True, help="TTF-Font file to be perturbed.")
    parser.add_argument("-o", "--output", type=str, required=True, help="Directory where all perturbed fonts will be saved.")
    parser.add_argument("-n", "--number", type=int, required=True, help="Number of perturbed fonts.")
    parser.add_argument("-p", "--points", type=int, required=True, help="Number of points to modify.")

    parser.add_argument("--preview", action="store_true", help="Generate a preview PDF file with all perturbed glyphs.")
    parser.add_argument("--train", action="store_true", help="Generate image data for training with all perturbed glyphs.")
    parser.add_argument("--dpis", nargs='+', default=[300])

    args = parser.parse_args()

    if not os.path.isfile(args.font):
        raise NotADirectoryError(args.fonts)

    if not os.path.isdir(args.output):
        raise NotADirectoryError(args.output)

    if len(os.listdir(args.output)) != 0:
        print(f"Output directory '{args.output}' is not empty. Quitting...")
        sys.exit(-1)

    for dpi in args.dpis:
        if not dpi.isdigit():
            raise TypeError("Only integers are allowed for dpi.")

    perturbed_fonts = []
    original_font_filename, extension = os.path.splitext(args.font)

    for i in tqdm(range(args.number)):
        # TODO in future: this only works with TTF right now... Add OTF support.
        font = TTFont(args.font)

        font = GlyphPerturber.rename_font(font, i+1)
        font = GlyphPerturber.perturb_glyphs(font, args.points)

        perturbed_font_filename = f"{original_font_filename}-PerturbedGlyphs-{i+1:02}"
        perturbed_fonts.append(f"{perturbed_font_filename}{extension}")

        font.save(os.path.join(args.output, f"{perturbed_font_filename}{extension}"))

        if args.train:
            for dpi in args.dpis:
                train_path = os.path.join(args.output, "train_data", f"{dpi}dpi")
                os.makedirs(train_path, exist_ok=True)

                training_png_filepath = PngGenerator(int(dpi)).generate_training_data(
                    os.path.join(args.output, f"{perturbed_font_filename}{extension}"),
                    train_path
                )

                GlyphExtractor.extract_glyphs(training_png_filepath)

    if args.preview:
        from pylatex.base_classes import Command
        from pylatex import Document, Package, NoEscape

        PdfGenerator.generate_preview(perturbed_fonts).generate_pdf(
            os.path.join(args.output, f"{original_font_filename}-PerturbedGlyphs-Preview"),
            clean_tex=True, compiler="xelatex"
        )
