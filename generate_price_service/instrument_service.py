class InstrumentService:
    def __init__(self, instrument_count):
        self.__instrument_names = self.__create_instruments(instrument_count)

    def names(self):
        return self.__instrument_names

    @staticmethod
    def __create_instruments(count):
        return [f'ticker_{i:02d}' for i in range(count)]