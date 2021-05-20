import string

from cv2 import cv2
import numpy as np
from tesserocr import PyTessBaseAPI, RIL, OEM
from PIL import Image
from io import BytesIO
import base64

# download poppler from http://blog.alivate.com.au/poppler-windows/ and set /bin folder to PATH

def recognizeCharacters(imageAsBase64):
    image = Image.open(BytesIO(base64.b64decode(imageAsBase64)))
    
    # TODO: Do we also need this parameter: oem=OEM.TESSERACT_LSTM_COMBINED ?
    with PyTessBaseAPI(lang='eng') as api:
        api.SetImage(image)

        boxes = api.GetComponentImages(RIL.SYMBOL, True)
        characters = api.GetUTF8Text().replace(' ', '').replace('\n', '')
        if len(boxes) != len(characters):
            raise IndexError('Not all characters were recognized correctly')

        characters_final = ''
        boxes_final = []

        whitelist = string.ascii_letters
        for index in range(len(characters)):
            if characters[index] in whitelist:
                characters_final = characters_final + characters[index]
                boxes_final.append(boxes[index])

        return characters_final, boxes_final

def drawBoxes(boxes, filename):
    img = cv2.imread(filename)
    for box in boxes:
        box = box[1]
        x, y, w, h = box['x'], box['y'], box['w'], box['h']
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)

    split_filename = filename.split(".")
    cv2.imwrite(split_filename[0] + "_result." + split_filename[1], img)


def createLetterImages(characters, boxes, filename, size, save_files=False):
    img = cv2.imread(filename)

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

        if save_files:
            split_filename = filename.split('.')
            cv2.imwrite(split_filename[0] + '_' + str(index) + '_' + characters[index] + '.' + split_filename[1],
                        empty_image)

        glyphs.append(empty_image)

    return glyphs
