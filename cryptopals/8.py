ans = (999, '')

def chunkify(s, n):
    return [s[i:i+n] for i in range(0, len(s), n)]

with open('./8.txt') as f:
    for line in f:
        pats = {}
        for chunk in chunkify(line,32):
            if chunk in pats:
                pats[chunk] += 1
            else:
                pats[chunk] = 1
        ans = min(ans, (len(pats), line))

print(ans)
for chunk in chunkify(ans[1],32):
    print(chunk)
