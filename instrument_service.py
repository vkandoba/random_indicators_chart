from random import random, seed

seed(42)

default_instrument_count = 100

base_price = 0
last_price = 0
prices = []


def create_instruments(count):
    return [f'ticker_{i:02d}' for i in range(count)]


def get_prices(name):
    return prices


def generate_next_price():
    global last_price
    next_diff = generate_movement()
    next_price = last_price + next_diff
    last_price = next_price
    return next_price


def generate_movement():
    movement = -1 if random() < 0.5 else 1
    return movement


def append_price(price):
    prices.append(price)
