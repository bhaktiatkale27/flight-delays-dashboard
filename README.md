# Flight Delays & Jet Fuel Cost - Streamlit Dashboard

1. Put `flight_delays_with_jet_fuel_cost.csv` inside the `data/` folder.
2. `pip install -r requirements.txt`
3. `streamlit run app.py`

Pages: Home, Univariate (5 charts), Bivariate (4), Multivariate (1), Executive Dashboard.

All charts are interactive Plotly versions of the charts in `Flight_Delays_EDA_Project.ipynb`
(histograms, boxplots, scatter, heatmap) and respond to the sidebar filters. Custom helpers: `utils/charts.py`.
