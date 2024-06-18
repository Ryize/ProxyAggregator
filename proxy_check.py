import json
import threading
import time

import requests
from proxy_checker import ProxyChecker

from parser.free_proxy_cz import get_proxy_list

enabled_proxy = []


def check_proxy_enable(proxies: list):
    threads = []
    for proxy in proxies:
        proxy = f"{proxy['ip']}:{proxy['port']}"
        thread = threading.Thread(target=_proxy_checker, args=(proxy,))
        thread.start()
        threads.append(thread)

        while len(threading.enumerate()) >= 500:
            time.sleep(0.5)
    for thread in threads:
        thread.join()

    with open('proxy.json') as file:
        data = json.load(file)
        print(data)

def _proxy_checker(proxy):
    checker = ProxyChecker()
    data = checker.check_proxy(proxy)
    if data:
        enabled_proxy.append({})
        _proxy = enabled_proxy[-1]
        _proxy['ip'] = proxy.split(':')[0]
        _proxy['port'] = proxy.split(':')[1]
        _proxy['proxy_type'] = data['protocols']
        _proxy['anonymity'] = data['anonymity']
        _proxy['timeout'] = data['timeout']
        _proxy['country'] = data['country']
        _proxy['country_code'] = data['country_code']

time_start = time.time()
proxys = get_proxy_list()
check_proxy_enable(proxys)

time_end = time.time()
print(len(proxys))
print(time_end - time_start)