import os

files_to_check = [
    'archive (7)/matches.csv', # 2018
    'archive (8)/matches.csv', # 2022 (Check if this exists)
    'archive (8)/matches_detailed.csv' # 2026
]

for f in files_to_check:
    if os.path.exists(f):
        print(f"SUCCESS: {f} found.")
    else:
        print(f"ERROR: {f} missing.")