from binascii import unhexlify
from code import xor_decode

s = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
raw = unhexlify(s)
best = xor_decode(raw)
print(best[1].decode())

