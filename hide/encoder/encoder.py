from error_correction import CRC


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
    code = CRC.CRTCode([1, 2, 3, 5, 7])

    # encode each chunk with error correction
    for chunk in chunks:
        # Encode with error correction
        m = CRC.Message(m_binary=chunk)
        code.encode(m)
        tmp.extend(code.getVals())

    # split bit_string into chunks the length of 3
    for x in tmp:
        result.append(format(x, '03b'))

    assert len(result) == len(tmp)
    return result


def encode2(plain_string, base=3):
    bit_string = ''.join([format(c, 'b').zfill(8)
                          for c in plain_string.encode('utf8')])

    # split bit_string into chunks the length of base
    chunks = [bit_string[::-1][i:i + base]
              for i in range(0, len(bit_string), base)]

    # reverse list of chunks AND every chunk itself.
    chunks = [chunk[::-1].zfill(base) for chunk in chunks[::-1]]

    return chunks


def to_ints(encoded):
    return [int(c, 2) for c in encoded]
