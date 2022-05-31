import pandas as pd
from dash._utils import patch_collections_abc
from datetime import timedelta, datetime
import plotly.graph_objs as go

from requests import get
from pathlib import Path
from dash import Dash, html, dcc, Input, Output, State
from dash_extensions import WebSocket

import plotly.express as px


def instrument_symbol_list():
    instruments_response = get("http://127.0.0.1:5000/instrument")
    if (instruments_response.ok):
        instruments = instruments_response.json()
        return [instrument['symbol'] for instrument in instruments]


def price_list(symbol):
    price_response = get(f"http://127.0.0.1:5000/instrument/{symbol}/price")
    if (price_response.ok):
        return price_response.json()


def create_timeline(price_response):
    timestamp = datetime.fromisoformat(price_response['timestamp'])
    return pd.date_range(end=timestamp, periods=len(price_response['prices']), freq='S');


def create_price_figure(price_data):
    time_df = pd.Series(price_data['values'], index=price_data['times'])
    time_df.index.name = 'Time UTC +00:00' # TODO: view with client timezone
    figure = px.line(time_df, x=time_df.index, y=time_df.values)
    return figure

app = Dash(__name__)
app.title = 'Test. Python'

scripts_dir = Path(__file__).parent / "client_scripts"
update_store_js = (scripts_dir / "update_store_callback.js").read_text()

update_graph_js = (scripts_dir / "update_price_graph_callback.js").read_text()

app.clientside_callback(update_graph_js,
                       Output('price-graph', 'figure'),
                       Input('price-data-store', 'data'),
                       State('price-graph', 'figure'))

app.clientside_callback(update_store_js,
                        Output('price-data-store', 'data'),
                        [Input('price-ws', 'message'), Input('instrument-price-data-store', 'data')],
                        [State('price-data-store', 'data'), State('price-graph', 'figure')])


def render_page():
    instruments = instrument_symbol_list()
    init_instrument_symbol = instruments[0]
    price_response = price_list(init_instrument_symbol)
    timeline = create_timeline(price_response)
    init_data = {'symbol': init_instrument_symbol, 'values': price_response['prices'], 'times': timeline}
    init_fig = create_price_figure(init_data)

    #init_timeline = px.timeline(x_start=timeline[0], x_end=timeline[-1])
    return html.Div(children=[
        html.H1(children='Chart'),

        html.Div(children='Select trading instrument:'),

        html.Div(
            [
                dcc.Dropdown(instruments, instruments[0], id='instrument-selector', clearable=False)
            ], style={"width": '15%'}),

        dcc.Store(id='price-data-store'),

        dcc.Store(id='instrument-price-data-store'),

        dcc.Graph(
            id='price-graph',
            figure=init_fig
        ),

        WebSocket(id='price-ws', url='ws://127.0.0.1:5000/ws/instrument/price/realtime')
    ])


app.layout = render_page


@app.callback(
    Output(component_id='instrument-price-data-store', component_property='data'),
    Input(component_id='instrument-selector', component_property='value'),
    State(component_id='price-graph', component_property='figure'))
def update_price_data(new_instrument, figure):
    prices_response = price_list(new_instrument)
    timeline = create_timeline(prices_response)
    return {'symbol': new_instrument, 'values': prices_response['prices'], 'times': timeline}


if __name__ == '__main__':
    app.run(debug=True)
