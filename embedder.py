from pylatex.base_classes import Command, Options, Arguments, CommandBase
from pylatex import Document, Package, NoEscape
import message_encoder

import string

import lorem


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


class FontChangeCommand(CommandBase):
    _latex_name = 'fch'


class Embedder:
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

    def __init__(self) -> None:
        self.doc = Document(document_options='a4paper', lmodern=False)

        for package in self.packages:
            self.doc.packages.append(package)

        self.doc.append(Command('setlength', arguments=Command('parindent'), extra_arguments='0em'))

        args = Arguments('m m O{black}', r'\fontfamily{#2}{\selectfont\color{#3}\normalsize #1}')
        args._escape = False
        self.doc.append(Command('NewDocumentCommand', arguments=Command('fch'), extra_arguments=args))

    def _change_font(self, text, font, color=None):
        args = Arguments(text, font)
        args._escape = False

        return FontChangeCommand(arguments=args, options=color, extra_arguments=[])

    def print_all_fontfamilies(self, is_colored=False):
        for fontfamily in DUMMY_CODEBOOK.values():
            color = fontfamily['color'] if is_colored else None

            self.doc.append(self._change_font(fontfamily['font'], fontfamily['font'], color))
            self.doc.append('\n')
            self.doc.append(self._change_font(string.ascii_letters, fontfamily['font'], color))
            self.doc.append('\n')

        self.doc.append('lmr')
        self.doc.append('\n')
        self.doc.append(string.ascii_letters)
        self.doc.append('\n')

    def embed(self, dummy_text, secret_message, is_colored=False):
        secret_ints = [int(c, 2) for c in secret_message]

        perturbed_text = r''
        for letter in dummy_text:
            text_to_append = letter

            if letter in string.ascii_letters:
                if secret_ints:
                    i = secret_ints.pop()
                    color = DUMMY_CODEBOOK[i]['color'] if is_colored else None

                    text_to_append = self._change_font(letter, DUMMY_CODEBOOK[i]['font'], color).dumps()

            perturbed_text += text_to_append

        self.doc.append(NoEscape(perturbed_text))
        self.doc.append("\n\n")

    def generate_document(self, file_name):
        self.doc.generate_pdf(file_name, clean_tex=True)
        self.doc.generate_tex(file_name)


if __name__ == "__main__":
    some_text = lorem.paragraph()
    some_secret = message_encoder.encode('Hello World', 3)

    embedder = Embedder()
    embedder.embed(some_text, some_secret)
    embedder.embed(some_text, some_secret, is_colored=True)
    embedder.generate_document('embedded_document')

    embedder = Embedder()
    embedder.print_all_fontfamilies(is_colored=True)
    embedder.generate_document('fontfamilies')
