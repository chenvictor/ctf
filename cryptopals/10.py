from Crypto.Cipher import AES
from base64 import b64decode
from code import cbc_decrypt

key = b'YELLOW SUBMARINE'

with open('./data/10.txt') as f:
    raw = b64decode(f.read())
    print(cbc_decrypt(raw, key))

