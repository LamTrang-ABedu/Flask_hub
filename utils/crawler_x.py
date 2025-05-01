import subprocess
import tempfile
import os

def crawl(tag="blonde", limit=30):
    print(f"[Rule34 Crawler] Start crawling tag: {tag}")
    output_dir = f"gallerydl_rule34_{tag.replace(' ', '_')}"
    os.makedirs(output_dir, exist_ok=True)

    # Build gallery-dl command
    cmd = [
        "gallery-dl",
        f"https://rule34.xxx/index.php?page=post&s=list&tags={tag}",
        "--range", f"1-{limit}",
        "--dest", output_dir,
        "--download-archive", os.path.join(output_dir, "archive.txt"),
        "--verbose"
    ]
    print(f"[Rule34 Crawler] Running command: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"[gallery-dl stdout]\n{result.stdout}")
        print(f"[gallery-dl stderr]\n{result.stderr}")
        if result.returncode != 0:
            print(f"[Rule34 Crawler] gallery-dl exited with code {result.returncode}")
            return []
    except Exception as e:
        print(f"[Rule34 Crawler] Exception: {e}")
        return []

    # Read downloaded media
    print(f"[Rule34 Crawler] Reading files from {output_dir}")
    results = []
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webm", ".mp4")):
                file_path = os.path.join(root, file)
                results.append({
                    "thumb": file_path,
                    "video": file_path if file.lower().endswith((".mp4", ".webm")) else None,
                    "title": file
                })

    print(f"[Rule34 Crawler] Found {len(results)} media files")
    return results