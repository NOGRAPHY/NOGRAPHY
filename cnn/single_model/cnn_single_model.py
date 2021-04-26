import os

import numpy as np
import tensorflow as tf
from tensorflow import keras

DUMMY_CODEBOOK = {
    0: {'font': 'qtm', 'color': 'blue', 'fontname': "Gyre Termes"},
    1: {'font': 'qpl', 'color': 'brown', 'fontname': "Gyre Pagella"},
    2: {'font': 'qbk', 'color': 'green', 'fontname': "Gyre Bonum"},
    3: {'font': 'qcs', 'color': 'magenta', 'fontname': "Gyre Schola"},
    4: {'font': 'put', 'color': 'orange', 'fontname': "Fourier"},
    5: {'font': 'Tinos-TLF', 'color': 'violet', 'fontname': "Tinos"},
    6: {'font': 'Clara-TOsF', 'color': 'teal', 'fontname': "Clara"},
    7: {'font': 'bch', 'color': 'lime', 'fontname': "Charter"},
}

class SingleModel:
    MODEL_FILNENAME = "model-20210309-1356.h5"

    LABELS = {
        0: (7, DUMMY_CODEBOOK[7]),  # Charter
        1: (6, DUMMY_CODEBOOK[6]),  # Clara
        2: (4, DUMMY_CODEBOOK[4]),  # Fourier
        3: (2, DUMMY_CODEBOOK[2]),  # GyreBonum
        4: (1, DUMMY_CODEBOOK[1]),  # GyrePagella
        5: (3, DUMMY_CODEBOOK[3]),  # GyreSchola
        6: (0, DUMMY_CODEBOOK[0]),  # GyreTermes
        7: (9, {'font': 'lmr', 'color': 'black', 'fontname': "Latin Modern Times"}),    # LatinModernTimes
        8: (5, DUMMY_CODEBOOK[5]),  # Tinos
    }

    DEFAULT_FONT = 9

    def __init__(self):
        model_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], self.MODEL_FILNENAME)

        self.model = keras.models.load_model(model_path)

    def predict(self, images):
        if isinstance(images, list):
            images = np.array(images)

        if not isinstance(images, np.ndarray):
            raise TypeError("predict() argument 'img_array' must be " +
                            str(type(np.ndarray([]))) + ", not " + str(type(images)))

        images = tf.image.rgb_to_grayscale(images)

        # Normalize image, if it is not yet done.
        if np.max(images) != 1.0:
            images = images / np.max(images)

        predictions = self.model.predict(images, workers=0)

        font_indexes = []
        font_info = []
        confidences = []

        for prediction in predictions:
            argmax = np.argmax(prediction).item()

            font_index, info = self.LABELS[argmax]

            # As soon the default font is recognized, the secret message was completely read.
            if font_index == self.DEFAULT_FONT:
                break

            font_indexes.append(font_index)
            font_info.append(info)
            confidences.append(np.max(prediction).item())

        confidence = {
            "mean": np.mean(confidences),
            "median": np.median(confidences),
            "min": np.min(confidences),
            "max": np.max(confidences)
        }

        return font_indexes, font_info, confidence
