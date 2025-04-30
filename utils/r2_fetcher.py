import requests
import os

R2_PUBLIC_BASE = "https://r2.lam.io.vn/"

# Mapping nguồn tương ứng file trên R2
SOURCE_TO_FILE = {
    "xvideos": "MEDIA/xvideos_media.json",
    "redgifs": "MEDIA/redgifs_media.json",
    "pornhub": "MEDIA/pornhub_media.json",
    "bin": "BIN/bins_real_full.json"
}

def fetch_media_from_r2(source):
    try:
        file_path = SOURCE_TO_FILE.get(source.lower())
        if not file_path:
            return None
        url = f"{R2_PUBLIC_BASE}/{file_path}"
        print(f"[Info] Fetching {url} from R2...")
        res = requests.get(url, timeout=10)
        if res.ok:
            data = res.json()
            print(f"[Success] Fetched {len(data)} items from {source} on R2")
            return data
        else:
            print(f"[Error] Failed to fetch {url}: {res.status_code}")
            return None
    except Exception as e:
        print(f"[Error] Fetch R2 {source}: {e}")
        return None
