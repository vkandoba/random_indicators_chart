import logging
from asyncio import AbstractEventLoop

from fastapi import FastAPI
from starlette.websockets import WebSocket

from generate_price_service import GeneratePriceService


class GeneratePriceServiceApi:
    def __init__(self,
                 main_loop: AbstractEventLoop,
                 generate_price_service: GeneratePriceService):
        self.fastapi_app = FastAPI()
        self.ws_connections = set()
        self.__service = generate_price_service
        self.__logger = logging.getLogger(__name__)

        main_loop.create_task(self.__send_price_updates())

        @self.fastapi_app.get('/')
        async def main_handler():
            return {'message': "Provide instrument and prices data with periodical random updates"}

        @self.fastapi_app.get('/instrument')
        async def instrument_list():
            return generate_price_service.instruments()

        @self.fastapi_app.get('/instrument/{symbol}/price')
        async def price_history(symbol):
            history = generate_price_service.prices_history(symbol)
            return history

        @self.fastapi_app.websocket('/ws/instrument/price/realtime')
        async def price_events_realtime(ws_connection: WebSocket):
            await ws_connection.accept()
            self.ws_connections.add(ws_connection)
            try:
                cancel_data = await ws_connection.receive()
            finally:
                if ws_connection in self.ws_connections:
                    self.ws_connections.remove(ws_connection)

    async def __send_price_updates(self):
        async for next_price_update in self.__service.prices_updates():
            for ws_connection in self.ws_connections:
                try:
                    self.__logger.debug(f'send to {ws_connection}')
                    await ws_connection.send_json(next_price_update)
                except RuntimeError:
                    if ws_connection in self.ws_connections:
                        self.ws_connections.remove(ws_connection)