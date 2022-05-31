from dash import Dash, Input, Output

from price_graph_page import PriceGraphPage


app = Dash(__name__)
app.title = 'Test. Python'

price_graph_page = PriceGraphPage({'endpoint': "127.0.0.1:5000"})

price_graph_page.add_client_callbacks(app)

app.layout = price_graph_page.render_page()


@app.callback(
    Output(component_id=price_graph_page.html_price_store_id, component_property='data'),
    Input(component_id=price_graph_page.html_selector_id, component_property='value'))
def update_price_data_server_callback(new_instrument):
    return price_graph_page.update_price_data(new_instrument)


if __name__ == '__main__':
    app.run(debug=False)
