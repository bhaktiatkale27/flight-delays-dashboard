# ✈️ Flight Delays & Jet Fuel Cost Analysis Dashboard

An end-to-end exploratory data analysis (EDA) project on **US domestic flights (2019–2023)**, combined with jet fuel price and estimated fuel cost per flight. The analysis is done in a Jupyter Notebook and presented as an interactive **Streamlit dashboard** built with Plotly.

> **Main target column:** `arr_delay` (arrival delay in minutes) — the number that matters most to passengers and airlines.

---

## 📑 Table of Contents

1. [Business Problem](#-business-problem)
2. [Project Objectives](#-project-objectives)
3. [Dataset](#-dataset)
4. [Data Cleaning & Preparation](#-data-cleaning--preparation)
5. [Dashboard Pages & Charts](#-dashboard-pages--charts)
6. [Key Insights](#-key-insights)
7. [Tech Stack](#-tech-stack)
8. [Project Structure](#-project-structure)
9. [Installation & Setup](#-installation--setup)
10. [How to Run](#-how-to-run)
11. [Deploying Online](#-deploying-online-optional)
12. [Future Improvements](#-future-improvements)
13. [Author](#-author)

---

## 🎯 Business Problem

Airlines and passengers are affected every day by late departures, late arrivals, cancellations and rising fuel costs. This project explores US domestic flight records together with jet fuel price and estimated fuel cost to find out **when, where and why flights get delayed**, and what drives fuel cost.

## 📌 Project Objectives

- Understand how delayed flights really are (distribution of departure and arrival delays)
- Find the main causes of delay (carrier, weather, NAS, security, late aircraft)
- Compare airlines on punctuality and cancellation
- Study cancellations and their reasons
- Find the best and worst times to fly (hour, day of week, month)
- Link flight distance with fuel cost
- Generate practical, business-style recommendations

---

## 📂 Dataset

| Item | Details |
|---|---|
| File | `flight_delays_with_jet_fuel_cost.csv` |
| Rows | ~300,000 flights |
| Columns | 26 |
| Period | 2019 – 2023 |
| Scope | US domestic flights |

**Column groups**

| Group | Columns (after renaming) |
|---|---|
| Flight info | `flight_date`, `airline`, `flight_number`, `origin`, `dest` |
| Schedule & actual times | `scheduled_dep_time`, `actual_dep_time`, `scheduled_arr_time`, `actual_arr_time` |
| Delays | `dep_delay`, `arr_delay` |
| Delay causes (minutes) | `delay_due_carrier`, `delay_due_weather`, `delay_due_nas`, `delay_due_security`, `delay_due_late_aircraft` |
| Status | `cancelled`, `cancellation_code` (A = Carrier, B = Weather, C = NAS, D = Security), `diverted` |
| Distance & time | `distance`, `air_time` |
| Fuel | `jet_fuel_price`, `est_fuel_cost` |

> ⚠️ **The CSV is not included in this repository if it is larger than GitHub's 100 MB limit.** Place it in the `data/` folder before running the app (see [Installation](#-installation--setup)).

---

## 🧹 Data Cleaning & Preparation

All steps are done in the notebook and repeated in `utils/data.py` so the dashboard uses the exact same data.

| Step | What was done | Why |
|---|---|---|
| Column names | Converted to lowercase and renamed unclear ones (e.g. `fl_date` → `flight_date`, `crs_dep_time` → `scheduled_dep_time`) | Readability |
| Date type | Converted `flight_date` to `datetime` | Enables month / day-of-week analysis |
| Missing delay causes | Filled with `0` | Empty simply means that cause added zero delay |
| Missing `cancellation_code` | Filled with `"NC"` (Not Cancelled) | Only cancelled flights have a code |
| Missing delay / time values | **Left empty** | These flights were cancelled and never flew; `0` would wrongly mean "on time" |
| Duplicates | Checked and removed | Avoid double counting |
| Extreme values (outliers) | **Found using IQR but kept** | They are real disrupted flights (weather, mechanical issues), not data errors |
| Imbalance | Checked `cancelled` and `diverted` | Both are rare, so the data is imbalanced |
| Helper columns | `month`, `month_num`, `day_of_week`, `dow_num`, `dep_hour`, `year` | Easier time-based charts |

---

## 📊 Dashboard Pages & Charts

The sidebar has three filters — **Year**, **Airline**, **Month** — and a **Reset filters** button. Every chart and KPI updates with the filters, and every chart has data labels and hover tooltips.

### 🏠 Home
- Business problem, objectives and analysis workflow
- Dataset overview (rows, columns, airlines, date range)
- Expandable column reference and sample data

### 📈 Univariate Analysis (one column at a time)
1. **Arrival delay distribution** – histogram with density curve (real values, extremes visible)
2. **Number of flights by airline** – sorted horizontal bar chart
3. **Scheduled departure hour** – flights per hour of day
4. **Delay causes** – five histograms (carrier, weather, NAS, late aircraft, security), counting only flights where that cause added delay
5. **Flights by cancellation code** – log-scale bar chart (NC = Not Cancelled)

### 📉 Bivariate Analysis (two columns together)
1. **Arrival delay by airline** – box plot sorted by median (dots = extreme flights)
2. **Arrival delay by scheduled departure hour** – line chart showing how delays build up
3. **Average departure delay by month** – seasonal pattern
4. **Distance vs estimated fuel cost** – scatter plot (5,000-flight random sample)

### 🔥 Multivariate Analysis (three columns together)
- **Average arrival delay by day of week × departure hour** – heatmap that shows the worst time to fly

### 🎯 Executive Dashboard
- 8 KPI cards: total flights, average arrival delay, on-time rate, average departure delay, cancellation rate, diversion rate, average fuel cost per flight, total estimated fuel cost
- Airline report card (delay, cancellation rate and fuel cost side by side)
- Delay causes and cancellation reasons tables
- Auto-generated management recommendations

---

## 💡 Key Insights

1. **Most flights are on time or close to it.** Delays cluster near zero with a long right tail of badly delayed flights; because of this tail the average delay is higher than the median.
2. **Extreme delays are real, not errors.** The delay-cause columns add up to the total arrival delay, so these are genuinely disrupted flights and were kept.
3. **Carrier and late-aircraft problems are the biggest delay causes.** Weather delays are less frequent but can be very long. Security delays are the rarest.
4. **Time matters.** Delays build up through the day, so early-morning flights are the most reliable and evening flights the least. Day of week and month also change delay levels.
5. **Airlines differ.** Some airlines are consistently more punctual and cancel less than others, and some show more extreme delays (less consistency).
6. **Distance drives fuel cost.** Longer flights burn and cost more fuel; fuel cost depends on route length, not on punctuality.
7. **Cancellations and diversions are rare**, so the data is imbalanced — important if a prediction model is built later.

> The exact numbers update live in the dashboard according to the selected filters.

### Recommendations
- Fix the biggest delay causes first (carrier operations and aircraft turnaround).
- Schedule important or connection-heavy flights in the morning and add buffer time for late-day flights.
- Add staff and buffers during peak-delay months and days.
- Learn from the most punctual airlines.
- Plan fuel purchasing and route optimisation around long-distance flights.
- Track on-time rate, cancellation rate and fuel cost every month.

---

## 🛠️ Tech Stack

| Purpose | Tool |
|---|---|
| Language | Python 3 |
| Data handling | Pandas, NumPy |
| EDA notebook charts | Matplotlib, Seaborn |
| Dashboard | Streamlit |
| Interactive charts | Plotly |
| Notebook | Jupyter |

---

## 🗂️ Project Structure

```
flight_dashboard/
│
├── app.py                          # Home page
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── Flight_Delays_EDA_Project.ipynb # Full EDA notebook
│
├── .streamlit/
│   └── config.toml                 # Streamlit theme/config
│
├── data/
│   └── flight_delays_with_jet_fuel_cost.csv   # Dataset (add this file)
│
├── pages/
│   ├── 1_Univariate_Analysis.py
│   ├── 2_Bivariate_Analysis.py
│   ├── 3_Multivariate_Analysis.py
│   └── 4_Executive_Dashboard.py
│
└── utils/
    ├── data.py                     # Data loading, cleaning, sidebar filters
    ├── styles.py                   # CSS, KPI cards, insight cards, chart layout
    └── charts.py                   # Custom Plotly charts (histogram + density, box plot)
```

---

## ⚙️ Installation & Setup

**1. Clone the repository**
```bash
git clone https://github.com/bhaktiatkale27/flight-delays-dashboard.git
cd flight-delays-dashboard
```

**2. Create and activate a virtual environment (recommended)**
```bash
# Windows (PowerShell)
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add the dataset**

Place `flight_delays_with_jet_fuel_cost.csv` inside the `data/` folder.

---

## ▶️ How to Run

**Dashboard**
```bash
streamlit run app.py
```
The app opens at `http://localhost:8501`.

**Notebook**
```bash
jupyter notebook Flight_Delays_EDA_Project.ipynb
```
Update the CSV path in the first code cell if your file is in a different folder.

---

## 🌐 Deploying Online (optional)

1. Push the project to GitHub (the CSV must be in the repo, or loaded from a link).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **Create app**, choose this repository, set the main file to `app.py`, and deploy.

> Make sure `venv/` is **not** committed — add `venv/` to `.gitignore`.

---

## 🚀 Future Improvements

- Build a machine-learning model to predict arrival delay and cancellation (handling class imbalance)
- Add airport-level analysis (top origin / destination airports and their delays)
- Add a fuel price trend chart over time
- Add a map view of routes and airports
- Add download buttons for filtered data and charts

---

## 👤 Author

**Bhakti Atkale**
GitHub: [@bhaktiatkale27](https://github.com/bhaktiatkale27)

---

⭐ If you found this project useful, consider giving the repository a star!
