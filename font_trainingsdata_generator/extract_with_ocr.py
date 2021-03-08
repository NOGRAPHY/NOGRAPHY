import os
import shutil

from embedder import embedder
from ocr import ocr

from pylatex.base_classes import Options
from pylatex import NoEscape, Package

from pdf2image import convert_from_path
import tempfile


ALPHABET_LOWER = "abcdefghijklmnopqrstuvwxyzäöü"
ALPHABET_UPPER = ALPHABET_LOWER.upper()

def append_glyphs_to_document(_doc, _fontfamily, is_colored=False, show_fontnames=True):
    color = _fontfamily['color'] if is_colored else None

    if show_fontnames:
        _doc.append(embedder.change_font(_fontfamily['fontname'] + " - " + _fontfamily['font'], _fontfamily['font'], color))
        _doc.append('\n')

    _doc.append(NoEscape(r"\textls{"))
    _doc.append(embedder.change_font(ALPHABET_LOWER + ALPHABET_UPPER, _fontfamily['font'], color))
    _doc.append(NoEscape(r"}"))
    _doc.append('\n')
    _doc.append('\n')

def fonts_to_single_file(is_colored=False, show_fontnames=True, single_font_per_page=False):
    doc = embedder.setup_document()
    doc.packages.append(Package('microtype', Options(letterspace=400)))
    doc.append(NoEscape(r"\pagenumbering{gobble}"))

    for fontfamily in embedder.DUMMY_CODEBOOK.values():
        append_glyphs_to_document(doc, fontfamily, is_colored, show_fontnames)

        if single_font_per_page:
            doc.append(NoEscape(r"\newpage"))

    if show_fontnames:
        doc.append('Latin Modern Times - lmr')
        doc.append('\n')
    doc.append(NoEscape(r"\textls{"))
    doc.append(ALPHABET_LOWER)
    doc.append('\n')
    doc.append(ALPHABET_UPPER)
    doc.append(NoEscape(r"}"))
    doc.append('\n')
    doc.append('\n')

    embedder.generate_document(doc, "fontfamily", clean_tex=False)

def fonts_to_multiple_files(ouput_path, is_colored=False, show_fontnames=True):
    for fontfamily in embedder.DUMMY_CODEBOOK.values():
        doc = embedder.setup_document()
        doc.packages.append(Package('microtype', Options(letterspace=150)))
        doc.append(NoEscape(r"\pagenumbering{gobble}"))

        append_glyphs_to_document(doc, fontfamily, is_colored, show_fontnames)

        embedder.generate_document(doc, os.path.join(ouput_path, fontfamily['fontname'].replace(' ', '')), clean_tex=True)

    doc = embedder.setup_document()
    doc.packages.append(Package('microtype', Options(letterspace=150)))
    doc.append(NoEscape(r"\pagenumbering{gobble}"))

    if show_fontnames:
        doc.append('Latin Modern Times - lmr')
        doc.append('\n')
    doc.append(NoEscape(r"\textls{"))
    doc.append(ALPHABET_LOWER + ALPHABET_UPPER)
    doc.append(NoEscape(r"}"))
    doc.append('\n')
    doc.append('\n')

    embedder.generate_document(doc, os.path.join(ouput_path, "Latin Modern Times".replace(' ', '')), clean_tex=True)


if __name__ == '__main__':
    dpis = [300, 900]

    clean_up = True

    base_dir = "glyphs_extracted_with_ocr"

    if os.path.isdir(base_dir):
        shutil.rmtree(base_dir)

    for dpi in dpis:
        print()
        print(str(dpi)+"dpi")

        dir_name = os.path.join(base_dir, str(dpi)+"dpi")
        os.makedirs(dir_name, exist_ok=True)

        # create PDF for each font in Codebook.
        fonts_to_multiple_files(dir_name, show_fontnames=False)

        for font_pdf in os.listdir(dir_name):
            new_pdf_dir = os.path.join(dir_name, os.path.splitext(font_pdf)[0])
            os.makedirs(new_pdf_dir, exist_ok=True)

            old_pdf_path = os.path.join(dir_name, font_pdf)
            new_pdf_path = os.path.join(new_pdf_dir, font_pdf)

            # move PDF of font into its own directory
            shutil.move(old_pdf_path, new_pdf_path)

            # convert PDF to PNG
            png_path = os.path.join(new_pdf_dir, os.path.splitext(font_pdf)[0]+".png")
            with tempfile.TemporaryDirectory() as path:
                images = convert_from_path(new_pdf_path, dpi=dpi, output_folder=path, fmt="png", thread_count=4)[0]
                images.save(png_path)

            # extract glyphs using OCR
            characters, boxes = ocr.recognizeCharacters(png_path)

            if len(ALPHABET_UPPER)*2 != len(boxes):
                msg = "All glyphs were _not_ extracted."
            else:
                msg = ""

            print(font_pdf + ":", len(boxes), "characters were recognized.", msg)

            ocr.createLetterImages(characters, boxes, png_path, 200)

            if clean_up:
                os.remove(new_pdf_path)
                os.remove(png_path)
