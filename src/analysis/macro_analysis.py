from pathlib import Path
from typing import Iterable, Sequence

import pandas as pd
import statsmodels.api as sm

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "merged_dataset.csv"

MACRO_COLUMNS = [
    "gdp_growth",
    "unemployment",
    "inflation_cpi",
    "exports_percent_gdp",
    "fdi_percent_gdp",
    "labor_force",
]


def load_macro_dataset(data_path: Path | str = DEFAULT_DATA_PATH) -> pd.DataFrame:
    """Load the merged macro dataset and coerce numeric columns."""
    df = pd.read_csv(data_path)

    if "year" not in df.columns:
        raise ValueError("The dataset must contain a 'year' column.")

    df = df.copy()
    df["year"] = pd.to_numeric(df["year"], errors="coerce")

    for column in df.columns:
        if column == "year":
            continue
        df[column] = pd.to_numeric(df[column], errors="coerce")

    return df.sort_values("year").reset_index(drop=True)


def filter_year_range(
    df: pd.DataFrame,
    start_year: int | None = None,
    end_year: int | None = None,
) -> pd.DataFrame:
    """Return a year-filtered copy of the dataset."""
    filtered = df.copy()

    if start_year is not None:
        filtered = filtered[filtered["year"] >= start_year]
    if end_year is not None:
        filtered = filtered[filtered["year"] <= end_year]

    return filtered.reset_index(drop=True)


def build_regression_frame(
    df: pd.DataFrame,
    target: str,
    features: Sequence[str],
) -> pd.DataFrame:
    """Select modeling columns and drop rows with missing values."""
    required_columns = [target, *features]
    frame = df.loc[:, ["year", *required_columns]].copy()
    frame = frame.dropna(subset=required_columns).reset_index(drop=True)
    return frame


def fit_ols(
    df: pd.DataFrame,
    target: str,
    features: Sequence[str],
):
    """Fit an OLS model with HC3 robust standard errors."""
    frame = build_regression_frame(df, target, features)
    design_matrix = sm.add_constant(frame[list(features)], has_constant="add")
    model = sm.OLS(frame[target], design_matrix).fit(cov_type="HC3")
    return model, frame


def coefficient_table(result) -> pd.DataFrame:
    """Create a compact coefficient table for notebook display."""
    confidence_intervals = result.conf_int()
    table = pd.DataFrame(
        {
            "coef": result.params,
            "std_err": result.bse,
            "t_value": result.tvalues,
            "p_value": result.pvalues,
            "ci_lower": confidence_intervals[0],
            "ci_upper": confidence_intervals[1],
        }
    )
    return table.round(4)
