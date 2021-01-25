from ocr import getLettersFromImage, drawBoundingBoxedOnImage, preprocessImage
from cv2 import cv2

def test_demo_01():
    img = cv2.imread('ocr/example/demo_01.png')
    test_image = preprocessImage(img)
    letters = getLettersFromImage(test_image)
    image_with_bounding_boxes = drawBoundingBoxedOnImage(test_image, letters)
    cv2.imwrite('ocr/example/result/demo_01_result.png', image_with_bounding_boxes)

def test_demo_02():
    img = cv2.imread('ocr/example/demo_02.png')
    test_image = preprocessImage(img)
    letters = getLettersFromImage(test_image)
    image_with_bounding_boxes = drawBoundingBoxedOnImage(test_image, letters)
    cv2.imwrite('ocr/example/result/demo_02_result.png', image_with_bounding_boxes)