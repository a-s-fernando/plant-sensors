from dash import Dash, html, dcc, page_container, page_registry
import dash_bootstrap_components as dbc
import matplotlib.pyplot as plt


plt.switch_backend('Agg')

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)

navbar = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem(page['name'], href=page['relative_path'])
                for page in page_registry.values()
            ],
            nav=True,
            in_navbar=True,
            label="Pages",
        ),
    ],
    brand="Plant-Sensors",
    color="#74B72E",
)

app.layout = dbc.Container([navbar,
                            page_container,
                            ])
