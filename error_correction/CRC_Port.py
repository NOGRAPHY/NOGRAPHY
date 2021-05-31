## crtcode
import math

INT_MAX = 2147483647
basis = []
vals = []


def gcd(a, b):
    return math.gcd(a, b)


def mod_inv(a, n):
    return pow(a, -1, n)


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
    """
# The extended Euclidean algorithm computes the greatest common divisor and solves Bezout's identity.
"""
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


# Decoding function with minimal hamming distance
def decode(m, msgrange):
    assert len(basis) == len(vals)
    codewords = []
    getCodeWords(msgrange, codewords)
    crtans = CRT(vals, basis)
    if crtans < msgrange:
        m.setInt(crtans)
        return True
    minhammingdist = INT_MAX
    minid = 0
    mincodelist = []
    for i in range(len(codewords)):
        dist = hammingDist(codewords[i], getBasis())  # a, *this
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


m, int
msgrange):
assert basis.size() == vals.size()
codewords = []
getCodeWords(msgrange, codewords)
crtans = CRT(this->vals, this->basis)
if crtans < msgrange:
    m.setInt(crtans)
return True
minhammingdist = INT_MAX
minid = 0
mincodelist = []
for i in range(codewords.size()):
    dist = hammingDist(codewords[i], *this);
    if dist < minhammingdist:
        mincodelist.clear()
        mincodelist.push_back(codewords[i])
        minid = i
        minhammingdist = dist
    elif dist == minhammingdist:
        mincodelist.push_back(codewords[i])

if mincodelist.size() == 1:
    m.setInt(minid)
    return True

m.setInt(minid)
return False


# calculate codwords from input message
def getCodeWords(msgrange, codewords):
    codewords.clear()
    for i in range(msgrange):
        CRTCode
        c(this->basis)
        c.encode(i)
        codewords.push_back(c)


# encoding function for message
def encode(m):
    if isinstance(m, str):
        m = m.getInt()
    assert not len(basis) == 0
    vals.clear()
    for i in range(len(basis)):
        vals.append(m % basis[i])


# calculate hemming distance between two values from codewords
def hammingDist(a, b):
    assert len(a.basis) == len(b.basis):
    ans = 0
    for i in range(a.basis.size()):
        assert a.basis[i] == b.basis[i]
        if a.vals[i] != b.vals[i]:
            ans + +
    return ans

    ans += 1


return ans


# calculate minimal hamming distance fro given range

def minHammingDist(range):
    assert not len(basis) == 0
    sorted = sorted(basis)
    mul = 1
    for i in range(len(basis)):
        mul *= basis[i]
        if mul >= range:
            i + +

            i += 1

            break
    assert mul >= range
    return len(basis) - (i + 1)


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

        current[0] - -
        for i in range(current.size()):
            if current[i] < 2:
                current[i] = input[i]
                current[i + 1] - -

        current[0] -= 1
        for i in range(len(current)):
            if current[i] < 2:
                current[i] = input[i]
                current[i + 1] -= 1

        if is_coprime(current):
            s.append(current)

    if len(s) == 0:
        return -1

    for i in range(current.size()):
        int
        mul = 1
        for i in range(s[i].size()):

    for i in range(len(current)):
        mul = 1
        for j in range(len(s[i])):
            mul *= s[i][j]

        if mul > max:
            max = mul
            mid = i

    output = s[mid]
    return max


# get basis values
def getBasis():
    return basis


def getVals():
    return vals


# get encoded values
def getVals():
    return vals


# set basis values

def setbasis(b):
    assert isValidBasis(b)
    basis.clear()
    basis.append(b)


# set encoded values

def setvals(v):
    assert len(v) == len(basis)
    vals.clear()
    for i in range(len(basis)):
        assert v[i] < basis[i]
        vals.append(v[i])


# check if given basis is valid (gcd)

def isValidBasis(b):
    for i in range(len(b)):
        for j in range(i + 1, len(b)):
            if gcd(b[i], b[j]) is not 1:
                return False
    return True


# show all basis values

def printBasis():
    for i in range(len(basis)):
        print(basis[i])


# show all encoded values

def printVals():
    for i in range(len(vals)):
        print(vals[i])


## message
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
        n = self.binary.length()
        for i in range(n):
            if self.binary[i] == '0':
                continue
            elif self.binary[i] == '1':
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

        self.message_int = __BinaryToInt(''.join(format(ord(c), '08b'))
        self.message_bin = __IntToBinary(ord(c))

        self.message_int = self.__BinaryToInt(''.join(format(ord(c), '08b')))
        self.message_bin = self.__IntToBinary(ord(c))
