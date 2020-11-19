def encode(plain_string, base):
    bit_string = ''.join([format(c, 'b').zfill(8) for c in plain_string.encode('utf8')])

    # split bit_string into chunks the length of base
    chunks = [bit_string[::-1][i:i + base] for i in range(0, len(bit_string), base)]

    # reverse list of chunks AND every chunk itself.
    chunks = [chunk[::-1].zfill(base) for chunk in chunks[::-1]]

    return chunks


def decode(coded_string):
    bit_string = ''.join(coded_string)

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
    decoded_string = ''.join([chr(int(c, 2)) for c in chunks])

    return decoded_string
