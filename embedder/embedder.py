from pylatex.base_classes import Command, Arguments, CommandBase
from pylatex import Document, Package, NoEscape

import string


DUMMY_CODEBOOK = {
    0: {'font': 'qtm', 'color': 'blue'},   # Gyre Termes
    1: {'font': 'qpl', 'color': 'brown'},   # Gyre Pagella
    2: {'font': 'qbk', 'color': 'green'},   # Gyre Bonum
    3: {'font': 'qcs', 'color': 'magenta'},   # Gyre Schola
    4: {'font': 'put', 'color': 'orange'},   # Fourier
    5: {'font': 'ppl', 'color': 'violet'},   # Palatino
    6: {'font': 'pbk', 'color': 'pink'},   # Bookman
    7: {'font': 'bch', 'color': 'lime'},   # Charter
}

packages = [
        Package('xparse'),
        Package('xcolor'),
        Package('xparse'),
        Package('tgtermes'),
        Package('tgpagella'),
        Package('tgbonum'),
        Package('tgschola'),
        Package('fourier'),
        Package('palatino'),
        Package('bookman'),
        Package('charter'),
        Package('lmodern'),
    ]

# How to test this, if it has no return value?
def embed(dummy_text, secret_message, is_colored=False):
    doc = Document(document_options='a4paper', lmodern=False)

    for package in packages:
        doc.packages.append(package)

    doc.append(Command('setlength', arguments=Command('parindent'), extra_arguments='0em'))

    args = Arguments('m m O{black}', r'\fontfamily{#2}{\selectfont\color{#3}\normalsize #1}')
    args._escape = False
    doc.append(Command('NewDocumentCommand', arguments=Command('fch'), extra_arguments=args))
    
    secret_ints = [int(c, 2) for c in secret_message]

    perturbed_text = r''
    for letter in dummy_text:
        text_to_append = letter

        if letter in string.ascii_letters:
            if secret_ints:
                i = secret_ints.pop()
                color = DUMMY_CODEBOOK[i]['color'] if is_colored else None

                text_to_append = _change_font(letter, DUMMY_CODEBOOK[i]['font'], color).dumps()

        perturbed_text += text_to_append

    doc.append(NoEscape(perturbed_text))
    doc.append("\n\n")
    return doc

 
def _change_font(text, font, color=None):
    args = Arguments(text, font)
    args._escape = False
    return FontChangeCommand(arguments=args, options=color, extra_arguments=[])


def generate_document(self, document, file_name):
    document.generate_pdf(file_name, clean_tex=True)
    document.generate_tex(file_name)

class FontChangeCommand(CommandBase):
    _latex_name = 'fch'
    