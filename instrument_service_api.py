from flask import Flask, jsonify

import instrument_service

app = Flask(__name__)


@app.route('/')
def main_handler():
    return 'Provide instrument data'


@app.route('/instrument')
def instrument_list():
    instrument_names = instrument_service.generate_instruments(instrument_service.instrument_count)

    # TODO: add updateInterval and initTimestamp to response
    instruments = [{'symbol': name} for name in instrument_names]
    return jsonify(instruments)


app.run(debug=True)
