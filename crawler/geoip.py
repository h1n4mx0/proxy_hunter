import requests

def get_country(ip: str) -> str:
    """Return ISO country code for given IP using ip-api.com."""
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = r.json()
        if data.get("status") == "success":
            return data.get("countryCode", "N/A")
    except Exception:
        pass
    return "N/A"
