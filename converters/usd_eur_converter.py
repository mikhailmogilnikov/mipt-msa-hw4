import requests
from converters.currency_converter import CurrencyConverter

class UsdEurConverter(CurrencyConverter):

    @property
    def target_currency(self) -> str:
        return 'EUR'

    def convert(self, amount_usd: float, rates: dict) -> float:
        rate = rates.get(self.target_currency)
        if rate is None:
            raise ValueError(f"Rate for {self.target_currency} not found.")
        return amount_usd * rate