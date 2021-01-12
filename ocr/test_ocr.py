from ocr import ocr

def test_ocr():
    boxes = ocr()
    assert len(boxes) > 0