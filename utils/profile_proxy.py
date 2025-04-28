import requests
import os

import socket

def is_localhost():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return ip.startswith("127.") or ip == "localhost"

IS_LOCAL = is_localhost()
PROFILE_SERVICES = [
    "https://profile-faker-service.onrender.com/api/profile",
    "https://09ef5a9c-b639-48b8-9bb1-d120097aef06-00-2ub7tkprj1vdf.sisko.replit.dev/api/profile"
    # "https://profile-faker-service-vercel.vercel.app/api/profile",
]

BIN_SERVICES = [
    "https://bin-fetcher-service.onrender.com/api/binlist",
    "https://2a850f82-d954-4117-9138-a237f6a53c53-00-2ujm3k5bp3tna.sisko.replit.dev/api/binlist"
    # "https://profile-faker-service-vercel.vercel.app/api/profile",
]
def generate_profile_proxy(locale="en_US"):
    print(f"generate_profile_proxy: {locale}")
    for url in PROFILE_SERVICES:
        try:
            if IS_LOCAL:
                # Nếu đang chạy trên localhost, không cần kiểm tra SSL
                response = requests.get(url, params=locale, timeout=5, verify=False)
            else:                # Kiểm tra SSL nếu không phải localhost
                response = requests.get(url, params=locale, timeout=5)
             
            if response.status_code == 200:
                print(f"generate_profile_proxy: {locale}")
                data = response.json()
                if data:  # Nếu trả về JSON không rỗng
                    return data
        except Exception as e:
            print(f"[Warning] Server {url} failed: {e}")
            continue  # Thử server tiếp theo
    # Nếu không server nào trả lời được
    return {"status": "error", "message": "All servers are unreachable"}

def generate_bin_proxy():
    for url in BIN_SERVICES:
        try:
            if IS_LOCAL:
                # Nếu đang chạy trên localhost, không cần kiểm tra SSL
                response = requests.get(url, timeout=5, verify=False)
            else:                # Kiểm tra SSL nếu không phải localhost
                response = requests.get(url, timeout=5)
             
            if response.status_code == 200:
                data = response.json()
                if data:  # Nếu trả về JSON không rỗng
                    return data
        except Exception as e:
            print(f"[Warning] Server {url} failed: {e}")
            continue  # Thử server tiếp theo
    # Nếu không server nào trả lời được
    return {"status": "error", "message": "All servers are unreachable"}