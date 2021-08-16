from decoder import decode, decode_from_font_indexes
from numpy import random

def test_decoding_with_ec():
    # Decoding correct encoded binary with error correction
    encoded_correct = ['000', '000', '000', '010', '010',
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
    # Decoding wrong encoded binary + missing value with error correction
                     #'100',
    encoded_error =  [       '000', '000', '010', '010',
                      '100', '001', '010', '001', '011',
                      '000', '000', '000', '011', '011',
                      '000', '000', '000', '011', '011',
                      '000', '001', '000', '001', '110',
                      '000', '000', '010', '010', '100',
                      '000', '001', '000', '010', '011',
                      '000', '001', '000', '001', '110',
                      '000', '000', '000', '100', '010',
                      '000', '000', '000', '011', '011',
                      '000', '000', '001', '000', '010']
    # Expected output string
    expected = 'Hello World'
    # Tests
    assert expected == decode(encoded_correct), "Char decoding \'{0}\' is incorrect to expected output \'{1}\'.".format(decode(encoded_correct), expected)
    print("Decoded correct secret:", decode(encoded_correct))
    assert expected == decode(encoded_error), "Char decoding \'{0}\' is incorrect to expected output \'{1}\'.".format(decode(encoded_error), expected)
    print("Decoded secret with error(s):", decode(encoded_error))


def test_decode_from_font_indexes():
    # Decoding random wrong encoded binary with error correction
    indexes_list = [0, 0, 0, 2, 2,
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
    indexes_list[random.randint(0, len(indexes_list)-1)] = random.randint(0, 7)
    # Expected output string
    expected = 'Hello World'
    assert expected == decode_from_font_indexes(indexes_list, base=3), "Char decoding \'{0}\' is incorrect to expected output \'{1}\'.".format(decode_from_font_indexes(indexes_list, 3), expected)
    print("Decoded secret:", decode_from_font_indexes(indexes_list, base=3))

if __name__ == "__main__":
    test_decoding_with_ec()
    test_decode_from_font_indexes()
