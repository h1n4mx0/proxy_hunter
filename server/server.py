from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime
from crawler.storage import (
    get_all_proxies,
    add_proxy,
    delete_proxy,
)
import uvicorn

app = FastAPI()
# app.mount("/static", StaticFiles(directory="dashboard/static"), name="static")


@app.get("/api/proxies", response_class=JSONResponse)
def get_proxies():
    result = []
    for p in get_all_proxies():
        uptime_percent = round((p['live_checks'] / max(p['total_checks'], 1)) * 100)
        result.append({
            **p,
            "uptime": f"{uptime_percent}% ({p['total_checks']}x)",
            "last_check_human": humanize_time(p['last_checked'])
        })
    return result


@app.post("/api/proxies", response_class=JSONResponse)
async def add_proxy_api(item: dict):
    ip = item.get("ip")
    port = item.get("port")
    if not ip or port is None:
        raise HTTPException(status_code=400, detail="ip and port required")
    add_proxy(ip, int(port))
    return {"status": "ok"}


@app.delete("/api/proxies/{ip}/{port}", response_class=JSONResponse)
def delete_proxy_api(ip: str, port: int):
    delete_proxy(ip, port)
    return {"status": "deleted"}


@app.get("/", response_class=HTMLResponse)
def dashboard():
    return HTMLResponse(content="""
<!DOCTYPE html>
<html>
<head><meta charset='UTF-8'><title>Proxy Dashboard</title></head>
<body>
<h2>Proxy Dashboard</h2>
<form id="add-form">
  IP <input id="ip" required> Port <input id="port" type="number" required>
  <button type="submit">Add</button>
</form>
<table border="1" cellpadding="5">
<thead><tr><th>IP</th><th>Port</th><th>Last Check</th><th>Latency</th><th>Uptime</th><th>Country</th><th></th></tr></thead>
<tbody id="proxy-table"></tbody>
</table>
<script>
async function loadProxies() {
  const res = await fetch('/api/proxies');
  const data = await res.json();
  const table = document.getElementById('proxy-table');
  table.innerHTML = '';
  for (const p of data) {
    const row = `<tr>
      <td>${p.ip}</td><td>${p.port}</td><td>${p.last_check_human}</td>
      <td>${p.latency_ms} ms</td><td>${p.uptime}</td><td>${p.country}</td>
      <td><button onclick="deleteProxy('${p.ip}', ${p.port})">Del</button></td>
    </tr>`;
    table.innerHTML += row;
  }
}

async function deleteProxy(ip, port) {
  await fetch(`/api/proxies/${ip}/${port}`, {method: 'DELETE'});
  loadProxies();
}

document.getElementById('add-form').onsubmit = async (e) => {
  e.preventDefault();
  const ip = document.getElementById('ip').value;
  const port = document.getElementById('port').value;
  await fetch('/api/proxies', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ip, port})
  });
  document.getElementById('ip').value = '';
  document.getElementById('port').value = '';
  loadProxies();
};

loadProxies();
</script>
</body>
</html>
""")


def humanize_time(dt: datetime) -> str:
    delta = datetime.utcnow() - dt
    seconds = delta.total_seconds()
    if seconds < 60:
        return f"{int(seconds)}s ago"
    elif seconds < 3600:
        return f"{int(seconds // 60)}m ago"
    elif seconds < 86400:
        return f"{int(seconds // 3600)}h ago"
    return f"{int(seconds // 86400)}d ago"


def run_dashboard():
    uvicorn.run(app, host="0.0.0.0", port=8000)
