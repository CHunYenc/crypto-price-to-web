import requests
import json

CRYPTO_API = "https://api.crypto.com"


def get_crypto_specify_symbol_price(symbol):
    URL = CRYPTO_API + "/v2/public/get-ticker?instrument_name=" + symbol
    # https://api.crypto.com/v2/public/get-ticker?instrument_name=BTC_USDT

    r = requests.get(URL)
    data = json.loads(r.text)
    return data
