from datetime import datetime
from price_service import PriceService
from random_price_shift_provider import RandomPriceShiftProvider


def create_instruments(count):
    return [f'ticker_{i:02d}' for i in range(count)]


default_instrument_count = 100

base_price = 0

shift_provider = RandomPriceShiftProvider(42)
price_service = PriceService(shift_provider, base_price, create_instruments(default_instrument_count))


def get_prices(name):
    price_list = price_service.get_prices(name)
    return {'prices': price_list, 'timestamp': datetime.utcnow().isoformat()}


def generate_next_price():
    next_prices = price_service.generate_next_prices()
    return {'new_prices': next_prices, 'timestamp': datetime.utcnow().isoformat()}


def append_price():
    price_service.append_prices()
