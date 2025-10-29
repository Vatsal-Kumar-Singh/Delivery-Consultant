import pandas as pd
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _read_csv(name: str) -> pd.DataFrame:
    path = DATA_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Required data file not found: {path}")
    return pd.read_csv(path)


def load_and_merge_data():
    """Loads and merges all datasets into a single unified DataFrame.

    Paths are resolved relative to the repository so the function works
    regardless of the current working directory when the app is launched.
    """
    orders = _read_csv("orders.csv")
    delivery = _read_csv("delivery_performance.csv")
    routes = _read_csv("routes_distance.csv")
    costs = _read_csv("cost_breakdown.csv")
    fleet = _read_csv("vehicle_fleet.csv")

    merged = (
        orders
        .merge(delivery, on="Order_ID", how="left")
        .merge(routes, on="Order_ID", how="left")
        .merge(costs, on="Order_ID", how="left")
    )

    # Safe defaults when columns are missing
    defaults = {}
    if "Traffic_Delay_Minutes" in merged.columns:
        defaults["Traffic_Delay_Minutes"] = 0
    if "Weather_Impact" in merged.columns:
        defaults["Weather_Impact"] = "None"
    if "Fuel_Consumption_L" in merged.columns:
        defaults["Fuel_Consumption_L"] = merged["Fuel_Consumption_L"].mean()
    if "Toll_Charges_INR" in merged.columns:
        defaults["Toll_Charges_INR"] = 0

    if defaults:
        merged.fillna(defaults, inplace=True)

    return merged
