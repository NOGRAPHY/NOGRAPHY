e# Steganography Team Project @HTWG WS2020/21
[![Build Status](https://travis-ci.com/steganographie-HTWG/steganographie.svg?branch=master)](https://travis-ci.com/github/steganographie-HTWG/steganographie)

## Local Setup
1. Clone the repo
2. Install Python 3.8.7 (e.g. with pyenv)
3. Have an IDE ready (e.g. Visual Studio Code or PyCharm)
4. `pip3 install -r requirements.txt` to install dependencies
5. `pytest` executes all test
6. To hide your secret in an image, start the webserver with `export FLASK_APP=server.py` and `flask run`, then open `http://localhost:5000/`
7. See documentation of packages below to see what you can do

## Server
### Installation
1. [Install poppler](https://github.com/Belval/pdf2image#how-to-install)
2. `pip3 install -r -requirements.txt`
3. `export FLASK_APP=server.py`

### Run
`flask run` then go to `http://127.0.0.1:5000/`

## CNN - Convolutional Neural Network

This module uses a CNN model and takes a list of glyph images and predicts their fonts and their representation in the codebook.
We have the glyphs a-z lower & uppercasee including german umlauts (ä, ö, ü). This leads to 58 glyphs.

We take two different approaches. In the [first approach](https://github.com/steganographie-HTWG/steganographie/wiki/CNN#model-per-glyph) we created & trained one CNN per existing glyph in our codebook. This leads to 58 different CNN models.

In the [second approach](https://github.com/steganographie-HTWG/steganographie/wiki/CNN#single-model) we build and train one single CNN model for all 58 glyphs.

## OCR - Optical Character Recognition

### Installation
We use tesseract for ocr, so you need to install it (and add it to your $PATH) to use the ocr package.
### Demo
In order to see the demo, just execute the tests with `pytest`. Two test images will be generated with bounding boxes around them.

## Encoder
Here we take an input string and convert it to a list of chunks in binary representation.

## Decoder
Here we take a list of chunks of binary digits and convert it to its string representation.

## Font Training Data Generator
This module generates images of text for training of neural networks.
- [font_augmenter.py](font_trainingsdata_generator/font_augmenter.py) - For augmenting images. [TextRecognitionDataGenerator](https://github.com/Belval/TextRecognitionDataGenerator) might be a better alternative.

## Embedder
By passing an input text and a secret message, this module creates a PDF file displaying the input text.
The secret message is embedded in the input text by perturbing the single glyphs.
