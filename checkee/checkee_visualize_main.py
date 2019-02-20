import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

from checkee_visualize_daily import *
from checkee_visualize_monthly import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1('Visualization of Checkee Data'),
    dcc.Tabs(id="tabs-example", value='daily', children=[
        dcc.Tab(label='Daily Data', value='daily'),
        dcc.Tab(label='Monthly Data', value='monthly'),
    ]),
    html.Div(id='tabs-content-example')
])


@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'daily':
        return daily_layout
    elif tab == 'monthly':
        return monthly_layout


if __name__ == '__main__':
    app.run_server(debug=True)
    # app.run_server(debug=False, host='0.0.0.0', port=8050)