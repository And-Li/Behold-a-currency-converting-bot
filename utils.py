import requests
import json
from config import keys


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if quote == base:
            raise APIException(f"Impossible to convert {base} to {base}, it's always 1")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Impossible to convert {quote}:\nno such currency in the list of /values')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Impossible to convert {base}:\nno such currency in the list of /values')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Impossible to process amount {amount}:\ninput proper quantity consisting of numbers.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = float(json.loads(r.content)[keys[base]])
        return total_base
