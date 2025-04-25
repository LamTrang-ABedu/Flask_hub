import requests
from bs4 import BeautifulSoup

def fetch_gallery(source, limit=20):
    if source == 'xvideos':
        return fetch_xvideos(limit)
    elif source == 'redgifs':
        return fetch_redgifs(limit)
    else:
        return {'status': 'error', 'message': 'Invalid source'}

def fetch_xvideos(limit):
    url = "https://www.xvideos.com/?k=popular"
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    cards = soup.select('div.thumb-inside')[:limit]

    results = []
    for card in cards:
        a = card.find_parent('a')
        href = a['href']
        video_link = 'https://www.xvideos.com' + href
        thumb = a.find('img')['data-src'] if a.find('img') else ''
        title = a.get('title', '').strip()
        results.append({'video': video_link, 'thumb': thumb, 'title': title})
    return {'status': 'ok', 'results': results}

def fetch_redgifs(limit):
    api = f"https://api.redgifs.com/v2/gifs/search?search=popular&count={limit}"
    r = requests.get(api)
    if not r.ok:
        return {'status': 'error', 'message': 'Failed to fetch RedGifs'}
    data = r.json().get('gifs', [])
    results = []
    for item in data:
        results.append({
            'video': item['urls']['hd'],
            'thumb': item['urls']['poster'],
            'title': item.get('title', 'RedGif')
        })
    return {'status': 'ok', 'results': results}
# Thêm vào cuối file gallery_fetcher.py

def fetch_media(keyword: str):
    # Tạm thời mặc định trả về redgifs nếu có từ "gif", còn lại là xvideos
    source = 'redgifs' if 'gif' in keyword.lower() else 'xvideos'
    return fetch_gallery(source)
