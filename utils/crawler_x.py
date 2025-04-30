import subprocess
import requests
import tempfile
import os

def crawl(username="femalemodels", limit=30):
    print(f"[Instagram Crawler] Crawling user: {username}")
    output_dir = f"gallerydl_ig_{username}"
    os.makedirs(output_dir, exist_ok=True)

    # Tải cookies từ R2
    cookies_url = "https://r2.lam.io.vn/cookies/instagram_cookies.txt"
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_cookie:
        res = requests.get(cookies_url, timeout=10)
        res.raise_for_status()
        tmp_cookie.write(res.content)
        cookie_path = tmp_cookie.name

    # Gọi gallery-dl
    cmd = [
        "gallery-dl",
        f"https://www.instagram.com/{username}/",
        "--cookies", cookie_path,
        "--range", f"1-{limit}",
        "--dest", output_dir,
        "--download-archive", os.path.join(output_dir, "archive.txt"),
        "--quiet"
    ]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[Instagram Crawler] Gallery-dl failed: {e}")
        return []

    # Kết quả dạng HopeHub
    results = []
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".mp4")):
                file_path = os.path.join(root, file)
                results.append({
                    "thumb": file_path,
                    "video": file_path if file.lower().endswith(".mp4") else None,
                    "title": file
                })

    return results