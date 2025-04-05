import requests
import json
import logging
import time
from typing import Optional, Dict

class ExchangeRateProvider:
    def __init__(self, api_url: str = "https://api.exchangerate-api.com/v4/latest/USD", max_retries: int = 3, retry_delay: int = 2, timeout: int = 10):
        self.api_url = api_url
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.timeout = timeout
        self.logger = self._setup_logger()
        self._rates: Optional[Dict[str, float]] = None
        self._last_fetch_time: Optional[float] = None

    def _setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        if not logger.hasHandlers():
            ch = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ch.setFormatter(formatter)
            logger.addHandler(ch)
        return logger

    def _fetch_rates_from_api(self) -> Optional[Dict[str, float]]:
        for attempt in range(self.max_retries):
            try:
                response = requests.get(self.api_url, timeout=self.timeout)
                response.raise_for_status()
                data = response.json()
                rates = data.get('rates')
                if rates and isinstance(rates, dict):
                    self.logger.info("Successfully fetched exchange rates.")
                    return rates
                else:
                    self.logger.error("API response does not contain 'rates' or 'rates' is not a dictionary.")
                    return None

            except requests.exceptions.RequestException as e:
                self.logger.error(f"API request error (attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                else:
                    self.logger.error("Maximum retries reached. Failed to fetch rates.")
                    return None

            except json.JSONDecodeError as e:
                self.logger.error(f"Error decoding JSON response: {e}")
                return None
            except Exception as e:
                self.logger.exception(f"Unexpected error while fetching rates: {e}")
                return None
        return None

    def get_rates(self) -> Optional[Dict[str, float]]:
        self.logger.info("Requesting new exchange rates...")
        fetched_rates = self._fetch_rates_from_api()
        if fetched_rates:
            self._rates = fetched_rates
            self._last_fetch_time = time.time()
            return self._rates
        else:
            self.logger.warning("Failed to fetch new rates. Returning last known rates (if available) or None.")
            return self._rates

if __name__ == '__main__':
    provider = ExchangeRateProvider()
    rates = provider.get_rates()
    if rates:
        print("Fetched rates:")
        print(rates)
    else:
        print("Failed to fetch rates.") 