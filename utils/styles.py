"""Look & feel: CSS, sidebar navigation, KPI cards, section headers, insight cards, chart helpers."""
import streamlit as st

BLUE = ["#BFE6FA", "#0288D1"]                 # light -> dark blue (value based)
ORANGE = ["#FB8C3C", "#9C3511"]
GREEN = "#22C55E"
MIXED = ["#0288D1", "#F97316", "#22C55E", "#E53935", "#7E57C2", "#00ACC1", "#F9A825", "#8D6E63"]
ORANGE_STEPS = ["#F97316", "#EA580C", "#C2410C", "#9A3412", "#7C2D12"]


def apply_styles():
    st.markdown(
        """
        <style>
        .block-container {padding-top: 1.6rem; max-width: 1350px;}
        [data-testid="stSidebarNav"] {display: none;}
        h1, h2, h3 {color: #0F172A;}

        .kpi {background:#fff; border-radius:12px; padding:16px 18px; margin-bottom:12px;
              box-shadow:0 1px 6px rgba(15,23,42,.12); border-top:5px solid var(--c);}
        .kpi .l {font-size:12px; color:#475569; font-weight:700; text-transform:uppercase; letter-spacing:.5px;}
        .kpi .v {font-size:28px; font-weight:800; color:#0F172A; margin-top:2px;}
        .kpi .s {font-size:12px; color:#64748B; margin-top:2px;}

        .sec {margin:20px 0 6px 0; padding-left:12px; border-left:6px solid #F97316;}
        .sec .t {font-size:21px; font-weight:800; color:#0F172A;}
        .sec .d {font-size:14px; color:#64748B;}
        .sec .ico {font-size:22px;}

        .ic {border-radius:10px; padding:12px 18px; margin:8px 0 14px 0; line-height:1.6;
             font-size:15px; border-left:6px solid var(--b); background:var(--bg); color:var(--fg);}
        .ic .h {font-weight:800; margin-bottom:2px;}
        .ic-obs {--b:#0288D1; --bg:#E3F2FD; --fg:#0B3954;}
        .ic-imp {--b:#F97316; --bg:#FFF1E6; --fg:#7C2D12;}
        .ic-rec {--b:#22C55E; --bg:#E8F8EE; --fg:#14532D;}

        .card {background:#E8F5E9; padding:22px; border-radius:10px; min-height:200px;
               font-size:18px; font-weight:600; color:#0F172A; line-height:2;}
        .rec {background:#fff; border-left:6px solid #22C55E; border-radius:8px; padding:12px 18px;
              margin-bottom:10px; box-shadow:0 1px 5px rgba(15,23,42,.10); color:#0F172A;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def sidebar_nav():
    with st.sidebar:
        st.markdown("## &#9992;&#65039; Flight Delays Analysis")
        st.page_link("app.py", label="Home", icon="\U0001F3E0")
        st.page_link("pages/1_Univariate_Analysis.py", label="Univariate Analysis", icon="\U0001F4C8")
        st.page_link("pages/2_Bivariate_Analysis.py", label="Bivariate Analysis", icon="\U0001F4C9")
        st.page_link("pages/3_Multivariate_Analysis.py", label="Multivariate Analysis", icon="\U0001F525")
        st.page_link("pages/4_Executive_Dashboard.py", label="Executive Dashboard", icon="\U0001F3AF")
        st.markdown("---")


def kpi(label, value, sub="", color="#0288D1"):
    st.markdown(f'<div class="kpi" style="--c:{color}"><div class="l">{label}</div>'
                f'<div class="v">{value}</div><div class="s">{sub}</div></div>', unsafe_allow_html=True)


def sec(title, subtitle="", icon=""):
    ic = f'<span class="ico">{icon}</span> ' if icon else ""
    st.markdown(f'<div class="sec"><div class="t">{ic}{title}</div><div class="d">{subtitle}</div></div>',
                unsafe_allow_html=True)


def _card(kind, head, text):
    st.markdown(f'<div class="ic ic-{kind}"><div class="h">{head}</div>{text}</div>', unsafe_allow_html=True)


def observation(text):    _card("obs", "Observation", text)
def impact(text):         _card("imp", "Business Impact", text)
def recommendation(text): _card("rec", "Recommendation", text)


def pl(fig, height=420, title=None):
    """Consistent white-card Plotly layout."""
    fig.update_layout(template="plotly_white", height=height, paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
                      margin=dict(l=10, r=20, t=50 if title else 30, b=10), font=dict(size=13, color="#0F172A"),
                      legend_title_text="", title=dict(text=title, font=dict(size=16)) if title else None,
                      uniformtext_minsize=9)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="#E5E9F0")
    return fig


def fmt_k(v):
    """12345 -> '12.3k'"""
    return f"{v / 1000:.1f}k" if abs(v) >= 1000 else f"{v:,.0f}"
