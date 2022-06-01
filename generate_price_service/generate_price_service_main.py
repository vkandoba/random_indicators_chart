import json
import logging
from pathlib import Path

from flask import Flask, jsonify
from flask_apscheduler import APScheduler
from flask_sock import Sock, ConnectionClosed
from datetime import datetime

from price_service import PriceService
from instrument_service import InstrumentService
from random_price_shift_provider import RandomPriceShiftProvider
from generate_price_service import GeneratePriceService


def create_flask_app():
    flask_app = Flask(__name__)

    ws_listener = Sock(flask_app)
    ws_connections = set()

    scheduler = APScheduler()
    scheduler.init_app(flask_app)

    service_location = Path(__file__).parent
    config = json.loads((service_location / f"generate_price_service_config_{flask_app.config['ENV']}.json").read_text())
    logs_location = service_location.parent / "logs" / f"{service_location.name}_{datetime.now().strftime('%H-%M-%S')}.log"

    logging.basicConfig(filename=logs_location,
                        format="%(levelname)s|%(asctime)s|%(name)s|%(message)s",
                        datefmt='%%d-%m-%Y %H:%M:%S',
                        encoding='utf-8',
                        level=logging.getLevelName(config['log_level']))

    shift_provider = RandomPriceShiftProvider(config['random_init_state'])
    instrument_service = InstrumentService(config['instrument_count'])
    price_service = PriceService(instrument_service, shift_provider, config['init_price'])
    generate_price_service = GeneratePriceService(price_service, instrument_service)

    @flask_app.route('/')
    def main_handler():
        return 'Provide instrument and prices data with periodical random updates'

    @flask_app.route('/instrument')
    def instrument_list():
        return jsonify(generate_price_service.instruments())

    @flask_app.route('/instrument/<symbol>/price')
    def price_history(symbol):
        history = generate_price_service.prices_history(symbol)
        return jsonify(history)

    @ws_listener.route('/ws/instrument/price/realtime')
    def price_events_realtime(ws_connection):
        ws_connections.add(ws_connection)
        try:
            cancel_data = ws_connection.receive()
        finally:
            if ws_connection in ws_connections:
                ws_connections.remove(ws_connection)

    @scheduler.task(
        "interval",
        id="job_generate_price",
        seconds=1,
        max_instances=1
    )
    def generate_price_task():
        next_prices = generate_price_service.prices_update()
        msg = json.dumps(next_prices)
        for ws_connection in ws_connections:
            try:
                logging.debug(f'send to {ws_connection}')
                ws_connection.send(msg)
            except ConnectionClosed:
                if ws_connection in ws_connections:
                    ws_connections.remove(ws_connection)

    scheduler.start()
    return flask_app


if __name__ == '__main__':
    app = create_flask_app()
    app.run(debug=False)  # on debug mode start and run scheduler twice