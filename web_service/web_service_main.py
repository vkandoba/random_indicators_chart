import json
from pathlib import Path

from dash import Dash
from flask import Flask

from price_graph_page import PriceGraphPage


def create_dash_app(server=None):
    source_folder = Path(__file__).parent
    scripts = 'client_scripts'

    if server is None:
        app = Dash(__name__, assets_folder=scripts)
        env = 'dev'
    else:
        app = Dash(__name__, assets_folder=scripts, server=server)
        env = app.server.config['ENV']

    config = json.loads((source_folder / f'web_service_config_{env}.json').read_text())

    app.title = "Test. Python"
    price_graph_page = PriceGraphPage(app, config)
    app.layout = price_graph_page.render_page()
    return app


def create_server():
    flask_app = Flask(__name__)
    create_dash_app(flask_app)
    return flask_app


if __name__ == '__main__':
    dash_app = create_dash_app()
    dash_app.run(debug=True)
