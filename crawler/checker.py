import requests
from concurrent.futures import ThreadPoolExecutor
from config import THREADS, TEST_URL, TIMEOUT
from crawler.storage import add_live_proxy

def check_proxy(proxy_line):
    proxy_line = proxy_line.strip()
    if not proxy_line:
        return
    proxies = {
        "http": f"http://{proxy_line}",
        "https": f"http://{proxy_line}"
    }
    try:
        r = requests.get(TEST_URL, proxies=proxies, timeout=TIMEOUT)
        if r.status_code == 200:
            ip, port = proxy_line.split(":")
            add_live_proxy(ip, int(port))
            print(f"[LIVE] {proxy_line}")
            return
    except:
        pass
    print(f"[DIE] {proxy_line}")

def check_proxies(proxy_file):
    with open(proxy_file, 'r') as f:
        proxies = f.read().splitlines()
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        executor.map(check_proxy, proxies)
