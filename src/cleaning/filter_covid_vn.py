from pathlib import Path
import pandas as pd

# =========================
# PATH SETUP
# =========================

CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parents[2]

RAW_PATH = PROJECT_ROOT / "data" / "raw" / "covid" / "owid_covid_data.csv"

OUTPUT_PATH = PROJECT_ROOT / "data" / "interim" / "covid" / "covid_vnm_cleaned.csv"

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

# =========================
# LOAD RAW DATA
# =========================

df = pd.read_csv(RAW_PATH)

# =========================
# FILTER VIETNAM
# =========================

df = df[df["iso_code"] == "VNM"].copy()

# =========================
# BASIC CLEANING
# =========================

df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

num_cols = df.select_dtypes(include="number").columns
df[num_cols] = df[num_cols].apply(pd.to_numeric, errors="coerce")

df = df.drop_duplicates(subset=["date"])

# =========================
# FEATURE SELECTION
# =========================

selected_cols = [
    # identifiers
    "iso_code",
    "location",
    "date",

    # core epidemiology
    "total_cases",
    "new_cases",
    "total_deaths",
    "new_deaths",

    # smoothed
    "new_cases_smoothed",
    "new_deaths_smoothed",

    # vaccination
    "total_vaccinations",
    "people_vaccinated",
    "people_fully_vaccinated",

    # testing
    "total_tests",
    "positive_rate",

    # policy
    "stringency_index",

    # socioeconomic
    "population",
    "gdp_per_capita",
    "life_expectancy"
]

selected_cols = [c for c in selected_cols if c in df.columns]
df = df[selected_cols].copy()

# =========================
# FINAL SORT
# =========================

df = df.sort_values(["location", "date"])

# =========================
# SAVE PROCESSED DATA
# =========================

df.to_csv(OUTPUT_PATH, index=False)

print(f"Vietnam COVID data saved to: {OUTPUT_PATH}")