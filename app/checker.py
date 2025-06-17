import requests
from concurrent.futures import ThreadPoolExecutor
from config import THREADS, TEST_URL, TIMEOUT
from app.storage import add_live_proxy, record_failed
from app.geoip import get_country


def check_proxy(proxy_line: str):
    proxy_line = proxy_line.strip()
    if not proxy_line:
        return
    proxies = {
        'http': f'http://{proxy_line}',
        'https': f'http://{proxy_line}'
    }
    try:
        r = requests.get(TEST_URL, proxies=proxies, timeout=TIMEOUT)
        if r.status_code == 200:
            ip, port = proxy_line.split(':')
            country = get_country(ip)
            add_live_proxy(ip, int(port), country=country)
            print(f'[LIVE] {proxy_line}')
            return
    except Exception:
        pass
    ip, port = proxy_line.split(':')
    record_failed(ip, int(port))
    print(f'[DIE] {proxy_line}')


def check_proxies(proxy_file: str):
    with open(proxy_file, 'r') as f:
        proxies = f.read().splitlines()
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        executor.map(check_proxy, proxies)

