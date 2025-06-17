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
                anonymity TEXT,
                PRIMARY KEY (ip, port)
            )'''
        )


init_db()


def add_live_proxy(ip: str, port: int, latency_ms: int = 500,
                   country: str = 'N/A', anonymity: str = 'unknown'):
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
                'live_checks=?, country=?, anonymity=? WHERE ip=? AND port=?',
                (latency_ms, now, total_checks + 1, live_checks + 1,
                 country, anonymity, ip, port)
            )
        else:
            _conn.execute(
                'INSERT INTO proxies (ip, port, latency_ms, last_checked, '
                'total_checks, live_checks, country, anonymity) '
                'VALUES (?, ?, ?, ?, 1, 1, ?, ?)',
                (ip, port, latency_ms, now, country, anonymity)
            )


def record_failed(ip: str, port: int):
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
                'UPDATE proxies SET last_checked=?, total_checks=? WHERE ip=? AND port=?',
                (now, total_checks + 1, ip, port)
            )
        else:
            _conn.execute(
                'INSERT INTO proxies (ip, port, latency_ms, last_checked, '
                'total_checks, live_checks, country, anonymity) '
                "VALUES (?, ?, -1, ?, 1, 0, 'N/A', 'unknown')",
                (ip, port, now)
            )


def get_all_proxies():
    with _lock, _conn:
        rows = _conn.execute(
            'SELECT ip, port, latency_ms, last_checked, total_checks, '
            'live_checks, country, anonymity FROM proxies'
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
            'anonymity': row[7]
        })
    return result


def add_proxy(ip: str, port: int, country: str = 'N/A',
              anonymity: str = 'unknown'):
    """Manually insert a proxy into the database."""
    now = datetime.utcnow().isoformat()
    with _lock, _conn:
        _conn.execute(
            'INSERT OR IGNORE INTO proxies '
            '(ip, port, latency_ms, last_checked, total_checks, '
            'live_checks, country, anonymity) '
            'VALUES (?, ?, -1, ?, 0, 0, ?, ?)',
            (ip, port, now, country, anonymity)
        )


def delete_proxy(ip: str, port: int):
    """Remove a proxy from the database."""
    with _lock, _conn:
        _conn.execute('DELETE FROM proxies WHERE ip=? AND port=?', (ip, port))

