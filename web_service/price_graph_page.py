import pandas as pd
from datetime import datetime

from dash import html, dcc, Input, Output, State
from dash_extensions import WebSocket

import plotly.express as px

from generate_price_service.generate_price_service_client import GeneratePriceServiceClient


class PriceGraphPage:
    def __init__(self, scripts_dir, config):
        self.config = config
        self.__price_service = GeneratePriceServiceClient(self.config['generate_price_service']['endpoint'])
        self.__scripts_dir = scripts_dir
        self.html_selector_id = 'instrument-selector'
        self.html_price_store_id = 'instrument-price-data-store'

    def render_page(self):
        instruments = self.__price_service.instruments()

        init_instrument_symbol = instruments[0]

        price_history = self.__price_service.price_history(init_instrument_symbol)
        timeline = [datetime.fromisoformat(item['timestamp']) for item in price_history]
        init_data = {
            'symbol': init_instrument_symbol,
            'values': [item['price'] for item in price_history],
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
            WebSocket(id='price-ws', url=self.__price_service.price_updates_realtime_url)
        ])

    def update_price_data(self, new_instrument_name):
        price_history = self.__price_service.price_history(new_instrument_name)
        timeline = [datetime.fromisoformat(item['timestamp']) for item in price_history]
        return {'symbol': new_instrument_name,
                'times': timeline,
                'values': [item['price'] for item in price_history]}

    def add_client_callbacks(self, app):
        update_store_js = self.read_callback_js('update_store_callback.js')
        app.clientside_callback(update_store_js,
                                Output('price-data-store', 'data'),
                                [Input('price-ws', 'message'), Input('instrument-price-data-store', 'data')],
                                State('price-data-store', 'data'))

        update_graph_js = self.read_callback_js("update_price_graph_callback.js")
        app.clientside_callback(update_graph_js,
                               Output('price-graph', 'figure'),
                               Input('price-data-store', 'data'),
                               State('price-graph', 'figure'))

    def read_callback_js(self, file_js):
        return (self.__scripts_dir / file_js).read_text()

    @staticmethod
    def __create_price_figure(price_data):
        time_df = pd.DataFrame(price_data)
        time_df['times'].name = 'Time UTC +00:00'
        figure = px.line(time_df, x='times', y='values', labels={
                     'times': "Time UTC +00:00",  # TODO: rename when will done view with client timezone
                     "values": "Price"
                 })
        return figure