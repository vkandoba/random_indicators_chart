from requests import get


class GeneratePriceServiceClient:
    def __init__(self, endpoint):
        self.__base_rest_api_url = f"http://{endpoint}"
        self.__realtime_base_url = f"ws://{endpoint}/ws"
        self.price_updates_realtime_url = f"{self.__realtime_base_url}/instrument/price/realtime"

    def instruments(self):
        instruments_response = get(f"{self.__base_rest_api_url}/instrument")
        if instruments_response.ok:
            instruments = instruments_response.json()
            return [instrument['symbol'] for instrument in instruments]

    def price_history(self, instrument_symbol):
        price_response = get(f"{self.__base_rest_api_url}/instrument/{instrument_symbol}/price")
        if price_response.ok:
            return price_response.json()