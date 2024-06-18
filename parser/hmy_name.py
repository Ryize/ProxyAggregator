import random
import threading
import time
from pprint import pprint

import requests

from bs4 import BeautifulSoup

user_agents = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
]


def get_random_user_agent() -> dict:
    """
    Получение случайного User Agent.

    Возвращает случайный User Agent из поля класса (user_agents).

    Returns:
        dict: Словарь в формате ['User-Agent'] = value
    """
    user_agent = random.choice(user_agents)
    return {'User-Agent': user_agent}


proxy = []


def get_proxy_list():
    html = requests.get('https://hmy.name/proxy-list/',
                        headers=get_random_user_agent()).text
    soup = BeautifulSoup(html, 'lxml')

    proxy_list_amount = int(soup.find(
        'div', class_='pagination'
    ).find_all('li')[-2].text) // 10 - 1

    for num_page in range(proxy_list_amount):
        thread = threading.Thread(target=_parser, args=(num_page,))
        thread.start()
        if num_page % 4 == 0:
            pprint(proxy)
            print(len(proxy))
            print(len(threading.enumerate()))
            time.sleep(2)
        time.sleep(0.3)

    while len(threading.enumerate()) >= 3:
        time.sleep(1)
    return proxy


def _parser(num_page):
    html = requests.get(
        f'https://hmy.name/proxy-list/?start={num_page * 64}#list',
        headers=get_random_user_agent()).text
    soup = BeautifulSoup(html, 'lxml')
    for i in soup.find_all('tr'):
        proxy.append({})
        proxy_ = proxy[-1]
        proxy_['ip'] = i.find_all('td')[0].text
        proxy_['port'] = i.find_all('td')[1].text
        proxy_['address'] = i.find_all('td')[2].text
        proxy_['proxy_type'] = i.find_all('td')[4].text
        proxy_['anonym'] = i.find_all('td')[5].text

# get_proxy_list()
