from error_correction import CRC_Port


def encode(plain_string, base=3):
    bit_string = ''.join([format(c, 'b').zfill(8)
                          for c in plain_string.encode('utf8')])

    # split bit_string into chunks the length of base
    chunks = [bit_string[::-1][i:i + base]
              for i in range(0, len(bit_string), base)]

    # reverse list of chunks AND every chunk itself.
    chunks = [chunk[::-1].zfill(base) for chunk in chunks[::-1]]

    result = []
    tmp = []
    # CRTCode Object is used for error correction
    code = CRC_Port.CRTCode([1, 2, 3, 5, 7])

    # encode each chunk with error correction
    for chunk in chunks:
        tmp.extend(encode_with_ec(chunk, code))
    for x in tmp:
        result.append(format(x, '03b'))

    assert len(result) == len(tmp)
    return result


# Encode with error correction
def encode_with_ec(data, code):
    m = CRC_Port.Message(m_binary=data)
    code.encode(m)
    return code.getVals()


def to_ints(encoded):
    result = []
    for x in encoded:
        result.append(int(x, 2))
    return result
