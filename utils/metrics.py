import pandas as pd
import numpy as np
import warnings


def compute_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Compute additional performance and cost metrics in a resilient way.

    This function will add missing columns with safe defaults instead of
    raising KeyError so the Streamlit app can run even when some datasets
    don't contain every expected field.
    """
    # Ensure cost columns exist; default to 0 when not present
    cost_cols = ["Fuel_Cost_INR", "Labor_Cost_INR", "Maintenance_Cost_INR", "Toll_Charges_INR"]
    for c in cost_cols:
        if c not in df.columns:
            warnings.warn(f"Missing expected column '{c}' — filling with 0s")
            df[c] = 0.0

    df["Total_Cost_INR"] = df[cost_cols].sum(axis=1)

    # Fuel per km: guard against missing columns and division by zero
    if "Fuel_Consumption_L" not in df.columns:
        warnings.warn("Missing 'Fuel_Consumption_L' — filling with NaN for Fuel_per_KM")
        df["Fuel_Consumption_L"] = np.nan
    if "Distance_KM" not in df.columns:
        warnings.warn("Missing 'Distance_KM' — filling with NaN for Fuel_per_KM")
        df["Distance_KM"] = np.nan

    df["Fuel_per_KM"] = np.where(
        (df["Distance_KM"] > 0) & df["Distance_KM"].notna(),
        df["Fuel_Consumption_L"] / df["Distance_KM"],
        np.nan,
    )

    # Delay and reliability: missing delays default to 0 (no delay)
    if "Traffic_Delay_Minutes" not in df.columns:
        warnings.warn("Missing 'Traffic_Delay_Minutes' — filling with 0s for Delay_Index")
        df["Traffic_Delay_Minutes"] = 0.0

    df["Delay_Index"] = df["Traffic_Delay_Minutes"] / 60.0

    max_delay = df["Delay_Index"].max() if not df["Delay_Index"].empty else 0.0
    denom = max(max_delay, 0.1)
    df["Reliability_Score"] = 1.0 - (df["Delay_Index"] / denom)

    return df
