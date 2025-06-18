from crawler.crawler import scan_all_ports
from crawler.checker import check_proxies
from crawler.scheduler import start_scheduler
import threading

if __name__ == '__main__':
    scan_all_ports("vn")  # Có thể đổi country code
    check_proxies("data/proxy_candidates.txt")

    from server.server import run_dashboard
    threading.Thread(target=run_dashboard, daemon=True).start()

    start_scheduler()
    input("\n[ENTER] để dừng chương trình...\n")
