import subprocess
import os

def crawl(gallery_url="https://www.imagefap.com/pictures/9145312/Asian-Girls", limit=30):
    print(f"[Imagefap Crawler] Start crawling gallery: {gallery_url}")
    output_dir = "gallerydl_imagefap"
    os.makedirs(output_dir, exist_ok=True)

    cmd = [
        "gallery-dl",
        gallery_url,
        "--range", f"1-{limit}",
        "--dest", output_dir,
        "--download-archive", os.path.join(output_dir, "archive.txt"),
        "--verbose"
    ]

    print(f"[Imagefap Crawler] Running command: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"[gallery-dl stdout]\n{result.stdout}")
        print(f"[gallery-dl stderr]\n{result.stderr}")
        if result.returncode != 0:
            print(f"[Imagefap Crawler] gallery-dl exited with code {result.returncode}")
            return []
    except Exception as e:
        print(f"[Imagefap Crawler] Exception: {e}")
        return []

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

    print(f"[Imagefap Crawler] Found {len(results)} media files")
    return results