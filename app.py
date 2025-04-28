import json
import os
import threading
from flask import Flask, render_template, request, jsonify
from utils.profile_faker import generate_profile
from utils.gallery_fetcher import fetch_media
from utils.media_downloader import download_from_url
from utils.telethon_helper import fetch_telegram_media
from utils.profile_proxy import generate_profile_proxy
from utils.bin_fetcher import generate_bin_cache
from utils.account_fetcher import fetch_accounts
# --- thêm mới ---
from utils.proxy_fetcher import background_worker
from utils.keepalive_bot import start_keepalive_bot
from utils.media_crawler import crawl_and_upload

start_keepalive_bot()

app = Flask(__name__)

# Start proxy fetcher bot in background
threading.Thread(target=background_worker, daemon=True).start()

@app.route('/')
def profile_faker_page():
    return render_template('profile_faker.html')

@app.route('/api/profile')
def api_profile():
    locale = request.args.get('locale', 'en_US')
    # profile_data = generate_profile_proxy({'locale': locale})
    return jsonify(generate_profile(locale))
    # return jsonify(profile_data)

@app.route('/media')
def media_gallery_page():
    return render_template('media_gallery.html')

@app.route('/api/media')
def api_media():
    keyword = request.args.get('keyword', '')
    if not keyword:
        return jsonify({'status': 'error', 'message': 'Missing keyword'}), 400
    return jsonify(fetch_media(keyword))

@app.route('/universal-downloader')
def universal_downloader_page():
    return render_template('media_downloader.html')

@app.route('/api/universal-download')
def api_universal_download():
    url = request.args.get('url', '')
    if not url:
        return jsonify({'status': 'error', 'message': 'Missing URL'}), 400
    return jsonify(download_from_url(url))

@app.route('/telegram')
def telegram_gallery_page():
    return render_template('telegram_gallery.html')

@app.route('/api/telegram-media')
def api_telegram_media():
    group = request.args.get('group', '').strip()
    if not group:
        return jsonify({'status': 'error', 'message': 'Missing group'})
    try:
        media = fetch_telegram_media(group)
        return jsonify({'status': 'ok', 'media': media})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    
@app.route('/binlist')
def binlist_page():
    return render_template('binlist_view.html')

@app.route('/api/binlist')
def api_binlist():
    try:
        with open('static/cache/bins_cache.json', 'r', encoding='utf-8') as f:
            bins = json.load(f)
        return jsonify({'status': 'ok', 'bins': bins})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/refresh-bin')
def api_refresh_bin():
    try:
        generate_bin_cache()
        return jsonify({'status': 'ok', 'message': 'BIN cache refreshed successfully!'})
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
def proxy_fetcher():
    return render_template('proxy_fetcher.html')

@app.route('/api/proxylist')
def api_proxylist():
    proxy_type = request.args.get('type', '').lower()
    country = request.args.get('country', '').upper()
    try:
        with open('static/cache/proxy_cache.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        results = data
        if proxy_type:
            results = [p for p in results if p['type'].lower() == proxy_type]
        if country:
            results = [p for p in results if p['country'].upper() == country]
        return jsonify({'status': 'ok', 'results': results})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
