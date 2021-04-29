from pylatex.base_classes import Command, Arguments, CommandBase, Options
from pylatex import Document, Package, NoEscape
import string

DUMMY_CODEBOOK = {
    0: {'font': 'qtm', 'color': 'blue', 'fontname': "Gyre Termes"},
    1: {'font': 'qpl', 'color': 'brown', 'fontname': "Gyre Pagella"},
    2: {'font': 'qbk', 'color': 'green', 'fontname': "Gyre Bonum"},
    3: {'font': 'qcs', 'color': 'magenta', 'fontname': "Gyre Schola"},
    4: {'font': 'put', 'color': 'orange', 'fontname': "Fourier"},
    5: {'font': 'Tinos-TLF', 'color': 'violet', 'fontname': "Tinos"},
    6: {'font': 'Clara-TOsF', 'color': 'teal', 'fontname': "Clara"},
    7: {'font': 'bch', 'color': 'lime', 'fontname': "Charter"},
}

packages = [
    Package('xparse'),
    Package('xcolor'),
    Package('tgtermes'),
    Package('tgpagella'),
    Package('tgbonum'),
    Package('tgschola'),
    Package('fourier'),
    Package('clara'),
    Package('tinos'),
    Package('charter'),
    Package('lmodern'),
]

class FontChangeCommand(CommandBase):
    _latex_name = 'fch'

def setup_document():
    document = Document(document_options='a4paper', lmodern=False)
    for package in packages:
        document.packages.append(package)

    # Increase spacing between glyphs
    document.packages.append(Package('microtype', Options(letterspace=10)))
    document.append(Command('lsstyle'))

    # Remove indent of paragraph
    document.append(Command('setlength', arguments=Command('parindent'), extra_arguments='0em'))

    # Remove pagenumber at bottom of page
    document.append(Command('pagenumbering', arguments='gobble'))

    args = Arguments('m m O{black}', r'\fontfamily{#2}{\selectfont\color{#3}\normalsize #1}')
    args._escape = False
    document.append(Command('NewDocumentCommand', arguments=Command('fch'), extra_arguments=args))

    return document

def embed(document, dummy_text, secret, is_colored=False):
    secret_ints = [int(c, 2) for c in secret]
    perturbed_text = r''

    for letter in dummy_text:
        text_to_append = letter

        if letter in string.ascii_letters:
            if secret_ints:
                i = secret_ints.pop(0)
                color = DUMMY_CODEBOOK[i]['color'] if is_colored else None
                text_to_append = change_font(letter, DUMMY_CODEBOOK[i]['font'], color).dumps()

        perturbed_text += text_to_append

    document.append(NoEscape(perturbed_text))
    document.append("\n\n")

    return document

def change_font(text, font, color=None):
    args = Arguments(text, font)
    args._escape = False

    return FontChangeCommand(arguments=args, options=color, extra_arguments=[])

# Cannot be tested automatically (travis has no pdf engine)
def generate_document(document, file_name, clean_tex=False):
    document.generate_pdf(file_name, clean_tex=clean_tex, compiler="pdflatex")
