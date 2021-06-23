import string

from cv2 import cv2
import numpy as np
import locale
locale.setlocale(locale.LC_ALL, 'C')
from tesserocr import PyTessBaseAPI, RIL
from PIL import Image
from io import BytesIO
import base64

# download poppler from http://blog.alivate.com.au/poppler-windows/ and set /bin folder to PATH

def recognizeCharacters(imageAsBase64):
    image = Image.open(BytesIO(base64.b64decode(imageAsBase64)))
    
    with PyTessBaseAPI(lang='eng') as api:
        api.SetImage(image)
        boxes = api.GetComponentImages(RIL.SYMBOL, True)
        return boxes

def drawBoxes(boxes, imageAsBase64):
    image = base64ToArrays(imageAsBase64)

    for box in boxes:
        box = box[1]
        x, y, w, h = box['x'], box['y'], box['w'], box['h']
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 1)

    return arraysToBase64(image)

def createGlyphImages(boxes, imageAsBase64, size):
    img = base64ToArrays(imageAsBase64)

    glyphs = []
    for index, box in enumerate(boxes):
        box = box[1]
        x, y, w, h = box['x'], box['y'], box['w'], box['h']
        letter_image = img[y:y + h, x:x + w]

        if w > h:
            scaling_factor = size / w
        else:
            scaling_factor = size / h

        resized_letter = cv2.resize(letter_image, (int(w * scaling_factor), int(h * scaling_factor)))

        empty_image = np.ones((size, size, 3), np.uint8) * 255

        x_offset = int((size - resized_letter.shape[1]) / 2)
        y_offset = int((size - resized_letter.shape[0]) / 2)

        empty_image[y_offset:y_offset + resized_letter.shape[0],
        x_offset:x_offset + resized_letter.shape[1]] = resized_letter

        glyphs.append(empty_image)
    return glyphs

def base64ToArrays(imageAsBase64):
    pillow_image = Image.open(BytesIO(base64.b64decode(imageAsBase64)))
    return cv2.cvtColor(np.array(pillow_image), cv2.COLOR_RGB2BGR)

def arraysToBase64(arrays):
    pillow_image = Image.fromarray(arrays)
    buffer = BytesIO()
    pillow_image.save(buffer, format="PNG")
    imageAsBase64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return imageAsBase64