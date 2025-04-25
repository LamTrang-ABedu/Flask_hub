import snscrape.modules.twitter as sntwitter

def fetch_media(keyword: str, limit=20):
    results = []
    query = f"{keyword} filter:images OR filter:videos"
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i >= limit:
            break
        media_urls = []
        if tweet.media:
            for media in tweet.media:
                if hasattr(media, 'fullUrl'):
                    media_urls.append(media.fullUrl)
        if media_urls:
            results.append({
                'tweet_id': tweet.id,
                'username': tweet.user.username,
                'text': tweet.content,
                'media': media_urls,
                'date': tweet.date.strftime('%Y-%m-%d %H:%M')
            })
    return {'status': 'ok', 'results': results}
