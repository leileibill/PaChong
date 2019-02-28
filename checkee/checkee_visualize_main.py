import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

from checkee_visualize_daily import *
from checkee_visualize_monthly import *
from checkee_visualize_by_category import *
from checkee_scrape import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1('US Visa Administrative Processing Statistics Visualization'),

    html.H5('Data is obtained from www.checkee.info'),
    html.H5('Checks with less than 7 waiting days are not included.'),

    dcc.Tabs(id="tabs-example", value='daily', children=[
        dcc.Tab(label='Daily Data', value='daily'),
        dcc.Tab(label='Monthly Data', value='monthly'),
        dcc.Tab(label='Category Data', value='category'),
    ]),

    html.Div(id='graph_tabs'),

    # html.H4('Designed and maintained by Yutian Lei.')
])


@app.callback(Output('graph_tabs', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'daily':
        return daily_layout
    elif tab == 'monthly':
        return monthly_layout
    elif tab == 'category':
        return category_layout


if __name__ == '__main__':

    scrape_everything()

    app.run_server(debug=True)
    # app.run_server(debug=False, host='0.0.0.0', port=8050)