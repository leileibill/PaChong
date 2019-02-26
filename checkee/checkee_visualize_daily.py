import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
from checkee_analyze import *
from datetime import datetime, timedelta

# load month table from csv
month_date, month_ratio, month_total, \
month_clear, month_pending , month_reject, \
month_average, month_median = load_and_process_month('2019-01')

month_date = [datetime.strptime(date, '%Y-%m-%d') for date in month_date]

current_date = datetime.now()
two_months_ago = current_date - timedelta(weeks=8)

# data by clear dates
date_by_clear_dates, total_by_clear_dates, waiting_days = load_and_process_by_clear_dates()

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
                marker=dict(color='#2ca02c')    # cooked asparagus green
            ),
            go.Bar(
                x=month_date,
                y=month_reject,
                name='Reject',
                marker=dict(color='#d62728')    # brick red
            ),
            go.Bar(
                x=month_date,
                y=month_pending,
                name='Pending',
                marker=dict(color='#1f77b4')    # muted blue
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
    # dcc.Graph(
    #     id='clear_dates',
    #     figure={
    #     'data': [
    #         go.Bar(
    #             x=month_date,
    #             y=month_average,
    #             name='Clear'
    #         ),
    #     ],
    #     'layout': go.Layout(
    #         title='Average waiting time by check dates',
    #         xaxis={'title': 'Date'},
    #         yaxis={'title': 'Waiting days'},
    #         showlegend=True
    #     )
    #     }
    # ),
    dcc.Graph(
        id='duration',
        figure={
        'data': [
            go.Bar(
                x=date_by_clear_dates,
                y=total_by_clear_dates,
                name='Total'
            ),
        ],
        'layout': go.Layout(
            title='Number of complete cases by complete dates',
            xaxis={'title': 'Complete date',
                   'range': [two_months_ago, current_date]
            },
            yaxis={'title': 'Number of cases'},
            # showlegend=True
        )
        }
    ),
    dcc.Graph(
        id='histogram',
        figure={
        'data': [
            go.Histogram(
                x=waiting_days,
                # histnorm='probability
                xbins=dict(size=5),
                marker=dict(
                    color='rgb(158,202,225)',
                    line=dict(
                        color='rgb(8,48,107)',
                        width=1.5,
                    )
                ),
            ),
        ],
        'layout': go.Layout(
            title='Distribution of waiting days for cases cleared in the past 4 weeks',
            xaxis={'title': 'Waiting days',
                   'range': [0, 90]
            },
            yaxis={'title': 'Number of cases'},
            # showlegend=True
        )
        }
    ),
])
