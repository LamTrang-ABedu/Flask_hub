import requests
import os
from functools import lru_cache

R2_PUBLIC_BASE = "https://r2.lam.io.vn/"

# Mapping nguồn tương ứng file trên R2
SOURCE_TO_FILE = {
    "xvideos": "MEDIA/xvideos_media.json",
    "redgifs": "MEDIA/redgifs_media.json",
    "pornhub": "MEDIA/pornhub_media.json",
    "reddit": "MEDIA/reddit_media.json",
    "bin": "BIN/bins_real_full.json"
}

# Internal cache (thay vì lru_cache decorator để dùng được force_reload)
_cached_media = {}

def fetch_media_from_r2(source, force_reload=False):
    source = source.lower()
    file_path = SOURCE_TO_FILE.get(source)
    if not file_path:
        print(f"[Error] Unknown source: {source}")
        return []

    if not force_reload and source in _cached_media:
        print(f"[Cache] Returning cached data for {source}")
        return _cached_media[source]

    try:
        url = f"{R2_PUBLIC_BASE}/{file_path}"
        print(f"[Info] Fetching {url} from R2...")
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()

        if isinstance(data, list):
            _cached_media[source] = data
            print(f"[Success] Fetched {len(data)} items from {source} on R2")
            return data
        else:
            print(f"[Warning] Unexpected data format from {source}, expected list.")
            return []

    except requests.RequestException as e:
        print(f"[Error] HTTP error while fetching {source}: {e}")
    except Exception as e:
        print(f"[Error] Failed to fetch or parse JSON for {source}: {e}")

    return []
