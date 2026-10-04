import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from utils.charts import hist_bars, hist_kde, palette
from utils.data import CANCEL_LABELS, CAUSE_LABELS, load_data, sidebar_filters
from utils.styles import (apply_styles, fmt_k, impact, kpi, observation, pl, recommendation, sec,
                          sidebar_nav)

st.set_page_config(page_title="Univariate Analysis", layout="wide")
apply_styles()
sidebar_nav()
f = sidebar_filters(load_data())
flown = f[f["cancelled"] == 0]

st.markdown("# &#128200; Univariate Analysis")
st.caption("Looking at one column at a time")

c = st.columns(4)
with c[0]: kpi("&#9992;&#65039; Flights", f"{len(f):,}", color="#0288D1")
with c[1]: kpi("&#9201;&#65039; Avg arrival delay", f"{flown['arr_delay'].mean():.1f} min", color="#22C55E")
with c[2]: kpi("&#128202; Median arrival delay", f"{flown['arr_delay'].median():.0f} min", color="#F9A825")
with c[3]: kpi("&#10060; Cancellation rate", f"{f['cancelled'].mean() * 100:.2f}%", color="#E53935")

# 1 ----------------------------------------------------------------
sec("1. Arrival Delay Distribution", "Do flights land on time? (real numbers - extreme values stay visible)", "&#9201;&#65039;")
fig = hist_kde(flown["arr_delay"], bins=100, color="indianred", xlabel="Arrival delay (minutes)")
st.plotly_chart(pl(fig, 420), use_container_width=True)
arr = flown["arr_delay"].dropna()
observation(f"Most flights land on time or very close to it: <b>{(arr <= 15).mean() * 100:.0f}%</b> arrive within 15 minutes, "
            f"and the middle (median) flight is {arr.median():.0f} min. A long right tail stretches out to "
            f"<b>{arr.max():,.0f} min</b>. Those few extreme flights pull the average ({arr.mean():.1f} min) above the median.")

# 2 & 3 ------------------------------------------------------------
left, right = st.columns(2)
with left:
    sec("2. Number of Flights by Airline", "Who flies the most?", "&#9992;&#65039;")
    a = f["airline"].value_counts().reset_index()
    a.columns = ["airline", "flights"]
    a["text"] = a.apply(lambda r: f"{fmt_k(r['flights'])}  ({r['flights'] / len(f) * 100:.1f}%)", axis=1)
    fig = go.Figure(go.Bar(x=a["flights"], y=a["airline"], orientation="h", text=a["text"],
                           marker_color=palette("Viridis", len(a)), textposition="outside", cliponaxis=False))
    fig.update_yaxes(autorange="reversed", title="")
    fig.update_xaxes(title="Number of flights", range=[0, a["flights"].max() * 1.35])
    st.plotly_chart(pl(fig, 520), use_container_width=True)
    top = a.iloc[0]
    observation(f"<b>{top['airline']}</b> operates the most flights ({top['flights'] / len(f) * 100:.1f}%). "
                "A few big airlines dominate the data.")

with right:
    sec("3. Scheduled Departure Hour", "When do flights depart?", "&#128336;")
    h = f["dep_hour"].value_counts().sort_index().reset_index()
    h.columns = ["hour", "flights"]
    fig = go.Figure(go.Bar(x=h["hour"], y=h["flights"], text=h["flights"].map(fmt_k), textposition="outside",
                           cliponaxis=False, textfont=dict(size=10), marker_color="navy",
                           hovertemplate="%{x}:00<br>%{y:,} flights<extra></extra>"))
    fig.update_layout(bargap=0.05, xaxis=dict(dtick=1, title="Hour of day (24h, from scheduled time)"),
                      yaxis=dict(title="Number of flights", range=[0, h["flights"].max() * 1.15]))
    st.plotly_chart(pl(fig, 520), use_container_width=True)
    h = f["dep_hour"].value_counts()
    observation(f"Departures cluster from morning to early evening and peak around <b>{int(h.idxmax())}:00</b>; "
                "they drop off overnight.")

# 4 ----------------------------------------------------------------
sec("4. Delay Causes (when they happen)", "Each chart only counts flights where that cause added delay minutes", "&#9888;&#65039;")
CAUSE_COLORS = {"delay_due_carrier": "crimson", "delay_due_weather": "slateblue", "delay_due_nas": "goldenrod",
                "delay_due_late_aircraft": "brown", "delay_due_security": "gray"}
cols = list(CAUSE_COLORS)
titles = []
for col in cols:
    n = int((f[col] > 0).sum())
    titles.append(f"{CAUSE_LABELS[col]} - {n:,} flights ({n / len(f) * 100:.2f}%)")
fig = make_subplots(rows=2, cols=3, subplot_titles=titles, vertical_spacing=0.2, horizontal_spacing=0.07)
for i, col in enumerate(cols):
    nz = f.loc[f[col] > 0, col]
    if len(nz):
        fig.add_trace(hist_bars(nz, bins=40, color=CAUSE_COLORS[col], label_min_frac=0.3),
                      row=i // 3 + 1, col=i % 3 + 1)
fig.update_annotations(font_size=12)
fig.update_xaxes(title_text="Delay minutes")
fig.update_yaxes(title_text="Flights")
fig.update_layout(bargap=0.02)
st.plotly_chart(pl(fig, 600), use_container_width=True)
cz = pd.Series({CAUSE_LABELS[c]: f[c].sum() for c in CAUSE_LABELS}).sort_values(ascending=False)
observation(f"<b>{cz.index[0]}</b> and <b>{cz.index[1]}</b> create most of the delay minutes; <b>{cz.index[-1]}</b> is the "
            "smallest. Weather delays are rarer but can be very long when they happen.")

# 5 ----------------------------------------------------------------
sec("5. Flights by Cancellation Code", "NC = Not Cancelled (log scale so small bars stay visible)", "&#10060;")
cc = f["cancellation_code"].value_counts().reset_index()
cc.columns = ["code", "flights"]
cc["label"] = cc["code"].map({**CANCEL_LABELS, "NC": "Not cancelled"})
cc["text"] = cc.apply(lambda r: f"{r['flights']:,}  ({r['flights'] / len(f) * 100:.2f}%)", axis=1)
fig = go.Figure(go.Bar(x=cc["code"], y=cc["flights"], text=cc["text"], customdata=cc["label"],
                       marker_color=px.colors.qualitative.Set2[:len(cc)], textposition="outside",
                       cliponaxis=False, hovertemplate="%{customdata}<br>%{y:,} flights<extra></extra>"))
fig.update_yaxes(type="log", title="Number of flights (log scale)")
fig.update_xaxes(title="Cancellation code (A=Carrier, B=Weather, C=NAS, D=Security)")
st.plotly_chart(pl(fig, 420), use_container_width=True)
cx = cc[cc["code"] != "NC"]
if cx.empty:
    observation("No cancelled flights in the current selection.")
else:
    observation(f"Almost all flights are <b>NC</b> (not cancelled). Among cancellations, <b>{cx.iloc[0]['label']}</b> is the "
                f"top reason. Only {f['cancelled'].mean() * 100:.2f}% of flights are cancelled, so the data is imbalanced.")

st.markdown("---")
impact("Most flights are fine, but a small share of badly delayed flights and a few dominant causes "
       "(carrier and late aircraft) create most of the lost time. Cancellations are rare yet costly.")
recommendation("Focus on the biggest delay causes first (carrier and late-aircraft turnaround), and keep "
               "weather/security cancellation playbooks ready.")
