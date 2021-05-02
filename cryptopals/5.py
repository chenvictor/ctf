from binascii import hexlify
from code import xor

s = b"Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
k = b'ICE'

print(hexlify(xor(s,k)).decode())

