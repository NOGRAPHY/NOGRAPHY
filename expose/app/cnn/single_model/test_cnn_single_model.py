from cnn.single_model.cnn_single_model import SingleModel

import os
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array


def test_single_model():
    image_paths = sorted(os.listdir("example"))

    assert len(image_paths) == 35  # We have 35 images.

    imgs = []
    for imagePath in image_paths:
        img_path = os.path.join("example", imagePath)
        img = load_img(img_path, color_mode="grayscale", target_size=(200, 200))
        img_array = img_to_array(img)
        imgs.append(img_array)

    imgs = np.array(imgs)

    model = SingleModel()
    font_indexes, _, _ = model.predict(imgs)

    assert len(font_indexes) == 30  # We have 30 relevant glyphs.

    expected = [4, 4, 1, 6, 6, 4, 4, 3, 7, 5, 5, 3, 5, 0, 0, 1, 7, 5, 1, 6, 6, 0, 3, 3, 5, 4, 1, 4, 4, 0]
    assert font_indexes == expected