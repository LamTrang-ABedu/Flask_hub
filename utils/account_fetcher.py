# utils/account_fetcher.py

import requests
import re
import json
import os
from datetime import datetime, timedelta

CACHE_FILE = 'cache/accounts.json'
CACHE_TIMEOUT = timedelta(hours=6)  # Tự động refresh sau mỗi 6h

def fetch_accounts(force_refresh=False):
    # Kiểm tra cache
    if not force_refresh and os.path.exists(CACHE_FILE):
        mtime = datetime.fromtimestamp(os.path.getmtime(CACHE_FILE))
        if datetime.now() - mtime < CACHE_TIMEOUT:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    
    # Crawl mới
    accounts = []
    
    try:
        # Ví dụ: crawl reddit page text
        url = "https://raw.githubusercontent.com/nhannt315/freecourses/main/README.md"
        res = requests.get(url, timeout=10)
        if res.ok:
            text = res.text
            matches = re.findall(r'(\S+@\S+\.\S+|\w+):(\S+)', text)
            for user, password in matches:
                accounts.append({
                    'username': user,
                    'password': password,
                    'source': 'GitHub FreeCourses',
                    'category': 'Education'
                })
    except Exception as e:
        print("Crawler error:", e)

    # Cache lại
    os.makedirs('cache', exist_ok=True)
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(accounts, f, ensure_ascii=False, indent=2)
    
    return accounts
