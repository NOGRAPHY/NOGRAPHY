from cv2 import cv2
from tesserocr import PyTessBaseAPI, RIL

def main():
    filename = 'demo_02'
    characters, boxes = recognizeCharacters('example/' + filename + '.png')
    img = cv2.imread('example/' + filename + '.png')
    drawBoxes(boxes, img, filename)
    createLetterImages(characters, boxes, img, filename)

def recognizeCharacters(filename):
    with PyTessBaseAPI() as api:
        api.SetImageFile(filename)
        boxes = api.GetComponentImages(RIL.SYMBOL, True)
        characters = api.GetUTF8Text().replace(" ", "").rstrip("\n")

        if len(boxes) != len(characters):
            raise IndexError("Not all characters were recognized correctly")
        else:
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

if __name__ == "__main__":
    main()