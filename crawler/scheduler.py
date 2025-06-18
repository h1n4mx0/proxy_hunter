from apscheduler.schedulers.background import BackgroundScheduler
from crawler.checker import check_proxies, recheck_db_proxies


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: check_proxies("data/proxy_candidates.txt"), 'interval', minutes=10)
    scheduler.add_job(recheck_db_proxies, 'interval', minutes=5)
    scheduler.start()
