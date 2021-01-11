from cv2 import cv2

import pytesseract

pytesseract.pytesseract.tesseract_cmd = '/usr/local/Cellar/tesseract/4.1.1/bin/tesseract'

img = cv2.imread('ocr/example/test.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hImg, wImg = img.shape

boxes = pytesseract.image_to_boxes(img)

print(boxes)

for b in boxes.splitlines():
    b = b.split(' ')
    x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
    cv2.rectangle(img, (x, hImg - y), (w, hImg - h), (0, 0, 255), 1)

cv2.imshow('Result', img)
cv2.waitKey(0)