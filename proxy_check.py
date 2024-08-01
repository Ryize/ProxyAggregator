import multiprocessing, threading
import time
import traceback

from proxy_checker import ProxyChecker

from parser.free_proxy_cz import get_proxy_list as free_proxy_cz
from parser.free_proxy_list_net import get_proxy_list as free_proxy_list_net
from parser.hmy_name import get_proxy_list as hmy_name

PROXYS = [free_proxy_cz, free_proxy_list_net, hmy_name]

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

    with open('actual_proxy.data', 'a', encoding='utf-8') as file:
        proxy_str = ''
        for i in enabled_proxy:
            proxy_str += f'{", ".join(i.values())}\n'
        file.write(proxy_str)
    for _ in enabled_proxy.copy():
        enabled_proxy.pop()


def _proxy_checker(proxy):
    checker = ProxyChecker()
    try:
        data = checker.check_proxy(proxy)
    except:
        print(proxy)
    if data:
        enabled_proxy.append({})
        _proxy = enabled_proxy[-1]
        _proxy['ip'] = proxy.split(':')[0]
        _proxy['port'] = proxy.split(':')[1]
        _proxy['proxy_type'] = '/'.join(data['protocols'])
        _proxy['anonymity'] = data['anonymity']
        _proxy['timeout'] = str(data['timeout'])
        _proxy['country'] = data['country']
        _proxy['country_code'] = data['country_code']


def infinity_checker():
    while True:
        with open('actual_proxy.data', 'w', encoding='utf-8'):
            pass
        time_start = time.time()
        for k, proxy_func in enumerate(PROXYS):
            try:
                check_proxy_enable(proxy_func())
            except:
                print(f'Произошла ошибка в {k} сервисе.'
                      f'Описание ошибки: {traceback.format_exc()}')
        time_end = time.time()
        print('Время работы:', time_end - time_start)
        with open('proxy.txt', 'w', encoding='utf-8') as file:
            file.write(open('actual_proxy.data').read())
        time.sleep(300)


def check_start():
    multiprocessing.Process(target=infinity_checker).start()
