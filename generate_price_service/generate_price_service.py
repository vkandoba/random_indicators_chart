from datetime import datetime


class GeneratePriceService:
    def __init__(self, price_service, instrument_service):
        self.__price_service = price_service
        self.__instrument_service = instrument_service

    def prices_history(self, instrument_name):
        price_list = self.__price_service.get_prices(instrument_name)
        return {'prices': price_list, 'timestamp': datetime.utcnow().isoformat()}

    def prices_update(self):
        next_prices = self.__price_service.generate_next_prices()
        self.__price_service.append_prices()
        return {'new_prices': next_prices, 'timestamp': datetime.utcnow().isoformat()}

    def append_price(self):
        return self.__price_service.append_prices()

    def instruments(self):
        # TODO: add updateInterval and initTimestamp to response
        return [{'symbol': name} for name in self.__instrument_service.names()]
