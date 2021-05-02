from Crypto.Cipher import AES
import base64

key = b'YELLOW SUBMARINE'

with open('./7.txt') as f:
    ciphertext = base64.b64decode(f.read())
    obj = AES.new(key, AES.MODE_ECB)
    plaintext = obj.decrypt(ciphertext)
    print(plaintext)

