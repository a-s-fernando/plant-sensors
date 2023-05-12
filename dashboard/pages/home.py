from dash import html, register_page
import dash_bootstrap_components as dbc


register_page(__name__, path='/')



layout = dbc.Container([
    html.H2("LMNH Plant-Sensor Visualisations"),
    html.H3("Click pages to navigate the visualisations.")
])
