import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import pandas as pd
import streamlit as st

from utils.data import load_data
from utils.styles import apply_styles, sidebar_nav

st.set_page_config(page_title="Flight Delays Analysis", layout="wide", initial_sidebar_state="expanded")
apply_styles()
sidebar_nav()
df = load_data()

st.markdown("# &#9992;&#65039; Flight Delays & Jet Fuel Cost Analysis Dashboard")
st.caption("US domestic flights, 2019-2023  |  main target column: arrival delay")

st.markdown("## &#127919; Business Problem")
st.info("""
Airlines and passengers are affected every day by late departures, late arrivals, cancellations and rising
fuel costs. This project explores US domestic flight records combined with jet fuel price and estimated fuel
cost per flight, to find **when, where and why flights get delayed** and what drives fuel cost.
""")

st.markdown("## &#128204; Project Objectives")
c1, c2 = st.columns(2)
c1.markdown("""<div class="card">
✓ Understand how delayed flights really are<br>✓ Find the main causes of delay<br>
✓ Compare airlines on punctuality<br>✓ Study cancellations</div>""", unsafe_allow_html=True)
c2.markdown("""<div class="card">
✓ Find the worst times to fly<br>✓ Link flight distance with fuel cost<br>
✓ Spot patterns across time and airlines<br>✓ Generate practical recommendations</div>""",
            unsafe_allow_html=True)

st.markdown("## &#128260; Analysis Workflow")
c = st.columns(4)
for col, t in zip(c, ["\U0001F4C2 Data Collection", "\U0001F9F9 Data Cleaning", "\U0001F4CA Exploratory Analysis", "\U0001F4A1 Business Insights"]):
    col.info(t)

st.markdown("## &#128202; Dataset Overview")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Rows", f"{df.shape[0]:,}")
c2.metric("Columns", df.shape[1])
c3.metric("Airlines", df["airline"].nunique())
c4.metric("Date range", f"{df['flight_date'].min():%b %Y} - {df['flight_date'].max():%b %Y}")

with st.expander("\U0001F4CB View Column Reference"):
    st.dataframe(pd.DataFrame({"Column Name": df.columns, "Data Type": df.dtypes.astype(str)}),
                 use_container_width=True)
with st.expander("\U0001F50D View Sample Data (First 10 Rows)"):
    st.dataframe(df.head(10), use_container_width=True)
st.caption("Use the sidebar to open the analysis pages.")
