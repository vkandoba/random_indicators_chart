from random import random, seed


class RandomPriceShiftProvider:
    def __init__(self, seed_value):
        seed(seed_value)

    @staticmethod
    def generate_movement():
        movement = -1 if random() < 0.5 else 1
        return movement
