class PriceService:
    def __init__(self, shift_provider, init_price, instrument_list):
        self.__shift_provider = shift_provider
        self.__instrument_to_index_dict = {name: i for i, name in enumerate(instrument_list)}
        init_prices = [init_price for _ in instrument_list]
        self.__price_history = [list(init_prices)]
        self.__last_prices = init_prices

    def generate_next_prices(self):
        next_prices = {}
        for name, index in self.__instrument_to_index_dict.items():
            next_diff = self.__shift_provider.generate_movement()
            next_prices[name] = self.__last_prices[index] + next_diff
            self.__last_prices[index] = next_prices[name]
        return next_prices

    def get_prices(self, instrument_name):
        instrument_index = self.__instrument_to_index_dict[instrument_name]
        return [prices[instrument_index] for prices in self.__price_history]

    def append_prices(self):
        self.__price_history.append(list(self.__last_prices))
