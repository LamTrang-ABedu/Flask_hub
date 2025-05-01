import requests
from bs4 import BeautifulSoup

def crawl(username="realgirlsvids", limit=20):
    print(f"[XCancel Crawler] Crawling user: {username}")
    url = f"https://xcancel.com/{username}/media"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, headers=headers, timeout=15)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
    except Exception as e:
        print(f"[XCancel Crawler] Failed to fetch: {e}")
        return []

    results = []
    items = soup.select("div.attachment.image > a[href], div.attachment.video > a[href]")[:limit]

    for item in items:
        href = item.get("href")
        thumb = item.find("img")["src"] if item.find("img") else None

        if href:
            results.append({
                "thumb": thumb or href,
                "video": href if href.endswith((".mp4", ".webm")) else None,
                "title": "Media from XCancel"
            })

    print(f"[XCancel Crawler] Found {len(results)} media item(s).")
    return results