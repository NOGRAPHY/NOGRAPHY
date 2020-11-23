import string
import random

from encoder_decoder.encoder_decoder import encode, decode

printable_ascii_string = list(string.printable)

for n in range(2, 33):
    # print("base", n)
    random.shuffle(printable_ascii_string)
    msg = ''.join(printable_ascii_string)

    assert msg == decode(encode(msg, n))


custom_msg = "https://www.htwg-konstanz.de/hochschule/fakultaeten/informatik/uebersicht/"
custom_base = 3

assert custom_msg == decode(encode(custom_msg, custom_base))
