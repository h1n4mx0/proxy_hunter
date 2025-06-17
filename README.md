
# 🕵️‍♂️ Proxy Hunter

**Proxy Hunter** là một công cụ tự động giúp bạn:
1. Cào dải IP theo quốc gia từ ipdeny.com
2. Quét các cổng proxy phổ biến bằng `zmap`
3. Kiểm tra proxy nào hoạt động thực sự bằng HTTP request

> Ví dụ: tìm proxy HTTP từ các IP ở Anh (GB), đang mở port 443/8080/3128 và phản hồi tốt.

---

## ⚙️ Yêu cầu hệ thống

- Python 3.7+
- Hệ điều hành: **Linux / macOS** (Không hỗ trợ Windows native)
- Công cụ:
  - [`zmap`](https://github.com/zmap/zmap)
  - `curl`, `jq`, `masscan` (tùy chọn)
  - Python module: `requests`

---

## 🚀 Cài đặt

Chạy script tự động:

```bash
chmod +x install.sh
./install.sh
```

Script sẽ:
- Cài `zmap`, `masscan`, `curl`, `jq`, `python3`, `pip`
- Tạo virtualenv (`./venv`) và cài `requests` bên trong

Kích hoạt môi trường sau này:

```bash
source venv/bin/activate
```

---

## 🧠 Cách sử dụng

```bash
python3 proxy_hunter.py
```

Sau đó nhập mã quốc gia theo ISO Alpha-2 (vd: `gb`, `vn`, `us`, `de`, ...)

Quá trình sẽ:
1. Cào IP dải từ ipdeny.com
2. Quét port 8080, 3128, 443 bằng zmap
3. Gộp IP:PORT thành danh sách proxy
4. Kiểm tra từng proxy xem có phản hồi thật sự qua HTTP không

---

## 📁 Output

| File              | Mô tả                            |
|-------------------|----------------------------------|
| `proxy_candidates.txt` | IP:PORT từ zmap quét được       |
| `live.txt`        | Proxy hoạt động thật sự         |
| `die.txt`         | Proxy không phản hồi / lỗi kết nối |

---

## 📚 Tham khảo

- [https://www.ipdeny.com/ipblocks/](https://www.ipdeny.com/ipblocks/)
- [https://github.com/zmap/zmap](https://github.com/zmap/zmap)
- [httpbin.org/ip](https://httpbin.org/ip) – dùng làm endpoint test proxy

---

## 🛡️ Lưu ý bảo mật

- Chạy tool với quyền `sudo` nếu `zmap` yêu cầu raw socket
- Đảm bảo sử dụng IP hợp pháp và tuân thủ luật pháp quốc tế về quét mạng

---

## 📦 TODO / Phát triển tiếp

- [ ] Hỗ trợ SOCKS4/5
- [ ] Lọc proxy theo tốc độ / quốc gia thực tế (GeoIP)
- [ ] Giao diện Web quản lý proxy pool
- [ ] Crawler thêm từ public proxy lists

---

## 🧑‍💻 Tác giả

Proxy Hunter được phát triển bởi bạn để xây dựng proxy pool riêng, kết hợp `zmap`, `ipdeny`, `requests` và automation Python.
