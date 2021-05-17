### Encoding
N       # Number of block in text - hole text divided into blocks
C = [N] # List of blocks, each denoted as C1, ..., Cn
n = 5   # count of letters in each block (here 5)
k = 3   # pairs of integers (ri,pi) (here 3)
u 	# original font u
s = 8	# integer embedding capacity of the original font (here 8)

# Block Ct = (C1, ...,Cn ), where Ci indicates a letter with its original font ui,
# whose integer embedding capacity is si (i.e., Ci’s font ui has si perturbed glyphs in the codebook)

## 1. Computing pi (mutually prime numbers):
# search n mutually prime numbers pi for i = 1...n, such that 
# pi <= si and the product of k minimal pi, denoted as Mt for each block Ct, is maximized
from math import gcd as bltin_gcd
def coprime2(a, b):
    return bltin_gcd(a, b) == 1

p = []
Mt = []
si = 8
for Ct in C:                # for every block in text 
    for i in range(n):      # for every letter in block (for Ci in Ct:)
        # search mutually prime number pi
        for i in range(1, si):
            for j in range(1, si):
                pi = bltin_gcd(i, j)

        if [pi <= si for i in range(len(pi))]:
	        p.append(pi[i])
        elif pi > si:       # Note 1: [pi > si for i in range(len(pi))]
            break
    Mt.append(k * min(p))
    # Repeat this process until a valid set of mutually prime numbers is found.
# Note 1: that if we could not find mutually prime numbers pi for block Ct, we simply ignore
# the letter whose embedding capacity is smallest among all si and include Cn+1 to this block. 


## 2. Determining mt (integer for each block):
# Given the plain message represented as a bit string M, we now split the bits into a sequence of chunks, 
# each of which is converted into an integer and assigned to a block Ct. 
# We assign to each block Ct an integer mt with |_ log2 Mt _| bits, which is sequentially cut from the bit string M.
plain_message = []  # plain string message
bit_string = ''.join([format(c, 'b').zfill(8) for c in plain_message.encode('utf8')])  # bit string M
mt = []
for Ct in range(len(C)):  # for every block in text
    # split bit_string into chunks the length of Mt for each block
    chunks = [bit_string[::-1][i:i + Mt[Ct].bit_length() - 1]
              for i in range(0, len(bit_string), Mt[Ct].bit_length() - 1)]

    # reverse list of chunks AND every chunk itself.
    chunks = [chunk[::-1].zfill(Mt[Ct].bit_length() - 1) for chunk in chunks[::-1]]

    # converted into an integer and assigned to block Ct
    block_integer = [int(c, 2) for c in chunks]
    mt.append(block_integer)

## 3. Embedding
# For every block Ct , we compute the codeword using the CRT encoding function 
# ϕ(m) = (m mod p1,m mod p2, ...,m mod pn ), obtaining r = (r1, ..., rn ).
# Each ri is then embedded in the glyph of the letter Ci in the block Ct as described in §4.5.
ϕm = []
for Ct in range(len(C)):    # for every block in text
    for i in range(n):      # for every letter in block (for Ci in Ct:)
        ϕm = mt[Ct] % p[i]  # every 5 values are r = (r1, ..., rn)


### Decoding
# At decoding time, we recognize the glyphs of the letters in a document and extract integers from them with OCR.
letter_sequence =[]

# Next, we divide the letter sequence into blocks.
letter_chunks = [letter_sequence[x:x+5] for x in range(0, len(letter_sequence), 5)]

# Repeat the algorithm of computing pi and Mt as in the encoding step, 
# for every block. Given a block Ct, the extracted integers from its letters 
# form a code vector r˜t = (r˜1, ..., r˜n)
# 1. Computing pi
p = []
# 2. Determining mt
mt = []

# To decode r˜t , we first compute m˜t = CRT(r˜t, pt) where pt stacks all pi in the block.
mt = chi_rem_thm(mt,p)

# If m˜t < Mt, then m˜t is the decoding result ϕ+(r˜t ), because the Hamming distance H((m˜t), r˜) = 0. 
if mt < Mt:
    pass
else:
# Otherwise, we decode r˜t using the Hamming decoding function: concretely, since we know the
# current block can encode an integer in the range [0, Mt ), we decode r˜t into the integer mt by finding
# m_t=ϕ^+(r ̃ )=arg  min┬(m∈[0,M_t))⁡ H(ϕ(m),r ̃ ).
    # Hamming decoding function
    mt = hamming_distance(ϕm, mt)

# Lastly, we convert mt into a bit string and concatenate mt 
# from all blocks sequentially to recover the plain message.
bit_string = ''.join(mt)

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

# modular inverse
def inverse_mod(a,b):
    x = a
    y = b
    oldolds = 1
    olds = 0
    oldoldt = 0
    oldt = 1
    while y != 0:
        q = x // y
        r = x % y
        x = y
        y = r
        s = oldolds - q * olds
        t = oldoldt - q * oldt
        oldolds = olds
        oldoldt = oldt
        olds = s
        oldt = t
    return oldolds
# The chinese remainder theorem
def chi_rem_thm(mn,an):
    m = 1
    Mn = []
    yn = []
    for k in range(0, len(mn)):
         m  = m * mn[k]
    
    for  k in range (0, len(mn)):
        Mk = m / mn[k]
        Mn.append(Mk)
        yk = inverse_mod(Mn[k],mn[k]) % mn[k]
        yn.append(yk)
    x = 0
    for  k in range (0, len(yn)):
        x = x + an[k] * Mn[k] * yn[k]
    while x >= m:
        x = x - m
    return x

# Return the Hamming distance between string1 and string2.
# string1 and string2 should be the same length.
def hamming_distance(encod_fct, codevector): 
    # Start with a distance of zero, and count up
    distance = 0
    # Loop over the indices of the string
    L = len(encod_fct)
    for i in range(L):
        # Add 1 to the distance if these two values are not equal
        if encod_fct[i] != codevector[i]:
            distance += 1
    # Return the final count of differences
    return distance
