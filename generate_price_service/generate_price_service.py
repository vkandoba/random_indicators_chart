import json
import logging
from datetime import datetime


class GeneratePriceService:
    def __init__(self, price_service, instrument_service):
        self.__price_service = price_service
        self.__instrument_service = instrument_service

        self.__logger = logging.getLogger(__name__)

    def prices_history(self, instrument_name):
        price_list = self.__price_service.get_prices(instrument_name)
        history = {'prices': price_list, 'timestamp': datetime.utcnow().isoformat()}
        self.__logger.info(f"prices_history: {json.dumps(history)}")
        return history

    def prices_update(self):
        next_prices = self.__price_service.generate_next_prices()
        self.__price_service.append_prices()
        update = {'new_prices': next_prices, 'timestamp': datetime.utcnow().isoformat()}
        self.__logger.info(f"prices_update: {json.dumps(update)}")
        return update

    def append_price(self):
        self.__logger.info(f"last prices update was added to history")
        self.__price_service.append_prices()

    def instruments(self):
        # TODO: add updateInterval and initTimestamp to response
        instruments = [{'symbol': name} for name in self.__instrument_service.names()]
        self.__logger.info(f"instruments: {json.dumps(instruments)}")
        return instruments
