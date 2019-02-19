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

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
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
            xaxis={'title': 'Date'},
            yaxis={'title': 'Waiting days'},
            showlegend=True
        )
        }        
    ),
    # dcc.Slider(
    #     id='year-slider',
    #     min=df['year'].min(),
    #     max=df['year'].max(),
    #     value=df['year'].min(),
    #     marks={str(year): str(year) for year in df['year'].unique()}
    # )
])


# @app.callback(
#     dash.dependencies.Output('graph-with-slider', 'figure'),
#     [dash.dependencies.Input('year-slider', 'value')])
# def update_figure(selected_year):
#     filtered_df = df[df.year == selected_year]
#     traces = []
#     for i in filtered_df.continent.unique():
#         df_by_continent = filtered_df[filtered_df['continent'] == i]
#         traces.append(go.Scatter(
#             x=df_by_continent['gdpPercap'],
#             y=df_by_continent['lifeExp'],
#             text=df_by_continent['country'],
#             mode='markers',
#             opacity=0.7,
#             marker={
#                 'size': 15,
#                 'line': {'width': 0.5, 'color': 'white'}
#             },
#             name=i
#         ))

#     return {
#         'data': traces,
#         'layout': go.Layout(
#             xaxis={'type': 'log', 'title': 'GDP Per Capita'},
#             yaxis={'title': 'Life Expectancy', 'range': [20, 90]},
#             margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
#             legend={'x': 0, 'y': 1},
#             hovermode='closest'
#         )
#     }


if __name__ == '__main__':
    app.run_server(debug=True)