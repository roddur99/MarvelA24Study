"""Fetch studio movies and write a CSV with selected fields.

Usage:
  python src/tmdb/get_studio_movies.py --company A24 --out data/processed/a24_movies.csv

Requires `TMDB_API_KEY` in the environment (see `.env.template`).
"""
import os
import sys
import time
import csv
import requests
import argparse

API = "063c2ef1ab7738bf8ac367e4aa63f25d"
if not API:
    sys.exit("Error: TMDB_API_KEY not set. See .env.template")


def find_company_id(name="A24"):
    r = requests.get("https://api.themoviedb.org/3/search/company", params={"api_key": API, "query": name}, timeout=15)
    r.raise_for_status()
    results = r.json().get("results", [])
    if not results:
        sys.exit(f"Company '{name}' not found")
    return results[0]["id"], results[0].get("name", name)


def discover_by_company(company_id, page=1):
    r = requests.get(
        "https://api.themoviedb.org/3/discover/movie",
        params={"api_key": API, "with_companies": company_id, "page": page, "sort_by": "primary_release_date.asc"},
        timeout=20,
    )
    r.raise_for_status()
    return r.json()


def fetch_all_movies(company_id):
    movies = []
    first = discover_by_company(company_id, page=1)
    movies.extend(first.get("results", []))
    total_pages = first.get("total_pages", 1)
    for p in range(2, total_pages + 1):
        time.sleep(0.2)
        page_data = discover_by_company(company_id, page=p)
        movies.extend(page_data.get("results", []))
    return movies


def write_csv(movies, out_path):
    fields = ["title", "movie_id", "popularity", "vote_count", "vote_average", "release_date"]
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for m in movies:
            try:
                votes = int(m.get("vote_count") or 0)
            except Exception:
                votes = 0
            if votes < 500:
                continue
            writer.writerow({
                "title": m.get("title") or m.get("original_title"),
                "movie_id": m.get("id"),
                "popularity": m.get("popularity"),
                "vote_count": m.get("vote_count"),
                "vote_average": m.get("vote_average"),
                "release_date": m.get("release_date"),
            })


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--company", default="A24", help="Company name to search (default: A24)")
    parser.add_argument("--out", default="data/processed/a24_movies.csv", help="Output CSV path")
    args = parser.parse_args()

    company_id, company_name = find_company_id(args.company)
    movies = fetch_all_movies(company_id)
    write_csv(movies, args.out)
    kept = sum(1 for m in movies if int(m.get("vote_count") or 0) >= 500)
    print(f"Wrote {kept} rows to {args.out} (min_vote_count=500)")


if __name__ == "__main__":
    main()
