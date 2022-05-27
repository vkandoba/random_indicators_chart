import pandas as pd

from requests import get

from dash import Dash, html, dcc, Input, Output
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

    dcc.Graph(
        id='price-graph',
        figure=init_fig
    ),

    dcc.Interval(
        id='interval-component',
        interval=1 * 1000,  # in milliseconds
        n_intervals=0
    )
])


@app.callback(
    Output(component_id='price-graph', component_property='figure'),
    [Input(component_id='interval-component', component_property='n_intervals'),
     Input(component_id='instrument-selector', component_property='value')]
)
def update_price_graph(iteration_number, instrument):
    values = price_list(instrument)
    fig = create_price_figure(values)
    return fig


if __name__ == '__main__':
    app.run(debug=True)