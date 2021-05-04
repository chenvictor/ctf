from base64 import b64decode
from string import printable
from os import urandom
from random import randint
from code import encryption_oracle, is_ecb, split_chunk

key = urandom(16)
prefix = urandom(randint(6,40))
unknown = b64decode("""
Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK""")

letters = printable.encode()

def oracle(raw):
    return encryption_oracle(prefix + raw + unknown, mode='ECB', key=key, pad=False)[0]

def deduce_blocksize():
    s = b''
    ll = len(oracle(s))
    while len(oracle(s + b'a')) == ll:
        s += b'a'
    return len(oracle(s + b'a')) - ll

mode = 'ECB' if is_ecb(oracle(b'a'*48)) else 'CBC'
print('mode      {}'.format(mode))
assert mode == 'ECB'

blocksize = deduce_blocksize()
print('blocksize {}'.format(blocksize))
assert blocksize == 16

def solve(oracle, blocksize):
    plaintext = bytearray()
    blockno = 0
    offset = 0
    prev = bytearray((b'a'))*blocksize
    next = bytearray()

    for i in range(len(unknown)):
        pad = bytes(prev[offset+1:])
        target = oracle(pad)[blockno*blocksize:(blockno+1)*blocksize]
        let = None
        for letter in letters:
            block = oracle(pad + bytes(next[:offset]) + bytes((letter,)))[:blocksize]
            if block == target:
                let = letter
                break
        if let is None:
            print('error: no match!')
            exit(1)
        next.append(let)
        plaintext.append(let)
        offset += 1
        if offset == blocksize:
            offset = 0
            blockno += 1
            prev = next
            next = bytearray()
    return plaintext

def find_prefix_pad():
    pad = urandom(1)
    ciphertext = oracle(pad*blocksize*10)
    chunks = split_chunk(ciphertext, blocksize)
    chunk_count = {}
    for chunk in chunks:
        if chunk in chunk_count:
            chunk_count[chunk] += 1
        else:
            chunk_count[chunk] = 1
    common = (0, b'')
    for chunk in chunk_count:
        common = max(common, (chunk_count[chunk], chunk))
    print('common block {}'.format(common))
    ret = pad*blocksize
    while common[1] not in split_chunk(oracle(ret), blocksize):
        ret = ret + pad
    return ret, split_chunk(oracle(ret), blocksize).index(common[1])

pad, blockno = find_prefix_pad()
print(pad)
print(blockno)

def oracle_wrap(raw):
    return oracle(pad + raw)[(blockno+1)*blocksize:]

print(solve(oracle_wrap, blocksize))

