from pathlib import Path
import pandas as pd

# =========================
# PATH SETUP
# =========================

CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parents[2]

INPUT_PATH = PROJECT_ROOT / "data" / "interim" / "covid" / "covid_vnm_cleaned.csv"

OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "covid_vnm_yearly_features.csv"

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

# =========================
# LOAD CLEANED DATA
# =========================

df = pd.read_csv(INPUT_PATH)

df["date"] = pd.to_datetime(df["date"])

# =========================
# CREATE YEAR COLUMN
# =========================

df["year"] = df["date"].dt.year

# =========================
# AGGREGATE TO YEARLY LEVEL
# =========================

df_yearly = df.groupby("year").agg({

    # =========================
    # EPIDEMIC SCALE
    # =========================
    "new_cases": "sum",
    "new_deaths": "sum",
    "total_cases": "max",
    "total_deaths": "max",

    # =========================
    # TREND (SMOOTHED)
    # =========================
    "new_cases_smoothed": "mean",
    "new_deaths_smoothed": "mean",

    # =========================
    # VACCINATION
    # =========================
    "total_vaccinations": "max",
    "people_vaccinated": "max",
    "people_fully_vaccinated": "max",

    # =========================
    # TESTING
    # =========================
    "total_tests": "max",
    "positive_rate": "mean",

    # =========================
    # POLICY SHOCK
    # =========================
    "stringency_index": "mean",

    # =========================
    # CONTROLS (MACRO)
    # =========================
    "population": "first",
    "gdp_per_capita": "first",
    "life_expectancy": "first"

}).reset_index()

# =========================
# FEATURE ENGINEERING (COVID SHOCK VARIABLES)
# =========================

# normalize theo dân số (rất quan trọng trong kinh tế vĩ mô)
df_yearly["cases_per_capita"] = df_yearly["new_cases"] / df_yearly["population"]
df_yearly["deaths_per_capita"] = df_yearly["new_deaths"] / df_yearly["population"]

# mức độ nghiêm trọng
df_yearly["fatality_rate"] = df_yearly["total_deaths"] / df_yearly["total_cases"]

# mức độ tiêm vaccine
df_yearly["vaccination_rate"] = df_yearly["people_vaccinated"] / df_yearly["population"]
df_yearly["full_vaccination_rate"] = df_yearly["people_fully_vaccinated"] / df_yearly["population"]

# chỉ số shock tổng hợp (quan trọng cho regression)
df_yearly["covid_intensity_index"] = (
    df_yearly["cases_per_capita"] * 0.6 +
    df_yearly["deaths_per_capita"] * 0.4
)

# policy shock
df_yearly["covid_policy_shock"] = df_yearly["stringency_index"]

# =========================
# FINAL SORT
# =========================

df_yearly = df_yearly.sort_values("year")

# =========================
# SAVE
# =========================

df_yearly.to_csv(OUTPUT_PATH, index=False)

print(f"Saved yearly COVID features to: {OUTPUT_PATH}")