import requests
import threading
import json
import time
import os
from bs4 import BeautifulSoup

CACHE_FILE = 'static/cache/proxy_cache.json'
ALIVE_FILE = 'static/cache/proxy_alive.json'

# Các nguồn public proxy miễn phí
SOURCES = [
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
]

# Fetch proxies từ các nguồn
def fetch_proxies():
    proxies = set()
    for url in SOURCES:
        try:
            res = requests.get(url, timeout=10)
            if res.ok:
                lines = res.text.strip().splitlines()
                for line in lines:
                    if ':' in line:
                        proxies.add(line.strip())
        except Exception as e:
            print(f"[Warning] Failed fetching from {url}: {e}")
    return list(proxies)

# Kiểm tra proxy
def check_proxy(proxy):
    try:
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
        res = requests.get("https://api.ipify.org", proxies=proxies, timeout=5)
        return res.ok
    except:
        return False

# Crawl và kiểm tra proxy
def refresh_proxies():
    print("[Info] Fetching proxy list...")
    proxies = fetch_proxies()
    alive = []

    def worker(proxy):
        if check_proxy(proxy):
            print(f"[Alive] {proxy}")
            alive.append(proxy)

    threads = []
    for p in proxies:
        t = threading.Thread(target=worker, args=(p,))
        t.start()
        threads.append(t)
        time.sleep(0.01)  # tránh quá tải

    for t in threads:
        t.join()

    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(ALIVE_FILE, "w") as f:
        json.dump(alive, f, indent=2)
    print(f"[Success] {len(alive)} alive proxies saved.")

# Hàm load cho Flask App
def load_proxies():
    try:
        with open(ALIVE_FILE) as f:
            return json.load(f)
    except:
        return []

# Worker nền
def background_worker():
    while True:
        refresh_proxies()
        time.sleep(3600)  # 1h refresh lại

# Khởi động riêng nếu chạy trực tiếp
if __name__ == "__main__":
    refresh_proxies()
