import os

import numpy as np
import tensorflow as tf
from tensorflow import keras

from embedder import embedder


class SingleModel:
    MODEL_FILNENAME = "LiberationSerif-model-20210429-0751.h5"

    LABELS = {
        0: (0, embedder.DUMMY_CODEBOOK[0]),
        1: (1, embedder.DUMMY_CODEBOOK[1]),
        2: (2, embedder.DUMMY_CODEBOOK[2]),
        3: (3, embedder.DUMMY_CODEBOOK[3]),
        4: (4, embedder.DUMMY_CODEBOOK[4]),
        5: (5, embedder.DUMMY_CODEBOOK[5]),
        6: (6, embedder.DUMMY_CODEBOOK[6]),
        7: (7, embedder.DUMMY_CODEBOOK[7]),
        8: (8, embedder.DUMMY_CODEBOOK[8]),
    }

    DEFAULT_FONT = 8

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
