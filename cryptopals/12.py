from base64 import b64decode
from string import printable
from os import urandom
from code import encryption_oracle, is_ecb
from sys import exit

key = urandom(16)
unknown = b64decode("""
Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK""")

letters = printable.encode()

def oracle(raw):
    return encryption_oracle(raw + unknown, mode='ECB', key=key, pad=False)[0]

def deduce_blocksize():
    s = b''
    ll = len(oracle(s))
    while len(oracle(s + b'a')) == ll:
        s += b'a'
    return len(oracle(s + b'a')) - ll

mode = 'ECB' if is_ecb(oracle(b'a'*48)) else 'CBC'
print('mode      {}'.format(mode))

blocksize = deduce_blocksize()
print('blocksize {}'.format(blocksize))

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

print(solve(oracle, blocksize))

