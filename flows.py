import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import joblib
from utils.data_processing import load_and_merge_data
from utils.metrics import compute_metrics

def train_delay_model():
    """Train a Random Forest model to predict delivery delays."""
    df = compute_metrics(load_and_merge_data())

    df["Weather_Impact"].fillna("None", inplace=True)
    df["Weather_Impact"] = df["Weather_Impact"].astype("category").cat.codes

    features = [
        "Distance_KM", "Fuel_Consumption_L", "Toll_Charges_INR",
        "Weather_Impact", "Fuel_per_KM", "Total_Cost_INR"
    ]
    target = "Traffic_Delay_Minutes"

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    score = r2_score(y_test, y_pred)
    print(f"✅ Model trained successfully | R² Score: {score:.3f}")

    joblib.dump(model, "data/delay_predictor.pkl")
    print("📦 Model saved to data/delay_predictor.pkl")

def load_model():
    """Load trained model."""
    return joblib.load("data/delay_predictor.pkl")

if __name__ == "__main__":
    train_delay_model()
