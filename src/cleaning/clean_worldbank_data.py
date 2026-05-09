from pathlib import Path
import pandas as pd

# =========================
# PATH SETUP
# =========================

CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parents[2]

RAW_DIR = PROJECT_ROOT / "data" / "raw" / "world_bank"
INTERIM_DIR = PROJECT_ROOT / "data" / "interim" / "world_bank"

INTERIM_DIR.mkdir(parents=True, exist_ok=True)

# =========================
# GET ALL FILES
# =========================

csv_files = list(RAW_DIR.glob("*.csv"))

print(f"Found {len(csv_files)} files")

# =========================
# CLEAN FUNCTION
# =========================

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        if col != "year":
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "year" in df.columns:
        df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
        df = df.drop_duplicates(subset=["year"])
        df = df.sort_values("year")

    return df

# =========================
# PROCESS ALL FILES
# =========================

for file in csv_files:
    print(f"Processing: {file.name}")

    df = pd.read_csv(file)

    df = clean_dataframe(df)

    output_file = INTERIM_DIR / f"{file.stem}_cleaned.csv"

    df.to_csv(output_file, index=False)

    print(f"Saved: {output_file}")

print("DONE CLEANING ALL FILES")