import pandas as pd

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
        prices = price_response.json()
        return prices


def create_price_figure(price_list):
    df = pd.DataFrame({'Time': range(len(price_list)), 'Price': price_list})
    return px.line(df, x="Time", y="Price")


app = Dash(__name__)
app.title = 'Test. Python'

instruments = instrument_symbol_list()
price_values = price_list(instruments[0])
init_fig = create_price_figure(price_values)

app.layout = html.Div(children=[
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

scripts_dir = Path(__file__).parent / "client_scripts"

update_store_js = (scripts_dir / "update_store_callback.js").read_text()
update_graph_js = (scripts_dir / "update_price_graph_callback.js").read_text()

app.clientside_callback(update_store_js,
                        Output('price-data-store', 'data'),
                        [Input('price-ws', 'message'), Input('instrument-price-data-store', 'data')],
                        State('price-data-store', 'data'))

app.clientside_callback(update_graph_js,
                        Output('price-graph', 'figure'),
                        Input('price-data-store', 'data'),
                        State('price-graph', 'figure'))

@app.callback(
    Output(component_id='instrument-price-data-store', component_property='data'),
    Input(component_id='instrument-selector', component_property='value')
)
def update_price_data(instrument):
    values = price_list(instrument)
    return {"symbol": instrument, "values": values}


if __name__ == '__main__':
    app.run(debug=True)
