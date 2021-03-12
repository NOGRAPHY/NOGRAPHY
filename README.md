# Steganography Team Project @HTWG WS2020/21
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

### Model per glyph
We currently train our network in Google Colab with the iPython notebook "font_recognition_cnn.ipynb".
1. If not you need to create a Google account and register to Google Colab
2. Open notebook "font_recognition_cnn.ipynb" in Google Colab
3. Import font images folder images/A from Github or copy it to your Google Drive (change in code as you like)
4. Run notebook "font_recognition_cnn.ipynb" in Google Colab
Link Google Drive: https://drive.google.com/drive/folders/10dmF_WKGJtFlquv14vsWFyvI9sph80eP?usp=sharing

### Single model

#### Glyph recognition

#### Training regimen
This [iPython notebook](cnn/single_model/training_regimen/train_cnn_single_model.ipynb) was used on [Google Colaboratory](https://colab.research.google.com/notebook) to train the model.

The basic structure of the used trainingdata is in [this directory](cnn/single_model/training_regimen/ocr_fonts). Used data was generated using [this script](https://github.com/steganographie-HTWG/steganographie/blob/traindata_with_ocr/font_trainingsdata_generator/extract_with_ocr.py).
Images of glyphs (a-z & öäü, A-Z & ÖÄÜ) of each font used in the [codebook](https://github.com/steganographie-HTWG/steganographie/blob/9109e9f13cab8d682a8d3a4db023def78ceaa9d2/embedder/embedder.py#L5) were ectracted using OCR in resolution of 300dpi and 900dpi.

By using [ImageDataGenerator](https://www.tensorflow.org/api_docs/python/tf/keras/preprocessing/image/ImageDataGenerator) and [imgaug](https://github.com/aleju/imgaug) the glyph images are randomly augmented while training the model.

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
