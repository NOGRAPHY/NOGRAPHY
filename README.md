# Steganography Team Project @HTWG WS2020/21
[![Build Status](https://travis-ci.com/steganographie-HTWG/steganographie.svg?branch=master)](https://travis-ci.com/github/steganographie-HTWG/steganographie)

## Local Setup
1. Clone the repo
2. Install Python 3.8.7 (e.g. with pyenv)
3. Have an IDE ready (e.g. Visual Studio Code or PyCharm)
4. `pip3 install -r requirements.txt` to install dependencies
5. `pytest` executes all test
6. See documentation of packages below to see what you can do.

## CNN - Convolutional Neural Network
We currently train our network in Google Colab with the iPython notebook "font_recognition_cnn.ipynb".
1. If not you need to create a Google account and register to Google Colab
2. Open notebook "font_recognition_cnn.ipynb" in Google Colab
3. Import font images folder images/A from Github or copy it to your Google Drive (change in code as you like)
4. Run notebook "font_recognition_cnn.ipynb" in Google Colab
Link Google Drive: https://drive.google.com/drive/folders/10dmF_WKGJtFlquv14vsWFyvI9sph80eP?usp=sharing

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
