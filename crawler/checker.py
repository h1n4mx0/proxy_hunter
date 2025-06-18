import requests
import time
from concurrent.futures import ThreadPoolExecutor
from config import THREADS, TEST_URL, TIMEOUT
from crawler.storage import add_live_proxy, remove_proxy, get_all_proxies
from crawler.geoip import get_country


def check_proxy(proxy_line: str):
    proxy_line = proxy_line.strip()
    if not proxy_line:
        return
    ip, port = proxy_line.split(":")
    proxies = {
        "http": f"http://{proxy_line}",
        "https": f"http://{proxy_line}",
    }
    try:
        start = time.perf_counter()
        r = requests.get(TEST_URL, proxies=proxies, timeout=TIMEOUT)
        latency_ms = int((time.perf_counter() - start) * 1000)
        if r.status_code == 200:
            country = get_country(ip)
            add_live_proxy(ip, int(port), latency_ms, country)
            print(f"[LIVE] {proxy_line} {latency_ms}ms")
            return
    except Exception:
        pass
    remove_proxy(ip, int(port))
    print(f"[DIE] {proxy_line}")


def check_proxies(proxy_file: str):
    with open(proxy_file, 'r') as f:
        proxies = f.read().splitlines()
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        executor.map(check_proxy, proxies)


def recheck_db_proxies():
    proxies = [f"{p['ip']}:{p['port']}" for p in get_all_proxies()]
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        executor.map(check_proxy, proxies)
