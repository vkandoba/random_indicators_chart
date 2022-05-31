import pandas as pd
from datetime import datetime

from requests import get

from dash import html, dcc, Input, Output, State
from dash_extensions import WebSocket

import plotly.express as px


class PriceGraphPage:
    def __init__(self, scripts_dir, config):
        self.config = config
        self.__base_rest_api_url = f"http://{self.config['generate_price_service']['endpoint']}/"
        self.__scripts_dir = scripts_dir
        self.html_selector_id = 'instrument-selector'
        self.html_price_store_id = 'instrument-price-data-store'

    def render_page(self):
        instruments = self.instrument_symbol_list()
        init_instrument_symbol = instruments[0]

        price_response = self.price_list(init_instrument_symbol)
        timeline = self.__create_timeline(price_response)
        init_data = {
            'symbol': init_instrument_symbol,
            'values': price_response['prices'],
            'times': timeline
        }
        init_fig = self.__create_price_figure(init_data)

        return html.Div(children=[
            html.H1(children='Price chart'),
            html.Div(children='Select trading instrument:'),
            html.Div(
                [
                    dcc.Dropdown(instruments, instruments[0], id=self.html_selector_id, clearable=False)
                ], style={"width": '15%'}),

            dcc.Store(id='price-data-store'),
            dcc.Store(id=self.html_price_store_id),

            dcc.Graph(
                id='price-graph',
                figure=init_fig
            ),

            WebSocket(id='price-ws', url='ws://127.0.0.1:5000/ws/instrument/price/realtime')
        ])

    def update_price_data(self, new_instrument_name):
        prices_response = self.price_list(new_instrument_name)
        timeline = self.__create_timeline(prices_response)
        return {'symbol': new_instrument_name, 'values': prices_response['prices'], 'times': timeline}

    @staticmethod
    def __create_timeline(price_response):
        timestamp = datetime.fromisoformat(price_response['timestamp'])
        return pd.date_range(end=timestamp, periods=len(price_response['prices']), freq='S');

    @staticmethod
    def __create_price_figure(price_data):
        time_df = pd.DataFrame(price_data)
        time_df['times'].name = 'Time UTC +00:00'
        figure = px.line(time_df, x='times', y='values', labels={
                     'times': "Time UTC +00:00",  # TODO: rename when will done view with client timezone
                     "values": "Price"
                 })
        return figure

    def add_client_callbacks(self, app):
        update_store_js = self.read_callback_js('update_store_callback.js')
        app.clientside_callback(update_store_js,
                                Output('price-data-store', 'data'),
                                [Input('price-ws', 'message'), Input('instrument-price-data-store', 'data')],
                                [State('price-data-store', 'data'), State('price-graph', 'figure')])

        update_graph_js = self.read_callback_js("update_price_graph_callback.js")
        app.clientside_callback(update_graph_js,
                               Output('price-graph', 'figure'),
                               Input('price-data-store', 'data'),
                               State('price-graph', 'figure'))

    def read_callback_js(self, file_js):
        return (self.__scripts_dir / file_js).read_text()

    def instrument_symbol_list(self):
        instruments_response = get(f"{self.__base_rest_api_url}instrument")
        if instruments_response.ok:
            instruments = instruments_response.json()
            return [instrument['symbol'] for instrument in instruments]

    def price_list(self, symbol):
        price_response = get(f"{self.__base_rest_api_url}/instrument/{symbol}/price")
        if price_response.ok:
            return price_response.json()
