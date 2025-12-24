"""Minimal normalization utilities (placeholder).
"""
import json
import os
from pathlib import Path


def normalize_tmdb_raw(infile, outfile):
    p = Path(infile)
    data = json.loads(p.read_text(encoding='utf-8'))
    rows = []
    for m in data.get('results', []):
        rows.append({
            'tmdb_id': m.get('id'),
            'title': m.get('title') or m.get('original_title'),
            'release_date': m.get('release_date'),
            'vote_average': m.get('vote_average'),
            'vote_count': m.get('vote_count'),
        })
    os.makedirs(os.path.dirname(outfile), exist_ok=True)
    with open(outfile, 'w', encoding='utf-8') as fh:
        json.dump(rows, fh, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print('Usage: python src/etl/normalize.py data/raw/tmdb.json data/processed/tmdb.json')
        sys.exit(1)
    normalize_tmdb_raw(sys.argv[1], sys.argv[2])
