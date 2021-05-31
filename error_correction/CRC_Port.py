## crtcode
import math

# global variables
INT_MAX = 2147483647
basis = []
vals = []

# Extended Euclidean Algorithm
def gcd(a, b):
    return math.gcd(a, b)

# inverse of a on mod n
def mod_inv(a, n):
    return pow(a, -1, n)

# Chinese Remainder Theorem with inverse modulo calculation
def chinese_remainder_theorem(vals, basis):
    mm = 1
    ans = 0

    for x in basis:
        mm *= x

    for x in range(len(basis)):
        mdm = mm / basis[x]
        bi = mod_inv(mdm, basis[x])
        ans += vals[x] * bi * mdm

    return ans % mm


# Extended Euclidean Algorithm
"""
def extgcd(a, b, d, x, y):
    '''The extended Euclidean algorithm computes the greatest common divisor and solves Bezout's identity.'''
    if not b:
        d = a
        x = 1
        y = 0
    else:
        extgcd(b, a % b, d, y, x)
        y -= x * (a / b)


    # greatest common divider between to variables
    def gcd(a, b):
    return b == 0 if a else gcd(b, a % b)
    # return b == 0 ? a : gcd(b, a % b)


    # inverse of a on mod n
    def mod_inv(a, n):
    d, x, y = None
    extgcd(a, n, d, x, y)
    return d == 1 if (x + n) % n else -1
    # return d == 1 ? (x+n) % n: -1

"""

# Chinese Remainder Theorem with inverse modulo calculation
def CRT(vals, basis):
    mm = 1
    ans = 0
    for i in range(len(basis)):
        mm *= basis[i]
    for i in range(len(basis)):
        mdm = mm / basis[i]
        bi = mod_inv(mdm, basis[i])
        ans += vals[i] * bi * mdm
    return ans % mm


## CRTCode class
class CRTCode:

    # class constructor
    def __init__(self, b=None):
        if b == None:
            print("No parameters for 'Message' class constructor omitted!")
            self.basis = None
        elif b is not None:
            assert self.isValidBasis(b) == True
            self.basis = b
        self.vals = None

    # get basis values
    def getBasis(self):
        return self.basis

    # get encoded values
    def getVals(self):
        return self.vals

    # set basis values
    def setbasis(self, b):
        assert self.isValidBasis(b)
        self.basis.clear()
        self.basis.append(b)

    # set encoded values
    def setvals(self, v):
        assert len(v) == len(self.basis)
        self.vals.clear()
        for i in range(len(self.basis)):
            assert v[i] < self.basis[i]
            self.vals.append(v[i])

    # check if given basis is valid (gcd)
    def isValidBasis(self, b):
        for i in range(len(b)):
            for j in range(i + 1, len(b)):
                if gcd(b[i], b[j]) is not 1:
                    return False
        return True

    # show all basis values
    def printBasis(self):
        for i in range(len(basis)):
            print(self.basis[i])

    # show all encoded values
    def printVals(self):
        for i in range(len(self.vals)):
            print(self.vals[i])


    # Decoding function with minimal hamming distance
    def decode(self, m, msgrange):
        assert len(self.basis) == len(self.vals)
        codewords = []  # list of CRTCode class objects
        codewords = self.getCodeWords(msgrange, codewords)
        crtans = CRT(self.vals, self.basis)
        if crtans < msgrange:
            m.setInt(crtans)
            return True
        minhammingdist = INT_MAX
        minid = 0
        mincodelist = []  # list of CRTCode class objects
        for i in range(len(codewords)):
            dist = self.hammingDist(codewords[i], self)  # a, *this
            if dist < minhammingdist:
                mincodelist.clear()
                mincodelist.append(codewords[i])
                minid = i
                minhammingdist = dist
            elif dist == minhammingdist:
                mincodelist.append(codewords[i])

        if len(mincodelist) == 1:
            m.setInt(minid)
            return True

    # calculate codwords from input message
    def getCodeWords(self, msgrange, codewords):
        codewords.clear()
        for i in range(msgrange):
            c = CRTCode(self.basis)
            c.encode(i)
            codewords.append(c)
        return codewords

    # encoding function for message
    def encode(self, m):  # message class object m
        if isinstance(m, object):
            m = m.getInt()
        if isinstance(m, str):
            m = ord(m)
        if isinstance(m, int):
            m = m
        if isinstance(m, bin):
            m = Message.__BinaryToInt(m)
        assert not len(self.basis) == 0
        self.vals.clear()
        for i in range(len(self.basis)):
            self.vals.append(m % self.basis[i])

    # calculate hemming distance between two values from codewords
    def hammingDist(self, a, b):
        assert len(a.basis) == len(b.basis)
        ans = 0
        for i in range(len(a.basis)):
            assert a.basis[i] == b.basis[i]
            if a.vals[i] != b.vals[i]:
                ans += 1
        return ans

    # calculate minimal hamming distance fro given range
    def minHammingDist(self, range):
        assert not len(self.basis) == 0
        sorted = sorted(self.basis)
        mul = 1
        for i in range(len(self.basis)):
            mul *= self.basis[i]
            if mul >= range:
                i += 1
                break
        assert mul >= range
        return len(self.basis) - (i + 1)


# check if values from input list are all coprime
def is_coprime(input):
    for i in range(len(input)):
        for j in range(i + 1, len(input)):
            if input[i] == input[j]:
                return False
            if gcd(input[i], input[j]) is not 1:
                return False
    return True


# calculate maximum coprime number(s)
def co_prime(input, output):
    max = 0
    mid = 0
    output.clear()
    current = input
    s = [[]]

    while (True):
        flag = True
        for i in range(len(current)):
            if current[i] is not 2:
                flag = False

        if flag:
            break

        current[0] -= 1
        for i in range(len(current)):
            if current[i] < 2:
                current[i] = input[i]
                current[i + 1] -= 1

        if is_coprime(current):
            s.append(current)

    if len(s) == 0:
        return -1

    for i in range(len(current)):
        mul = 1
        for j in range(len(s[i])):
            mul *= s[i][j]

        if mul > max:
            max = mul
            mid = i

    output = s[mid]
    return max


## Message class
class Message:

    def __init__(self, m_integer=None, m_binary=None, m_char=None):
        if m_integer == None and m_binary == None and m_char == None:
            print("No parameters for 'Message' class constructor omitted!")
            return
        if m_integer is not None:
            assert m_integer >= 0
            self.message_int = m_integer
            self.message_bin = self.__IntToBinary(m_integer)
            self.message_char = chr(m_integer)
        if m_binary is not None:
            assert m_binary >= 0
            self.message_bin = m_binary
            self.message_int = self.__BinaryToInt(m_binary)
            self.message_char = chr(m_integer)
        if m_char is not None:
            assert m_char >= 0
            self.message_char = m_char
            self.message_int = self.__BinaryToInt(''.join(format(ord(m_char), '08b')))
            self.message_bin = self.__IntToBinary(ord(m_char))

    def __IntToBinary(self, n):
        ans = ""
        if n == 0:
            return "0"
        while n > 0:
            ans = str(n % 2) + ans
            n /= 2
        return ans

    def __BinaryToInt(self, binary):
        ans = 0
        n = binary.length()
        for i in range(n):
            if binary[i] == '0':
                continue
            elif binary[i] == '1':
                ans += (1 << (n - i - 1))
            else:
                print("invalid input message")
                return
        return ans

    def getInt(self):
        return self.m_integer

    def getBin(self):
        return self.m_binary

    def getChar(self):
        return self.message_char

    def setBin(self, s):
        assert s >= 0
        self.message_bin = s
        self.message_int = self.__BinaryToInt(s)
        self.message_char = chr(self.__BinaryToInt(s))

    def setInt(self, i):
        assert i >= 0
        self.message_int = i
        self.message_bin = self.__IntToBinary(i)
        self.message_char = chr(i)

    def setChar(self, c):
        assert c >= 0
        self.message_char = c

        self.message_int = self.__BinaryToInt(''.join(format(ord(c), '08b')))
        self.message_bin = self.__IntToBinary(ord(c))

        self.message_int = self.__BinaryToInt(''.join(format(ord(c), '08b')))
        self.message_bin = self.__IntToBinary(ord(c))
