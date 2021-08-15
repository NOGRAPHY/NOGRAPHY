# Glyph Perturber

This script takes [TrueType Fonts (TTF)](https://de.wikipedia.org/wiki/TrueType) and randomly perturbs every glyph a-z and A-Z, by moving random points of the glyph by a random value.

## Installation

Unlike NOGRAPHY, this script is to be run locally and developed with [Python 3.8.7](https://www.python.org/downloads/release/python-387/). Therefore, some packages are needed.
By running `pip install -r requirements.txt` in this directory the needed Python packages should be installed sufficiently.

### tesserocr

For [tesserocr](https://github.com/sirfz/tesserocr) you'll need to install `tesseract-ocr`, because it only works as a wrapper for it. [Here's](https://github.com/sirfz/tesserocr#requirements) a guide how to install it.

### PyLaTeX

[PyLaTeX](https://github.com/JelteF/PyLaTeX) is only **optional**. It is used to generate a PDF document, which displays all the perturbed fonts.
If you want to use this functionality, you'll need to install LaTeX on your device, PyLaTeX is only a wrapper for it. [Here's](https://github.com/JelteF/PyLaTeX#installation) an example how to install it.

## Usage

    $ python glyph_perturber.py
    usage: glyph_perturber.py [-h] -f FONT -o OUTPUT -n NUMBER -p POINTS [--preview] [--train] [--dpis DPIS [DPIS ...]]
    
    Perturbs glyphs of a given TTF-font file.
    
    optional arguments:
      -h, --help            show this help message and exit
      -f FONT, --font FONT  TTF-Font file to be perturbed.
      -o OUTPUT, --output OUTPUT
                            Directory where all perturbed fonts will be saved.
      -n NUMBER, --number NUMBER
                            Number of perturbed fonts.
      -p POINTS, --points POINTS
                            Number of points to modify.
      --preview             Generate a preview PDF file with all perturbed glyphs.
      --train               Generate image data for training with all perturbed glyphs.
      --dpis DPIS [DPIS ...]
