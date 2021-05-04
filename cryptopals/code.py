from Crypto.Cipher import AES
from os import urandom
import binascii, base64
from sys import argv
from string import printable
from math import inf
from random import randint

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

## Part 2

# default 16 bytes = 128 bit AES
def pkcs7_pad(raw, blocksize=16):
    padlen = (blocksize - len(raw)) % blocksize
    if padlen == 0:
        padlen = blocksize
    ba = bytearray(raw)
    return bytes(ba + bytearray((padlen,))*padlen)

def pkcs7_unpad(raw):
    padlen = raw[-1]
    pad = raw[-1:] * padlen
    if raw[-padlen:] == pad:
        return raw[:-padlen]
    raise ValueError('invalid pkcs7 padding')

def is_ecb(raw):
    chunks = split_chunk(raw, 16)
    return len(set(chunks)) < len(chunks)

def ecb_encrypt(raw, key):
    raw = pkcs7_pad(raw)
    obj = AES.new(key, AES.MODE_ECB)
    return obj.encrypt(raw)

def ecb_decrypt(raw, key):
    obj = AES.new(key, AES.MODE_ECB)
    return pkcs7_unpad(obj.decrypt(raw))

def cbc_decrypt(raw, key, iv = bytes((0,))):
    obj = AES.new(key, AES.MODE_ECB)
    chunks = split_chunk(raw, 16)
    plaintext = bytearray()
    for chunk in chunks:
        plaintext += bytearray(xor(obj.decrypt(chunk), iv))
        iv = chunk
    return pkcs7_unpad(bytes(plaintext))

def cbc_encrypt(raw, key, iv = bytes((0,))):
    raw = pkcs7_pad(raw)
    obj = AES.new(key, AES.MODE_ECB)
    chunks = split_chunk(raw, 16)
    ciphertext = bytearray()
    for chunk in chunks:
        next = obj.encrypt(xor(chunk, iv))
        ciphertext += next
        iv = next
    return bytes(ciphertext)

def encryption_oracle(raw, mode=None, key = urandom(16), pad=True):
    if pad:
        pad1 = urandom(randint(5,10))
        pad2 = urandom(randint(5,10))
        raw = pad1 + raw + pad2

    if mode is None:
        mode = 'ECB' if randint(0,1) else 'CBC'
    ciphertext = None

    if mode == 'ECB':
        ciphertext = ecb_encrypt(raw, key)
    elif mode == 'CBC':
        ciphertext = cbc_encrypt(raw, key, iv=urandom(16))

    return ciphertext, mode

def kv_parse(s):
    obj = {}
    for kv in s.decode().split('&'):
        k, v = kv.split('=')
        obj[k] = v
    return obj

