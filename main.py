import logging
from converters import AVAILABLE_CONVERTERS, ExchangeRateProvider

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        amount_str = input('Enter the amount in USD: \n')
        amount_usd = float(amount_str)
    except ValueError:
        logger.error(f"Invalid input: '{amount_str}'. Please enter a number.")
        return
    except EOFError:
        logger.warning("Input was not provided.")
        return

    rate_provider = ExchangeRateProvider()
    rates = rate_provider.get_rates()

    if rates is None:
        logger.error("Failed to get exchange rates. Check network connection or API configuration.")
        return

    logger.info(f"Converting {amount_usd} USD...")

    for converter_class in AVAILABLE_CONVERTERS:
        try:
            converter = converter_class()
            target_currency = converter.target_currency
            converted_amount = converter.convert(amount_usd, rates)
            print(f"{round(amount_usd, 2)} USD = {round(converted_amount, 2)} {target_currency}")
        except ValueError as e:
            logger.error(f"Conversion error for {getattr(converter_class, 'target_currency', converter_class.__name__)}: {e}")
        except Exception as e:
            logger.exception(f"Unexpected error with converter {converter_class.__name__}: {e}")

if __name__ == "__main__":
    main()