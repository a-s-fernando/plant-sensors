from dash import Dash, html, dcc, page_container, page_registry
import matplotlib.pyplot as plt


plt.switch_backend('Agg')

app = Dash(__name__, use_pages=True)

app.layout = html.Div([
    html.H1('Plant Sensor Dashboard'),

    html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{page['name']} - {page['path']}", href=page["relative_path"]
                )
            )
            for page in page_registry.values()
        ]
    ),

    page_container
])