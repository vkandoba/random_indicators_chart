import json
import logging
from datetime import datetime


class PriceService:
    def __init__(self, instrument_service, shift_provider, init_price):
        self.__shift_provider = shift_provider
        self.__instrument_names = instrument_service.names()
        init_prices = {name: init_price for name in self.__instrument_names}
        self.__price_update_history = [{'timestamp': datetime.utcnow().isoformat(), 'prices': dict(init_prices)}]
        self.__last_prices = init_prices

        self.__logger = logging.getLogger(__name__)

    def generate_next_prices(self):
        self.__logger.debug(f"last prices: {json.dumps(self.__last_prices)}")

        next_prices = {}
        for name in self.__last_prices:
            next_diff = self.__shift_provider.generate_movement()
            next_prices[name] = self.__last_prices[name] + next_diff

        self.__last_prices= dict(next_prices)
        self.__logger.debug(f"next prices: {json.dumps(next_prices)}")
        return next_prices

    def add_prices(self, new_prices):
        self.__price_update_history.append({'timestamp': datetime.utcnow().isoformat(), 'prices': new_prices})

    def last_prices(self):
        return self.__price_update_history[-1]

    def price_history(self, instrument_name):
        prices = [{'price': update['prices'][instrument_name], 'timestamp': update['timestamp']}
                  for update in self.__price_update_history]
        return prices
