import pandas as pd
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]

covid_path = ROOT_DIR / "data" / "processed" / "covid_vnm_yearly_features.csv"
worldbank_path = ROOT_DIR / "data" / "processed" / "world_bank_macro_yearly.csv"

output_path = ROOT_DIR / "data" / "processed" / "merged_dataset.csv"

df_covid = pd.read_csv(covid_path)
df_worldbank = pd.read_csv(worldbank_path)

df_final = pd.merge(
    df_worldbank,
    df_covid,
    on="year",
    how="outer"
)

df_final = df_final.fillna(0)

df_final = df_final.sort_values("year")

df_final.to_csv(output_path, index=False)

print(f"Saved merged dataset to: {output_path}")
print(df_final.head())