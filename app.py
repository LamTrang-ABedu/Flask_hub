import json
import os
import requests
from flask import Flask, render_template, request, jsonify, Response
from utils.profile_faker import generate_profile
from utils.gallery_fetcher import fetch_media
from utils.media_downloader import download_from_url
from utils.fallback_proxy import generate_profile_proxy, api_media_download, api_telegram_download
from utils.account_fetcher import fetch_accounts
# --- thêm mới ---
from utils.proxy_fetcher import load_proxies
from utils.keepalive_bot import start_keepalive_bot
from utils.r2_fetcher import fetch_media_from_r2
from utils.crawler_x import crawl
from urllib.parse import unquote, urlparse

start_keepalive_bot()

app = Flask(__name__)

@app.route('/')
def profile_faker_page():
    return render_template('profile_faker.html')

@app.route('/api/profile')
def api_profile():
    locale = request.args.get('locale', 'en_US')
    # profile_data = jsonify(generate_profile(locale))
    profile_data = generate_profile_proxy({'locale': locale})
    return jsonify(profile_data)

@app.route('/media')
def media_gallery_page():
    return render_template('media_gallery.html')

@app.route('/api/media')
def api_media():
    source = request.args.get('source', '').strip().lower()
    if not source:
        return jsonify({'status': 'error', 'message': 'Missing source'}), 400

    try:
        media = fetch_media_from_r2(source)
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Internal error: {str(e)}'}), 500

    if not isinstance(media, list):
        return jsonify({'status': 'error', 'message': 'Unexpected data format'}), 500

    return jsonify({'status': 'ok', 'results': media})

@app.route('/universal-downloader')
def universal_downloader_page():
    return render_template('media_downloader.html')

@app.route('/api/universal-download')
def api_universal_download():
    url = request.args.get('url', '')
    if not url:
        return jsonify({'status': 'error', 'message': 'Missing URL'}), 400
    return jsonify(api_media_download(url))

@app.route('/telegram')
def telegram_gallery_page():
    return render_template('telegram_gallery.html')

@app.route('/api/ig-gallery')
def api_instagram_gallery():
    username = request.args.get("username", "").strip()
    if not username:
        return jsonify({"status": "error", "message": "Missing username"}), 400

    print(f"[Instagram Crawler] Crawling user: {username}")
    media = crawl(username=username)
    if not media:
        return jsonify({"status": "error", "message": "No media found"}), 404

    return jsonify({"status": "ok", "results": media})
    
    
@app.route('/binlist')
def binlist_page():
    return render_template('binlist_view.html')

@app.route('/api/binlist')
def api_binlist():
    try:
        bins = fetch_media_from_r2("bin")
        print(f"[Success] Fetched {len(bins)} BINs from R2")
        if not bins:
            return jsonify({'status': 'error', 'message': 'No media found'}), 404
        return jsonify({'status': 'ok', 'bins': bins})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    
# Route account fetcher page
@app.route('/account-fetcher')
def account_fetcher_page():
    return render_template('account_fetcher.html')

# API trả danh sách account
@app.route('/api/account-fetcher')
def api_account_fetcher():
    try:
        accounts = fetch_accounts()
        return jsonify({'status': 'ok', 'accounts': accounts})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    
@app.route('/proxy')
def proxy_fetcher_page():
    return render_template('proxy_fetcher.html')

@app.route('/api/proxies')
def api_proxies():
    proxies = load_proxies()
    return jsonify({'proxies': proxies})

@app.route("/tranh18")
def tranh18():
    return render_template("tranh18.html")

@app.route("/proxy-image")
def proxy_image():
    raw_url = request.args.get("url")
    if not raw_url:
        return "Missing URL", 400

    try:
        url = unquote(raw_url)
        
        if "tranh18" in url:
            headers = {"Referer": "https://tranh18x.com"}
            r = requests.get(url, headers=headers, stream=True, timeout=10)
    
            return Response(r.content, content_type=r.headers.get("Content-Type", "image/jpeg"))
        parsed = urlparse(url)
        domain = parsed.netloc

        # Chỉ cho phép proxy ảnh từ các domain hợp lệ
        allowed_domains = {
            "tranh18.com": "https://tranh18.com",
            "cdn600.tranh18.com": "https://tranh18.com",
            "manhwa18.net": "https://manhwa18.net",
            "static.manhwa18.net": "https://manhwa18.net",
        }
        
        referer = allowed_domains.get(domain)
        if not referer:
            return "Forbidden", 403

        headers = {
            "Referer": referer,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        r = requests.get(url, headers=headers, stream=True, timeout=10)
        return Response(r.content, content_type=r.headers.get("Content-Type", "image/jpeg"))

    except Exception as e:
        return f"Error: {e}", 500

@app.route("/api/proxy")
def proxy():
    real_url = request.args.get("real_url")
    if not real_url:
        return "Missing URL", 400

    headers = {
        'User-Agent': request.headers.get("User-Agent"),
        'Referer': request.args.get("referer") or 'https://www.pornhub.com',
    }

    # Chuyển tiếp cả header Range
    if "Range" in request.headers:
        headers["Range"] = request.headers["Range"]

    r = requests.get(real_url, headers=headers, stream=True)

    response = Response(r.iter_content(chunk_size=8192),
                        status=r.status_code,
                        content_type=r.headers.get("Content-Type"))

    # Bổ sung header hỗ trợ seek
    response.headers["Content-Range"] = r.headers.get("Content-Range")
    response.headers["Accept-Ranges"] = "bytes"
    response.headers["Content-Length"] = r.headers.get("Content-Length")

    return response

@app.route("/api/crawl-callback", methods=["POST"])
def crawl_callback():
    data = request.json
    print(f"[Callback] Crawl for {data.get('username')} DONE")
    # Ghi log / update DB / push notification frontend
    return {"status": "ok"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
