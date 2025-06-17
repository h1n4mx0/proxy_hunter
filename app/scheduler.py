from apscheduler.schedulers.background import BackgroundScheduler
from app.checker import check_proxies

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: check_proxies("data/proxy_candidates.txt"), 'interval', minutes=10)
    scheduler.start()