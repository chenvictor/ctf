from os import urandom
from code import cbc_encrypt, cbc_decrypt, split_chunk, xor

KEY = urandom(16)
BLOCKSIZE = 16

def encode(raw):
    raw = raw.replace(b';', b'')
    raw = raw.replace(b'=', b'')
    prepend = b'comment1=cooking%20MCs;userdata='
    append = b';comment2=%20like%20a%20pound%20of%20bacon'
    raw = prepend + raw + append
    return cbc_encrypt(raw, KEY), raw

def is_admin(raw):
    plaintext = cbc_decrypt(raw, KEY)
    print('plaintext {}'.format(plaintext))
    return b';admin=true;' in plaintext

data, plaintext = encode(b'a'*BLOCKSIZE)
print(is_admin(data))

data = split_chunk(bytearray(data), BLOCKSIZE)
admin_block = b';admin=true;'
admin_block = admin_block + (BLOCKSIZE-len(admin_block))*b';'
assert len(admin_block) == BLOCKSIZE

plaintext = split_chunk(plaintext, BLOCKSIZE)

data[1] = xor(xor(plaintext[2], admin_block), data[1])
data = b''.join(data)

print(is_admin(data))

