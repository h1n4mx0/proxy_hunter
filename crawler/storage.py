import os
import sqlite3
import threading
from datetime import datetime

DB_PATH = os.path.join('data', 'proxies.db')
_conn = sqlite3.connect(DB_PATH, check_same_thread=False)
_lock = threading.Lock()


def init_db():
    os.makedirs('data', exist_ok=True)
    with _conn:
        _conn.execute(
            '''CREATE TABLE IF NOT EXISTS proxies (
                ip TEXT,
                port INTEGER,
                latency_ms INTEGER,
                last_checked TEXT,
                total_checks INTEGER,
                live_checks INTEGER,
                country TEXT,
                PRIMARY KEY (ip, port)
            )'''
        )


init_db()


def add_live_proxy(ip: str, port: int, latency_ms: int, country: str = 'N/A'):
    now = datetime.utcnow().isoformat()
    with _lock, _conn:
        cur = _conn.execute(
            'SELECT live_checks, total_checks FROM proxies WHERE ip=? AND port=?',
            (ip, port)
        )
        row = cur.fetchone()
        if row:
            live_checks, total_checks = row
            _conn.execute(
                'UPDATE proxies SET latency_ms=?, last_checked=?, total_checks=?, '
                'live_checks=?, country=? WHERE ip=? AND port=?',
                (latency_ms, now, total_checks + 1, live_checks + 1,
                 country, ip, port)
            )
        else:
            _conn.execute(
                'INSERT INTO proxies (ip, port, latency_ms, last_checked, '
                'total_checks, live_checks, country) '
                'VALUES (?, ?, ?, ?, 1, 1, ?)',
                (ip, port, latency_ms, now, country)
            )


def remove_proxy(ip: str, port: int):
    with _lock, _conn:
        _conn.execute('DELETE FROM proxies WHERE ip=? AND port=?', (ip, port))


def get_all_proxies():
    with _lock, _conn:
        rows = _conn.execute(
            'SELECT ip, port, latency_ms, last_checked, total_checks, '
            'live_checks, country FROM proxies'
        ).fetchall()
    result = []
    for row in rows:
        result.append({
            'ip': row[0],
            'port': row[1],
            'latency_ms': row[2],
            'last_checked': datetime.fromisoformat(row[3]),
            'total_checks': row[4],
            'live_checks': row[5],
            'country': row[6],
        })
    return result


def add_proxy(ip: str, port: int, country: str = 'N/A'):
    now = datetime.utcnow().isoformat()
    with _lock, _conn:
        _conn.execute(
            'INSERT OR IGNORE INTO proxies '
            '(ip, port, latency_ms, last_checked, total_checks, live_checks, country) '
            'VALUES (?, ?, -1, ?, 0, 0, ?)',
            (ip, port, now, country)
        )


def delete_proxy(ip: str, port: int):
    remove_proxy(ip, port)
