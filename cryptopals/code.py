import binascii, base64
from sys import argv
from string import printable
from math import inf

## Part 1

def xor(a, b):
    return bytes(x^b[i % len(b)] for (i,x) in enumerate(a))

# statistical score of plaintext (etaoin shrdlu)
def score(s):
    if not all(c in bytes(printable.encode()) for c in s):
        return -inf
    s = s.lower()
    return s.count(b' ')*10 + s.count(b'e')*6 + s.count(b't')*5 + s.count(b'a')*5

# returns score, decoded, key
def xor_decode(raw):
    best = (-inf, b'none', None)
    for i in range(256):
        s2 = xor(raw, [i])
        best = max(best, (score(s2), s2, i))
    return best

def hamming(arr1, arr2):
    return bin(int.from_bytes(xor(arr1,arr2), 'little')).count('1')

def score_blocksize(raw, bsize):
    ll = len(raw)
    total = 0
    count = 0
    # average over hamming of adjacent blocks
    for i in range(bsize, ll - ll % bsize, bsize):
        total += hamming(raw[i-bsize:i], raw[i:i+bsize])
        count += 1
    return total / count / bsize

def guess_blocksize(raw, min=2, max=10):
    sizes = list(range(min,max))
    return sorted(sizes, key=lambda sz: score_blocksize(raw, sz))

def split_ith(raw, i):
    ll = len(raw)
    return [raw[j:ll:i] for j in range(i)]

def split_chunk(raw, i):
    return [raw[j:j+i] for j in range(0,len(raw), i)]

def aes_ecb(raw, key, len=16):
    chunks = split_chunk(raw, len)
    plains = [xor(chunk,key) for chunk in chunks]
    return b''.join(plains)

## Part 2

def pkcs7(raw, blocksize):
    padlen = (blocksize - len(raw)) % blocksize
    ba = bytearray(raw)
    return bytes(ba + bytearray((padlen,))*padlen)

