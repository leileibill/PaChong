import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
from checkee_analyze import *
from datetime import datetime
import pandas as pd

# load month table from csv
df_embassy, df_visa = load_and_process_by_category()

embassies = ['BeiJing', 'ShangHai', 'GuangZhou', 'ShenYang', 'ChengDu']
visas = ['F1', 'J1', 'H1', 'H4', 'B1', 'B2']

category_layout = html.Div([
    dcc.Graph(
        id='embassy',
        figure={
        'data': [
            go.Bar(
                x = embassies,
                y = df_embassy.loc[embassies, 'Waiting Day(s)'],
                # marker=dict(color='#2ca02c',)   # cooked asparagus green
            ),
        ],
        'layout': go.Layout(
            title='Avarege waiting days for cleared applications in the past 30 days by Embassy',
            xaxis={'title': 'Date'},
            yaxis={'title': 'Average waiting days'},
            # barmode='stack',
            # hovermode='closest'
        )
        }
    ),
    dcc.Graph(
        id='visa',
        figure={
        'data': [
            go.Bar(
                x = visas,
                y = df_visa.loc[visas, 'Waiting Day(s)'],
                # marker=dict(color='#2ca02c',)   # cooked asparagus green
            ),
        ],
        'layout': go.Layout(
            title='Avarege waiting days for cleared applications in the past 30 days by Visa type',
            xaxis={'title': 'Date'},
            yaxis={'title': 'Average waiting days'},
            # barmode='stack',
            # hovermode='closest'
        )
        }
    ),
])
