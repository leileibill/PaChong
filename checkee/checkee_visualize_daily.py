import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
from checkee_analyze import *
from datetime import datetime

# load month table from csv
month_date, month_ratio, month_total, \
month_clear, month_pending , month_reject, \
month_average, month_median = load_and_process_month('2019-01')

month_date = [datetime.strptime(date, '%Y-%m-%d') for date in month_date]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

daily_layout = html.Div([
    dcc.Graph(
        id='number',
        figure={
        'data': [
            go.Bar(
                x=month_date,
                y=month_clear,
                name='Clear',
                marker=dict(
                    color='#2ca02c',    # cooked asparagus green
                )
            ),
            go.Bar(
                x=month_date,
                y=month_reject,
                name='Reject',
                marker=dict(
                    color='#d62728',    # brick red
                )                
            ),
            go.Bar(
                x=month_date,
                y=month_pending,
                name='Pending',
                marker=dict(
                    color='#1f77b4',    # muted blue
                )                
            )
        ],
        'layout': go.Layout(
            title='Case status by check dates',
            xaxis={'title': 'Date'},
            yaxis={'title': 'Number of cases'},
            barmode='stack',
            # hovermode='closest'
        )
        }        
    ),
    dcc.Graph(
        id='duration',
        figure={
        'data': [
            go.Bar(
                x=month_date,
                y=month_average,
                name='Clear'
            ),
        ],
        'layout': go.Layout(
            title='Average waiting time by check dates',
            xaxis={'title': 'Date'},
            yaxis={'title': 'Waiting days'},
            showlegend=True
        )
        }        
    ),
    dcc.Graph(
        id='duration',
        figure={
        'data': [
            go.Bar(
                x=month_date,
                y=month_average,
                name='Clear'
            ),
        ],
        'layout': go.Layout(
            title='Number of cleared cases by clear dates (under development)',
            xaxis={'title': 'Date'},
            yaxis={'title': 'Waiting days'},
            showlegend=True
        )
        }        
    ),
])
