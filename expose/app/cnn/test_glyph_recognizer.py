from glyph_recognizer import GlyphRecognizer

import os
import numpy as np
import cv2


def test_glyph_recognizer():
    image_paths = sorted(os.listdir("example"))

    assert len(image_paths) == 35  # We have 35 images.

    glyph_images = []
    for image_path in image_paths:
        glyph_images.append(cv2.imread(os.path.join("example", image_path)))

    glyph_images = np.array(glyph_images)

    model = GlyphRecognizer()
    font_indexes = model.predict(glyph_images)

    assert len(font_indexes) == 30  # We have 30 relevant glyphs.

    expected = [0, 4, 4, 1, 4, 5, 3, 3, 0, 6, 6, 1, 5, 7, 1, 0, 0, 5, 3, 5, 5, 7, 3, 4, 4, 6, 6, 1, 4, 4]

    assert font_indexes == expected
