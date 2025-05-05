import requests

import socket

def is_localhost():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return ip.startswith("127.") or ip == "localhost"

IS_LOCAL = is_localhost()
PROFILE_SERVICES = [
    "https://profile-faker-service.onrender.com",
    "https://09ef5a9c-b639-48b8-9bb1-d120097aef06-00-2ub7tkprj1vdf.sisko.replit.dev"
    # "https://profile-faker-service-vercel.vercel.app/api/profile",
]

MEDIA_SERVERS = [
    "https://download.lam.io.vn",
    "https://media-downloader.up.railway.app",
    # "https://media-downloader.fly.dev"
]

TELEGRAM_SERVERS = [
    "https://telegram-downloader-qtyq.onrender.com",
    # "https://telegram-downloader-railway.app",
    # "https://telegram-downloader.fly.dev"
]

def generate_profile_proxy(locale="en_US"):
    for server in PROFILE_SERVICES:
        try:
            if IS_LOCAL:
                # Nếu đang chạy trên localhost, không cần kiểm tra SSL
                response = requests.get(f"{server}/api/profile", params=locale, timeout=5, verify=False)
            else:                # Kiểm tra SSL nếu không phải localhost
                response = requests.get(f"{server}/api/profile", params=locale, timeout=5)
             
            if response.status_code == 200:
                print(f"generate_profile_proxy: {locale}")
                data = response.json()
                if data:  # Nếu trả về JSON không rỗng
                    return data
        except Exception as e:
            print(f"[WARN] Failed to fetch from {server}: {e}")
            continue  # Thử server tiếp theo
    # Nếu không server nào trả lời được
    return {"status": "error", "message": "All servers are unreachable"}

def api_media_download(url = ""):
    for server in MEDIA_SERVERS:
        try:
            res = requests.get(f"{server}/api/media-download", params={"url": url}, timeout=6)
            if res.status_code == 200:
                return res.json()
        except Exception as e:
            print(f"[WARN] Failed to fetch from {server}: {e}")

def api_telegram_download(group = ""):
    for server in TELEGRAM_SERVERS:
        try:
            res = requests.get(f"{server}/api/telegram-download", params={"group": group}, timeout=6)
            if res.status_code == 200:
                return res.json()
        except Exception as e:
            print(f"[WARN] Failed to fetch from {server}: {e}")