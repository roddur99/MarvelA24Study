import csv
import os
import sys

INFILE = sys.argv[1] if len(sys.argv) > 1 else "data/processed/a24_movies.csv"
OUTFILE = sys.argv[2] if len(sys.argv) > 2 else "data/processed/a24_movies_pop500.csv"
THRESHOLD = float(sys.argv[3]) if len(sys.argv) > 3 else 500.0

os.makedirs(os.path.dirname(OUTFILE) or ".", exist_ok=True)

count_in = 0
count_out = 0
with open(INFILE, newline='', encoding='utf-8') as inf, open(OUTFILE, 'w', newline='', encoding='utf-8') as outf:
    reader = csv.DictReader(inf)
    writer = csv.DictWriter(outf, fieldnames=reader.fieldnames)
    writer.writeheader()
    for row in reader:
        count_in += 1
        try:
            pop = float(row.get('popularity') or 0)
        except Exception:
            pop = 0.0
        if pop >= THRESHOLD:
            writer.writerow(row)
            count_out += 1

print(f"Read {count_in} rows from {INFILE}; wrote {count_out} rows to {OUTFILE} (threshold={THRESHOLD})")
