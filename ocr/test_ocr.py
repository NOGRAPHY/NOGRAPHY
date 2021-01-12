from ocr import getLettersFromImage, drawBoundingBoxedOnImage
from cv2 import cv2

def test_demo_01():
    test_image = cv2.cvtColor(cv2.imread('ocr/example/demo_01.png'), cv2.COLOR_BGR2GRAY)
    letters = getLettersFromImage(test_image)
    image_with_bounding_boxes = drawBoundingBoxedOnImage(test_image, letters)
    cv2.imwrite('ocr/example/result/demo_01_result.png', image_with_bounding_boxes)

def test_demo_02():
    test_image = cv2.cvtColor(cv2.imread('ocr/example/demo_02.png'), cv2.COLOR_BGR2GRAY)
    letters = getLettersFromImage(test_image)
    image_with_bounding_boxes = drawBoundingBoxedOnImage(test_image, letters)
    cv2.imwrite('ocr/example/result/demo_02_result.png', image_with_bounding_boxes)