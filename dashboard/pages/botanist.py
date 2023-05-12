from datetime import datetime,date
from dash import html, dcc, register_page, callback, Input, Output
import pandas as pd
import plotly.express as px

from combine_data import get_comprehensive_plants

register_page(__name__, path='/botanist')

botanist_df = get_comprehensive_plants()
botanist_df['last_watered'] = pd.to_datetime(botanist_df['last_watered'])

layout = html.Section([
                        dcc.DatePickerRange(id='my-date-picker-range',
                                             initial_visible_month=date(2023, 5, 10)),
                        html.Div(id='Line Graph')
                        ])

@callback(
    Output(component_id='Line Graph', component_property='children'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'))
def update_output(start_date, end_date):
    '''Plot Graph based on date range selected.'''
    
    fig = px.scatter(data_frame=botanist_df.loc[(botanist_df['last_watered']\
                                                  <= datetime.strptime(end_date, '%Y-%m-%d')) &\
                                        (botanist_df['last_watered'] >=\
                                          datetime.strptime(start_date, '%Y-%m-%d'))],\
                                              x='last_watered', y='botanist_fn',\
                                                title="Botanist Watering Times",\
                                                      hover_data='name',\
                                                      labels={"last_watered": "Last Water Date",\
                                                               "botanist_fn": "Botanist"})
    print(start_date, end_date)
    return dcc.Graph(id='Line Graph', figure=fig)
