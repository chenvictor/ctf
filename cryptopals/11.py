from base64 import b64decode
from code import encryption_oracle, is_ecb

def pad(raw):
    pad1 = urandom(randint(5,10))
    pad2 = urandom(randint(5,10))
    return pad1 + raw + pad2

raw = b'a'*48
N_TRIALS = 100
success  = 0

for i in range(N_TRIALS):
    ciphertext, mode = encryption_oracle(raw)
    guess_mode = 'ECB' if is_ecb(ciphertext) else 'CBC'
    if mode == guess_mode:
        success += 1
print('guessed correctly {}/{} times'.format(success, N_TRIALS))
assert success == N_TRIALS

