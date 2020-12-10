def decode(encoded_string):
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
    decoded_string = ''.join([chr(int(c, 2)) for c in chunks])

    return decoded_string