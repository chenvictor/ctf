from base64 import b64decode
from code import hamming, guess_blocksize, split_ith, xor_decode, xor

print(hamming(b'this is a test', b'wokka wokka!!!'))

with open('./6.txt') as f:
    raw = b64decode(f.read())

    # first 5 sizes
    sizes = guess_blocksize(raw, 2, 40)[:5]
    for sz in sizes:
        blocks = split_ith(raw, sz)
        key = bytearray()
        sz_score = 0
        for block in blocks:
            score, _, k = xor_decode(block)
            sz_score += score
            key.append(k)
        if sz_score < 0:
            continue
        print('size {}'.format(sz))
        print('key  {}'.format(bytes(key)))
        print(xor(raw, key).decode())
    
