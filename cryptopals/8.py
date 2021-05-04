from binascii import unhexlify
from base64 import b64decode
from code import is_ecb

with open('./data/8.txt') as f:
    cnt = 0
    for line in f:
        print(cnt)
        cnt += 1
        print(len(line))
        raw = unhexlify(line)
        if is_ecb(raw):
            print(raw)
            break

