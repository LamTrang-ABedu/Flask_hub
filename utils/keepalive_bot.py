# keepalive_bot.py

import time
import threading
import requests

# 🌟 List các URL server cần ping giữ sống (bạn thêm bao nhiêu tuì ý)
TARGET_URLS = [
    "https://profile-faker-service.onrender.com/api/profile",
    "https://09ef5a9c-b639-48b8-9bb1-d120097aef06-00-2ub7tkprj1vdf.sisko.replit.dev/api/profile",
    "https://bin-fetcher-service.onrender.com/api/binlist",
    "https://2a850f82-d954-4117-9138-a237f6a53c53-00-2ujm3k5bp3tna.sisko.replit.dev/api/binlist"
]

# 🔍 Khoảng thời gian ping (s giây) — mỗi 5 phút = 300s
PING_INTERVAL = 300
def ping_service(url):
    try:
        requests.get(url, timeout=PING_INTERVAL)
    except Exception:
        pass  # im lặng, vì chỉ cần ping

def background_keepalive():
    while True:
        for url in TARGET_URLS:
            ping_service(url)
        time.sleep(600)  # cứ mỗi 10 phút ping 1 vòng

def start_keepalive_bot():
    threading.Thread(target=background_keepalive, daemon=True).start()