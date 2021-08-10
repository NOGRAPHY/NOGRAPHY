from error_correction import CRC_Port

def decode(data):
    result = []
    code = CRC_Port.CRTCode([1, 2, 3, 5, 7])
    # iterate through message and set vals
    for x in range(0, len(data), 5):
        tmp = data[x:x + 5]
        tmp_int = []
        # transform to integer representation
        for y in tmp:
            tmp_int.append(int(y, 2))
        # clear vals to avoid errors
        code.vals.clear()
        code.vals.extend(tmp_int)

        # old method
        #result.extend(decode_ec(code))

        # decode with error correction
        decoded = CRC_Port.Message()
        # decoding to correct basis
        code.decode(decoded, 256)
        result.extend(decoded.getChar())

    return ''.join(result)


def decode2(encoded_string):
    bit_string = ''.join(encoded_string)

    # split bit_string into chunks the length of 8
    chunks = [bit_string[::-1][i:i + 8] for i in range(0, len(bit_string), 8)]

    # reverse list of chunks AND every chunk itself.
    chunks = [chunk[::-1] for chunk in chunks[::-1]]

    # remove all the chunks with 0x00 in the beginning
    while chunks:
        chunk = chunks.pop(0)
        if int(chunk, 2) != 0:
            chunks.insert(0, chunk)
            break

    # cast chunks as characters and concatenate
    decoded_string = b''.join([int(c, 2).to_bytes((len(c) + 7) // 8, byteorder='big') for c in chunks]).decode('utf-8')

    return decoded_string


# decode with error correction
def decode_ec(code):
    decoded = CRC_Port.Message()
    # decoding
    code.decode(decoded, 256)
    return decoded.getChar()


def decode_from_font_indexes(indexes_list, base):
    # convert decimal indexes to binary
    indexes_in_binary = [format(i, 'b').zfill(base) for i in indexes_list]

    return decode(indexes_in_binary)
