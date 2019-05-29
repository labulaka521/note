from concurrent.futures import ThreadPoolExecutor
import requests

def fetch(url):
    r = requests.get(url)
    return r.text


pool = ThreadPoolExecutor(10)
u1 = pool.submit(fetch, 'http://www.baudu.com')
u2 = pool.submit(fetch, 'http://www.python.org')

print(u1.result)
print(u2.result)

