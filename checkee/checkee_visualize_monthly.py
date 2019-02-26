import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from datetime import datetime, timedelta

# load main table from csv
file_name = 'data/checkee_main_table.csv'
df = pd.read_csv(file_name)


month = df.loc[:, 'Month'][::-1]
total = np.array(df.loc[:, 'Total'], dtype=np.float)[::-1]
clear = np.array(df.loc[:, 'Clear'], dtype=np.float)[::-1]
pending = np.array(df.loc[:, 'Pending'], dtype=np.float)[::-1]
reject = np.array(df.loc[:, 'Reject'], dtype=np.float)[::-1]

month = [datetime.strptime(date, '%Y-%m') for date in month]
ratio = np.divide(clear, total)

duration = np.array(df.loc[1:, 'Ave. Waiting Days for Complete Cases'], dtype=np.float)[::-1]

current_date = datetime.now()
five_years_ago = current_date - timedelta(weeks=52*5)

monthly_layout = html.Div([
    dcc.Graph(
        id='ratio',
        figure={
        'data': [
            go.Bar(
                x=month,
                y=clear,
                name='Cleared',
                marker=dict(
                    color='#2ca02c',    # cooked asparagus green
                )
            ),
            go.Bar(
                x=month,
                y=pending,
                name='Pending',
                marker=dict(
                    color='#1f77b4',    # muted blue
                )
            ),
            go.Bar(
                x=month,
                y=reject,
                name='Rejected',
                marker=dict(
                    color='#d62728',    # brick red
                )
            )
        ],
        'layout': go.Layout(
            xaxis={'title': 'Date', 'range': [five_years_ago, current_date]},
            yaxis={'title': 'Number of cases'},
            barmode='stack',
        )
        }
    ),
    dcc.Graph(
        id='duration',
        figure={
        'data': [
            go.Bar(
                x=month,
                y=duration,
            )
        ],
        'layout': go.Layout(
            xaxis={'title': 'Date', 'range': [five_years_ago, current_date]},
            yaxis={'title': 'Average waiting days', 'range': [0, 60]},
            showlegend=True
        )
        }
    ),

])

