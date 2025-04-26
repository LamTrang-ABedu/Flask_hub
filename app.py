from flask import Flask, render_template, request, jsonify
from utils.profile_faker import generate_profile
from utils.gallery_fetcher import fetch_media
from utils.media_downloader import download_from_url
from utils.telethon_helper import fetch_telegram_media
from utils.profile_proxy import generate_profile_proxy
app = Flask(__name__)

@app.route('/')
def profile_faker_page():
    return render_template('profile_faker.html')

@app.route('/api/profile')
def api_profile():
    locale = request.args.get('locale', 'en_US')
    profile_data = generate_profile_proxy({'locale': locale})
    # return jsonify(generate_profile(locale))
    return jsonify(profile_data)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
