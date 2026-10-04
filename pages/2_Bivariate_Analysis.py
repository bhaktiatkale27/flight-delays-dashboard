import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.charts import horizontal_box, palette
from utils.data import MONTHS, load_data, sidebar_filters
from utils.styles import apply_styles, impact, observation, pl, recommendation, sec, sidebar_nav

st.set_page_config(page_title="Bivariate Analysis", layout="wide")
apply_styles()
sidebar_nav()
f = sidebar_filters(load_data())
flown = f[f["cancelled"] == 0]

st.markdown("# &#128201; Bivariate Analysis")
st.caption("Looking at two columns together")

# 1 ----------------------------------------------------------------
sec("1. Arrival Delay by Airline", "Which airlines are most punctual? (real data, dots = extreme flights)", "&#127970;")
med = flown.groupby("airline")["arr_delay"].median().sort_values()
fig = horizontal_box(flown, "airline", "arr_delay", list(med.index), palette("Spectral", len(med)))
st.plotly_chart(pl(fig, 560), use_container_width=True)
mean = flown.groupby("airline")["arr_delay"].mean().sort_values()
observation(f"Ordered by median delay: <b>{med.index[0]}</b> is the most punctual and <b>{med.index[-1]}</b> the slowest. "
            f"On average <b>{mean.index[-1]}</b> lands latest ({mean.iloc[-1]:.1f} min) and <b>{mean.index[0]}</b> earliest "
            f"({mean.iloc[0]:.1f} min). More dots to the right means less consistency, not just a higher average.")

# 2 ----------------------------------------------------------------
sec("2. Arrival Delay by Scheduled Departure Hour", "Do delays build up through the day?", "&#128336;")
g = f.groupby("dep_hour")["arr_delay"].mean().reset_index()
g["text"] = g["arr_delay"].map(lambda v: f"{v:.1f}")
fig = px.line(g, x="dep_hour", y="arr_delay", text="text", markers=True, color_discrete_sequence=["crimson"],
              labels={"dep_hour": "Scheduled departure hour (24h)", "arr_delay": "Average arrival delay (minutes)"})
fig.update_traces(textposition="top center", textfont_size=10, line=dict(width=3), marker=dict(size=8), hovertemplate="%{x}:00<br>%{y:.1f} min<extra></extra>")
fig.update_layout(xaxis=dict(dtick=1))
st.plotly_chart(pl(fig, 440), use_container_width=True)
observation(f"Early-morning flights are closest to on time; delays pile up later in the day and peak around "
            f"<b>{int(g.loc[g['arr_delay'].idxmax(), 'dep_hour'])}:00</b>. Hours with very few flights can look spiky.")

left, right = st.columns(2)

# 3 ----------------------------------------------------------------
with left:
    sec("3. Average Departure Delay by Month", "Is there a seasonal pattern?", "&#128197;")
    g = f.groupby("month_num")["dep_delay"].mean().reset_index()
    g["month"] = g["month_num"].map(lambda x: MONTHS[x - 1])
    fig = go.Figure(go.Bar(x=g["month"], y=g["dep_delay"], marker_color=palette("RdBu_r", len(g)),
                           text=g["dep_delay"].map(lambda v: f"{v:.1f}"), textposition="outside", cliponaxis=False,
                           hovertemplate="%{x}<br>%{y:.1f} min<extra></extra>"))
    fig.update_xaxes(tickangle=-45, title="Month")
    fig.update_yaxes(title="Average departure delay (minutes)", range=[min(0, g["dep_delay"].min() * 1.3), g["dep_delay"].max() * 1.2])
    st.plotly_chart(pl(fig, 460), use_container_width=True)
    w = g.loc[g["dep_delay"].idxmax()]
    observation(f"<b>{w['month']}</b> has the highest average departure delay ({w['dep_delay']:.1f} min). "
                "Busy summer and holiday/winter months run later.")

# 4 ----------------------------------------------------------------
with right:
    sec("4. Distance vs Estimated Fuel Cost", "What drives fuel cost? (random sample of 5,000 flights)", "&#9981;")
    s = f.sample(min(5000, len(f)), random_state=42)
    fig = px.scatter(s, x="distance", y="est_fuel_cost", opacity=0.4, color_discrete_sequence=["purple"],
                     labels={"distance": "Distance (miles)", "est_fuel_cost": "Estimated fuel cost ($)"})
    st.plotly_chart(pl(fig, 460), use_container_width=True)
    corr = f["distance"].corr(f["est_fuel_cost"])
    observation(f"Fuel cost rises steadily with distance (correlation <b>{corr:.2f}</b>): longer flights burn more fuel "
                "and cost more. Route length drives fuel cost, not punctuality.")

st.markdown("---")
impact("Delays are not random: they depend on the airline, the time of day and the season. Fuel cost depends mainly "
       "on distance, so it can be planned separately from punctuality.")
recommendation("Add schedule buffers in late-day and peak-month flights, learn from the most punctual airlines, "
               "and optimise long routes for fuel.")
