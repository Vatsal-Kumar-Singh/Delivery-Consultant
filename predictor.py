import os
from typing import Any
import numpy as np
import pandas as pd

MODEL_PATH = "model.joblib"


class DummyModel:
    """A trivial model used when there's insufficient data to train."""
    def predict(self, X):
        # return zeros matching number of rows
        try:
            return np.zeros(len(X))
        except Exception:
            return np.array([0.0])


class PredictWrapper:
    """Wraps a sklearn-style model and provides DataFrame-friendly predict.

    The wrapper prepares the feature matrix from an incoming DataFrame so
    callers (like the Streamlit app) can pass the same `input_data` DataFrame
    they already build in `main.py`.
    """
    def __init__(self, model, features):
        self.model = model
        self.features = features

    def _preprocess(self, df: pd.DataFrame) -> np.ndarray:
        X = df.copy()
        # compute Fuel_per_KM if missing
        if "Fuel_per_KM" not in X.columns and "Fuel_Consumption_L" in X.columns:
            X["Fuel_per_KM"] = X["Fuel_Consumption_L"] / X["Distance_KM"].replace(0, 1)

        weather_map = {"None": 0, "Light_Rain": 1, "Heavy_Rain": 2, "Fog": 3}
        if "Weather_Impact" in X.columns:
            X["Weather_Impact_Num"] = X["Weather_Impact"].map(weather_map).fillna(0)
        elif "Weather_Impact_Num" not in X.columns:
            X["Weather_Impact_Num"] = 0

        # Ensure all features exist
        for f in self.features:
            if f not in X.columns:
                X[f] = 0

        return X[self.features].fillna(0).values

    def predict(self, df_or_array):
        # Accept DataFrame (preferred) or array-like
        if isinstance(df_or_array, (pd.DataFrame,)):
            Xp = self._preprocess(df_or_array)
        else:
            Xp = np.array(df_or_array)
        return self.model.predict(Xp)


def load_model() -> Any:
    """Load or train a simple regression model and return a predict-friendly wrapper.

    If a saved model exists at `MODEL_PATH` it will be loaded. Otherwise the
    function will attempt to load project data (via `utils`) and train a
    LinearRegression model. If training is not possible, a DummyModel is
    returned so the app remains functional.
    """
    try:
        # Lazy import heavy deps only when needed
        from sklearn.linear_model import LinearRegression
        from utils.data_processing import load_and_merge_data
        from utils.metrics import compute_metrics
    except Exception:
        # If imports fail, return a dummy model
        return PredictWrapper(DummyModel(), ["Distance_KM", "Fuel_per_KM", "Weather_Impact_Num", "Total_Cost_INR"])

    if os.path.exists(MODEL_PATH):
        try:
            # Load with joblib if available; otherwise skip loading
            import joblib as _joblib
            model = _joblib.load(MODEL_PATH)
            # If the persisted object is a PredictWrapper, return as-is
            if hasattr(model, "predict"):
                return model
        except Exception:
            # fall through and retrain
            pass

    # Attempt to load data and train
    try:
        df = compute_metrics(load_and_merge_data())
        weather_map = {"None": 0, "Light_Rain": 1, "Heavy_Rain": 2, "Fog": 3}
        df["Weather_Impact_Num"] = df.get("Weather_Impact", pd.Series()).map(weather_map).fillna(0)

        features = ["Distance_KM", "Fuel_per_KM", "Weather_Impact_Num", "Total_Cost_INR"]
        # Ensure Fuel_per_KM exists
        if "Fuel_per_KM" not in df.columns and "Fuel_Consumption_L" in df.columns:
            df["Fuel_per_KM"] = df["Fuel_Consumption_L"] / df["Distance_KM"].replace(0, 1)

        X = df[features].fillna(0).values
        y = df.get("Traffic_Delay_Minutes", pd.Series(np.zeros(len(X)))).fillna(0).values

        if len(X) < 2 or len(y) < 2:
            wrapper = PredictWrapper(DummyModel(), features)
            return wrapper

        model = LinearRegression()
        model.fit(X, y)
        wrapper = PredictWrapper(model, features)
        try:
            import joblib as _joblib
            _joblib.dump(wrapper, MODEL_PATH)
        except Exception:
            # Don't fail if saving the model isn't possible (permissions, missing joblib, etc.)
            pass
        return wrapper

    except Exception:
        # On any training/load error return a dummy model to keep the UI working
        return PredictWrapper(DummyModel(), ["Distance_KM", "Fuel_per_KM", "Weather_Impact_Num", "Total_Cost_INR"])
