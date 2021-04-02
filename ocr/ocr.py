from cv2 import cv2
from tesserocr import PyTessBaseAPI, RIL
import numpy as np
from pdf2image import convert_from_path


# download poppler from http://blog.alivate.com.au/poppler-windows/ and set /bin folder to PATH


def checkType(filename):
    type = filename[-3] + filename[-2] + filename[-1]
    if type == 'pdf':
        pages = convert_from_path(filename, 500)
        for page in pages:
            filename = filename[:-3] + "png"
            page.save(filename, 'PNG')
            return filename
    else:
        return filename


def recognizeCharacters(filename):
    whitelist_array = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                       'T',
                       'U', 'V', 'W', 'X', 'Y', 'Z', 'Ä', 'Ö', 'Ü',
                       'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                       't',
                       'u', 'v', 'w', 'x', 'y', 'z', 'ä', 'ö', 'ü']

    with PyTessBaseAPI() as api:
        api.SetImageFile(filename)

        boxes = api.GetComponentImages(RIL.SYMBOL, True)
        characters = api.GetUTF8Text().replace(' ', '').replace('\n', '')
        characters_final = ''
        boxes_final = []
        if len(boxes) != len(characters):
            raise IndexError('Not all characters were recognized correctly')

        for index in range(len(characters)):
            if characters[index] in whitelist_array:
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


def createLetterImages(characters, boxes, filename, size, save_files=True):
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
