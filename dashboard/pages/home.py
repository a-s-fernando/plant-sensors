import matplotlib.pyplot as plt
import plotly.express as px
from dash import html, dcc, callback, Input, Output, register_page


register_page(__name__, path='/')



layout = html.Section([
                        html.H1(id="break"),
                        html.Div(id='Box plot')
                           ])
