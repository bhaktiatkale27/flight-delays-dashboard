"""Plotly versions of the notebook's seaborn charts that have no one-line equivalent."""
import numpy as np
import plotly.graph_objects as go
from plotly.colors import sample_colorscale


def palette(name, n):
    """n colours spread across a named Plotly colour scale (like a seaborn palette)."""
    pts = [0.5] if n == 1 else list(np.linspace(0, 1, n))
    return sample_colorscale(name, pts)


def _k(v):
    return f"{v / 1000:.1f}k" if v >= 1000 else f"{v:,.0f}"


def hist_bars(values, bins=40, color="steelblue", label_min_frac=0.25, unit="min"):
    """Histogram drawn as bars with data labels on the taller bins (labelling all bins would be unreadable)."""
    x = np.asarray(values, dtype=float)
    x = x[~np.isnan(x)]
    counts, edges = np.histogram(x, bins=bins)
    centers = (edges[:-1] + edges[1:]) / 2
    text = [_k(c) if c >= label_min_frac * counts.max() else "" for c in counts]
    return go.Bar(x=centers, y=counts, width=np.diff(edges), text=text, textposition="outside", cliponaxis=False,
                  textfont=dict(size=9), marker=dict(color=color, line=dict(width=0)), showlegend=False,
                  hovertemplate="%{x:.0f} " + unit + "<br>%{y:,} flights<extra></extra>")


def hist_kde(values, bins=100, color="steelblue", xlabel="", ylabel="Number of flights"):
    """seaborn histplot(kde=True): bars + a smoothed density curve in 'count' units."""
    x = np.asarray(values, dtype=float)
    x = x[~np.isnan(x)]
    counts, edges = np.histogram(x, bins=bins)
    centers = (edges[:-1] + edges[1:]) / 2
    k = np.exp(-0.5 * (np.arange(-8, 9) / 2.0) ** 2)          # gaussian, sigma = 2 bins
    smooth = np.convolve(counts, k / k.sum(), mode="same")
    fig = go.Figure()
    text = [_k(c) if c >= 0.10 * counts.max() else "" for c in counts]      # label the taller bins only
    fig.add_bar(x=centers, y=counts, width=np.diff(edges), text=text, textposition="outside", cliponaxis=False,
                textfont=dict(size=9), marker=dict(color=color, opacity=0.6, line=dict(width=0)),
                name="Flights", hovertemplate="%{x:.0f} min<br>%{y:,} flights<extra></extra>")
    fig.add_scatter(x=centers, y=smooth, mode="lines", line=dict(color=color, width=2.5), name="Density curve",
                    hoverinfo="skip")
    fig.update_layout(bargap=0, showlegend=False)
    fig.update_xaxes(title=xlabel)
    fig.update_yaxes(title=ylabel)
    return fig


def horizontal_box(df, cat, val, order, colors, max_outliers=400, seed=42):
    """seaborn horizontal boxplot with the REAL full data. Quartiles/whiskers are computed from every row;
    only the outlier dots are thinned (max_outliers per box) so the browser stays fast."""
    rng = np.random.default_rng(seed)
    fig = go.Figure()
    labels = []
    for c, col in zip(order, colors):
        s = df.loc[df[cat] == c, val].dropna().to_numpy()
        if len(s) == 0:
            continue
        q1, med, q3 = np.percentile(s, [25, 50, 75])
        c = f"{c}  (median {med:.0f})"          # data label: median shown next to each name
        labels.append(c)
        iqr = q3 - q1
        lo, hi = s[s >= q1 - 1.5 * iqr].min(), s[s <= q3 + 1.5 * iqr].max()
        out = s[(s < lo) | (s > hi)]
        if len(out) > max_outliers:
            out = rng.choice(out, max_outliers, replace=False)
        fig.add_trace(go.Box(y=[c], q1=[q1], median=[med], q3=[q3], lowerfence=[lo], upperfence=[hi],
                             orientation="h", name=c, fillcolor=col, line=dict(color="#334155", width=1.2),
                             showlegend=False, hoverinfo="x"))
        fig.add_trace(go.Scatter(x=out, y=[c] * len(out), mode="markers", showlegend=False, hoverinfo="x",
                                 marker=dict(size=3.5, color="#1E293B", opacity=0.45)))
    fig.update_yaxes(categoryorder="array", categoryarray=labels[::-1], title="")
    fig.update_xaxes(title="Arrival delay (minutes)")
    return fig
