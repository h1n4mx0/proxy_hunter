import os
import subprocess
import requests
from time import sleep
from config import PORTS, ZMAP_PATH


def fetch_cidrs(country_code: str) -> str:
    url = f"https://www.ipdeny.com/ipblocks/data/countries/{country_code.lower()}.zone"
    r = requests.get(url)
    r.raise_for_status()
    cidrs = r.text.strip().split('\n')
    path = f"data/{country_code}_cidrs.txt"
    with open(path, 'w') as f:
        f.write('\n'.join(cidrs))
    return path


def run_zmap(cidr_file: str, port: int) -> str:
    out_file = f"data/{os.path.basename(cidr_file)}_{port}.txt"
    cmd = ['sudo', ZMAP_PATH, '-p', str(port), '-w', cidr_file, '-o', out_file, '-q']
    subprocess.run(cmd, check=True)
    return out_file


def merge_results(port_files: dict, output: str = 'data/proxy_candidates.txt') -> str:
    with open(output, 'w') as out:
        for port, file in port_files.items():
            with open(file) as f:
                for ip in f:
                    out.write(f"{ip.strip()}:{port}\n")
    return output


def scan_all_ports(country_code: str):
    os.makedirs('data', exist_ok=True)
    cidr_file = fetch_cidrs(country_code)
    port_outputs = {}
    for port in PORTS:
        out = run_zmap(cidr_file, port)
        port_outputs[port] = out
        sleep(0.5)
    merge_results(port_outputs)

