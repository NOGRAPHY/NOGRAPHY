# Steganography Team Project @HTWG WS2020/21
[![Build Status](https://travis-ci.com/steganographie-HTWG/steganographie.svg?branch=master)](https://travis-ci.com/github/steganographie-HTWG/steganographie)

## Local Setup
1. Clone the repo
2. Install Python 3.8.7 (e.g. with pyenv)
3. Have an IDE ready (e.g. Visual Studio Code or PyCharm)
4. `pip3 install -r requirements.txt` to install dependencies
5. `pytest` executes all test
6. To hide your secret in an image, start the webserver with `export FLASK_APP=server.py` and `flask run`, then open `http://localhost:5000/hide`
7. See documentation of packages below to see what you can do

## Server
### Installation
1. [Install poppler](https://github.com/Belval/pdf2image#how-to-install)
2. `pip3 install -r -requirements.txt`
3. `export FLASK_APP=server.py`

### Run
`flask run` then go to `http://127.0.0.1:5000/`

## CNN - Convolutional Neural Network
// TODO

## OCR - Optical Character Recognition
### Installation
We use tesseract for ocr, so you need to install it (and add it to your $PATH) to use the ocr package.
### Demo
In order to see the demo, just execute the tests with `pytest`. Two test images will be generated with bounding boxes around them.

## Decoder
// TODO

## Encoder
// TODO

## Font Training Data Generator
// TODO

## Embedder
// TODO