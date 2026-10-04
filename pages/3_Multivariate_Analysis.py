import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import plotly.express as px
import streamlit as st

from utils.data import DAYS, load_data, sidebar_filters
from utils.styles import apply_styles, impact, observation, pl, recommendation, sec, sidebar_nav

st.set_page_config(page_title="Multivariate Analysis", layout="wide")
apply_styles()
sidebar_nav()
f = sidebar_filters(load_data())
flown = f[f["cancelled"] == 0]

st.markdown("# &#128293; Multivariate Analysis")
st.caption("Looking at three columns together")

sec("Average Arrival Delay by Day of Week and Departure Hour", "When is the worst time to fly?", "&#128293;")

pv = flown.pivot_table(index="dow_num", columns="dep_hour", values="arr_delay", aggfunc="mean")
cnt = flown.pivot_table(index="dow_num", columns="dep_hour", values="arr_delay", aggfunc="size")
pv.index = [DAYS[i] for i in pv.index]
cnt.index = pv.index

fig = px.imshow(pv, aspect="auto", text_auto=".0f", color_continuous_scale="YlOrRd",
                labels=dict(x="Scheduled departure hour", y="Day of week", color="Avg arrival delay (min)"))
fig.update_traces(textfont_size=10)
fig.update_xaxes(dtick=1)
st.plotly_chart(pl(fig, 520), use_container_width=True)

s = pv.where(cnt >= 30).stack().dropna()          # pick the worst slot only among cells with enough flights
note = ", slots with under 30 flights ignored"
if s.empty:                              # very narrow filter: no cell has 30 flights, so use all cells
    s, note = pv.stack().dropna(), ", based on small samples"
worst_day, worst_hour = s.idxmax()
observation(f"Darker boxes mean worse delays for that day and hour combined. The worst reliable slot is "
            f"<b>{worst_day} at {int(worst_hour)}:00</b> ({s.max():.0f} min on average{note}). "
            "Early morning stays cooler on almost every day.")
impact("Time of day and day of week together tell more than either alone. Late-evening flights on busy weekdays "
       "carry the highest risk of long delays and missed connections.")
recommendation("Schedule important or connection-heavy flights in the morning, and add buffer time and spare crew "
               "for the darkest evening slots.")
