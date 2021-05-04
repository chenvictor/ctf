from os import urandom
from code import kv_parse, ecb_encrypt, ecb_decrypt, pkcs7_pad

KEY = urandom(16)

def profile_for(email):
    email = email.replace(b'&', b'')
    email = email.replace(b'=', b'')
    return b'email=' + email + b'&uid=10&role=user'

def oracle(email):
    return ecb_encrypt(profile_for(email), KEY)

def decode(ciphertext):
    return kv_parse(ecb_decrypt(ciphertext, KEY))

#print(kv_parse(b'foo=bar&baz=qux&zap=zazzle'))
#print(profile_for(b'foo@bar.com'))

BLOCKSIZE = 16
padlen = BLOCKSIZE - len('email=')
pad = b'a'*padlen
admin = pkcs7_pad(b'admin', BLOCKSIZE)
admin_block = oracle(pad + admin)[BLOCKSIZE:BLOCKSIZE+BLOCKSIZE]

padlen = (BLOCKSIZE - len('email=&uid=10&role=')) % BLOCKSIZE
email = b'a'*padlen
ciphertext = oracle(email)

admin_text = ciphertext[:-16] + admin_block
admin_profile = decode(admin_text)

print(admin_profile)
assert admin_profile['role'] == 'admin'

