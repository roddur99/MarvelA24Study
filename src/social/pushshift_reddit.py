"""Simple Pushshift (Reddit) query helper placeholder."""
import requests

BASE = 'https://api.pushshift.io/reddit/search/comment/'

def search_comments(query, size=100, before=None, after=None):
    params = {'q': query, 'size': size}
    if before: params['before'] = before
    if after: params['after'] = after
    r = requests.get(BASE, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

if __name__ == '__main__':
    import sys
    q = sys.argv[1] if len(sys.argv) > 1 else 'A24'
    print(search_comments(q))
