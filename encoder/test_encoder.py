from encoder import encode

def test_encoding():
    expected = [
        '000', '100', '100', '001', '100', '101', '011', '011',
        '000', '110', '110', '001', '101', '111', '001', '000',
        '000', '101', '011', '101', '101', '111', '011', '100',
        '100', '110', '110', '001', '100', '100']
    assert expected == encode('Hello World', 3)
