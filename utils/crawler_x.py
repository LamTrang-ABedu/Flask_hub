import subprocess
import requests
import tempfile
import os

def crawl(username="femalemodels", limit=30):
    print(f"[Instagram Crawler] Start crawling user: {username}")
    output_dir = f"gallerydl_ig_{username}"
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Load cookies from R2
    try:
        cookies_url = "https://r2.lam.io.vn/cookies/instagram_cookies.txt"
        print(f"[Instagram Crawler] Downloading cookies from {cookies_url}")
        res = requests.get(cookies_url, timeout=10)
        res.raise_for_status()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w') as tmp_cookie:
            tmp_cookie.write(res.text)
            cookie_path = tmp_cookie.name
        print(f"[Instagram Crawler] Saved cookies to: {cookie_path}")
    except Exception as e:
        print(f"[Instagram Crawler] Failed to load cookies: {e}")
        return []

    # Step 2: Build gallery-dl command
    cmd = [
        "gallery-dl",
        f"https://www.instagram.com/{username}/",
        "--cookies", cookie_path,
        "--range", f"1-{limit}",
        "--dest", output_dir,
        "--download-archive", os.path.join(output_dir, "archive.txt"),
        "--verbose"
    ]
    print(f"[Instagram Crawler] Running command: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"[gallery-dl stdout]\n{result.stdout}")
        print(f"[gallery-dl stderr]\n{result.stderr}")
        if result.returncode != 0:
            print(f"[Instagram Crawler] gallery-dl failed with exit code {result.returncode}")
            return []
    except Exception as e:
        print(f"[Instagram Crawler] Exception during gallery-dl call: {e}")
        return []

    # Step 3: Collect media files
    print(f"[Instagram Crawler] Checking output dir: {output_dir}")
    results = []
    file_count = 0
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".mp4")):
                file_path = os.path.join(root, file)
                results.append({
                    "thumb": file_path,
                    "video": file_path if file.lower().endswith(".mp4") else None,
                    "title": file
                })
                file_count += 1
    print(f"[Instagram Crawler] Found {file_count} media file(s)")

    return results