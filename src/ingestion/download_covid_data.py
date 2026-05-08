from pathlib import Path
import requests

# ==========================================
# PATH SETUP
# ==========================================

CURRENT_FILE = Path(__file__).resolve()

PROJECT_ROOT = CURRENT_FILE.parents[2]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw" / "covid"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================
# DOWNLOAD
# ==========================================

url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"

output_file = RAW_DATA_DIR / "owid_covid_data.csv"

response = requests.get(url)

with open(output_file, "wb") as f:
    f.write(response.content)

print(f"Saved to: {output_file}")