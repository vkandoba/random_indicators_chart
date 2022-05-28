class PriceService:
    def __init__(self, shift_provider, init_prices):
        self.__shift_provider = shift_provider
        self.__last_prices = init_prices
        self.__prices = [init_prices]

    def generate_next_price(self):
        next_diff = self.__shift_provider.generate_movement()
        next_price = self.__last_prices + next_diff
        self.__last_prices = next_price
        return next_price

    def get_prices(self, name):
        return self.__prices

    def append_price(self, price):
        self.__prices.append(price)
