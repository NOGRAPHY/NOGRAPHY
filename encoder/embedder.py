from pylatex.base_classes import Command
from pylatex import Document, Package
import message_encoder

import string

import lorem


FONT_PACKAGES = [
        Package('xcolor'),
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

DUMMY_CODEBOOK = {
    0: 'qtm',   # Gyre Termes
    1: 'qpl',   # Gyre Pagella
    2: 'qbk',   # Gyre Bonum
    3: 'qcs',   # Gyre Schola
    4: 'put',   # Fourier
    5: 'ppl',   # Palatino
    6: 'pbk',   # Bookman
    7: 'bch',   # Charter
}

COLORS = {
    0: 'blue',
    1: 'brown',
    2: 'green',
    3: 'magenta',
    4: 'orange',
    5: 'violet',
    6: 'pink',
    7: 'lime',
}


def change_font(text, font, color=None, as_command=False):
    fontchanger = r'\fontfamily{' + font + r'}{\selectfont\normalsize ' + text + '}'

    if color:
        fontchanger = r'\fontfamily{' + font + r'}{\selectfont\color{' + color + r'}\normalsize ' + text + '}'

    if as_command:
        return Command(fontchanger[1:])

    return fontchanger


def print_fontfamilies(_doc):
    for fontfamily in DUMMY_CODEBOOK.values():
        _doc.append(change_font(fontfamily, fontfamily))
        _doc.append('\n')
        _doc.append(change_font(string.ascii_letters, fontfamily))
        _doc.append('\n')


def embedder(dummy_text, secret_message):
    doc = Document(document_options='a4paper', lmodern=False)
    for package in FONT_PACKAGES:
        doc.packages.append(package)
    doc.append(Command(r'setlength{\parindent}{0em}'))

    for print_times in range(2):
        secret_int = [int(c, 2) for c in secret_message]

        perturbed_text = r'smallskip '  # TODO: how to remove smallskip...
        for letter in dummy_text:
            text_to_append = letter

            if letter in string.ascii_letters:
                if len(secret_int):
                    i = secret_int.pop()
                    color = COLORS[i] if print_times == 0 else None

                    text_to_append = change_font(letter, DUMMY_CODEBOOK[i], color)

            perturbed_text += text_to_append

        doc.append(Command(perturbed_text))
        doc.append("\n\n")

    doc.generate_pdf('embedded_document', clean_tex=True)
    doc.generate_tex('embedded_document')


embedder(lorem.paragraph(), message_encoder.encode('Hello World', 3))
