import string

from cv2 import cv2
import numpy as np
import locale
locale.setlocale(locale.LC_ALL, 'C')
from tesserocr import PyTessBaseAPI, RIL, OEM
from PIL import Image
from io import BytesIO
import base64
import datetime

# download poppler from http://blog.alivate.com.au/poppler-windows/ and set /bin folder to PATH


def recognize_boxes(image_as_base64, check_whitelist=True):
    image = Image.open(BytesIO(base64.b64decode(image_as_base64)))
    
    # TODO: Do we also need this parameter: oem=OEM.TESSERACT_LSTM_COMBINED ?
    with PyTessBaseAPI(lang='eng') as api:
        api.SetImage(image)
        boxes = api.GetComponentImages(RIL.SYMBOL, True)
        characters = api.GetUTF8Text().replace(' ', '').replace('\n', '')

        if check_whitelist:
            if len(boxes) != len(characters):
                raise RuntimeError("OCR was not able to recognize every character.")

            boxes_final = []

            # Filter boxes, so that only A-Z & a-z gets recognized.
            whitelist = string.ascii_letters
            for index, character in enumerate(characters):
                if character in whitelist:
                    boxes_final.append(boxes[index])
        else:
            boxes_final = boxes

        return boxes_final


def create_glyph_images(boxes, image_as_base64, output_size):
    pillow_image = Image.open(BytesIO(base64.b64decode(image_as_base64)))
    img = cv2.cvtColor(np.array(pillow_image), cv2.COLOR_RGB2BGR)

    glyphs = []
    for index, box in enumerate(boxes):
        box = box[1]
        x, y, w, h = box['x'], box['y'], box['w'], box['h']
        letter_image = img[y:y + h, x:x + w]

        if w > h:
            scaling_factor = output_size / w
        else:
            scaling_factor = output_size / h

        resized_letter = cv2.resize(letter_image, (int(w * scaling_factor), int(h * scaling_factor)))

        empty_image = np.ones((output_size, output_size, 3), np.uint8) * 255

        x_offset = int((output_size - resized_letter.shape[1]) / 2)
        y_offset = int((output_size - resized_letter.shape[0]) / 2)

        empty_image[y_offset:y_offset + resized_letter.shape[0], x_offset:x_offset + resized_letter.shape[1]] = resized_letter

        glyphs.append(empty_image)

    return glyphs


# This generates an image, where all recognized boxes are framed in a blue rectangle.
def draw_boxes(boxes, image_as_base64):
    pillow_image = Image.open(BytesIO(base64.b64decode(image_as_base64)))
    cv2_img = cv2.cvtColor(np.array(pillow_image), cv2.COLOR_RGB2BGR)

    for box in boxes:
        box = box[1]
        x, y, w, h = box['x'], box['y'], box['w'], box['h']
        cv2.rectangle(cv2_img, (x, y), (x + w, y + h), (255, 0, 0), 1)

    filename = f"boxes_{datetime.datetime.now().strftime('%Y%m%d-%H%M')}.png"
    print("draw_boxes: Saved file as:", filename)
    cv2.imwrite(filename, cv2_img)
