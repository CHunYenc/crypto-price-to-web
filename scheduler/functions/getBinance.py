import requests
import json

BINANCE_API = "https://api1.binance.com/api/"


def get_binance_all_symbol_price(symbol):
    URL = BINANCE_API + "v3/ticker/price?symbol=" + symbol
    # https://api1.binance.com/api/v3/ticker/price?symbol=BTCUSDT

    r = requests.get(URL)
    data = json.loads(r.text)
    return data