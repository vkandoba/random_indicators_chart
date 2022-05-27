from requests import get
from dash import Dash, html, dcc


def instrument_symbol_list():
    instruments_response = get("http://127.0.0.1:5000/instrument")
    if (instruments_response.ok):
        instruments = instruments_response.json()
        return [instrument['symbol'] for instrument in instruments]


app = Dash(__name__)
app.title = 'Test. Python'

instruments = instrument_symbol_list()

app.layout = html.Div(children=[
    html.H1(children='Chart'),

    html.Div(children='Select trading instrument:'),

    html.Div(
        [
            dcc.Dropdown(instruments, instruments[0], clearable=False)
        ], style={"width": '15%'})
])

if __name__ == '__main__':
    app.run(debug=True)