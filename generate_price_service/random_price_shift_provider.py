from random import random, seed

import logging


class RandomPriceShiftProvider:
    def __init__(self, seed_value: int):
        seed(seed_value)

    @staticmethod
    def generate_movement() -> int:
        rnd_value = random()
        movement = -1 if rnd_value < 0.5 else 1

        logging.debug(f"random generate {rnd_value}")

        return movement
