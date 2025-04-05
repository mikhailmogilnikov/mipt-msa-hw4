from converters.currency_converter import CurrencyConverter

class UsdGbpConverter(CurrencyConverter):

    @property
    def target_currency(self) -> str:
        return 'GBP'

    def convert(self, amount_usd: float, rates: dict) -> float:
        rate = rates.get(self.target_currency)
        if rate is None:
            raise ValueError(f"Rate for {self.target_currency} not found.")
        return amount_usd * rate