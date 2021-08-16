from error_correction import CRC
from numpy import random

def decode(data):
    # if length of font indexes is lower than five times secret message, raise error
    #assert len(data) % 5 == 0, "Binary secret data to be decoded is to short (-{0}).".format(5-(len(data) % 5))
    # and insert dummy value at first position
    if len(data) % 5 != 0:
        data.insert(0, format(0, 'b').zfill(3))
    result = []
    # CRTCode Object is used for error correction
    code = CRC.CRTCode([1, 2, 3, 5, 7])
    # iterate through message and set values
    for x in range(0, len(data), 5):
        tmp = data[x:x + 5]
        tmp_int = []
        # transform to integer representation
        for y in tmp:
            tmp_int.append(int(y, 2))
        # clear values to avoid errors
        code.vals.clear()
        code.vals.extend(tmp_int)

        # decode with error correction
        decoded = CRC.Message()
        # decoding to correct basis
        code.decode(decoded, 256)
        result.extend(decoded.getChar())

    return ''.join(result)

def decode_from_font_indexes(indexes_list, base = 3):
    # convert decimal indexes to binary
    indexes_in_binary = [format(i, 'b').zfill(base) for i in indexes_list]

    return decode(indexes_in_binary)
