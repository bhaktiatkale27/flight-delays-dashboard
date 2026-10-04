import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
import streamlit as st

from utils.data import CANCEL_LABELS, CAUSE_LABELS, DAYS, MONTHS, load_data, sidebar_filters
from utils.styles import apply_styles, kpi, sec, sidebar_nav

st.set_page_config(page_title="Executive Dashboard", layout="wide")
apply_styles()
sidebar_nav()
f = sidebar_filters(load_data())
flown = f[f["cancelled"] == 0]

st.markdown("# &#127919; Executive Dashboard")
st.caption("High-level overview for the current filters")

sec("Key Performance Indicators", icon="&#128200;")
on_time = (flown["arr_delay"] <= 15).mean() * 100
c = st.columns(4)
with c[0]: kpi("&#9992;&#65039; Total Flights", f"{len(f):,}", color="#0288D1")
with c[1]: kpi("&#9201;&#65039; Avg Arrival Delay", f"{flown['arr_delay'].mean():.1f} min", f"median {flown['arr_delay'].median():.0f} min", "#22C55E")
with c[2]: kpi("&#9989; On-time Rate", f"{on_time:.1f}%", "arrived within 15 min", "#00ACC1")
with c[3]: kpi("&#128747; Avg Departure Delay", f"{flown['dep_delay'].mean():.1f} min", color="#F9A825")
c = st.columns(4)
with c[0]: kpi("&#10060; Cancellation Rate", f"{f['cancelled'].mean() * 100:.2f}%", color="#E53935")
with c[1]: kpi("&#128256; Diversion Rate", f"{f['diverted'].mean() * 100:.2f}%", color="#7E57C2")
with c[2]: kpi("&#9981; Avg Fuel Cost / Flight", f"${f['est_fuel_cost'].mean():,.0f}", color="#F97316")
with c[3]: kpi("&#128176; Total Est. Fuel Cost", f"${f['est_fuel_cost'].sum() / 1e6:,.1f} M", color="#8D6E63")

sec("Airline Report Card", "Delay, cancellation and fuel cost side by side", "&#128203;")
rc = f.groupby("airline").agg(
    flights=("airline", "size"),
    avg_dep_delay_min=("dep_delay", "mean"),
    avg_arr_delay_min=("arr_delay", "mean"),
    cancellation_rate_pct=("cancelled", lambda s: s.mean() * 100),
    avg_fuel_cost_usd=("est_fuel_cost", "mean"),
).round(2).sort_values("avg_arr_delay_min", ascending=False)
st.dataframe(rc, use_container_width=True)

left, right = st.columns(2)
cz = pd.DataFrame({
    "Cause": list(CAUSE_LABELS.values()),
    "% of flights": [(f[col] > 0).mean() * 100 for col in CAUSE_LABELS],
    "Total minutes": [f[col].sum() for col in CAUSE_LABELS],
}).sort_values("% of flights", ascending=False).round(2)
with left:
    sec("Delay Causes", "Share of flights affected", "&#9888;&#65039;")
    st.dataframe(cz, use_container_width=True, hide_index=True)
with right:
    sec("Cancellation Reasons", "Cancelled flights only", "&#10060;")
    cc = f[f["cancelled"] == 1]["cancellation_code"].map(CANCEL_LABELS).value_counts().reset_index()
    cc.columns = ["Reason", "Flights"]
    if len(cc):
        cc["Share %"] = (cc["Flights"] / cc["Flights"].sum() * 100).round(1)
    st.dataframe(cc, use_container_width=True, hide_index=True)

sec("Management Recommendations", "Generated from the current selection", "&#128161;")
best, worst = rc["avg_arr_delay_min"].idxmin(), rc["avg_arr_delay_min"].idxmax()
by_month = f.dropna(subset=["dep_delay"]).groupby("month_num")["dep_delay"].mean()
by_dow = flown.groupby("dow_num")["arr_delay"].mean()
hh = flown.groupby("dep_hour")["arr_delay"].agg(["mean", "size"])
hh = hh[hh["size"] >= 100] if (hh["size"] >= 100).any() else hh   # narrow filters: fall back to all hours

recs = [
    ("Improve punctuality at the weakest airlines",
     f"<b>{worst}</b> has the highest average arrival delay ({rc.loc[worst, 'avg_arr_delay_min']:.1f} min) while "
     f"<b>{best}</b> is the best ({rc.loc[best, 'avg_arr_delay_min']:.1f} min). Study the best performer's practices."),
    ("Target the biggest delay cause",
     f"<b>{cz.iloc[0]['Cause']}</b> delays affect the most flights. Fix operations there first."),
    ("Plan for peak-delay periods",
     f"Departure delays peak in <b>{MONTHS[by_month.idxmax() - 1]}</b>; arrival delays are worst on "
     f"<b>{DAYS[by_dow.idxmax()]}</b>. Add buffers and staff in these periods."),
    ("Move key flights earlier in the day",
     f"Delays are worst around <b>{int(hh['mean'].idxmax())}:00</b>; early-morning departures are the most reliable."),
    ("Control fuel cost through route planning",
     "Fuel cost follows distance, not punctuality - optimise route length and fuel purchasing."),
    ("Keep monitoring KPIs",
     "Track on-time rate, cancellation rate and fuel cost every month to catch problems early."),
]
for i, (t, d) in enumerate(recs, 1):
    st.markdown(f'<div class="rec"><b>{i}. {t}</b><br>{d}</div>', unsafe_allow_html=True)
