import requests
import os

R2_PUBLIC_BASE = "https://lam.io.vn/MEDIA/"

# Mapping nguồn tương ứng file trên R2
SOURCE_TO_FILE = {
    "xvideos": "Xvideos/xvideos_media.json",
    "redgifs": "Redgifs/redgifs_media.json",
    "pornhub": "Pornhub/pornhub_media.json"
}

def fetch_media_from_r2(source):
    try:
        file_path = SOURCE_TO_FILE.get(source.lower())
        if not file_path:
            return None
        url = f"{R2_PUBLIC_BASE}/{file_path}"
        res = requests.get(url, timeout=10)
        if res.ok:
            data = res.json()
            return data
        else:
            return None
    except Exception as e:
        print(f"[Error] Fetch R2 {source}: {e}")
        return None
