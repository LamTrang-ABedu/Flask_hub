import requests
import os
import tempfile
import json
from utils.gdrive_uploader import upload_file_to_drive
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

                video_link = upload_media(video_url, title + '.mp4')
                thumb_link = upload_media(thumb_url, title + '.jpg')

                results.append({
                    'title': title,
                    'source': 'redgifs',
                    'thumb': thumb_link,
                    'video': video_link,
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

                thumb_link = upload_media(thumb, title + '.jpg')

                results.append({
                    'title': title,
                    'source': 'xvideos',
                    'thumb': thumb_link,
                    'video': video_page,
                    'type': 'page'
                })

    save_gallery_cache(source, results)

def upload_media(url, filename):
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            r = requests.get(url, stream=True)
            for chunk in r.iter_content(chunk_size=8192):
                tmp.write(chunk)
            tmp_path = tmp.name

        uploaded_link = upload_file_to_drive(tmp_path, filename)

        os.remove(tmp_path)
        return uploaded_link
    except Exception as e:
        print(f"[Error] Upload media failed: {e}")
        return ''

def save_gallery_cache(source, media_list):
    if not os.path.exists('static/cache'):
        os.makedirs('static/cache')

    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            cache = json.load(f)
    else:
        cache = {}

    cache[source] = media_list

    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)
    print(f"[Success] Saved {len(media_list)} media to cache for {source}")