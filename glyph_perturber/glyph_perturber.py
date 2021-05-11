import os
import sys
import shutil
import string
import random
import argparse
import tempfile

from ocr import ocr

from tqdm import tqdm
from fontTools.ttLib import TTFont
from imgaug import parameters as iap
from pdf2image import convert_from_path
from pylatex.base_classes import Command
from pylatex import Document, Package, NoEscape


class GlyphPerturber:
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

    @staticmethod
    def generate_training_pdf(perturbed_font):
        document = PdfGenerator.setup_document(letterspace=15)

        document.append(Command('setmainfont', arguments=NoEscape(perturbed_font)))
        document.append(string.ascii_lowercase)
        document.append("\n")
        document.append("\n")
        document.append(string.ascii_uppercase)
        document.append("\n")

        return document


class GlyphExtractor:
    @staticmethod
    def extract_glyphs(font_pdf_path, dpis):
        for dpi in dpis:
            filename = os.path.splitext(os.path.basename(font_pdf_path))[0]
            new_pdf_dir = os.path.join(os.path.dirname(font_pdf_path), f"{dpi}dpi", filename)
            os.makedirs(new_pdf_dir, exist_ok=True)

            new_pdf_path = os.path.join(new_pdf_dir, os.path.basename(font_pdf_path))

            # copy PDF of font into its own directory
            shutil.copy(font_pdf_path, new_pdf_path)

            # convert PDF to PNG
            png_path = os.path.join(new_pdf_dir, f"{filename}.png")
            with tempfile.TemporaryDirectory() as path:
                images = convert_from_path(new_pdf_path, dpi=int(dpi), output_folder=path, fmt="png")[0]
                images.save(png_path)

            characters, boxes = ocr.recognizeCharacters(png_path)

            if len(GlyphPerturber.characters) != len(boxes):
                raise RuntimeError("OCR was not able to recognize all glyphs.")

            ocr.createLetterImages(characters, boxes, png_path, 200, save_files=True)

            os.remove(new_pdf_path)
            os.remove(png_path)

        os.remove(font_pdf_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Perturbs glyphs of a given font file.")
    parser.add_argument("-f", "--font", type=str, required=True, help="Font file to be perturbed.")
    parser.add_argument("-o", "--output", type=str, required=True, help="Directory where all perturbed fonts will be saved.")
    parser.add_argument("-n", "--number", type=int, required=True, help="Number of perturbed fonts.")
    parser.add_argument("-p", "--points", type=int, required=True, help="Number of points to modify.")

    parser.add_argument("--preview", action="store_true", help="Generate a preview PDF file with all perturbed glyphs.")
    parser.add_argument("--train", action="store_true", help="Generate image data for training with all perturbed glyphs.")
    parser.add_argument("--dpis", nargs='+', default=300)

    args = parser.parse_args()

    if not os.path.isfile(args.font):
        raise NotADirectoryError(args.fonts)

    if not os.path.isdir(args.output):
        raise NotADirectoryError(args.output)

    if len(os.listdir(args.output)) != 0:
        print(f"Output directory '{args.output}' is not empty. Quitting...")
        sys.exit(-1)

    perturbed_font_names = []
    original_font_name, extension = os.path.splitext(args.font)

    for i in tqdm(range(args.number)):
        # TODO: this only works with TTF right now... Add OTF support.
        font = TTFont(args.font)

        font = GlyphPerturber.rename_font(font, i+1)
        font = GlyphPerturber.perturb_glyphs(font, args.points)

        perturbed_font_name = f"{original_font_name}-PerturbedGlyphs-{i+1}{extension}"
        perturbed_font_names.append(perturbed_font_name)

        font.save(os.path.join(args.output, perturbed_font_name))

        if args.train:
            train_path = os.path.join(args.output, "train_data")
            os.makedirs(train_path, exist_ok=True)

            train_pdf_filename = f"{original_font_name}-PerturbedGlyphs-{i+1}"

            PdfGenerator.generate_training_pdf(perturbed_font_name).generate_pdf(
                os.path.join(args.output, train_pdf_filename),
                clean_tex=True, compiler="xelatex"
            )

            shutil.move(os.path.join(args.output, f"{train_pdf_filename}.pdf"),
                        os.path.join(train_path, f"{train_pdf_filename}.pdf"))

            GlyphExtractor.extract_glyphs(font_pdf_path=os.path.join(train_path, f"{train_pdf_filename}.pdf"),
                                          dpis=[] + args.dpis)

    if args.preview:
        PdfGenerator.generate_preview(perturbed_font_names).generate_pdf(
            os.path.join(args.output, f"{original_font_name}-PerturbedGlyphs-Preview"),
            clean_tex=True, compiler="xelatex"
        )
