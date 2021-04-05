import os

import numpy as np
import tensorflow as tf
from tensorflow import keras

from embedder import embedder

class PerGlyphModel:
    glyph = ''
    model = keras.models()
    models_filepath = "/cnn_models/"
    #model_filename = "model-" + glyph + "_2021-03-18-16:08:00.h5"
    DEFAULT_FONT = 9

    LABELS = {
        0: (7, embedder.DUMMY_CODEBOOK[7]),  # Charter
        1: (6, embedder.DUMMY_CODEBOOK[6]),  # Clara
        2: (4, embedder.DUMMY_CODEBOOK[4]),  # Fourier
        3: (2, embedder.DUMMY_CODEBOOK[2]),  # GyreBonum
        4: (1, embedder.DUMMY_CODEBOOK[1]),  # GyrePagella
        5: (3, embedder.DUMMY_CODEBOOK[3]),  # GyreSchola
        6: (0, embedder.DUMMY_CODEBOOK[0]),  # GyreTermes
        7: (9, {'font': 'lmr', 'color': 'black', 'fontname': "Latin Modern Times"}),  # LatinModernTimes
        8: (5, embedder.DUMMY_CODEBOOK[5]),  # Tinos
    }

    models_uppercase = ['A', 'Ä', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                        'N', 'O', 'Ö', 'P', 'Q', 'R', 'S', 'T', 'U', 'Ü', 'V', 'W', 'X', 'Y', 'Z']

    models_lowercase = ['a', 'ä', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                        'n', 'o', 'ö', 'p', 'q', 'r', 's', 't', 'u', 'ü', 'v', 'w', 'x', 'y', 'z']

    def __init__(self):
       # self.glyph = glyph
       # self.model_filename = "model-" + self.glyph
       # model_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], self.model_filename)
       # self.model = keras.models.load_model(model_path)

    def predict(self, image):
        if image.isupper():
            for letter in self.models_uppercase:
                if image.startswith(letter): # bool(re.match('A', image, re.I))
                    model_path = os.path.join(os.path.split(os.path.realpath(__file__))[0] + self.models_filepath, "model-" + letter + ".h5")
                    self.model = keras.models.load_model(model_path)
        elif image.islower():
            for letter in self.models_lowercase:
                if image.startswith(letter):  # bool(re.match('a', image, re.I))
                    model_path = os.path.join(os.path.split(os.path.realpath(__file__))[0] + self.models_filepath,
                                              "model-" + letter + ".h5")
                    self.model = keras.models.load_model(model_path)

        if isinstance(image, list):
            image = np.array(image)

        if not isinstance(image, np.ndarray):
            raise TypeError("predict() argument 'img_array' must be " +
                            str(type(np.ndarray([]))) + ", not " + str(type(image)))



        image = tf.image.rgb_to_grayscale(image)

        # Normalize image, if it is not yet done.
        if np.max(image) != 1.0:
            image = image / np.max(image)

        predictions = self.model.predict(image, workers=0)

        font_indexes = []
        font_info = []

        for prediction in predictions:
            argmax = np.argmax(prediction).item()

            font_index, info = self.LABELS[argmax]

            # As soon the default font is recognized, the secret message was completely read.
            if font_index == self.DEFAULT_FONT:
                break

            font_indexes.append(font_index)
            font_info.append(info)

        return font_indexes, font_info

