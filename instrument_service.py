from random import random, seed
from price_service import PriceService
from random_price_shift_provider import RandomPriceShiftProvider


default_instrument_count = 100

base_price = 0

shift_provider = RandomPriceShiftProvider(42)
price_service = PriceService(shift_provider, base_price)


def create_instruments(count):
    return [f'ticker_{i:02d}' for i in range(count)]


def get_prices(name):
    return price_service.get_prices(name)


def generate_next_price():
    return price_service.generate_next_price()


def append_price(price):
    price_service.append_price(price)
