from cv2 import cv2
from tesserocr import PyTessBaseAPI, RIL, OEM
import numpy as np

def main():

    filename = 'example/demo_06.png'
    characters, boxes = recognizeCharacters(filename)
    drawBoxes(boxes, filename)
    createLetterImages(characters, boxes, filename, 200)

def recognizeCharacters(filename):
    with PyTessBaseAPI(lang="deu", oem=OEM.TESSERACT_LSTM_COMBINED) as api:
        api.SetImageFile(filename)
        boxes = api.GetComponentImages(RIL.SYMBOL, True)
        characters = api.GetUTF8Text().replace(' ', '').replace('\n', '')

        return characters, boxes

def drawBoxes(boxes, filename):
    img = cv2.imread(filename)
    for box in boxes:
        box = box[1]
        x, y, w, h = box['x'], box['y'], box['w'], box['h']
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)

    split_filename = filename.split(".")
    cv2.imwrite(split_filename[0] + "_result." + split_filename[1], img)

def createLetterImages(characters, boxes, filename, size):
    img = cv2.imread(filename)
    index = 0
    for box in boxes:
        box = box[1]
        x, y, w, h = box['x'], box['y'], box['w'], box['h']
        letter_image = img[y:y + h, x:x + w]
        if(w > h):
            scaling_factor = size / w
        else:
            scaling_factor = size / h
        resized_letter = cv2.resize(letter_image, (int(w * scaling_factor), int(h * scaling_factor)))
        
        empty_image = np.ones((size, size, 3), np.uint8) * 255

        x_offset = int((size - resized_letter.shape[1])/2)
        y_offset = int((size - resized_letter.shape[0])/2)

        empty_image[y_offset:y_offset+resized_letter.shape[0], x_offset:x_offset+resized_letter.shape[1]] = resized_letter

        split_filename = filename.split('.')
        cv2.imwrite(split_filename[0] + '_' + str(index) + '.' + split_filename[1], empty_image)
        index += 1

if __name__ == "__main__":
    main()