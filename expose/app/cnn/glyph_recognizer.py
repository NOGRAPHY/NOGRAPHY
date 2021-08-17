import os

import numpy as np
import tensorflow as tf
from tensorflow import keras


class GlyphRecognizer:
    MODEL_FILNENAME = "LiberationSerif-model-20210802-1357.h5"
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

        predictions = self.model.predict(images)

        keras.backend.clear_session()

        font_indexes = []

        for prediction in predictions:
            argmax = np.argmax(prediction).item()

            # As soon the default font is recognized, the secret message was completely read.
            if argmax == self.DEFAULT_FONT:
                break

            font_indexes.append(argmax)

        return font_indexes
