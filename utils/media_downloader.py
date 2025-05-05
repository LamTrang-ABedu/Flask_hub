from yt_dlp import YoutubeDL, DownloadError
import requests
import os
from urllib.parse import urlparse
import random # Thêm import random
# URL cookies từ R2
from .proxy_fetcher import load_proxies, refresh_proxies # Thêm import proxy loader

# URL cookies từ R2
COOKIE_URL_MAP = {
    "x.com": "https://r2.lam.io.vn/cookies/x_cookies.txt",
    "twitter.com": "https://r2.lam.io.vn/cookies/x_cookies.txt",
    "instagram.com": "https://r2.lam.io.vn/cookies/instagram_cookies.txt",
    "facebook.com": "https://r2.lam.io.vn/cookies/facebook_cookies.txt",
    "tiktok.com": "https://r2.lam.io.vn/cookies/tiktok_cookies.txt",
}
def download_from_url(url):
    # --- Cải thiện logic xử lý proxy cho YouTube ---
    refresh_proxies()
    active_proxies = load_proxies()
    proxies_to_try = [None] + random.sample(active_proxies, len(active_proxies)) # Thử không proxy trước, sau đó thử các proxy đã load (random thứ tự)
    try:
        domain = urlparse(url).netloc.replace("www.", "")
        cookiefile = None
        if domain in COOKIE_URL_MAP:
            print(f"Downloading cookies for {domain}...")
            cookiefile = f"/tmp/{domain.replace('.', '_')}_cookies.txt"

            # Tải cookie và xử lý lỗi
            if not _download_cookie_once(COOKIE_URL_MAP[domain], cookiefile):
                return {'status': 'error', 'message': f"Failed to download cookies for {domain}"}

        ydl_opts = {
            "quiet": True,
            "force_generic_extractor": False,
            "skip_download": True, # Đảm bảo chỉ lấy info, không tải file thực sự ở bước này
        }
        if domain == 'tiktok.com':
            ydl_opts.update({
                'cookiefile': cookiefile,
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...',
                    'Referer': 'https://www.tiktok.com/',
                    'Origin': 'https://www.tiktok.com',
                    'Accept-Language': 'en-US,en;q=0.9'
                }
            })

        elif domain == 'youtube.com':
            # Chỉ cần đặt User-Agent, proxy sẽ được xử lý trong vòng lặp thử lại
            ydl_opts.update({
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                },
                # 'force_ipv6': True, # Tùy chọn: Thử bật nếu server có IPv6
            })

        elif domain == 'x.com' or domain == 'twitter.com' or domain == 'instagram.com' or domain == 'facebook.com':
            ydl_opts['cookiefile'] = cookiefile

        # --- Vòng lặp thử lại với các proxy (hoặc không proxy) ---
        last_error = None
        for proxy in proxies_to_try if domain == 'youtube.com' else [None]: # Chỉ áp dụng retry proxy cho YouTube
            current_opts = ydl_opts.copy() # Tạo bản sao để không ảnh hưởng lần lặp sau
            if proxy:
                print(f"Attempting YouTube download with proxy: {proxy}")
                current_opts['proxy'] = f"http://{proxy}" # yt-dlp cần schema http://
            else:
                print("Attempting YouTube download directly (no proxy)")

            try:
                with YoutubeDL(current_opts) as ydl:
                    print(f"Attempting to extract info for: {url} with options: {current_opts}") # Thêm log
                    info = ydl.extract_info(url, download=False)
                    if not info:
                            # Nếu không có info nhưng không có lỗi, coi như lỗi không rõ
                        raise DownloadError("Failed to extract media info (no data returned)")

                    # --- Xử lý kết quả thành công ---
                    media_list = []
                    if 'entries' in info:
                        for entry in info['entries']:
                            media_list.append(_extract_item(entry))
                    else:
                        media_list.append(_extract_item(info))
                    return {'status': 'ok', 'media': media_list} # Thành công -> thoát khỏi hàm
            except DownloadError as e:
                last_error = e # Lưu lỗi cuối cùng gặp phải
                err_msg = str(e)
                print(f"[Downloader Attempt Failed] Proxy: {proxy}, Error: {err_msg}")
                if "HTTP Error 429" in err_msg:
                    print("Rate limited (429), trying next proxy...")
                    continue # Lỗi 429 -> thử proxy tiếp theo
                elif domain != 'youtube.com': # Nếu không phải YouTube, lỗi là lỗi cuối cùng
                    break
                # Các lỗi khác với YouTube cũng thử proxy tiếp theo (ví dụ timeout)
                continue
            except Exception as e: # Các lỗi không phải DownloadError
                last_error = e
                print(f"[Downloader Attempt Failed] Proxy: {proxy}, Unexpected Error: {type(e).__name__} - {e}")
                if domain != 'youtube.com': # Nếu không phải YouTube, lỗi là lỗi cuối cùng
                    break
                continue # Thử proxy tiếp theo

        # Nếu vòng lặp kết thúc mà không thành công
        print(f"[Downloader Error] All attempts failed for {url}. Last error: {last_error}")
        error_message = str(last_error) if last_error else "Unknown error after trying all proxies."
        if isinstance(last_error, DownloadError) and "HTTP Error 429" in error_message:
                return {'status': 'error', 'message': 'Rate limited by YouTube (HTTP 429) even after trying proxies.'}
        return {'status': 'error', 'message': f"Failed after trying proxies: {error_message}"}
    except Exception as e:
        # Các lỗi xảy ra bên ngoài vòng lặp thử proxy (ví dụ lỗi tải cookie)
        print(f"[Downloader Error] Failed to process {url}: {type(e).__name__} - {e}") # Log lỗi chi tiết hơn
        return {'status': 'error', 'message': str(e)}

def _download_cookie_once(remote_url, local_path):
    try:
        if not os.path.exists(local_path):
            resp = requests.get(remote_url)
            if resp.ok:
                with open(local_path, 'w', encoding='utf-8') as f:
                    f.write(resp.text)
                return True
            else:
                print(f"Failed to download cookies from {remote_url}: {resp.status_code}")
                return False
        return True
    except Exception as e:
        print(f"Error downloading cookies: {str(e)}")
        return False

def _extract_item(info):
    source_url = info.get('webpage_url', '')
    ext = info.get('ext')
    url = info.get('url')

    # ✅ Fallback: nếu url bị null thì lấy từ formats
    if not url and 'formats' in info:
        formats = [f for f in info['formats'] if f.get('url')]
        if formats:
            best = formats[-1]
            url = best.get('url')
            ext = best.get('ext', ext)

    # 🐦 Twitter/X
    if 'x.com' in source_url or 'twitter.com' in source_url:
        best_format = None
        if 'formats' in info:
            formats = [f for f in info['formats'] if f.get('ext') == 'mp4' and f.get('url')]
            best_format = formats[-1] if formats else None

        return {
            'title': info.get('title'),
            'url': best_format.get('url') if best_format else url,
            'thumbnail': info.get('thumbnail'),
            'ext': best_format.get('ext') if best_format else ext,
            'webpage_url': source_url
        }

    # 📸 Instagram
    elif 'instagram.com' in source_url:
        # Nếu là ảnh
        if url and url.endswith(('.jpg', '.jpeg', '.png')):
            return {
                'title': info.get('title') or 'Instagram Image',
                'url': url,
                'thumbnail': url,
                'ext': 'jpg',
                'webpage_url': source_url
            }
        # Nếu là video
        elif ext == 'mp4':
            return {
                'title': info.get('title') or 'Instagram Video',
                'url': url,
                'thumbnail': info.get('thumbnail'),
                'ext': 'mp4',
                'webpage_url': source_url
            }

    # 🌐 Mặc định (Facebook, TikTok, YouTube...)
    return {
        'title': info.get('title'),
        'url': url,
        'thumbnail': info.get('thumbnail'),
        'ext': ext,
        'webpage_url': source_url
    }
