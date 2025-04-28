# Proxy Fetcher V2.5 Full Source

import requests
import json
import random
import time
import threading

PROFILE_FAKER_URLS = [
    "https://profile-faker-service.onrender.com/api/profile",
    "https://09ef5a9c-b639-48b8-9bb1-d120097aef06-00-2ub7tkprj1vdf.sisko.replit.dev/api/profile"
]

BIN_FETCHER_URLS = [
    "https://bin-fetcher-service.onrender.com/api/binlist",
    "https://2a850f82-d954-4117-9138-a237f6a53c53-00-2ujm3k5bp3tna.sisko.replit.dev/api/binlist"
]

TRIAL_SOURCES = [
    {"service": "Geonode", "trial_url": "https://geonode.com/free-trial", "auto_signup": True},
    {"service": "PacketStream", "trial_url": "https://packetstream.io/#buy", "auto_signup": True},
    {"service": "Oxylabs", "trial_url": "https://oxylabs.io/", "auto_signup": False},
    {"service": "SmartProxy", "trial_url": "https://smartproxy.com", "auto_signup": False},
    {"service": "BrightData", "trial_url": "https://brightdata.com", "auto_signup": False},
    {"service": "ProxyMesh", "trial_url": "https://proxymesh.com", "auto_signup": False},
    {"service": "StormProxies", "trial_url": "https://stormproxies.com", "auto_signup": False},
    {"service": "NetNut.io", "trial_url": "https://netnut.io", "auto_signup": False},
    {"service": "ProxyRack", "trial_url": "https://proxyrack.com", "auto_signup": False},
    {"service": "VPN Unlimited", "trial_url": "https://www.vpnunlimitedapp.com/", "auto_signup": False},
    {"service": "NordVPN", "trial_url": "https://nordvpn.com", "auto_signup": False},
    {"service": "ExpressVPN", "trial_url": "https://expressvpn.com", "auto_signup": False},
    {"service": "Surfshark", "trial_url": "https://surfshark.com", "auto_signup": False},
    {"service": "VeePN", "trial_url": "https://veepn.com", "auto_signup": False},
    {"service": "TorGuard", "trial_url": "https://torguard.net", "auto_signup": False},
    {"service": "Hide.me VPN", "trial_url": "https://hide.me", "auto_signup": False},
    {"service": "PrivadoVPN", "trial_url": "https://privadovpn.com", "auto_signup": False}
    # ... và còn nhiều dịch vụ khác trong danh sách
]

PROXY_CACHE_FILE = "proxy_cache.json"
ALIVE_CACHE_FILE = "proxy_alive.json"

# Fetch fake profile
def fetch_profile():
    for url in PROFILE_FAKER_URLS:
        try:
            res = requests.get(url, timeout=10)
            if res.ok:
                return res.json()
        except:
            continue
    raise Exception("All Profile Faker servers unreachable")

# Fetch BIN list
def fetch_bin():
    for url in BIN_FETCHER_URLS:
        try:
            res = requests.get(url, timeout=10)
            if res.ok:
                bins = res.json().get('bins', [])  # <- Phải get 'bins' chứ không phải 'results'
                if not bins:
                    raise Exception("BIN list empty")
                return random.choice(bins)
        except Exception as e:
            print(f"[Warning] BIN server {url} failed: {e}")
            continue
    raise Exception("All BIN servers unreachable")


# Simulate signup function
def signup_trial(service):
    profile = fetch_profile()
    bin_card = fetch_bin()
    proxy_info = {
        "ip": f"{random.randint(10,250)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
        "port": random.randint(1000,9999),
        "user": profile['email'],
        "pass": bin_card['bin'],
        "provider": service['service'],
        "expire": time.strftime('%Y-%m-%d', time.localtime(time.time() + 3*24*3600))
    }
    return proxy_info

# Save proxy cache
def save_cache(data):
    with open(PROXY_CACHE_FILE, "w") as f:
        print(f"[Info] Saving {len(data)} proxies to cache...")
        json.dump(data, f, indent=2)

# Load proxy cache
def load_cache():
    try:
        with open(PROXY_CACHE_FILE) as f:
            return json.load(f)
    except:
        return []

# Check proxy alive
def check_proxy(proxy):
    try:
        proxies = {
            "http": f"http://{proxy['ip']}:{proxy['port']}",
            "https": f"http://{proxy['ip']}:{proxy['port']}"
        }
        res = requests.get("https://api.ipify.org", proxies=proxies, timeout=5)
        return res.ok
    except:
        return False

# Main refresh logic
def refresh_proxy():
    cache = load_cache()
    alive = []
    for proxy in cache:
        if check_proxy(proxy):
            alive.append(proxy)
    with open(ALIVE_CACHE_FILE, "w") as f:
        json.dump(alive, f, indent=2)
    print(f"[Info] Alive proxies: {len(alive)}")
    if len(alive) < 20:
        print("[Warning] Proxy low! Auto sign up...")
        for _ in range(30 - len(alive)):
            service = random.choice([s for s in TRIAL_SOURCES if s['auto_signup']])
            new_proxy = signup_trial(service)
            print(f"[Info] New proxy: {new_proxy}")
            alive.append(new_proxy)
        save_cache(alive)

# Background worker
def background_worker():
    while True:
        refresh_proxy()
        time.sleep(3600)

if __name__ == "__main__":
    t = threading.Thread(target=background_worker)
    t.daemon = True
    t.start()
    print("[System] Proxy Fetcher V2.5 running...")
    while True:
        time.sleep(3600)
