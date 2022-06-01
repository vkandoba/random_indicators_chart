import json
from pathlib import Path

from dash import Dash, Input, Output

from price_graph_page import PriceGraphPage

source_folder = Path(__file__).parent
config = json.loads((source_folder / "main_config.json").read_text())
scripts_location = config["scripts_location"]

price_graph_page = PriceGraphPage(Path(__file__).parent / scripts_location, config)

app = Dash(__name__, assets_folder=scripts_location)
app.title = 'Test. Python'

price_graph_page.add_client_callbacks(app)

app.layout = price_graph_page.render_page()


# TODO: move to the page class, may be a register method instead the callback decorator
@app.callback(
    Output(component_id=price_graph_page.html_price_store_id, component_property='data'),
    Input(component_id=price_graph_page.html_selector_id, component_property='value'))
def update_price_data_server_callback(new_instrument):
    return price_graph_page.update_price_data(new_instrument)


if __name__ == '__main__':
    app.run(debug=config['debug'])
