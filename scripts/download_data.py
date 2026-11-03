"""Download the raw data files for US Elections: The Midterm Effect.

Run from the project root: .venv/bin/python scripts/download_data.py

Notes:
- The MIT House file on Harvard Dataverse (DOI 10.7910/DVN/IG0UN2, file
  13592823) refuses direct download because it requires a guestbook
  response. The build therefore uses the keithpotz/Election-Prediction
  mirror of the same file, and cross checks its seat totals against the
  official party division table in scripts/build_processed.py.
- The Dataverse API URLs below fetch the president and Senate files
  without a guestbook form.
"""
import os
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")
os.makedirs(RAW, exist_ok=True)

FILES = [
    ("president_1976_2024.csv",
     "https://dataverse.harvard.edu/api/access/datafile/13887042"),
    ("senate_1976_2024.tab",
     "https://dataverse.harvard.edu/api/access/datafile/13887039"),
    ("house_1976_2024_mirror.csv",
     "https://raw.githubusercontent.com/keithpotz/Election-Prediction/main/src/data/polling_data/house_1976_2024.csv"),
]

for name, url in FILES:
    path = os.path.join(RAW, name)
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        print("exists, skipping:", path)
        continue
    print("downloading:", url)
    urllib.request.urlretrieve(url, path)
    print("saved:", path, os.path.getsize(path), "bytes")
print("Done.")
