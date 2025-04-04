
# ⛽ NSW Fuel Price Dashboard



Welcome to the **NSW FuelApp** – a project built to fetch, clean, and visualize live fuel price data from New South Wales, Australia. This repository demonstrates a complete **ETL (Extract, Transform, Load)** pipeline in Python, with a simple dashboard for fuel price insights.

---

## 🚀 Tech Stack

<p align="left">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" />
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" />
  <img src="https://img.shields.io/badge/Dash-00AEEF?style=for-the-badge&logo=plotly&logoColor=white" />
  <img src="https://img.shields.io/badge/JSON-000000?style=for-the-badge&logo=json&logoColor=white" />
</p>

---

## 📦 Project Structure

```
NSW_FuelApp/
│
├── NswAPI_call.py       # Extracts raw data from NSW Fuel API
├── DB_Ingest.py         # Loads raw API data into SQLite DB
├── Dataclean.py         # Cleans and transforms the raw data
├── Fueldashboard2.py    # Creates a dashboard to visualize the data
├── fuel_data.db         # SQLite DB storing stations and prices
└── README.md            # You're here!
```

---

## 🔄 ETL Pipeline Breakdown

### 1. `NswAPI_call.py` – **Extract**

This module connects to the official NSW Government Fuel API to retrieve real-time data about fuel stations and prices. It structures the data into a dictionary ready for ingestion.

### 2. `DB_Ingest.py` – **Load**

- Reads the structured data from `NswAPI_call`.
- Creates two tables: `stations` and `prices` in a local `SQLite` database.
- Inserts or updates the records to ensure the latest data is maintained.

### 3. `Dataclean.py` – **Transform**

- Fetches raw data from the SQLite DB.
- Standardizes station names and addresses.
- Fills in missing values and enforces consistent data types.
- Re-uploads the cleaned data back to the DB.

### 4. `Fueldashboard2.py` – **Visualize**

- Creates an interactive dashboard using Dash/Plotly.
- Displays current fuel prices, price trends, and station locations.
- Helps analyze and compare fuel prices across regions and fuel types.

---

## 🗺️ ETL Architecture Diagram

```mermaid
graph TD
    A[NSW Fuel API] --> B[NswAPI_call.py]
    B --> C[DB_Ingest.py]
    C --> D[SQLite Database (fuel_data.db)]
    D --> E[Dataclean.py]
    E --> D
    D --> F[Fueldashboard2.py]
    F --> G[Interactive Dash Dashboard]
```

---

## 🔧 Usage Instructions

1. **Clone the Repository**
```bash
git clone https://github.com/llEraserheadll/NSW_FuelApp.git
cd NSW_FuelApp
```

2. **Install Requirements**
```bash
pip install -r requirements.txt
```

3. **Run the ETL Pipeline**
```bash
python NswAPI_call.py
python DB_Ingest.py
python Dataclean.py
```

4. **Launch the Dashboard**
```bash
python Fueldashboard2.py
```

The dashboard should open at `http://127.0.0.1:8050/`

---

## 🌟 Features

- Live API data fetch from NSW Government API
- Local DB creation and update
- Clean and well-structured data handling with Pandas
- Interactive visualizations with filtering options

---

## 🛠️ Future Improvements

- Dockerize the pipeline for deployment
- Add automated scheduling with cron/airflow
- Expand dashboard features with predictive trends

---

Feel free to explore, fork, and contribute to the project!

Made with ❤️ by `llEraserheadll`
