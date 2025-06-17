from datetime import datetime

live_proxies = []

def add_live_proxy(ip, port):
    live_proxies.append({
        'ip': ip,
        'port': port,
        'latency_ms': 500,
        'last_checked': datetime.utcnow(),
        'total_checks': 1,
        'live_checks': 1,
        'country': 'N/A',
        'anonymity': 'unknown'
    })

def get_all_proxies():
    return live_proxies