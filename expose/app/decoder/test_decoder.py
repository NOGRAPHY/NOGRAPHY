from decoder import decode, decode2


def test_decoding_without_ec():
    encoded = [
        '000', '100', '100', '001', '100', '101', '011', '011',
        '000', '110', '110', '001', '101', '111', '001', '000',
        '000', '101', '011', '101', '101', '111', '011', '100',
        '100', '110', '110', '001', '100', '100']
    expected = 'Hello World'
    assert expected == decode2(encoded)


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
    # Decoding wrong encoded binary with error correction
    encoded_error = ['100', '000', '000', '010', '010',
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