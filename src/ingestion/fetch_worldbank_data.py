import requests
import pandas as pd
from pathlib import Path

# ==========================================
# CONFIG
# ==========================================

COUNTRY_CODE = "VNM"

START_YEAR = 2000
END_YEAR = 2025

# indicator_code : output_filename
INDICATORS = {
    "FP.CPI.TOTL.ZG": "inflation_cpi",
    "NY.GDP.MKTP.KD.ZG": "gdp_growth",
    "SL.UEM.TOTL.ZS": "unemployment",
    "SL.TLF.TOTL.IN": "labor_force",
    "NE.EXP.GNFS.ZS": "exports_percent_gdp",
    "BX.KLT.DINV.WD.GD.ZS": "foreign_direct_investment_percent_gdp",
}

# ==========================================
# PATH SETUP
# ==========================================

CURRENT_FILE = Path(__file__).resolve()

PROJECT_ROOT = CURRENT_FILE.parents[2]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw" / "world_bank"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================
# FETCH FUNCTION
# ==========================================

def fetch_indicator(indicator_code: str, output_name: str):

    url = (
        f"https://api.worldbank.org/v2/country/{COUNTRY_CODE}"
        f"/indicator/{indicator_code}"
        f"?format=json"
        f"&date={START_YEAR}:{END_YEAR}"
        f"&per_page=100"
    )

    print(f"\nFetching {indicator_code} ...")

    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed request: {response.status_code}")
        return

    data = response.json()

    if len(data) < 2:
        print(f"No data returned for {indicator_code}")
        return

    records = data[1]

    rows = []

    for item in records:

        rows.append({
            "year": int(item["date"]),
            output_name: item["value"]
        })

    df = pd.DataFrame(rows)

    df = df.sort_values(by="year")

    output_file = RAW_DATA_DIR / f"{output_name}.csv"

    df.to_csv(output_file, index=False)

    print(f"Saved -> {output_file}")

# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    for indicator, filename in INDICATORS.items():
        fetch_indicator(indicator, filename)

    print("\nAll done")