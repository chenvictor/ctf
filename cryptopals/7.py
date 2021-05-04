from base64 import b64decode
from code import ecb_decrypt

key = b'YELLOW SUBMARINE'

with open('./data/7.txt') as f:
    ciphertext = b64decode(f.read())
    plaintext = ecb_decrypt(ciphertext, key)
    print(plaintext)

