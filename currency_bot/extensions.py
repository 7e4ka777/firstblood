import requests
import json
from config import keys

class APIException(Exception):
    pass

class CryptoConverter():
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {quote}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get(
            f'https://currate.ru/api/?get=rates&pairs={quote_ticker}{base_ticker}&key=c03642d76d931d9af5f1757a4adbf7d6')
        result = json.loads(r.content)
        result = result.get('data')
        total_base = result.get(f'{keys[quote]}{keys[base]}')  # вставьте ваши валюты
        return total_base