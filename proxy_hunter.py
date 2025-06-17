import os
import requests
import subprocess
from concurrent.futures import ThreadPoolExecutor
from time import sleep

# ==== CONFIG ====
PORTS = [8080, 3128, 443]
ZMAP_PATH = 'zmap'  # Ensure zmap is in PATH
THREADS = 50
TEST_URL = 'https://httpbin.org/ip'
TIMEOUT = 5

# ==== STEP 1: Fetch CIDRs ====
def fetch_cidrs(country_code):
    url = f"https://www.ipdeny.com/ipblocks/data/countries/{country_code.lower()}.zone"
    r = requests.get(url)
    r.raise_for_status()
    cidrs = r.text.strip().split('\n')
    cidr_file = f"{country_code}_cidrs.txt"
    with open(cidr_file, 'w') as f:
        f.write('\n'.join(cidrs))
    print(f"[+] Fetched {len(cidrs)} CIDRs into {cidr_file}")
    return cidr_file

# ==== STEP 2: ZMap Port Scan ====
def run_zmap(cidr_file, port):
    out_file = f"{cidr_file}_{port}.txt"
    cmd = [ZMAP_PATH, '-p', str(port), '-w', cidr_file, '-o', out_file, '-q']
    print(f"[*] Scanning port {port} with zmap...")
    subprocess.run(cmd, check=True)
    return out_file

# ==== STEP 3: Merge IP + Port ====
def merge_results(port_files, output='proxy_candidates.txt'):
    with open(output, 'w') as out:
        for port, file in port_files.items():
            with open(file) as f:
                for ip in f:
                    out.write(f"{ip.strip()}:{port}\n")
    print(f"[+] Merged into {output}")
    return output

# ==== STEP 4: Check Proxy ====
def check_proxy(proxy_line):
    proxy_line = proxy_line.strip()
    if not proxy_line:
        return
    proxies = {
        "http": f"http://{proxy_line}",
        "https": f"http://{proxy_line}",
    }
    try:
        r = requests.get(TEST_URL, proxies=proxies, timeout=TIMEOUT)
        if r.status_code == 200:
            print(f"[LIVE] {proxy_line}")
            with open('live.txt', 'a') as f:
                f.write(proxy_line + '\n')
            return
    except:
        pass
    print(f"[DIE] {proxy_line}")
    with open('die.txt', 'a') as f:
        f.write(proxy_line + '\n')

def check_proxies(proxy_file):
    with open(proxy_file, 'r') as f:
        proxies = f.read().splitlines()

    open('live.txt', 'w').close()
    open('die.txt', 'w').close()

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        executor.map(check_proxy, proxies)

# ==== MAIN ====
def main():
    country = input("🌍 Enter country code (e.g., gb, vn, us): ").strip().lower()
    cidr_file = fetch_cidrs(country)

    port_outputs = {}
    for port in PORTS:
        out = run_zmap(cidr_file, port)
        port_outputs[port] = out
        sleep(0.5)  # tránh overload máy

    merged = merge_results(port_outputs)
    check_proxies(merged)
    print("\n✅ Done. Check live.txt and die.txt for results.")

if __name__ == '__main__':
    main()
