from yt_dlp import YoutubeDL

def download_from_url(url):
    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'force_generic_extractor': False,
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            media_list = []
            if 'entries' in info:
                for entry in info['entries']:
                    media_list.append(_extract_item(entry))
            else:
                media_list.append(_extract_item(info))
        return {'status': 'ok', 'media': media_list}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

def _extract_item(info):
    return {
        'title': info.get('title'),
        'url': info.get('url'),
        'thumbnail': info.get('thumbnail'),
        'ext': info.get('ext'),
        'webpage_url': info.get('webpage_url')
    }
