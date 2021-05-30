## crtcode
INT_MAX = 2147483647
basis = []
vals = []

def extgcd(a, b, &d, &x, &y):
    if not b:
        d = a
        x = 1
        y = 0
    else:
        extgcd(b, a % b, d, y, x)
        y -= x * (a/b)


def gcd(a, b):
    return b == 0 ? a : gcd(b, a % b)


def mod_inv(int a,int n):   # inverse of a on mod n
    d, x, y = null
    extgcd(a, n, d, x, y)
    return d == 1 ? (x+n) % n: -1


def CRT(const vector<int>& vals, const vector<int>& basis):
    mm=1
    ans=0
    for i in range(basis.size()):
        mm*=basis[i]
    for i in range(basis.size()):
        mdm = mm / basis[i]
        bi = mod_inv(mdm, basis[i])
        ans += vals[i] * bi * mdm
    return ans % mm


def decode(Message &m, int msgrange):
    assert basis.size() == vals.size()
    codewords = []
    getCodeWords(msgrange, codewords)
    crtans = CRT(this->vals, this->basis)
    if crtans < msgrange:
        m.setInt(crtans)
        return True
    minhammingdist=INT_MAX
    minid=0
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

def getCodeWords(msgrange, codewords):
    codewords.clear()
    for i in range(msgrange):
        CRTCode c(this->basis)
        c.encode(i)
        codewords.push_back(c)

def encode(m){
    if m.type == String:
        m = m.getInt()
    assert not basis.empty()
    vals.clear()
    for i in range(basis.size()):
        vals.push_back(m % basis[i])

def hammingDist(a, b):
    assert a.basis.size() == b.basis.size():
    ans = 0
    for i in range(a.basis.size()):
        assert a.basis[i] == b.basis[i]
        if a.vals[i] != b.vals[i]:
            ans++
    return ans

def minHammingDist(range):
    assert not basis.empty()
    sorted = basis
    sort(sorted.begin(), sorted.end())
    mul = 1
    for i in range(basis.size()):
        mul *= basis[i]
        if mul >= range:
            i++
            break
    assert mul >= range
    return basis.size() - (i + 1)

def is_coprime(input):
    for i in range(input.size()):
        for j=(i+1) in range(input.size()):
            if input[i] == input[j]:
                return False
            if gcd(input[i], input[j]) not 1:
                return False
    return True

def co_prime(input, output):
    max=0
    mid=0
    output.clear()
    current = input
    s = [][]

    while (True):
        flag = True
        for i in range(current.size()):
            if current[i] != 2:
                flag = False

        if flag:
            break

        current[0]--
        for i in range(current.size()):
            if current[i] < 2:
                current[i] = input[i]
                current[i+1]--

        if is_coprime(current):
            s.push_back(current)

    if s.empty():
        return -1

    for i in range(current.size()):
        int mul=1
        for i in range(s[i].size()):
            mul *= s[i][j]

        if mul > max:
            max = mul
            mid = i

    output = s[mid]
    return max


def getBasis():
    return basis

def getVals():
    return vals

def setbasis(b):
    assert isValidBasis(b)
    basis = b

def setvals(v):
    assert v.size() == basis.size()
    vals.clear()
    for i in range(basis.size())
        assert v[i] < basis[i]
        vals.push_back(v[i])

def isValidBasis(b):
    for i in range(b.size()):
        for j=i+1 in range(b.size()):
            if gcd(b[i], b[j]) not 1:
                return False
    return True

def printBasis():
    for i in range(basis.size()):
        print(basis[i])

def printVals():
    for i in range(vals.size()):
        print(vals[i])

## message
class Message:

    def __init__(self, m_integer=None, m_binary=None, m_char=None):
        if m_integer == None and m_binary==None and m_char==None:
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
            ans = to_string(n % 2) + ans
            n /= 2
        return ans

    def __BinaryToInt(self, binary):
        ans = 0
        n = self.binary.length()
        for i in range(n):
            if self.binary[i] == '0':
                continue
            elif self.binary[i] == '1':
                ans += (1<<(n-i-1))
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
        self.message_int = __BinaryToInt(s)
        self.message_char = chr(__BinaryToInt(s))

    def setInt(self, i):
        assert i >= 0
        self.message_int = i
        self.message_bin = __IntToBinary(i)
        self.message_char = chr(i)

    def setChar(self, c):
        assert c >= 0
        self.message_char = c
        self.message_int = __BinaryToInt(''.join(format(ord(c), '08b'))
        self.message_bin = __IntToBinary(ord(c))