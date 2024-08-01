import random, base64
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
    html = requests.get(
        f'https://advanced.name/ru/freeproxy',
        headers=get_random_user_agent()).text
    soup = BeautifulSoup(html, 'lxml')

    proxy_list_amount = int(
        soup.find('ul', class_='pagination pagination-lg').find_all('li')[
            -2].text)
    for i in range(1, proxy_list_amount + 1):
        html = requests.get(
            f'https://advanced.name/ru/freeproxy?page={i}',
            headers=get_random_user_agent()).text
        soup = BeautifulSoup(html, 'lxml')
        for i in soup.find_all('tr'):
            if i.find('th'):
                continue
            proxy.append({})
            proxy_ = proxy[-1]
            proxy_['ip'] = base64.b64decode(
                i.find_all('td')[1]['data-ip']
            ).decode("utf-8")
            proxy_['port'] = base64.b64decode(
                i.find_all('td')[2]['data-port']
            ).decode("utf-8")
            proxy_['address'] = i.find_all('td')[4].text.replace('\n', '')
            proxy_type = i.find_all('td')[3].text.replace('\n', ' ')
            proxy_[
                'anonym'] = 'Elite' if 'elite' in proxy_type.lower() else 'Нет'
            proxy_['proxy_type'] = proxy_type.replace('ELITE', '')
    return proxy
