from CRC import *


# Error correction test function
def test_CRC():
    print("Chinese Remainder Code Error Correction Test\n")

    # assume we want to encode '01000001'(8bit) to 'ABCDE'. capacity of ABCDE are '13 7 15 17 11', respectively.
    # first we create a message that present the information we want to encode.
    m = Message(m_binary="01000001")  # A

    # if you want, you can also create m by a int value.
    m = Message(m_integer=65)  # 01000001

    # we can check the value in m.
    print("char message: " + m.getChar() + "\nbinary message: " + str(m.getBin()) + "\nint message: " + str(m.getInt()))
    # then we create CRTcode for 'ABCDE'
    # code = CRTCode([13, 7, 15, 17, 11])  # must make sure basis are co-prime.

    code = CRTCode([1, 2, 3, 5, 7])  # must make sure basis are co-prime.

    # show encoding capacity within five letter block
    print("\nencoding capacity: {0}\n".format(code.getBasis()))

    # encoding
    code.encode(m)

    # we can check the encode result
    encoderesult = code.getVals()
    for i in range(len(encoderesult)):
        print(str(m.getInt()) + " mod " + str(code.getBasis()[i]) + " is " + str(encoderesult[i]))

    # if we want to decode, first we must know the encode range.
    # since our encode message is 8-bits, so the range is 0-255, totally 256.
    # next we create a message to store the decoded information
    decoded = Message()

    # decoding
    code.decode(decoded, 256)

    # we can check the decode result.
    print("\norigin message: {0} -> {1} -> {2}".format(m.getChar(), m.getBin(), m.getInt()))
    print("decode message: {0} <- {1} <- {2}".format(decoded.getChar(), decoded.getBin(), decoded.getInt()))

    # if we have a transition error, for example:
    print("\nnow with one transition error: {0} ".format(code.getVals()), end='')
    encoderesult[0] -= 2
    # two errors
    # encoderesult[3] -= 6
    print("-> {1}\n".format(code.getVals(), encoderesult), end='')
    code.setvals(encoderesult)

    # we can still decode
    errordecode = Message()
    code.decode(errordecode, 256)
    print("\nerror decode message: {0} <- {1} <- {2}".format(errordecode.getChar(), errordecode.getBin(),
                                                             errordecode.getInt()))

