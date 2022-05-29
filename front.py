import pandas as pd

from requests import get

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

    #  WebSocket(id='price-ws', url='ws://127.0.0.1:5000/ws/instrument/price/realtime')
    WebSocket(id='price-ws', url='ws://127.0.0.1:5000/instrument/price/realtime')
])

#  TODO: move to js file
update_store = '''
    function(msg, instrument_data, current_data) {
        console.log('msg: ')
        console.log(msg)        
        console.log('instrument_data:')
        console.log(instrument_data)
        console.log('current_data: ' + current_data)

        if (!current_data || !msg)
            return instrument_data || {'symbol': "", 'values': []}

        if (instrument_data && instrument_data.symbol != current_data.symbol)
            return instrument_data
                    
        //const data = JSON.parse(msg.data);  // read the data
        var new_price = parseInt(msg.data);
        current_data.values.push(new_price);
        return current_data; 
}
'''

app.clientside_callback(update_store,
                        Output('price-data-store', 'data'),
                        [Input("price-ws", "message"), Input('instrument-price-data-store', 'data')],
                        State('price-data-store', 'data'))


@app.callback(
    Output(component_id='price-graph', component_property='figure'),
    Input(component_id='price-data-store', component_property='data')
)
def update_price_graph(data):
    print(type(data))
    print(data)
    fig = create_price_figure(data['values'])
    return fig


@app.callback(
    Output(component_id='instrument-price-data-store', component_property='data'),
    Input(component_id='instrument-selector', component_property='value')
)
def update_price_data(instrument):
    values = price_list(instrument)
    return {"symbol": instrument, "values": values}



if __name__ == '__main__':
    app.run(debug=True)
