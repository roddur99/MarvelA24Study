"""Twitter ingestion helper (placeholder). Use `TWITTER_BEARER` env var."""
import os
import requests

BEARER = os.environ.get('TWITTER_BEARER')

def search_recent(query, max_results=100):
    if not BEARER:
        raise RuntimeError('TWITTER_BEARER not set')
    url = 'https://api.twitter.com/2/tweets/search/recent'
    headers = {'Authorization': f'Bearer {BEARER}'}
    params = {'query': query, 'max_results': max_results}
    r = requests.get(url, headers=headers, params=params, timeout=30)
    r.raise_for_status()
    return r.json()
