def encode(plain_string, base=3):
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
