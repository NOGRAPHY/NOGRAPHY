from pylatex.base_classes import Command, Arguments, CommandBase, Options
from pylatex import Document, Package, NoEscape
import string


DUMMY_CODEBOOK = {
    0: {'font': 'LiberationSerif-PerturbedGlyphs-1.ttf', 'color': 'blue', 'fontname': "LiberationSerif-PerturbedGlyphs-1"},
    1: {'font': 'LiberationSerif-PerturbedGlyphs-2.ttf', 'color': 'brown', 'fontname': "LiberationSerif-PerturbedGlyphs-2"},
    2: {'font': 'LiberationSerif-PerturbedGlyphs-3.ttf', 'color': 'green', 'fontname': "LiberationSerif-PerturbedGlyphs-3"},
    3: {'font': 'LiberationSerif-PerturbedGlyphs-4.ttf', 'color': 'magenta', 'fontname': "LiberationSerif-PerturbedGlyphs-4"},
    4: {'font': 'LiberationSerif-PerturbedGlyphs-5.ttf', 'color': 'orange', 'fontname': "LiberationSerif-PerturbedGlyphs-5"},
    5: {'font': 'LiberationSerif-PerturbedGlyphs-6.ttf', 'color': 'violet', 'fontname': "LiberationSerif-PerturbedGlyphs-6"},
    6: {'font': 'LiberationSerif-PerturbedGlyphs-7.ttf', 'color': 'teal', 'fontname': "LiberationSerif-PerturbedGlyphs-7"},
    7: {'font': 'LiberationSerif-PerturbedGlyphs-8.ttf', 'color': 'lime', 'fontname': "LiberationSerif-PerturbedGlyphs-8"},
    8: {'font': 'LiberationSerif-PerturbedGlyphs-9.ttf', 'color': 'black', 'fontname': "LiberationSerif-PerturbedGlyphs-9"},    # Default Font
}

DEFAULT_FONT_INDEX = 8

packages = [
    Package('xparse'),
    Package('xcolor'),
    Package('fontspec'),
]

class FontChangeCommand(CommandBase):
    _latex_name = 'fch'

def setup_document():
    document = Document(document_options='a4paper', lmodern=False,
                        inputenc=None, page_numbers=False, indent=False)

    for package in packages:
        document.packages.append(package)

    document.packages.append(Command('defaultfontfeatures', arguments=f"LetterSpace=5.0"))

    args = Arguments('m m O{black}', r'\fontspec{#2}[Path=fonts/]{\color{#3}\normalsize #1}')
    args._escape = False
    document.append(Command('NewDocumentCommand', arguments=Command('fch'), extra_arguments=args))

    return document

def embed(document, dummy_text, secret, is_colored=False):
    secret_ints = [int(c, 2) for c in secret]
    perturbed_text = r''
    dummy_tex_list = list(dummy_text)

    while dummy_tex_list:
        text_to_append = dummy_tex_list.pop(0)

        if text_to_append in string.ascii_letters:
            if secret_ints:
                i = secret_ints.pop(0)
                color = DUMMY_CODEBOOK[i]['color'] if is_colored else None
                text_to_append = change_font(text_to_append, DUMMY_CODEBOOK[i]['font'], color).dumps()

        perturbed_text += text_to_append

        if not secret_ints:
            break

    default_font = DUMMY_CODEBOOK[DEFAULT_FONT_INDEX]['font']
    default_font_color = DUMMY_CODEBOOK[DEFAULT_FONT_INDEX]['color'] if is_colored else None

    document.append(NoEscape(perturbed_text))
    document.append(NoEscape(change_font(''.join(dummy_tex_list), default_font, default_font_color).dumps()))
    document.append("\n\n")

    return document

def change_font(text, font, color=None):
    args = Arguments(text, font)
    args._escape = False

    return FontChangeCommand(arguments=args, options=color, extra_arguments=[])

# Cannot be tested automatically (travis has no pdf engine)
def generate_document(document, file_name, clean_tex=False):
    document.generate_pdf(file_name, clean_tex=clean_tex, compiler='xelatex')
