from flask import Flask, jsonify
from flask_apscheduler import APScheduler

import instrument_service

app = Flask(__name__)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


@scheduler.task(
    "interval",
    id="job_generate_numbers",
    seconds=3,
    max_instances=1
)
def generate_numbers_task():
    price = instrument_service.generate_next_price()
    instrument_service.append_price(price)
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


if __name__ == '__main__':
    app.run(debug=False) # on debug mode start and run sheduler twice