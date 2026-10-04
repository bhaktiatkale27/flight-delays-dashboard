"""Data loading + cleaning (same steps as the notebook; extreme values are kept) and sidebar filters."""
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
CSV_NAME = "flight_delays_with_jet_fuel_cost.csv"
CANDIDATES = [ROOT / "data" / CSV_NAME, ROOT / CSV_NAME]

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
CANCEL_LABELS = {"A": "Carrier", "B": "Weather", "C": "NAS / Air traffic", "D": "Security"}
CAUSE_LABELS = {
    "delay_due_carrier": "Carrier",
    "delay_due_weather": "Weather",
    "delay_due_nas": "NAS (Air traffic)",
    "delay_due_security": "Security",
    "delay_due_late_aircraft": "Late aircraft",
}


@st.cache_data(show_spinner="Loading data...")
def _load(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip().str.lower()
    df = df.rename(columns={
        "fl_date": "flight_date", "fl_number": "flight_number",
        "crs_dep_time": "scheduled_dep_time", "crs_arr_time": "scheduled_arr_time",
        "dep_time": "actual_dep_time", "arr_time": "actual_arr_time",
    })
    df["flight_date"] = pd.to_datetime(df["flight_date"])
    causes = list(CAUSE_LABELS)
    df[causes] = df[causes].fillna(0)
    df["cancellation_code"] = df["cancellation_code"].fillna("NC")
    df = df.drop_duplicates()
    df["year"] = df["flight_date"].dt.year
    df["month_num"] = df["flight_date"].dt.month
    df["month"] = df["flight_date"].dt.month_name()
    df["dow_num"] = df["flight_date"].dt.dayofweek
    df["day_of_week"] = df["flight_date"].dt.day_name()
    df["dep_hour"] = (df["scheduled_dep_time"] // 100).astype(int) % 24
    return df


def load_data() -> pd.DataFrame:
    for p in CANDIDATES:
        if p.exists():
            return _load(str(p))
    st.error(f"CSV not found. Put **{CSV_NAME}** inside the `data` folder of this project and refresh.")
    st.stop()


def _reset_filters():
    for k in ("f_year", "f_airline", "f_month"):
        st.session_state[k] = "All"


def sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Three simple dropdowns. Leave on 'All' to see everything."""
    st.sidebar.markdown("### &#128270; Filters")
    st.sidebar.caption("Pick a value, or leave it on **All**.")
    year = st.sidebar.selectbox("Year", ["All"] + sorted(df["year"].unique().tolist()), key="f_year")
    airline = st.sidebar.selectbox("Airline", ["All"] + sorted(df["airline"].unique().tolist()), key="f_airline")
    month = st.sidebar.selectbox("Month", ["All"] + MONTHS, key="f_month")
    st.sidebar.button("Reset filters", on_click=_reset_filters, use_container_width=True)

    f = df
    if year != "All":
        f = f[f["year"] == year]
    if airline != "All":
        f = f[f["airline"] == airline]
    if month != "All":
        f = f[f["month"] == month]

    st.sidebar.info(f"**{len(f):,}** of {len(df):,} flights")
    if f.empty:
        st.warning("No flights match this combination. Click **Reset filters** in the sidebar.")
        st.stop()
    return f
