from flask import Flask, render_template, request, jsonify
from utils.profile_faker import generate_profile
from utils.gallery_fetcher import fetch_media
from utils.media_downloader import download_from_url

app = Flask(__name__)

@app.route('/')
def profile_faker_page():
    return render_template('profile_faker.html')

@app.route('/api/profile')
def api_profile():
    locale = request.args.get('locale', 'en_US')
    return jsonify(generate_profile(locale))

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)