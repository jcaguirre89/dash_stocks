import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objs as go
from dash.dependencies import Input, Output

from price_scraper import Company
from tickers_scraper import get_tickers

import datetime
import json
import os
from flask import send_from_directory

app = dash.Dash()
"""
# Serve static files from external url
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
"""

# Serving them locally

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True
appDir = os.path.dirname(os.path.realpath(__file__))


# get list of tickers and names for S&P 500
tickers_and_names = get_tickers()

app.layout = html.Div([
    # stylesheets and general head
    html.Link(href='/static/style.css', rel='stylesheet'),
    # Fonts
    html.Link(href="https://fonts.googleapis.com/css?family=Roboto", rel="stylesheet"),
    # html.Script(src='/static/javascript.js'),

    html.H1('Test dashboard', className='title'),
    html.Div([

        dcc.Dropdown(
            id='select-ticker',
            options=[{'label': v, 'value': k} for k, v in tickers_and_names.items()],
            placeholder='Select a company'
        ),

        html.Div(id='company-data-json',
                 hidden=True),

        dcc.DatePickerRange(
            id='date-picker',
            min_date_allowed=datetime.date(2008, 1, 1),
            max_date_allowed=datetime.datetime.today().date(),
            initial_visible_month=datetime.datetime.today().date(),
            start_date=datetime.date(2018, 1, 1),
            end_date=datetime.datetime.today().date(),
        )
        ],
        className='options'
    ),

    html.Div(children=[
        html.Div(className='company-item', children=[
            html.P('Price to Book'),
            html.Div(id='price-book')
            ]
        ),
        html.Div(className='company-item', children=[
            html.P('Price to Earnings (trailing)'),
            html.Div(id='pe-trailing')
            ]
        ),
        html.Div(className='company-item', children=[
            html.P('EV to EBITDA'),
            html.Div(id='ev-ebitda')
            ]
        ),
        html.Div(className='company-item', children=[
            html.P('PE to growth ratio'),
            html.Div(id='peg')
            ]
        ),
        html.Div(className='company-item', children=[
            html.P('Debt to Equity'),
            html.Div(id='debt-equity')
            ]
        ),
        ],
        className='company-data'
    ),

    html.Div(children=[
        dcc.Graph(id='price-chart'),
        ],
        className='chart'
    ),

    html.P(
        id='summary'
    )

    ],
    className='main-wrapper'
)


@app.callback(Output('company-data-json', 'children'),
              [Input('select-ticker', 'value')])
def get_company_data(ticker):
    company = Company(ticker)
    data = company.data
    data.pop('scrape_date')
    return json.dumps(data)


@app.callback(Output('summary', 'children'),
              [Input('company-data-json', 'children')])
def update_summary(data):
    data_dict = json.loads(data)
    return data_dict['summary']

@app.callback(Output('price-book', 'children'),
              [Input('company-data-json', 'children')])
def update_price_book(data):
    data_dict = json.loads(data)
    return round(data_dict['price_book'], 2)

@app.callback(Output('debt-equity', 'children'),
              [Input('company-data-json', 'children')])
def update_debt_equity(data):
    data_dict = json.loads(data)
    return data_dict['debt_to_equity']

@app.callback(Output('peg', 'children'),
              [Input('company-data-json', 'children')])
def update_peg(data):
    data_dict = json.loads(data)
    return data_dict['peg']

@app.callback(Output('ev-ebitda', 'children'),
              [Input('company-data-json', 'children')])
def update_ev_ebitda(data):
    data_dict = json.loads(data)
    return round(data_dict['ev_ebitda'], 2)


@app.callback(Output('pe-trailing', 'children'),
              [Input('company-data-json', 'children')])
def update_pe_trailing(data):
    data_dict = json.loads(data)
    return round(data_dict['price'] / data_dict['eps_t'], 2)

@app.callback(Output('price-chart', 'figure'),
              [Input('select-ticker', 'value'),
               Input('date-picker', 'start_date'),
               Input('date-picker', 'end_date')])
def price_chart(ticker, start_date, end_date, size=(600, 800)):
    # get prices
    company = Company(ticker)
    df = company.get_price(start_date, end_date)

    trace = go.Candlestick(
        x=df.index,
        open=df['Open'],
        close=df['Close'],
        high=df['High'],
        low=df['Low'],
    )

    data = [trace]

    layout = go.Layout(
        height=size[0],
        width=size[1],
        xaxis=dict(
            rangeslider=dict(
                visible=False
            )
        )
    )

    fig = go.Figure(data=data, layout=layout)

    return fig


# include static files (css and js)
@app.server.route('/static/<path:path>')
def static_file(path):
    static_folder = os.path.join(appDir, 'static')
    return send_from_directory(static_folder, path)


if __name__ == '__main__':
    app.run_server(debug=True)
