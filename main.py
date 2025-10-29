import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils.data_processing import load_and_merge_data
from utils.metrics import compute_metrics
from crew_setup import create_crew
from predictor import load_model


st.set_page_config(page_title="AI Delivery Delay Predictor", layout="wide")

st.title("🚚 AI-Powered Delivery Delay Prediction & Optimization Dashboard")
st.write("Predict potential delivery delays and get AI-driven corrective actions in real-time.")

# --- Load Data and Model ---
raw = load_and_merge_data()
# ensure date parsing
try:
    raw["Order_Date"] = pd.to_datetime(raw["Order_Date"])
except Exception:
    # If parsing fails, keep as-is and downstream code will handle it
    pass

df = compute_metrics(raw)
model = load_model()
crew = create_crew()


def _prepare_input(distance_km, fuel_l, toll_inr, weather_label, total_cost):
    weather_map = {"None": 0, "Light_Rain": 1, "Heavy_Rain": 2, "Fog": 3}
    fuel_per_km = fuel_l / distance_km if distance_km else 0
    return pd.DataFrame([{
        "Distance_KM": distance_km,
        "Fuel_Consumption_L": fuel_l,
        "Toll_Charges_INR": toll_inr,
        "Weather_Impact_Num": weather_map.get(weather_label, 0),
        "Fuel_per_KM": fuel_per_km,
        "Total_Cost_INR": total_cost
    }])


def estimate_impact(model, base_input: pd.DataFrame, changes: dict) -> float:
    """Estimate predicted delay after applying numeric changes to base_input.

    `changes` is a mapping of column -> new_value or multiplier (if value is tuple ('mul', factor)).
    Returns predicted delay difference (base - new), i.e., estimated reduction in minutes.
    """
    inp = base_input.copy()
    for k, v in changes.items():
        if isinstance(v, tuple) and v and v[0] == "mul":
            factor = v[1]
            if k in inp.columns:
                inp[k] = inp[k] * factor
        else:
            inp[k] = v

    base_pred = float(model.predict(base_input)[0]) if base_input.shape[0] else 0.0
    new_pred = float(model.predict(inp)[0]) if inp.shape[0] else 0.0
    return max(0.0, base_pred - new_pred)


def generate_corrective_actions(df: pd.DataFrame, model, base_input: pd.DataFrame, crew):
    """Produce prioritized corrective actions with estimated impact and short plans.

    Returns a list of dicts: {title, priority, est_delay_reduction_min, est_cost_change, details}
    """
    actions = []

    # 1) Route re-optimization: find routes with highest avg delay
    # Use the 'Route' column from the merged dataset (fallback to Order_ID if missing)
    route_col = "Route" if "Route" in df.columns else "Order_ID"
    route_delays = df.groupby(route_col)["Traffic_Delay_Minutes"].mean().sort_values(ascending=False)
    top_route = route_delays.index[0] if not route_delays.empty else None
    if top_route is not None:
        # simulate 10% shorter route
        est_reduce = estimate_impact(model, base_input, {"Distance_KM": ("mul", 0.9)})
        actions.append({
            "title": f"Re-route deliveries currently on Route {top_route} to shorter/less-congested alternatives",
            "priority": 1,
            "est_delay_reduction_min": round(est_reduce, 1),
            "est_cost_change": "±small",
            "details": (
                "Use historical congestion and distance data to pick alternate paths that reduce distance or avoid peak traffic. "
                "Prioritize high-delay routes for immediate re-routing."
            ),
        })

    # 2) Schedule shift: reduce weather/peak exposure by shifting 1 hour earlier (modelled as small weather effect reduction)
    est_shift = estimate_impact(model, base_input, {"Weather_Impact_Num": max(0, int(base_input.get("Weather_Impact_Num", pd.Series([0]))[0]) - 1)})
    actions.append({
        "title": "Shift departure times earlier for weather/peak-hour avoidance",
        "priority": 2,
        "est_delay_reduction_min": round(est_shift, 1),
        "est_cost_change": "small"
    })

    # 3) Fuel & vehicle optimization: target high fuel_per_km drivers
    est_fuel = estimate_impact(model, base_input, {"Fuel_per_KM": ("mul", 0.85)})
    actions.append({
        "title": "Driver coaching and load optimization to reduce fuel per km",
        "priority": 3,
        "est_delay_reduction_min": round(est_fuel, 1),
        "est_cost_change": "reduces fuel costs",
        "details": "Coach drivers on eco-driving, optimize loads, and perform vehicle maintenance to improve fuel efficiency."
    })

    # Let CrewAI expand and rank the top action if available
    if crew:
        try:
            prompt = (
                "You are an operations expert. Given these suggested actions: \n" +
                "\n".join([f"- {a['title']} (est_reduce={a.get('est_delay_reduction_min', '?')}m)" for a in actions]) +
                "\nProvide a concise 2-3 step execution plan for the top 2 actions and state which to do first."
            )
            expanded = crew.run(prompt)
            # attach expanded text to first action
            if actions:
                actions[0]["details"] = (actions[0].get("details", "") + "\n\nCrew suggestion:\n" + expanded)
        except Exception:
            # ignore crew failures
            pass

    # Sort by priority
    actions = sorted(actions, key=lambda x: x.get("priority", 99))
    return actions


# --- Sidebar Inputs ---
st.sidebar.header("🔮 Predict Future Delay")
distance = st.sidebar.number_input("Distance (KM)", 10.0, 5000.0, 500.0)
fuel = st.sidebar.number_input("Fuel Consumption (L)", 1.0, 1000.0, 100.0)
toll = st.sidebar.number_input("Toll Charges (₹)", 0.0, 5000.0, 200.0)
weather = st.sidebar.selectbox("Weather", ["None", "Light_Rain", "Heavy_Rain", "Fog"])
cost = st.sidebar.number_input("Estimated Total Cost (₹)", 100.0, 50000.0, 2000.0)

base_input = _prepare_input(distance, fuel, toll, weather, cost)

# --- Prediction & Actions Section ---
if st.sidebar.button("Predict Delay"):
    predicted_delay = float(model.predict(base_input)[0])
    st.metric("⏰ Predicted Delay (minutes)", f"{predicted_delay:.2f}")

    st.subheader("🧠 AI-Powered Corrective Actions")
    actions = generate_corrective_actions(df, model, base_input, crew)

    for a in actions:
        with st.expander(f"{a['title']} — est. delay reduction {a.get('est_delay_reduction_min', '?')} min"):
            st.write(f"Priority: {a.get('priority')}")
            if "details" in a:
                st.write(a["details"])
            # small callout box
            st.info(f"Estimated delay reduction: {a.get('est_delay_reduction_min', 0)} minutes — Cost impact: {a.get('est_cost_change', 'unknown')}")


# --- Historical Analytics ---
st.subheader("📊 Delivery Analytics Overview")

# --- Filters (sidebar) ---
st.sidebar.markdown("---")
st.sidebar.header("📋 Dashboard Filters")
# Carrier filter
carrier_opts = sorted(df["Carrier"].dropna().unique().tolist()) if "Carrier" in df.columns else []
selected_carriers = st.sidebar.multiselect("Carrier", options=carrier_opts, default=carrier_opts)

# Weather filter
weather_opts = sorted(df["Weather_Impact"].dropna().unique().tolist()) if "Weather_Impact" in df.columns else ["None"]
selected_weather = st.sidebar.multiselect("Weather", options=weather_opts, default=weather_opts)

# Priority / Product filters
priority_opts = sorted(df["Priority"].dropna().unique().tolist()) if "Priority" in df.columns else []
selected_priority = st.sidebar.multiselect("Priority", options=priority_opts, default=priority_opts)

# Date range filter
if "Order_Date" in df.columns and pd.api.types.is_datetime64_any_dtype(df["Order_Date"]):
    min_date = df["Order_Date"].min().date()
    max_date = df["Order_Date"].max().date()
    selected_dates = st.sidebar.date_input("Order Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)
else:
    selected_dates = None

# Apply filters to create a filtered dataframe used for charts
filtered = df.copy()
if selected_carriers:
    if "Carrier" in filtered.columns:
        filtered = filtered[filtered["Carrier"].isin(selected_carriers)]
if selected_weather:
    if "Weather_Impact" in filtered.columns:
        filtered = filtered[filtered["Weather_Impact"].isin(selected_weather)]
if selected_priority:
    if "Priority" in filtered.columns:
        filtered = filtered[filtered["Priority"].isin(selected_priority)]
if selected_dates and "Order_Date" in filtered.columns and pd.api.types.is_datetime64_any_dtype(filtered["Order_Date"]):
    start, end = pd.to_datetime(selected_dates[0]), pd.to_datetime(selected_dates[1])
    filtered = filtered[(filtered["Order_Date"] >= start) & (filtered["Order_Date"] <= end)]

col1, col2 = st.columns((2, 1))

with col1:
    fig = px.scatter(filtered, x="Distance_KM", y="Traffic_Delay_Minutes", color="Weather_Impact", size="Total_Cost_INR",
                     title="Historical Delays by Route & Weather", hover_data=["Order_ID", "Route"])
    st.plotly_chart(fig, use_container_width=True)

    # top delayed orders table
    st.markdown("### 🔻 Top Delayed Orders")
    top = filtered.sort_values("Traffic_Delay_Minutes", ascending=False).head(10)
    cols_for_table = [c for c in ["Order_ID", "Route", "Distance_KM", "Traffic_Delay_Minutes", "Total_Cost_INR"] if c in top.columns]
    st.dataframe(top[cols_for_table])

    # Download filtered data
    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("Download Filtered Data (CSV)", data=csv, file_name="filtered_delivery_data.csv", mime="text/csv")

with col2:
    # Cost breakdown
    cost_cols = [c for c in ["Fuel_Cost_INR", "Labor_Cost_INR", "Maintenance_Cost_INR", "Toll_Charges_INR"] if c in df.columns]
    cost_sums = filtered[cost_cols].sum() if cost_cols else pd.Series()
    if not cost_sums.empty:
        pie = px.pie(values=cost_sums.values, names=cost_sums.index, title="Cost Breakdown")
        st.plotly_chart(pie, use_container_width=True)

    # Delay distribution
    hist = px.histogram(filtered, x="Traffic_Delay_Minutes", nbins=30, title="Delay Distribution (minutes)")
    st.plotly_chart(hist, use_container_width=True)

    # Fuel vs Distance
    if "Fuel_per_KM" in filtered.columns:
        sc = px.scatter(filtered, x="Distance_KM", y="Fuel_per_KM", color="Traffic_Delay_Minutes", title="Fuel efficiency vs Distance")
        st.plotly_chart(sc, use_container_width=True)

    # Average delay by carrier (bar chart)
    if "Carrier" in filtered.columns:
        bar = px.bar(filtered.groupby("Carrier")["Traffic_Delay_Minutes"].mean().reset_index().sort_values(by="Traffic_Delay_Minutes", ascending=False),
                     x="Carrier", y="Traffic_Delay_Minutes", title="Average Delay by Carrier")
        st.plotly_chart(bar, use_container_width=True)

    # Delay over time (line chart)
    if "Order_Date" in filtered.columns and pd.api.types.is_datetime64_any_dtype(filtered["Order_Date"]):
        time_series = filtered.groupby(filtered["Order_Date"].dt.date)["Traffic_Delay_Minutes"].mean().reset_index()
        time_series.columns = ["Order_Date", "Avg_Delay_Minutes"]
        line = px.line(time_series, x="Order_Date", y="Avg_Delay_Minutes", title="Average Delay Over Time")
        st.plotly_chart(line, use_container_width=True)

    # Export corrective actions if any were generated in the session
    try:
        if 'actions' in locals() and actions:
            import io, csv
            out = io.StringIO()
            w = csv.DictWriter(out, fieldnames=actions[0].keys())
            w.writeheader()
            w.writerows(actions)
            st.download_button("Download Actions (CSV)", data=out.getvalue().encode('utf-8'), file_name='corrective_actions.csv', mime='text/csv')
    except Exception:
        pass

