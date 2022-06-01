import json

from flask import Flask, jsonify
from flask_apscheduler import APScheduler
from flask_sock import Sock, ConnectionClosed

from price_service import PriceService
from instrument_service import InstrumentService
from random_price_shift_provider import RandomPriceShiftProvider
from generate_price_service import GeneratePriceService

random_init_state = 42
default_instrument_count = 100
init_price = 0

flask_app = Flask(__name__)
sock = Sock(flask_app)
scheduler = APScheduler()
scheduler.init_app(flask_app)
scheduler.start()
ws_connections = set()

shift_provider = RandomPriceShiftProvider(random_init_state)
instrument_service = InstrumentService(default_instrument_count)
price_service = PriceService(instrument_service, shift_provider, init_price)
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


@sock.route('/ws/instrument/price/realtime')
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
    for ws_connection in ws_connections:
        try:
            ws_connection.send(json.dumps(next_prices))
        except ConnectionClosed:
            if ws_connection in ws_connections:
                ws_connections.remove(ws_connection)


if __name__ == '__main__':
    flask_app.run(debug=False)  # on debug mode start and run scheduler twice

