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

#### Introduction
This module version uses a trained CNN model per glyph. It takes a glyph images and predicts as outcome the corresponding font arccording to the [codebook](https://github.com/steganographie-HTWG/steganographie/blob/9109e9f13cab8d682a8d3a4db023def78ceaa9d2/embedder/embedder.py#L5). 

#### Dataset
The dataset used for the training process is located in [this directory](cnn/model_per_glyph/images). It is structured into directories for lower- and upper-case images of glyphes from (a-z & öäü, A-Z & ÖÄÜ). [//]: # https://drive.google.com/drive/folders/10dmF_WKGJtFlquv14vsWFyvI9sph80eP?usp=sharing
These images where created using this [ocr module](https://github.com/steganographie-HTWG/steganographie/blob/traindata_with_ocr/font_trainingsdata_generator/extract_with_ocr.py) in resolution of 300 dpi and 900 dpi.

#### Preprocessing of Dataset:
Because of the small dataset size image augmentation is suggested for the training process. By using the [ImageDataGenerator](https://www.tensorflow.org/api_docs/python/tf/keras/preprocessing/image/ImageDataGenerator) and [imgaug](https://github.com/aleju/imgaug) the glyph images are randomly augmented with the following augmentations during the training process:
* Gaussian blur whose standard deviation is uniformly distributed between 0 (no blur) and 3px
* Gaussian noise with zero mean and standard deviation 3

#### CNN Architecture:
The network is designed according to the [paper](https://www.cs.columbia.edu/cg/fontcode/fontcode.pdf). It structure is based of a first convolutional neural network containing 3 convolutional layers with following max-pooling of 2x2 and a second fully connected neural network with 2  layers. For optimization purposes each layer contains a following normalization and a dopout layer. In the first layer the kernel size is set to 7 instead of 8. 

**Convolution Neural Network**
* Convolution Layer 1 (7×7×32)
* Convolution Layer 2 (5×5×64)
* Convolution Layer 3 (3×3×32)
**Fully Connected Neural Network**
* Fully Connected Layer 1 (128 neurons)
* Fully Connected Layer 2 (9 neurons)

#### Framework (Keras):
As framework for the training and evaluation is keras used because of ist simplicity and variability. 

#### Method
We currently train our network in Google Colab with the iPython notebook [font_recognition_cnn.ipynb](https://colab.research.google.com/drive/1bq4lRkcF5dtDlimXMb_6uV1uIa5rGySB?usp=sharing).
1. If not you need to create a [Google Account](https://accounts.google.com/signup/v2/webcreateaccount?flowName=GlifWebSignIn&flowEntry=SignUp) first and register to [Google Colab](https://colab.research.google.com/notebook)
2. Then open the [iPython notebook](https://colab.research.google.com/drive/1bq4lRkcF5dtDlimXMb_6uV1uIa5rGySB?usp=sharing) in Google Colab
3. Import [font image folder](cnn/model_per_glyph/images) from Github or copy it to your Google Drive (change in code as you like)
4. Run notebook [font_recognition_cnn.ipynb](https://colab.research.google.com/drive/1bq4lRkcF5dtDlimXMb_6uV1uIa5rGySB?usp=sharing) in Google Colab

### Single model

#### Glyph recognition

This module uses a CNN model and takes a list of glyph images and predicts their fonts and their representation in the [codebook](https://github.com/steganographie-HTWG/steganographie/blob/9109e9f13cab8d682a8d3a4db023def78ceaa9d2/embedder/embedder.py#L5).

#### Training regimen
This [iPython notebook](cnn/single_model/training_regimen/train_cnn_single_model.ipynb) was used on [Google Colaboratory](https://colab.research.google.com/notebook) to train the model.

The basic structure of the used trainingdata is in [this directory](cnn/single_model/training_regimen/ocr_fonts). Used data was generated using [this script](https://github.com/steganographie-HTWG/steganographie/blob/traindata_with_ocr/font_trainingsdata_generator/extract_with_ocr.py).
Images of glyphs (a-z & öäü, A-Z & ÖÄÜ) of each font used in the [codebook](https://github.com/steganographie-HTWG/steganographie/blob/9109e9f13cab8d682a8d3a4db023def78ceaa9d2/embedder/embedder.py#L5) were extracted using OCR in resolution of 300dpi and 900dpi.

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
