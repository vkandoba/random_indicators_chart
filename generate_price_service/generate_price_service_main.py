import os

from pathlib import Path
from datetime import datetime

import json
import logging

import asyncio
import uvicorn
from fastapi import FastAPI
from starlette.websockets import WebSocket

from price_service import PriceService
from instrument_service import InstrumentService
from random_price_shift_provider import RandomPriceShiftProvider
from generate_price_service import GeneratePriceService

env = os.environ['SERVER_ENV']
service_location = Path(__file__).parent
config = json.loads((service_location / f"generate_price_service_config_{env}.json").read_text())

logs_location = service_location.parent / "logs" / f"{service_location.name}_{datetime.now().strftime('%H-%M-%S')}.log"
log_level_name = "INFO" if env == 'prod' else "DEBUG"
logging.basicConfig(filename=logs_location,
                    format="%(levelname)s|%(asctime)s|%(name)s|%(message)s",
                    datefmt='%%d-%m-%Y %H:%M:%S',
                    encoding='utf-8',
                    level=logging.getLevelName(log_level_name))

shift_provider = RandomPriceShiftProvider(config['random_init_state'])
instrument_service = InstrumentService(config['instrument_count'])
price_service = PriceService(instrument_service, shift_provider, config['init_price'])
generate_price_service = GeneratePriceService(price_service, instrument_service)

ws_connections = set()


def create_application():
    fastapi_app = FastAPI()

    @fastapi_app.get('/')
    async def main_handler():
        return {'message': "Provide instrument and prices data with periodical random updates"}

    @fastapi_app.get('/instrument')
    async def instrument_list():
        return generate_price_service.instruments()

    @fastapi_app.get('/instrument/{symbol}/price')
    async def price_history(symbol):
        history = generate_price_service.prices_history(symbol)
        return history

    @fastapi_app.websocket('/ws/instrument/price/realtime')
    async def price_events_realtime(ws_connection: WebSocket):
        await ws_connection.accept()
        ws_connections.add(ws_connection)
        try:
            cancel_data = await ws_connection.receive()
        finally:
            if ws_connection in ws_connections:
                ws_connections.remove(ws_connection)

    return fastapi_app


async def send_price_updates():
    while True:
        next_price_update = generate_price_service.prices_update()
        for ws_connection in ws_connections:
            try:
                logging.debug(f'send to {ws_connection}')
                await ws_connection.send_json(next_price_update)
            except RuntimeError:
                if ws_connection in ws_connections:
                    ws_connections.remove(ws_connection)
        await asyncio.sleep(1)


def create_server(application, main_event_loop, endpoint):
    return uvicorn.Server(config=(uvicorn.Config(app=application,
                                                 loop=main_event_loop,
                                                 host=endpoint['host'],
                                                 port=endpoint['port'])))


if __name__ == '__main__':
    main_loop = asyncio.new_event_loop()
    app = create_application()
    price_updates_task = main_loop.create_task(send_price_updates())
    server = create_server(app, main_loop, config['endpoint'])
    main_loop.run_until_complete(server.serve())