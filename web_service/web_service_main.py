import json
from pathlib import Path

from dash import Dash

from price_graph_page import PriceGraphPage

source_folder = Path(__file__).parent
config = json.loads((source_folder / "main_config.json").read_text())
scripts_location = config["scripts_location"]

app = Dash(__name__, assets_folder=scripts_location)
app.title = 'Test. Python'

price_graph_page = PriceGraphPage(app, config)
app.layout = price_graph_page.render_page()

if __name__ == '__main__':
    app.run(debug=config['debug'])
