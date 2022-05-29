from flask import Flask, jsonify
from flask_apscheduler import APScheduler
from flask_sock import Sock
from simple_websocket import ConnectionClosed

import instrument_service

app = Flask(__name__)
sock = Sock(app)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

ws_connections = set()

@scheduler.task(
    "interval",
    id="job_generate_price",
    seconds=3,
    max_instances=1
)
def generate_price_task():
    price = instrument_service.generate_next_price()
    instrument_service.append_price(price)
    print(f"connections: {len(ws_connections)}")
    for ws_connection in ws_connections:
        try:
            ws_connection.send(str(price))
        except ConnectionClosed:
            if ws_connection in ws_connections:
                print('remove connection from generate price')
                ws_connections.remove(ws_connection)
    print(f"generate task: {price}")


@app.route('/')
def main_handler():
    return 'Provide instrument data'


@app.route('/instrument')
def instrument_list():
    instrument_names = instrument_service.create_instruments(instrument_service.default_instrument_count)

    # TODO: add updateInterval and initTimestamp to response
    instruments = [{'symbol': name} for name in instrument_names]
    return jsonify(instruments)


@app.route('/instrument/<symbol>/price')
def price_list(symbol):
    prices = instrument_service.get_prices(symbol)
    return jsonify(prices)


@sock.route('ws/instrument/price/realtime')
def price_events_realtime(ws_connection):
    print('new ws connection')
    ws_connections.add(ws_connection)
    try:
        cancel_data = ws_connection.receive()
    finally:
        print('remove connection from handler')
        if ws_connection in ws_connections:
            ws_connections.remove(ws_connection)

if __name__ == '__main__':
    app.run(debug=False)  # on debug mode start and run scheduler twice

