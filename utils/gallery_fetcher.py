import requests
from bs4 import BeautifulSoup

REDDGIFS_TOKEN = None

def get_redgifs_token():
    global REDDGIFS_TOKEN
    if REDDGIFS_TOKEN:
        return REDDGIFS_TOKEN
    res = requests.post("https://api.redgifs.com/v2/auth/temporary")
    if res.ok:
        REDDGIFS_TOKEN = res.json()["access_token"]
    return REDDGIFS_TOKEN


def fetch_gallery(source, limit=20):
    if source == 'xvideos':
        return fetch_xvideos(limit)
    elif source == 'redgifs':
        return fetch_redgifs(limit)
    else:
        return {'status': 'error', 'message': 'Invalid source'}


def fetch_xvideos(limit):
    url = "https://www.xvideos.com/?k=popular"
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://www.xvideos.com/'
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    cards = soup.select('div.thumb-block')[:limit]
    results = []

    for card in cards:
        a = card.find('a', href=True)
        img = card.find('img')

        if not a or not img:
            continue

        href = a['href']
        video_link = 'https://www.xvideos.com' + href
        thumb = img.get('data-src') or img.get('src')
        title = a.get('title', '').strip() or img.get('alt', 'Xvideos')

        results.append({'video': video_link, 'thumb': thumb, 'title': title})

    return {'status': 'ok', 'results': results}


def fetch_redgifs(limit):
    token = get_redgifs_token()
    if not token:
        return {'status': 'error', 'message': 'Cannot get RedGifs token'}

    headers = {'Authorization': f'Bearer {token}'}
    api = f"https://api.redgifs.com/v2/gifs/search?search=popular&count={limit}"
    r = requests.get(api, headers=headers)

    if not r.ok:
        return {'status': 'error', 'message': 'Failed to fetch RedGifs'}

    data = r.json().get('gifs', [])
    results = []

    for item in data:
        urls = item.get('urls', {})
        results.append({
            'video': urls.get('hd', ''),
            'thumb': urls.get('thumbnail', urls.get('poster', '')),
            'title': item.get('title', 'RedGif')
        })

    return {'status': 'ok', 'results': results}


def fetch_media(keyword: str):
    # Tạm thời mặc định trả về redgifs nếu có từ "gif", còn lại là xvideos
    source = 'redgifs' if 'gif' in keyword.lower() else 'xvideos'
    return fetch_gallery(source)
