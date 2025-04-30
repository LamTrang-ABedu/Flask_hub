import requests
import os
import tempfile
import json
from bs4 import BeautifulSoup

CACHE_FILE = 'static/cache/gallery_cache.json'

def crawl_and_upload(source):
    print(f"[Crawler] Fetching media from {source}...")
    results = []

    if source == 'redgifs':
        api = "https://api.redgifs.com/v2/gifs/search?search=popular&count=10"
        r = requests.get(api)
        if r.ok:
            data = r.json().get('gifs', [])
            for item in data:
                video_url = item['urls']['hd']
                thumb_url = item['urls']['poster']
                title = item.get('title', 'RedGif')

                results.append({
                    'title': title,
                    'source': 'redgifs',
                    'type': 'video'
                })

    elif source == 'xvideos':
        url = "https://www.xvideos.com/?k=popular"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers)
        if r.ok:
            soup = BeautifulSoup(r.text, 'html.parser')
            cards = soup.select('div.thumb-inside')[:10]

            for card in cards:
                a_tag = card.find_parent('a')
                if not a_tag:
                    continue
                href = a_tag['href']
                video_page = 'https://www.xvideos.com' + href

                thumb = a_tag.find('img')['data-src'] if a_tag.find('img') else ''
                title = a_tag.get('title', 'Xvideos Video')

                results.append({
                    'title': title,
                    'source': 'xvideos',
                    'video': video_page,
                    'type': 'page'
                })

    save_gallery_cache(source, results)

def save_gallery_cache(source, media_list):
    print(f"[Success] Saving {len(media_list)} media to cache for {source}")
    if not os.path.exists('static/cache'):
        os.makedirs('static/cache')

    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            cache = json.load(f)
    else:
        cache = {}

    cache[source] = media_list
    print(f"[Success] Saved {len(media_list)} media to cache for {source}")

    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)
    print(f"[Success] Saved {len(media_list)} media to cache for {source}")

def fetch_media(keyword):
    try:
        if not os.path.exists(CACHE_FILE):
            return []
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            cache = json.load(f)
        
        # Lọc các media theo từ khóa (keyword như 'xvideos', 'redgifs')
        filtered = [item for item in cache if item.get('source', '').lower() == keyword.lower()]
        return filtered
    except Exception as e:
        print(f"[Error] Fetch media failed: {e}")
        return []