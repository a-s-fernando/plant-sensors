# pylint: disable=unused-variable

from dash import dcc, register_page, html, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from combine_data import get_comprehensive_records
RECORDS = get_comprehensive_records()

grouped_moisture = RECORDS.groupby([RECORDS['recording_taken'].dt.date, RECORDS['name']])['soil_moisture'].mean()
grouped_moisture = grouped_moisture.to_frame().reset_index(level=[0,1])
grouped_moisture['recording_taken'] = pd.to_datetime(grouped_moisture['recording_taken'])

grouped_temperature = RECORDS.groupby([RECORDS['recording_taken'].dt.date, RECORDS['name']])['temperature'].mean()
grouped_temperature = grouped_temperature.to_frame().reset_index(level=[0,1])
grouped_temperature['recording_taken'] = pd.to_datetime(grouped_temperature['recording_taken'])

register_page(__name__, title="", path='/averages')
# Averages per day for soil moisture and temp. - Callback to pick plants - Alain 

layout = dbc.Container([
    html.H3("Daily Averages"),
    html.P("Select a plant:"),
    dbc.Select(id='select', options=[{"label": plant, "value": plant}
               for plant in grouped_moisture["name"].unique()]),
    dcc.Graph(id="average_moisture"),
    dcc.Graph(id="average_temperature"),
])


@callback(
    Output('average_moisture', 'figure'),
    Input('select', 'value'))
def select_plant_for_moisture_graph(plant):
    """Update the moisture graph element with the selected plant."""
    fig = px.bar(grouped_moisture[grouped_moisture['name'] == plant], x="recording_taken", y="soil_moisture",
                 labels={'soil_moisture': 'Average Soil Moisture', 'recording_taken': 'Date of Recording'})
    return fig

@callback(
    Output('average_temperature', 'figure'),
    Input('select', 'value'))
def select_plant_for_temperature_graph(plant):
    """Update the temperature graph element with the selected plant."""
    fig = px.bar(grouped_temperature[grouped_temperature['name'] == plant], x="recording_taken", y="temperature",
                 labels={'temperature': 'Average Temperature', 'recording_taken': 'Date of Recording'})
    return fig
