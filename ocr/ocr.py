from cv2 import cv2
import pytesseract
import imutils
import numpy as np
import os

from PIL import Image
from tesserocr import PyTessBaseAPI, RIL


def preprocessImage(image):
    image = imutils.resize(image, width=800, )
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # image = cv2.GaussianBlur(thresh, (3, 3), 0)
    return image


def getLettersFromImage(image):
    return list(map(mapLineToLetter, pytesseract.image_to_boxes(image).splitlines()))


def mapLineToLetter(line):
    partitions = line.split(' ')
    return Letter(partitions[0], int(partitions[1]), int(partitions[2]), int(partitions[3]), int(partitions[4]))


def drawBoundingBoxedOnImage(image, letters):
    image_height = int(image.shape[0])
    for letter in letters:
        # Rectangle from bottom left to top right
        cv2.rectangle(image, (letter.x, image_height - letter.y), (letter.width, image_height - letter.height),
                      (0, 0, 255), 1)
    return image


class Letter:

    def __init__(self, letter, x, y, width, height):
        self.letter = letter
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __str__(self):
        return '\n' + str(self.letter) + ' at (' + str(self.x) + ',' + str(self.y) + ') with ' + str(
            self.width) + 'x' + str(self.height) + 'px'

    def __repr__(self):
        return self.__str__()


def recognizeCharacters(filename):
    with PyTessBaseAPI() as api:
        api.SetImageFile('example/' + filename + '.png')
        boxes = api.GetComponentImages(RIL.SYMBOL, True)
        characters = api.GetUTF8Text().replace(" ", "")
        print(characters)
        # print('Found {} image components.'.format(len(boxes)))
        return characters, boxes


def drawBoxes(boxes, img, filename):
    for box in boxes:
        box = box[1]
        x, y, w, h = box['x'], box['y'], box['w'], box['h']
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)
    cv2.imwrite('example/result/' + filename + '_result.png', img)


def createLetterImages(characters, boxes, img, filename):
    index = 0
    for box in boxes:
        box = box[1]
        x, y, w, h = box['x'], box['y'], box['w'], box['h']
        letter = img[y:y + h, x:x + w]
        cv2.imwrite('example/result/letters/' + filename + '/' + str(index) + '_' + characters[index] + '.png', letter)
        index += 1


def main():
    filename = 'demo_02'

    characters, boxes = recognizeCharacters(filename)

    # check with other examples if -1 is correct
    if len(boxes) != len(characters) - 1:
        raise IndexError("Not all characters were recognized correctly")

    else:
        img = cv2.imread('example/' + filename + '.png')
        drawBoxes(boxes, img, filename)
        createLetterImages(characters, boxes, img, filename)


if __name__ == "__main__":
    main()
