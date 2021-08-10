from encoder import encode, to_ints


def test_encoding():
    expected = [
        '000', '100', '100', '001', '100', '101', '011', '011',
        '000', '110', '110', '001', '101', '111', '001', '000',
        '000', '101', '011', '101', '101', '111', '011', '100',
        '100', '110', '110', '001', '100', '100']
    assert expected == encode('Hello World', 3)


def test_to_ints():
    expected = [0, 4, 4, 1, 4, 5, 3, 3, 0, 6, 6, 1, 5, 7,
                1, 0, 0, 5, 3, 5, 5, 7, 3, 4, 4, 6, 6, 1, 4, 4]
    assert expected == to_ints([
        '000', '100', '100', '001', '100', '101', '011', '011',
        '000', '110', '110', '001', '101', '111', '001', '000',
        '000', '101', '011', '101', '101', '111', '011', '100',
        '100', '110', '110', '001', '100', '100'])

def test():
    # binary encoding test with error correction
    expected_bin = ['000', '000', '000', '010', '010',
                    '000', '001', '010', '001', '011',
                    '000', '000', '000', '011', '011',
                    '000', '000', '000', '011', '011',
                    '000', '001', '000', '001', '110',
                    '000', '000', '010', '010', '100',
                    '000', '001', '000', '010', '011',
                    '000', '001', '000', '001', '110',
                    '000', '000', '000', '100', '010',
                    '000', '000', '000', '011', '011',
                    '000', '000', '001', '000', '010']
    assert expected_bin == encode('Hello World', 8), "Binary encoding is incorrect to expected output."
    print("Binary encoding:", encode('Hello World', 8))

    # binary to integer encoding test with error correction
    expected_int = [0, 0, 0, 2, 2,
                    0, 1, 2, 1, 3,
                    0, 0, 0, 3, 3,
                    0, 0, 0, 3, 3,
                    0, 1, 0, 1, 6,
                    0, 0, 2, 2, 4,
                    0, 1, 0, 2, 3,
                    0, 1, 0, 1, 6,
                    0, 0, 0, 4, 2,
                    0, 0, 0, 3, 3,
                    0, 0, 1, 0, 2]
    assert expected_int == to_ints(encode('Hello World', 8)), "Binary to integer encoding is incorrect to expected output."
    print("Binary to integer encoding:", to_ints(encode('Hello World', 8)))


if __name__ == '__main__':
    test()
