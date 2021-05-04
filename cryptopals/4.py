from binascii import unhexlify
from code import xor_decode

with open('./data/4.txt') as f:
    best = (0, b'none', 0)
    num = 0
    i = 0
    for line in f.read().split():
        i += 1
        test = xor_decode(unhexlify(line))
        if test[0] > best[0]:
            best = test
            num = i

    print(best[1].decode())
    print('from line {}'.format(num))

