import pandas as pd
from datetime import datetime

from dash import html, dcc, Input, Output, State
from dash_extensions import WebSocket

import plotly.express as px

from generate_price_service_client import GeneratePriceServiceClient


class PriceGraphPage:
    def __init__(self, dash_app, config):
        self.config = config
        self.__price_service = GeneratePriceServiceClient(self.config['generate_price_service']['endpoint'])
        self.html_selector_id = 'instrument-selector'
        self.html_price_store_id = 'instrument-price-data-store'
        self.__register_client_callbacks(dash_app)

        @dash_app.callback(
            Output(component_id='price-graph', component_property='figure'),
            Input(component_id=self.html_selector_id, component_property='value'))
        def update_price_data_server_callback(new_instrument):
            return self.__update_price_data(new_instrument)

    def render_page(self):
        instruments = self.__price_service.instruments()

        init_instrument_symbol = instruments[0]
        init_fig = self.__update_price_data(init_instrument_symbol)

        return html.Div(children=[
            html.H1(children='Price chart'),
            html.Div(children='Select trading instrument:'),
            html.Div(
                [
                    dcc.Dropdown(instruments, instruments[0], id=self.html_selector_id, clearable=False)
                ], style={"width": '15%'}),

            dcc.Store(id='price-update-store'),
            dcc.Store(id=self.html_price_store_id),

            dcc.Graph(
                id='price-graph',
                figure=init_fig
            ),
            WebSocket(id='price-ws', url=self.__price_service.price_updates_realtime_url)
        ])

    def __register_client_callbacks(self, app):
        app.clientside_callback('update_store_callback',
                                Output('price-update-store', 'data'),
                                Input('price-ws', 'message'),
                                State(self.html_selector_id, 'value'))

        app.clientside_callback('update_price_graph_callback',
                                Output('price-graph', 'extendData'),
                                Input('price-update-store', 'data'))

    def __update_price_data(self, new_instrument_name):
        price_history = self.__price_service.price_history(new_instrument_name)
        timeline = [datetime.fromisoformat(item['timestamp']) for item in price_history]
        return self.__create_price_figure({'symbol': new_instrument_name,
                                           'times': timeline,
                                           'values': [item['price'] for item in price_history]})

    @staticmethod
    def __create_price_figure(price_data):
        time_df = pd.DataFrame(price_data)
        time_df['times'].name = 'Time UTC +00:00'
        figure = px.line(time_df, x='times', y='values', labels={
                     'times': "Time UTC +00:00",  # TODO: rename when will done view with client timezone
                     "values": "Price"
                 })
        return figure
