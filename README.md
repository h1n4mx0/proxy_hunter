# 🕵️ Proxy Hunter Dashboard

**Proxy Hunter Dashboard** là hệ thống tự động quét IP theo quốc gia, kiểm tra proxy hoạt động và hiển thị qua FastAPI.

## 🚀 Tính năng
- Tự động tải CIDR từ ipdeny.com
- Scan cổng phổ biến qua zmap (8080, 3128, 443)
- Kiểm tra proxy sống bằng HTTP(S) và lưu vào SQLite
- Tích hợp tra cứu GeoIP qua ip-api.com
- Giao diện dashboard trực quan
- Lập lịch kiểm tra lại proxy định kỳ

## 🗂 Cấu trúc thư mục
```
proxy_hunter/
├── crawler/             # Logic proxy
│   ├── checker.py
│   ├── crawler.py
│   ├── scheduler.py
│   ├── storage.py
│   └── geoip.py
├── server/              # FastAPI dashboard
│   └── server.py
├── data/                # CIDRs, proxy output, database
├── config.py            # Cấu hình
├── main.py              # Entry point
└── requirements.txt     # Thư viện
```

## ▶️ Hướng dẫn chạy
### 1. Cài đặt
```bash
pip install -r requirements.txt
sudo apt install zmap
```

### 2. Khởi chạy
```bash
python main.py
```
Dashboard truy cập tại: <http://localhost:8000>

## ⚙️ Tuỳ chỉnh
Trong `config.py`:
```python
PORTS = [8080, 3128, 443]
THREADS = 50
TEST_URL = 'https://httpbin.org/ip'
```
