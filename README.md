# Delivery Consultant

An AI-powered delivery optimization system that predicts delays and provides real-time solutions for logistics networks. This intelligent consultant uses machine learning to analyze delivery patterns, predict potential delays, and suggest corrective actions.

## Features

- Real-time delivery delay prediction
- AI-driven corrective action suggestions
- Interactive dashboard using Streamlit
- Data visualization with Plotly
- Automated route optimization
- Weather impact analysis
- Cost optimization recommendations

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Vatsal-Kumar-Singh/Delivery-Consultant.git
cd Delivery-Consultant
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/Scripts/activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit dashboard:
```bash
streamlit run main.py
```

The dashboard will be available at http://localhost:8501

## Project Structure

- `main.py`: Main Streamlit dashboard application
- `predictor.py`: Machine learning model and prediction logic
- `crew_setup.py`: AI agent configuration for recommendations
- `utils/`: Helper functions and data processing utilities
- `data/`: Dataset files
  - `orders.csv`: Order information
  - `delivery_performance.csv`: Delivery metrics
  - `routes_distance.csv`: Route information
  - `vehicle_fleet.csv`: Vehicle data
  - `warehouse_inventory.csv`: Inventory data
  - `customer_feedback.csv`: Customer feedback
  - `cost_breakdown.csv`: Cost analysis data

## Requirements

- Python 3.8+
- Streamlit
- Pandas
- Plotly
- Scikit-learn
- CrewAI
- Other dependencies listed in requirements.txt

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

---

# 📊 SEO Consultant

An AI-powered **Search Engine Optimization (SEO) Consultant** built with **[CrewAI](https://docs.crewai.com/)** and **Streamlit**, developed by *Vatsal Kumar Singh*.

This app helps you:

* Analyze your website for SEO performance
* Identify top competitors in your niche
* Research competitor strategies and keywords
* Generate a comprehensive, professional SEO report

---

## 🚀 Features

* **Website Analysis** – evaluates site structure, weaknesses, and areas for SEO improvement.
* **Competitor Discovery** – finds 5–10 relevant competitors with URLs.
* **Competitor Research** – provides comparative insights & keyword suggestions.
* **SEO Report Writing** – delivers a 2–3 page structured report.
* **Interactive UI** – built with Streamlit for easy usage.
* **Flow-based Orchestration** – powered by CrewAI’s Flow system for modular and extensible pipelines.

---

## 🛠️ Tech Stack

* [Python 3.10+](https://www.python.org/)
* [CrewAI](https://docs.crewai.com/) – Agent orchestration & Flows
* [Streamlit](https://streamlit.io/) – UI layer
* [OpenAI](https://platform.openai.com/) – LLMs for analysis & writing
* [Serper](https://serper.dev/) – Google search API
* [Pydantic](https://docs.pydantic.dev/) – State management

---

## 📂 Project Structure

```
SEO-consultant/
│── agents.py        # Defines AI agents (website analyst, competitor analyst, etc.)
│── task.py          # Defines tasks assigned to each agent
│── flows.py         # Orchestrates workflow using CrewAI Flows
│── main.py          # Streamlit app entry point
│── requirements.txt # Dependencies
│── README.md        # Project documentation
```

---

## ⚙️ Installation & Setup

1. **Clone the repository**

```bash
git clone https://github.com/your-username/SEO-consultant.git
cd SEO-consultant
```

2. **Create virtual environment (recommended)**

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set API Keys**
   You need:

* OpenAI API Key → [Get here](https://platform.openai.com/)
* Serper API Key → [Get here](https://serper.dev/)

Either export them in your terminal:

```bash
export OPENAI_API_KEY="your_openai_api_key"
export SERPER_API_KEY="your_serper_api_key"
```

Or enter them directly in the Streamlit sidebar when running the app.

---

## ▶️ Usage

Run the Streamlit app:

```bash
streamlit run main.py
```

* Enter your **website URL**
* Provide **OpenAI + Serper API keys**
* Choose a model (e.g. `gpt-4o`, `gpt-4.1-mini`)
* Get your full SEO analysis & competitor insights!

---

## 🧠 How It Works

1. **Flow Orchestration (`flows.py`)**

   * Starts with website analysis
   * Finds competitors
   * Researches competitors
   * Writes final report

2. **Agents (`agents.py`)**

   * Each agent is specialized (analyst, researcher, writer).

3. **Tasks (`task.py`)**

   * Define the work each agent must do.

4. **Streamlit (`main.py`)**

   * Provides the user interface.

---

## 📌 Example Output

* Overall SEO score
* Site weaknesses & improvement actions
* Competitor list with URLs
* Comparative analysis of competitors
* Suggested keywords to rank higher
* Final professional SEO report

---

## 👤 Author

**Vatsal Kumar Singh**

---

# AI Delivery Delay Predictor

Lightweight, local Streamlit app to predict delivery delays, generate prioritized corrective actions, and explore delivery performance with interactive visualizations.

---

## Quick start (Windows)

1. Open PowerShell or Git Bash and go to project root:
   ```bash
   cd "d:/SEO consultant - Copy/Search-Engine-Optimization-Tool-main"
   ```

2. (If you don't have the venv) Create and activate a venv:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1   # PowerShell
   # or for cmd:
   .\.venv\Scripts\activate.bat
   ```

3. Install dependencies (if `requirements.txt` exists) or install minimal packages:
   ```bash
   .venv\Scripts\python -m pip install --upgrade pip
   .venv\Scripts\python -m pip install -r requirements.txt
   # If you face a missing package error (e.g., plotly), install manually:
   .venv\Scripts\python -m pip install plotly streamlit pandas scikit-learn joblib
   ```

4. Run the app (recommended: use the venv Python so correct packages are used):
   ```bash
   .venv\Scripts\python -m streamlit run main.py
   ```
   To pick a specific port:
   ```bash
   .venv\Scripts\python -m streamlit run main.py --server.port 8501
   ```

---

## Purpose / What it does

- Loads and merges multiple CSV datasets (orders, delivery performance, routes, costs, fleet).
- Computes derived business metrics (Fuel_per_KM, Total_Cost_INR, Delay_Index, Reliability_Score, etc.).
- Trains/loads a delay prediction model and runs counterfactual simulations to estimate impact of interventions.
- Generates prioritized corrective actions with estimated delay reduction and (optional) CrewAI expansion.
- Interactive dashboard: scatter, histogram, pie, bar, line charts; filters; downloadable CSV exports.

---

## Data requirements

Place CSV files in the `data/` folder. Typical files and columns expected:
- `orders.csv` — Order_ID, Order_Date, Route, Carrier, Priority, ...
- `delivery_performance.csv` — Order_ID, Scheduled_Arrival, Actual_Arrival, Traffic_Delay_Minutes, Weather_Impact, ...
- `routes_distance.csv` — Route, Distance_KM, Baseline_Time
- `cost_breakdown.csv` — Order_ID/Route, Fuel_Cost_INR, Labor_Cost_INR, Maintenance_Cost_INR, Toll_Charges_INR
- `vehicle_fleet.csv` — Vehicle_ID, Fuel_Efficiency, Capacity, Maintenance_History

If some columns are missing the app will use safe defaults (zero or NaN) and continue to run — warnings will appear in the UI.

---

## Main features

- Predict delay for a hypothetical delivery via sidebar inputs.
- Generate prioritized corrective actions (re-route, schedule shift, fuel/vehicle optimization).
- Interactive visualizations (plotly): scatter, histogram, pie, bar, line (hover + zoom).
- Filters: Carrier, Weather, Priority, Date range — dashboard updates dynamically.
- Export: Download filtered dataset and generated actions as CSV.
- CrewAI integration: optional — set up credentials to enable richer action expansion. If unavailable, a local fallback is used.

---

## Recommended workflow

1. Ensure `data/` contains required CSVs.
2. Start app with the venv Python (see Quick start).
3. Use sidebar filters to narrow data; inspect charts and top delayed orders.
4. Use Predict Delay inputs to simulate scenarios and generate corrective actions.
5. Export filtered data and action plans for operational handoff.

---

## Environment notes & troubleshooting

- ModuleNotFoundError for `plotly` or other libs:
  - Ensure you run Streamlit with the venv Python:
    ```
    .venv\Scripts\python -m streamlit run main.py
    ```
  - Or install the missing package into the venv:
    ```
    .venv\Scripts\python -m pip install plotly
    ```

- If the app is served by a different Python (system) and you see missing modules, always use the `.venv\Scripts\python -m streamlit run ...` pattern.

- Port in use:
  - Use `--server.port <port>` to start on a free port.
  - To find processes using a port (PowerShell):
    ```powershell
    netstat -ano | findstr :8501
    tasklist /FI "PID eq <pid>"
    taskkill /PID <pid> /F
    ```

- To force the app to use the local Crew fallback (avoid external LLM attempts), set:
  - PowerShell:
    ```powershell
    $env:FORCE_LOCAL_CREW = '1'
    .venv\Scripts\python -m streamlit run main.py
    ```
  - Git Bash:
    ```bash
    export FORCE_LOCAL_CREW=1
    .venv/Scripts/python -m streamlit run main.py
    ```

---

## Code structure

- `main.py` — Streamlit app and dashboard logic
- `utils/data_processing.py` — data loading and merging (repo-relative paths)
- `utils/metrics.py` — derived metric calculations and missing-data handling
- `predictor.py` — model load/train wrapper and predict API
- `crew_setup.py` — CrewAI creation helper with local fallback
- `data/` — input CSVs (not included)

---

## Success & next steps

- Validate predictions on a held-out period.
- Run sensitivity simulations (multi-scenario) and export priorities.
- If desired, add a scheduled retraining pipeline and richer routing integrations.

---

If you want, I can:
- Add a sample-data generator for demos,
- Produce an installation script (PowerShell) that creates the venv and installs deps,
- Or produce a condensed `requirements-min.txt` for a smaller install.
