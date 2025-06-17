import os
import geoip2.database

DB_FILE = os.getenv('GEOIP_DB', 'data/GeoLite2-Country.mmdb')
_reader = None


def init_reader():
    global _reader
    if os.path.exists(DB_FILE):
        _reader = geoip2.database.Reader(DB_FILE)


init_reader()


def get_country(ip: str) -> str:
    if not _reader:
        return 'N/A'
    try:
        resp = _reader.country(ip)
        return resp.country.iso_code or 'N/A'
    except Exception:
        return 'N/A'

