from code import pkcs7_pad, pkcs7_unpad

plaintext = b'YELLOW SUBMARINE'

print(pkcs7_pad(plaintext, 20))

assert pkcs7_unpad(pkcs7_pad(plaintext, 20)) == plaintext


