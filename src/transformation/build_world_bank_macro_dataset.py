from pathlib import Path
import pandas as pd
from functools import reduce

CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parents[2]

INTERIM_DIR = PROJECT_ROOT / "data" / "interim" / "world_bank"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "world_bank_macro_yearly.csv"

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

files = list(INTERIM_DIR.glob("*_cleaned.csv"))

if not files:
    raise ValueError("No cleaned files found")

dfs = []

for file in files:
    df = pd.read_csv(file)

    dfs.append(df)

df_merged = reduce(
    lambda left, right: pd.merge(left, right, on="year", how="outer"),
    dfs
)

df_merged = df_merged.sort_values("year")

df_merged.to_csv(OUTPUT_PATH, index=False)

print(f"Merged dataset saved to: {OUTPUT_PATH}")