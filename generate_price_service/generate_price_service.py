import asyncio
import json
import logging

from instrument_service import InstrumentService
from price_service import PriceService


class GeneratePriceService:
    def __init__(self,
                 price_service: PriceService,
                 instrument_service: InstrumentService,
                 update_interval: int):
        self.__price_service = price_service
        self.__instrument_service = instrument_service
        self.__update_interval = update_interval

        self.__logger = logging.getLogger(__name__)

    def prices_history(self, instrument_name: str) -> [dict]:
        history = self.__price_service.price_history(instrument_name)
        self.__logger.info(f"prices_history: {json.dumps(history)}")
        return history

    async def prices_updates(self) -> [dict]:
        while True:
            next_prices = self.__price_service.generate_next_prices()
            self.__price_service.add_prices(next_prices)
            update = self.__price_service.last_prices()
            self.__logger.info(f"prices_update: {json.dumps(update)}")

            yield update

            await asyncio.sleep(self.__update_interval)

    def instruments(self) -> [dict]:
        # TODO: add updateInterval and initTimestamp to response
        instruments = [{'symbol': name} for name in self.__instrument_service.names()]
        self.__logger.info(f"instruments: {json.dumps(instruments)}")
        return instruments
