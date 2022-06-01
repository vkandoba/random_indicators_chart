import json
import logging

class GeneratePriceService:
    def __init__(self, price_service, instrument_service):
        self.__price_service = price_service
        self.__instrument_service = instrument_service

        self.__logger = logging.getLogger(__name__)

    def prices_history(self, instrument_name):
        history = self.__price_service.price_history(instrument_name)
        self.__logger.info(f"prices_history: {json.dumps(history)}")
        return history

    def prices_update(self):
        next_prices = self.__price_service.generate_next_prices()
        self.__price_service.add_prices(next_prices)
        update = self.__price_service.last_prices()

        self.__logger.info(f"prices_update: {json.dumps(update)}")

        return update

    def instruments(self):
        # TODO: add updateInterval and initTimestamp to response
        instruments = [{'symbol': name} for name in self.__instrument_service.names()]
        self.__logger.info(f"instruments: {json.dumps(instruments)}")
        return instruments
