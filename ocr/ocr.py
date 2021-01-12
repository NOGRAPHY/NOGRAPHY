from cv2 import cv2
import pytesseract
    
def getLettersFromImage(image):
    return list(map(mapLineToLetter, pytesseract.image_to_boxes(image).splitlines()))

def mapLineToLetter(line):
    partitions = line.split(' ')
    return Letter(partitions[0], int(partitions[1]), int(partitions[2]), int(partitions[3]), int(partitions[4]))

def drawBoundingBoxedOnImage(image, letters):
    height, width = image.shape
    for letter in letters:
        # TODO: Verify this does what it is expected to.
        cv2.rectangle(image, (letter.x, height - letter.y), (letter.width, height - letter.height), (0, 0, 255), 1)
    return image

class Letter:

    def __init__(self, letter, x, y, width, height):
        self.letter = letter
        self.x = x
        self.y = y
        self. width = width
        self.height = height

    def __str__(self):
        return '\n' + str(self.letter) + ' at (' + str(self.x) + ',' + str(self.y) +') with ' + str(self.width) + 'x' + str(self.height) + 'px'

    def __repr__(self):
        return self.__str__()