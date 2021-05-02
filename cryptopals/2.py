from binascii import unhexlify
from code import xor

s1 = '1c0111001f010100061a024b53535009181c'
s2 = '686974207468652062756c6c277320657965'

r1 = unhexlify(s1)
r2 = unhexlify(s2)

print(xor(r1,r2).decode())

