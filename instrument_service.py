instrument_count = 100


def generate_instruments(count):
    return [f'ticker_{i:02d}' for i in range(count)]